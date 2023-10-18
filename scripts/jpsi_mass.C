#include <TFile.h>
#include <TList.h>
#include <TKey.h>
#include <TDirectoryFile.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <RooFit.h>
#include <RooWorkspace.h>
#include <RooDataHist.h>

void jpsi_mass() {
  auto fin = TFile::Open("output_jpsi.root");
  std::vector<TString> keys;
  auto dir = (TDirectoryFile*)fin->Get("histo");
  TIter next(dir->GetListOfKeys());
  TKey *key;
  while((key = (TKey*)next())) {
    if(TString(key->GetName()).Contains("xb_mass_jpsi_") && !TString(key->GetName()).Contains("ttbar")) keys.push_back(TString(key->GetName()));
  }

  auto c1 = new TCanvas("c1", "c1", 800, 800);
  c1->cd();

  auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / jet #it{p}_{T}", 10, 0, 1);
  //auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / #Sigma #it{p}_{T}^{ch}", 10, 0, 1);

  for(int ibin = 0; ibin < 10; ibin++) {
    auto h_mass = (TH1F*)fin->Get(TString::Format("histo/xb_mass_jpsi_%d_TTToSemiLeptonic_16", ibin));
    h_mass->Add((TH1F*)((TH1F*)fin->Get(TString::Format("histo/xb_mass_jpsi_%d_TTToSemiLeptonic_16APV", ibin)))->Clone());
    for(auto &key : keys) {
      if(key.Contains(TString::Format("_%d_", ibin)))
        h_mass->Add((TH1F*)fin->Get(TString::Format("histo/%s", key.Data())));
      //h_mass->Add((TH1F*)fin->Get(TString::Format("histo/xb_mass_jpsi_%d_%s", ibin, key.Data())));
    }
    //h_mass->Rebin(2);
    auto w = new RooWorkspace("w");
    // J/Psi -> mu mu signal Crystal Ball
    w->factory("RooCBShape::sig(jpsi[2.8,3.4],mean[3.097, 2.9, 3.11],sigma[.02, 0.001, 0.25],alpha[1, 0, 5], n[5, 0, 10])");
    //w->factory("Gaussian::sig(jpsi[2.8,3.4],mean[3.097],sigma[.02])");
    // D0 -> KK
    // D0 -> pi pi
    // Exponential background
    w->factory("Exponential::bkg(jpsi,lambda[-2.7,-10,10])");
    // Extra Gaussian bkg
    w->factory("Gaussian::gbkg(jpsi, mean_bkg_low[2.8, 2.8, 2.85], sigma_bkg_low[.4, 0, .5])");
    w->factory("SUM::model(nsig[800,0,100000]*sig, nbkg[0,0,1000000]*bkg)");
    w->Print("v");
    auto jpsi = w->var("jpsi");
    jpsi->SetTitle("J/#psi mass [GeV]");
    auto d = new RooDataHist("jpsi_mass", "jpsi_mass", *jpsi, RooFit::Import(*(TH1F*)h_mass->Clone()));
    auto frame = jpsi->frame();
    d->plotOn(frame)->Draw();
    //jpsi->setRange("red", 2.83, 1.97);
    w->Print("v");
    w->function("model")->Print("v");
    //((RooAbsPdf*)w->function("model"))->fitTo(*d);
    ((RooAbsPdf*)w->function("model"))->fitTo(*d);
    //w->pdf("model2")->fitTo(*d, RooFit::Range("red"));
    //auto model = w->function("model");
    auto model = w->pdf("model");
    model->plotOn(frame);
    model->plotOn(frame, RooFit::Components("sig"), RooFit::LineColor(kRed));
    model->plotOn(frame, RooFit::Components("bkg"), RooFit::LineStyle(kDashed));
    frame->Draw();

    float chi2 = frame->chiSquare();//"model", "data", 3);
    std::cout << std::endl << "chi2 " << chi2 << std::endl << std::endl;
    std::cout << "Total=" << h_mass->Integral()
              << "\tnjpsi=" << w->var("nsig")->getVal() / h_mass->Integral()
              << "\tnbkg=" << w->var("nbkg")->getVal() / h_mass->Integral() << std::endl;

    TPaveText *pt = new TPaveText(0.12,0.85,0.3,0.65,"NDC"); //NB blNDC
    pt->SetFillStyle(0);
    pt->SetTextAlign(11);
    pt->SetBorderSize(0);
    pt->SetTextFont(42);
    pt->SetTextSize(0.046);
    TString text = TString::Format("N_{J/#psi}= %.0f +/- %.0f (stat)", w->var("nsig")->getVal(), sqrt(w->var("nsig")->getVal()));
    pt->AddText(text);
    pt->Draw();
    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/jpsi_mass_%d.png", ibin));
    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/jpsi_mass_%d.pdf", ibin));

    float sig = w->var("nsig")->getVal();
    h_xb->SetBinContent(ibin+1, sig);

  }
  h_xb->Draw();
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/jpsi_xb.png"));
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/jpsi_xb.pdf"));
}
