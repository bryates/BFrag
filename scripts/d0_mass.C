#include <TFile.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <RooFit.h>
#include <RooWorkspace.h>
#include <RooDataHist.h>

void d0_mass() {
  auto fin = TFile::Open("/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_320.root");
  auto Events = (TTree*)fin->Get("Events");
  //auto Events = new TChain("Events");
  //Events->Add("/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_*.root");

  auto c1 = new TCanvas("c1", "c1", 800, 800);
  c1->cd();

  auto h_mass = new TH1F("h_mass", "h_mass", 30, 1.7, 2.0);
  //Events->Draw("BToCharm_fit_mass>>+h_mass", "Generator_weight*(BToCharm_jetIdx && BToCharm_svprob>0.02 && BToCharm_chi2<5)", "goff");
  //Events->Draw("BToCharm_fit_mass>>+h_mass", "BToCharm_jetIdx && BToCharm_svprob>0.02 && Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5", "goff");
  Events->Draw("BToCharm_fit_mass>>+h_mass", "Generator_weight*(BToCharm_jetIdx && BToCharm_svprob>0.02 && Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5 && (nMuon + nElectron) > 0 && nJet > 1 && Jet_pt[0]>30)", "goff");
  h_mass->Scale(138 * 1000 * 832 / 43559567000.0);
  h_mass->Scale(670);
  auto w = new RooWorkspace("w");
  // D0 -> pi K signal Gaussian
  w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864, 1.7, 2.0],sigma[.02])");//, 0, 1])");
  //w->factory("Gaussian::sig(d0[1.7,2.0],mean[1.864],sigma[.02])");
  // D0 -> KK
  w->factory("Gaussian::kk(d0, mean_kk[1.77], sigma_kk[.02])");
  // D0 -> pi pi
  w->factory("Gaussian::pp(d0, mean_pp[1.94], sigma_pp[.02])");
  // Exponential background
  w->factory("Exponential::bkg(d0,lambda[-2.7,-10,10])");
  w->factory("SUM::cabibbo(nkk[800,0,10000]*kk, npp[800, 0, 10000]*pp)");
  //w->factory("SUM::cabibbo(nkk[400,0,10000]*kk, npp[400, 0, 10000]*pp)");
  w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[200, 0, 100000]*cabibbo)");
  //w->factory("SUM::bkgModel(nexpo[180000,0,1000000]*bkg, nc[400, 0, 10000]*cabibbo)");
  w->factory("SUM::model(nsig[8000,0,1000000000]*sig, nbkg[1800,0,1000000]*bkgModel)");
  //w->factory("SUM::model(nsig[4000,0,100000]*sig, nbkg[180000,0,1000000]*bkgModel)");
  auto d0 = w->var("d0");
  d0->SetTitle("D^{0} mass [GeV]");
  auto d = new RooDataHist("d0_mass", "d0_mass", *d0, RooFit::Import(*(TH1F*)h_mass->Clone()));
  auto frame = d0->frame();
  d->plotOn(frame)->Draw();
  w->pdf("model")->fitTo(*d);
  auto model = w->pdf("model");
  model->plotOn(frame)->Draw();

  c1->SaveAs("/eos/home-b/byates/www/BFrag/d0_mass.png");
  c1->SaveAs("/eos/home-b/byates/www/BFrag/d0_mass.pdf");

  auto l0pt = new TH1F("l0pt", "l0pt", 50, 0, 100);
  Events->Draw("Muon_pt[0]>>+l0pt", "Generator_weight*(Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5 && (nMuon) > 0 && nJet > 1 && Muon_pt[0]>25)", "goff");
  Events->Draw("Electron_pt[0]>>+l0pt", "Generator_weight*(Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5 && (nElectron) > 0 && nJet > 1 && Electron_pt[0]>25 && Jet_pt[0]>30)", "goff");
  //Events->Draw("Muon_pt>>+l0pt", "Generator_weight*(Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5 && (nMuon + nElectron) > 0 && nJet > 1 && (Muon_pt[0]>25 || Electron_pt[0]>25))", "goff");
  //Events->Draw("Electron_pt>>+l0pt", "Generator_weight*(Jet_btagDeepFlavB[BToCharm_jetIdx]>0.3040 && BToCharm_chi2<5 && (nMuon + nElectron) > 0 && nJet > 1 && (Muon_pt[0]>25 || Electron_pt[0]>25)", "goff");
  l0pt->Scale(138 * 1000 * 832 / 43559567000.0);
  //l0pt->Scale(670);
  l0pt->Draw();
  std::cout << l0pt->Integral() << std::endl;
  c1->SaveAs("/eos/home-b/byates/www/BFrag/l0pt.png");
  c1->SaveAs("/eos/home-b/byates/www/BFrag/l0pt.pdf");

  std::cout << Events->GetEntries() << std::endl;
  auto sumw = new TH1F("sumw", "sumw", 2, 0, 2);
  //Events->Draw("Generator_weight/303.", "Generator_weight*(Generator_weight/303.)");
  return;
  Float_t evt;
  Events->SetBranchAddress("Generator_weight", &evt);
  for(size_t ievt = 0; ievt < Events->GetEntriesFast(); ievt++) {
    Events->GetEntry(ievt);
    sumw->Fill(1, evt);
  }
  sumw->Draw();
  std::cout << "sumw=" << sumw->Integral() << std::endl;
  c1->SaveAs("/eos/home-b/byates/www/BFrag/nevt.png");
  c1->SaveAs("/eos/home-b/byates/www/BFrag/nevt.pdf");
}
