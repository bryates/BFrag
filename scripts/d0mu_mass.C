#include <TFile.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <RooFit.h>
#include <RooWorkspace.h>
#include <RooDataHist.h>

void d0mu_mass() {
  auto fin = TFile::Open("output.root");

  auto c1 = new TCanvas("c1", "c1", 800, 800);
  c1->cd();

  std::vector<float> d0mu_xb_bins = {0., 0.2, 0.4, 0.6, 0.8, 1.};
  //std::vector<float> d0mu_xb_bins = {0, .2, .4, .5, .6, .7, .8, .9, 1.};
  auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / jet #it{p}_{T}", d0mu_xb_bins.size()-1, d0mu_xb_bins.data());
  //auto h_xb = new TH1F("xb", "xb;D^{0} #it{p}_{T} / #Sigma #it{p}_{T}^{ch}", 10, 0, 1);

  float width = 0;
  for(int ibin = 0; ibin < d0mu_xb_bins.size()-1; ibin++) {
    auto h_mass = (TH1F*)fin->Get(TString::Format("histo/xb_mass_d0mu_%d_ttbar", ibin));
    h_mass->Rebin(2);
    auto w = new RooWorkspace("w");
    // D0 -> pi K signal Gaussian
    w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864, 1.8, 1.9],sigma[.02])");//, 0, 1])");
    //w->factory("Gaussian::bkg_pol(d0[1.7,2.0],mean[1.864, 1.8, 1.9],sigma2[.002, 0.001, 0.02])");
    //w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864],sigma[.02])");
    // D0 -> KK
    w->factory("Gaussian::kk(d0, mean_kk[1.77, 1.75, 1.8], sigma_kk[.02, 0.01, 0.05])");
    // D0 -> pi pi
    w->factory("Gaussian::pp(d0, mean_pp[1.94, 1.9, 2.0], sigma_pp[.02, 0.01, 0.05])");
    // Exponential background
    w->factory("Exponential::bkg(d0,lambda[-2.7,-10,10])");
    // Extra Gaussian bkg
    //w->factory("Gaussian::gbkg(d0, mean_bkg[1.864, 1.7, 2.0], sigma_bkg[.02, 0, 0.5])");
    w->factory("Polynomial::bkg_pol(d0[1.7,2.0], {a0[0,-10,1], a1[0]})");
    //w->pdf("bkg_pol")->Print("v");
    w->factory("SUM::cabibbo(nkk[0,0,10000]*kk, npp[0, 0, 10000]*pp)");
    //w->factory("SUM::cabibbo(nkk[400,0,10000]*kk, npp[400, 0, 10000]*pp)");
    //w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[200, 0, 100000]*cabibbo)");
    //w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[400, 0, 10000]*cabibbo)");
    //w->factory("SUM::model(nsig[8000,0,1000000000]*sig, nbkg[1800,0,1000000]*bkg)");
    //w->factory("SUM::sigM(nsig[800,0,100000]*sig, nbkg_pol[800,0,100000]*bkg_pol)");
    //w->factory("SUM::model(nsig[800,0,100000]*sig, nbkg[1800,0,1000000]*bkgModel)");
    //w->factory("SUM::model2(nsig[800,0,100000]*model, nbkg[1800,0,1000000]*bkg_pol)");
    //w->factory("SUM::model2(nmod[8000,0,1000000000]*model, ngbkg[1800,0,1000000]*gbkg)");
    //w->factory("SUM::model3(nsig[800,0,100000]*sig,nkk[0,0,10000]*kk, npp[0,0,10000]*pp, nbkg[1800, 0, 1000000]*bkg)");
    w->factory("SUM::model3(nsig[8000,0,1000000000]*sig,nc[0, 0, 100000]*cabibbo,nbkg[1800,0,1000000]*bkg)");
    auto d0 = w->var("d0");
    d0->SetTitle("D^{0} mass [GeV]");
    auto d = new RooDataHist("d0_mass", "d0_mass", *d0, RooFit::Import(*(TH1F*)h_mass->Clone()));
    auto frame = d0->frame();
    d->plotOn(frame)->Draw();
    //d0->setRange("red", 1.73, 1.97);
    w->Print("v");
    w->function("model3")->Print("v");
    ((RooAbsPdf*)w->function("model3"))->fitTo(*d);
    //w->pdf("model2")->fitTo(*d, RooFit::Range("red"));
    auto model = w->function("model3");
    //auto model = w->pdf("model2");
    model->plotOn(frame);
    //model->plotOn(frame, RooFit::Components("kk", "pp", "bkg", "bkg_po"), RooFit::LineStyle(kDashed))->Draw();
    model->plotOn(frame, RooFit::Components("sig"), RooFit::LineColor(kRed));
    model->plotOn(frame, RooFit::Components("kk"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("pp"), RooFit::LineStyle(kDashed));
    model->plotOn(frame, RooFit::Components("bkg"), RooFit::LineStyle(kDashed));
    //model->plotOn(frame, RooFit::Components("bkg_pol"), RooFit::LineStyle(kDashed));
    frame->Draw();

    float chi2 = frame->chiSquare();//"model", "data", 3);
    std::cout << std::endl << "chi2 " << chi2 << std::endl << std::endl;
    std::cout << "Total=" << h_mass->Integral()
              << "\tnd0=" << w->var("nsig")->getVal() / h_mass->Integral()
              << "\tnbkg=" << w->var("nbkg")->getVal() / h_mass->Integral() << std::endl;

    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0mu_mass_%d.png", ibin));
    c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0mu_mass_%d.pdf", ibin));

    float sig = w->var("nsig")->getVal();
    //h_xb->SetBinContent(ibin+1, sig / h_xb->GetBinWidth(ibin+1));
    h_xb->SetBinContent(ibin+1, sig);
    width += h_xb->GetBinWidth(ibin+1);

  }
  //h_xb->Scale(width);
  h_xb->Draw();
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0mu_xb.png"));
  c1->SaveAs(TString::Format("/eos/home-b/byates/www/BFrag/xb_mass/d0mu_xb.pdf"));
}
