#include <TFile.h>
#include <TList.h>
#include <TKey.h>
#include <TDirectoryFile.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <RooFit.h>
#include <RooWorkspace.h>
#include <RooDataHist.h>

void d0_mass() {
  auto fin = TFile::Open("output_d0.root");
  std::vector<TString> keys;
  auto dir = (TDirectoryFile*)fin->Get("histo");
  TIter next(dir->GetListOfKeys());
  TKey *key;
  while((key = (TKey*)next())) {
    if(TString(key->GetName()).Contains("xb_mass_d0_") && !TString(key->GetName()).Contains("TTTo")) keys.push_back(TString(key->GetName()));
  }

  auto c1 = new TCanvas("c1", "c1", 800, 800);
  c1->cd();

  auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / jet #it{p}_{T}", 10, 0, 1);
  auto h_bkg = new TH1F("bkg", "bkg;D^{0} #it{p}_{T} / jet #it{p}_{T}", 10, 0, 1);
  //auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / #Sigma #it{p}_{T}^{ch}", 10, 0, 1);

  for(int ibin = 0; ibin < 10; ibin++) {
    auto h_mass = (TH1F*)fin->Get(TString::Format("histo/xb_mass_d0_%d_TTToSemiLeptonic_16", ibin));
    h_mass->Add((TH1F*)((TH1F*)fin->Get(TString::Format("histo/xb_mass_d0_%d_TTToSemiLeptonic_16APV", ibin)))->Clone());
    for(auto &key : keys) {
      std::cout << key << std::endl;
      if(key.Contains(TString::Format("_%d_", ibin)))
        h_mass->Add((TH1F*)fin->Get(TString::Format("histo/%s", key.Data())));
      //h_mass->Add((TH1F*)fin->Get(TString::Format("histo/xb_mass_d0_%d_%s", ibin, key.Data())));
    }
    //h_mass->Rebin(2);
    auto w = new RooWorkspace("w");
    // D0 -> pi K signal Gaussian
    w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864, 1.84, 1.88],sigma[.02])");//, 0, 1])");
    w->factory("Gaussian::sig2(d0,mean,sigma2[.01])");//, 0, 0.05])");
    //w->factory("Gaussian::bkg_pol(d0[1.7,2.0],mean[1.864, 1.8, 1.9],sigma2[.002, 0.001, 0.02])");
    //w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864],sigma[.02])");
    // D0 -> KK
    w->factory("Gaussian::kk(d0, mean_kk[1.77, 1.75, 1.85], sigma_kk[.02, 0.01, 0.05])");
    // D0 -> pi pi
    w->factory("Gaussian::pp(d0, mean_pp[1.94, 1.9, 2.0], sigma_pp[.02, 0.01, 0.05])");
    // Exponential background
    w->factory("Exponential::bkg(d0,lambda[-2.7,-10,10])");
    // Extra Gaussian bkg
    w->factory("Gaussian::gbkg(d0, mean_bkg_low[1.7, 1.7, 1.75], sigma_bkg_low[.4, 0, .5])");
    w->factory("Gaussian::bkg_pol(d0, mean_bkg[1.864, 1.8, 1.9], sigma_bkg[0.5, .1, 5])");
    //w->factory("Polynomial::bkg_pol(d0[1.7,2.0], {a0[-5,-10,1], a1[0]})");
    w->pdf("bkg_pol")->Print("v");
    w->factory("SUM::cabibbo(nkk[0,0,10000]*kk, npp[0, 0, 10000]*pp)");
    //w->factory("SUM::cabibbo(nkk[400,0,10000]*kk, npp[400, 0, 10000]*pp)");
    w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[0, 0, 100000]*cabibbo)");
    //w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[400, 0, 10000]*cabibbo)");
    //w->factory("SUM::model(nsig[8000,0,1000000000]*sig, nbkg[1800,0,1000000]*bkg)");
    //w->factory("SUM::sigM(nsig[800,0,100000]*sig, nsig2[80,0,100000]*sig2)");
    //w->factory("SUM::model(nsig[800,0,100000]*sigM, nbkg[1800,0,1000000]*bkgModel)");
    //w->factory("SUM::model2(nsig[800,0,100000]*model, nbkg[1800,0,1000000]*bkg_pol)");
    //w->factory("SUM::model2(nsig[800,0,100000]*model, nbkg[1800,0,1000000]*bkg_pol)");
    //w->factory("SUM::model2(nmod[8000,0,1000000000]*model, ngbkg[180,0,1000]*gbkg)");
    w->factory("SUM::model3(nsig1[800,0,1000000000]*sig,nsig2[800,0,1000000000]*sig2,nc[0, 0, 100000]*cabibbo,nbkg[1800,0,1000000]*bkg,ngbkg[0,0,1000]*gbkg,nbkgp[8000,0,1000000000]*bkg_pol)");
    //w->factory("SUM::model3(nsig1[8000,0,1000000000]*sig,nsig2[8000,0,1000000000]*sig2,nc[0, 0, 100000]*cabibbo,nbkg[1800,0,1000000]*bkg,ngbkg[0,0,1000]*gbkg)");
    auto d0 = w->var("d0");
    d0->SetTitle("D^{0} mass [GeV]");
    h_mass->Rebin();
    auto d = new RooDataHist("d0_mass", "d0_mass", *d0, RooFit::Import(*(TH1F*)h_mass->Clone()));
    auto frame = d0->frame();
    d->plotOn(frame)->Draw();
    //d0->setRange("red", 1.73, 1.97);
    w->Print("v");
    w->function("model3")->Print("v");
    //((RooAbsPdf*)w->function("model"))->fitTo(*d);
    ((RooAbsPdf*)w->function("model3"))->fitTo(*d);
    //w->pdf("model2")->fitTo(*d, RooFit::Range("red"));
    //auto model = w->function("model");
    auto model = w->pdf("model3");
    model->plotOn(frame);
    //model->plotOn(frame, RooFit::Components("kk", "pp", "bkg", "bkg_po"), RooFit::LineStyle(kDashed))->Draw();
    model->plotOn(frame, RooFit::Components("sig"), RooFit::LineColor(kRed));
    //model->plotOn(frame, RooFit::Components("sig2"), RooFit::LineColor(kRed));
    model->plotOn(frame, RooFit::Components("kk"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("pp"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("bkg"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("gbkg"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("bkg_pol"), RooFit::LineStyle(kDashed));
    frame->Draw();

    float chi2 = frame->chiSquare();//"model", "data", 3);
    std::cout << std::endl << "chi2 " << chi2 << std::endl << std::endl;
    std::cout << "Total=" << h_mass->Integral()
              << "\tnd0=" << w->var("nsig1")->getVal() / h_mass->Integral()
              << "\tnbkg=" << w->var("nbkg")->getVal() / h_mass->Integral() << std::endl;

    TPaveText *pt = new TPaveText(0.12,0.85,0.3,0.65,"NDC"); //NB blNDC
    pt->SetFillStyle(0);
    pt->SetTextAlign(11);
    pt->SetBorderSize(0);
    pt->SetTextFont(42);
    pt->SetTextSize(0.046);
    TString text = TString::Format("N_{D^{0}}= %.0f +/- %.0f (stat)", w->var("nsig1")->getVal(), sqrt(w->var("nsig1")->getVal()));
    pt->AddText(text);
    pt->Draw();
    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0_mass_%d.png", ibin));
    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0_mass_%d.pdf", ibin));

    float sig = w->var("nsig1")->getVal() + w->var("nsig2")->getVal();
    std::cout << "Total nd0=" << w->var("nsig1")->getVal() << std::endl;
    float bkg = w->var("nbkg")->getVal() + w->var("nbkgp")->getVal() + w->var("nc")->getVal();
    h_xb->SetBinContent(ibin+1, sig);
    h_bkg->SetBinContent(ibin+1, bkg);

  }
  h_xb->Draw();
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0_xb.png"));
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0_xb.pdf"));
  auto fout = TFile::Open("xb_out.root", "RECREATE");
  h_xb->SetDirectory(fout);
  h_xb->Write();
  h_bkg->SetDirectory(fout);
  h_bkg->Write();
  auto data_obs = (TH1F*)h_bkg->Clone("data_obs"); 
  data_obs->Add(h_xb);
  data_obs->SetDirectory(fout);
  data_obs->Write();
  fout->Close();
}
