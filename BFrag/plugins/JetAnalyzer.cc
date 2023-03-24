// -*- C++ -*-
//
// Package:    BFrag/BFrag
// Class:      BFrag
//
/**\class BFrag BFrag.cc BFrag/BFrag/plugins/JetAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Brent Yates
//         Created:  Wed, 22 Mar 2023 15:46:59 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include "TLorentzVector.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


class JetAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit JetAnalyzer(const edm::ParameterSet&);
      ~JetAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      edm::EDGetTokenT<reco::VertexCollection> vtxToken_;

      edm::EDGetTokenT<pat::MuonCollection> muonToken_;
      edm::EDGetTokenT<edm::View<pat::Electron>  >  electronToken_;
      edm::EDGetTokenT<edm::ValueMap<bool> > eleVetoIdMapToken_;
      edm::EDGetTokenT<edm::ValueMap<bool> > eleLooseIdMapToken_;
      edm::EDGetTokenT<edm::ValueMap<bool> > eleMediumIdMapToken_;
      edm::EDGetTokenT<edm::ValueMap<bool> > eleTightIdMapToken_;

      edm::EDGetTokenT<edm::View<pat::Jet> > jetToken_;
      edm::EDGetTokenT<std::vector<reco::GenJet>  > genJetsToken_;

      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      std::vector<std::string> muTriggersToUse_, elTriggersToUse_;

      TTree *tree_;
      edm::Service<TFileService> fs;

      // ----------member data ---------------------------

  //Vertex and triggers
  Int_t nvtx;
  Int_t muTrigger;
  Int_t elTrigger;

  //Leptons
  Int_t nl;
  Bool_t isPromptFinalState[500];
  Bool_t isDirectPromptTauDecayProductFinalState[500];
  Int_t l_id[500];
  Float_t l_g[500];
  Float_t l_charge[500];
  Float_t l_pt[500];
  Float_t l_eta[500];
  Float_t l_phi[500];
  Float_t l_mass[500];
  Float_t l_g_pt[500];
  Float_t l_g_eta[500];
  Float_t l_g_phi[500];
  Float_t l_g_mass[500];
  Float_t l_g_id[500];
  Int_t l_pid[500];
  Float_t l_chargedHadronIso[500];
  Float_t l_relIso[500];
  Float_t l_ip3d[500];
  Float_t l_ip3dsig[500];
  Float_t l_dxy[500];
  Float_t l_dxyE[500];
  Float_t l_dz[500];
  Float_t l_dzE[500];
  Bool_t l_global[500];
  Float_t l_pf[500];
  Float_t l_nValTrackerHits[500];
  Float_t l_nValPixelHits[500];
  Float_t l_nMatchedStations[500];
  Float_t l_pixelLayerWithMeasurement[500];
  Float_t l_trackerLayersWithMeasurement[500];
  Float_t l_validFraction[500];
  Float_t l_chi2LocalPosition[500];
  Float_t l_trkKink[500];
  Float_t l_chi2norm[500];
  Float_t l_globalTrackNumberOfValidHits[500];

  // Jets
  Int_t nj;
  Int_t ng;
  Int_t npf;
  Float_t j_pt[500];
  Float_t j_eta[500];
  Float_t j_phi[500];
  Int_t j_g[500];
  Float_t j_deepB[500];
  Float_t j_partflav[500];
  Float_t j_hadflav[500];
  Float_t pf_pt[500];
  Float_t pf_eta[500];
  Float_t pf_phi[500];
  Int_t pf_id[500];
  Float_t pf_j[500];
  Float_t pf_g_pt[500];
  Float_t pf_g_eta[500];
  Float_t pf_g_phi[500];
  Int_t pf_g_id[500];
  Float_t pf_g_j[500];
  Float_t g_j_pt[500];
  Float_t g_j_eta[500];
  Float_t g_j_phi[500];
  Int_t g_j_id[500];
  Float_t g_pt[500];
  Float_t g_eta[500];
  Float_t g_phi[500];
  Int_t g_id[500];

  //Fragmentation stuff
  /*
  std::vector<float> d0_mass;
  std::vector<float> d0_pt;
  std::vector<float> jpsi_mass;
  std::vector<float> jpsi_pt;
  std::vector<float> meson_j;
  //std::vector<float> xb;
  */
  Int_t nmeson;
  Int_t meson_j[500];
  Float_t d0_mass[500];
  Float_t d0_pt[500];
  Float_t jpsi_mass[500];
  Float_t jpsi_pt[500];
  Float_t xb[500];

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
JetAnalyzer::JetAnalyzer(const edm::ParameterSet& iConfig) : 
  vtxToken_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
  muonToken_(consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"))),
  eleVetoIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleVetoIdMap"))),
  eleLooseIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleLooseIdMap"))),
  eleMediumIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleMediumIdMap"))),
  eleTightIdMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleTightIdMap"))),
  jetToken_(consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets"))),  
  genJetsToken_(consumes<std::vector<reco::GenJet> >(edm::InputTag("pseudoTop:jets"))),
  triggerBits_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerBits")))
{
   electronToken_ = mayConsume<edm::View<pat::Electron> >(iConfig.getParameter<edm::InputTag>("electrons"));
   elTriggersToUse_ = iConfig.getParameter<std::vector<std::string> >("elTriggersToUse");
   muTriggersToUse_ = iConfig.getParameter<std::vector<std::string> >("muTriggersToUse");
   //now do what ever initialization is needed
   //tree_ = new TTree("data","Tree with vectors");
   tree_ = fs->make<TTree>("JetData","JetData");

  //Vertex and triggers
  tree_->Branch("nvtx", &nvtx, "nvtx/I");
  tree_->Branch("muTrigger", &muTrigger, "muTrigger/I");
  tree_->Branch("elTrigger", &elTrigger, "elTrigger/I");

  //Leptons
  tree_->Branch("nl", &nl, "nl/I");
  tree_->Branch("isPromptFinalState", isPromptFinalState, "isPromptFinalState[nl]/B");
  tree_->Branch("isDirectPromptTauDecayProductFinalState", isDirectPromptTauDecayProductFinalState, "isDirectPromptTauDecayProductFinalState[nl]/B");
  tree_->Branch("l_id", l_id, "l_id[nl]/I");
  tree_->Branch("l_g", l_g, "l_g[nl]/F");
  tree_->Branch("l_charge", l_charge, "l_charge[nl]/F");
  tree_->Branch("l_pt", l_pt, "l_pt[nl]/F");
  tree_->Branch("l_eta", l_eta, "l_eta[nl]/F");
  tree_->Branch("l_phi", l_phi, "l_phi[nl]/F");
  tree_->Branch("l_mass", l_mass, "l_mass[nl]/F");
  tree_->Branch("l_g_pt", l_g_pt, "l_g_pt[nl]/F");
  tree_->Branch("l_g_eta", l_g_eta, "l_g_eta[nl]/F");
  tree_->Branch("l_g_phi", l_g_phi, "l_g_phi[nl]/F");
  tree_->Branch("l_g_mass", l_g_mass, "l_g_mass[nl]/F");
  tree_->Branch("l_g_id", l_g_id, "l_g_id[nl]/F");
  tree_->Branch("l_pid", l_pid, "l_pid[nl]/I");
  tree_->Branch("l_chargedHadronIso", l_chargedHadronIso, "l_chargedHadronIso[nl]/F");
  tree_->Branch("l_relIso", l_relIso, "l_relIso[nl]/F");
  tree_->Branch("l_ip3d", l_ip3d, "l_ip3d[nl]/F");
  tree_->Branch("l_ip3dsig", l_ip3dsig, "l_ip3dsig[nl]/F");
  tree_->Branch("l_dxy", l_dxy, "l_dxy[nl]/F");
  tree_->Branch("l_dxyE", l_dxyE, "l_dxyE[nl]/F");
  tree_->Branch("l_dz", l_dz, "l_dz[nl]/F");
  tree_->Branch("l_dzE", l_dzE, "l_dzE[nl]/F");
  tree_->Branch("l_global", l_global, "l_global[nl]/B");
  tree_->Branch("l_pf", l_pf, "l_pf[nl]/F");
  tree_->Branch("l_nValTrackerHits", l_nValTrackerHits, "l_nValTrackerHits[nl]/F");
  tree_->Branch("l_nValPixelHits", l_nValPixelHits, "l_nValPixelHits[nl]/F");
  tree_->Branch("l_nMatchedStations", l_nMatchedStations, "l_nMatchedStations[nl]/F");
  tree_->Branch("l_pixelLayerWithMeasurement", l_pixelLayerWithMeasurement, "l_pixelLayerWithMeasurement[nl]/F");
  tree_->Branch("l_trackerLayersWithMeasurement", l_trackerLayersWithMeasurement, "l_trackerLayersWithMeasurement[nl]/F");
  tree_->Branch("l_validFraction", l_validFraction, "l_validFraction[nl]/F");
  tree_->Branch("l_chi2LocalPosition", l_chi2LocalPosition, "l_chi2LocalPosition[nl]/F");
  tree_->Branch("l_trkKink", l_trkKink, "l_trkKink[nl]/F");
  tree_->Branch("l_chi2norm", l_chi2norm, "l_chi2norm[nl]/F");
  tree_->Branch("l_globalTrackNumberOfValidHits", l_globalTrackNumberOfValidHits, "l_globalTrackNumberOfValidHits[nl]/F");

  tree_->Branch("nj", &nj, "nj/I");
  tree_->Branch("ng", &ng, "ng/I");
  tree_->Branch("npf", &npf, "npf/I");
  tree_->Branch("j_pt", j_pt, "j_pt[nj]/F");
  tree_->Branch("j_eta", j_eta, "j_eta[nj]/F");
  tree_->Branch("j_phi", j_phi, "j_phi[nj]/F");
  tree_->Branch("j_g", j_g, "j_g[nj]/I");
  tree_->Branch("j_deepB", j_deepB, "j_deepB[nj]/F");
  tree_->Branch("j_partflav", j_partflav, "j_partflav[nj]/F");
  tree_->Branch("j_hadflav", j_hadflav, "j_hadflav[nj]/F");
  tree_->Branch("pf_pt", pf_pt, "pf_pt[npf]/F");
  tree_->Branch("pf_eta", pf_eta, "pf_eta[npf]/F");
  tree_->Branch("pf_phi", pf_phi, "pf_phi[npf]/F");
  tree_->Branch("pf_id", pf_id, "pf_id[npf]/I");
  tree_->Branch("pf_j", pf_j, "pf_j[npf]/F");
  tree_->Branch("pf_g_pt", pf_g_pt, "pf_g_pt[npf]/F");
  tree_->Branch("pf_g_eta", pf_g_eta, "pf_g_eta[npf]/F");
  tree_->Branch("pf_g_phi", pf_g_phi, "pf_g_phi[npf]/F");
  tree_->Branch("pf_g_id", pf_g_id, "pf_g_id[npf]/I");
  tree_->Branch("pf_g_j", pf_g_j, "pf_g_j[npf]/F");
  tree_->Branch("g_j_pt", g_j_pt, "g_j_pt[ng]/F");
  tree_->Branch("g_j_eta", g_j_eta, "g_j_eta[ng]/F");
  tree_->Branch("g_j_phi", g_j_phi, "g_j_phi[ng]/F");
  tree_->Branch("g_j_id", g_j_id, "g_j_id[ng]/I");
  tree_->Branch("g_pt", g_pt, "g_pt[ng]/F");
  tree_->Branch("g_eta", g_eta, "g_eta[ng]/F");
  tree_->Branch("g_phi", g_phi, "g_phi[ng]/F");
  tree_->Branch("g_id", g_id, "g_id[ng]/I");

  //Fragmentation stuff
  tree_->Branch("nmeson", &nmeson, "nmeson/I");
  tree_->Branch("meson_j",&meson_j, "meson_j[nmeson]/I");
  tree_->Branch("d0_mass", &d0_mass, "d0_mass[nmeson]/F");
  tree_->Branch("d0_pt", &d0_pt, "d0_pt[nmeson]/F");
  tree_->Branch("jpsi_mass", &jpsi_mass, "jpsi_mass[nmeson]/F");
  tree_->Branch("jpsi_pt", &jpsi_pt, "jpsi_pt[nmeson]/F");
  tree_->Branch("xb", xb, "xb[nmeson]/F");
}


JetAnalyzer::~JetAnalyzer()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}

// Define a function to save pt of jet constituents
/*
void saveJetConstituentPt(const pat::Jet* jet, std::vector<double>& recoJetConstituentPt, std::vector<double>& genJetConstituentPt, const reco::GenJet* genJetColl) {

    // Loop over the jet constituents
    for(unsigned int i = 0; i < jet->numberOfDaughters(); ++i) {
        const reco::Candidate* constituent = jet->daughter(i);

        // Save the reco level pt of the jet constituent
        recoJetConstituentPt.push_back(constituent->pt());

        // Find the gen jet constituent with the smallest delta R
        double minDeltaR = 999.;
        double genPt = -1.;
        for(auto &genJet = genJetColl->begin();  genJetColl != genJetColl->end(); ++genJetColl)
        //for (const auto& genJet : genJetColl) {
            for (unsigned int iGen = 0; iGen < genJet.numberOfDaughters(); ++iGen) {
                const reco::Candidate* genConstituent = genJet.daughter(iGen);
                double deltaR = reco::deltaR(*genConstituent, *constituent);
                if (deltaR < minDeltaR) {
                    minDeltaR = deltaR;
                    genPt = genConstituent->pt();
                }
            }
        }
        // Save the gen level pt of the jet constituent
        genJetConstituentPt.push_back(genPt);
    }
}
*/


//
// member functions
//

// ------------ method called for each event  ------------
void
JetAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  const bool isData  = iEvent.isRealData();
  //VERTICES
  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vtxToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  const reco::Vertex &primVtx = vertices->front();
  reco::VertexRef primVtxRef(vertices,0);
  nvtx = vertices->size();
  if(nvtx==0) return;

  //TRIGGER INFORMATION
  edm::Handle<edm::TriggerResults> h_trigRes;
  iEvent.getByToken(triggerBits_, h_trigRes);
  std::vector<std::string> triggerList;
  edm::Service<edm::service::TriggerNamesService> tns;
  tns->getTrigPaths(*h_trigRes,triggerList);
  int mutrig = 0;
  int eltrig = 0;
  for (unsigned int i=0; i< h_trigRes->size(); i++) {
      if( !(*h_trigRes)[i].accept() ) continue;
      for(size_t imu=0; imu<muTriggersToUse_.size(); imu++)
	{
	  if (triggerList[i].find(muTriggersToUse_[imu])==std::string::npos) continue;
	  mutrig |= (1 << imu);
	}
      for(size_t iel=0; iel<elTriggersToUse_.size(); iel++) 
	{
	  if (triggerList[i].find(elTriggersToUse_[iel])==std::string::npos)continue;
	  eltrig |= (1 << iel);
	}
  }
  muTrigger = mutrig;
  elTrigger = eltrig;
  bool passMuTrigger(isData ? mutrig!=0 : true);
  bool passElTrigger(isData ? eltrig!=0 : true);  
  if(!passMuTrigger && !passElTrigger) return;

  int nleptons(0);
  nl = 0;
  //MUON SELECTION: cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
  edm::Handle<pat::MuonCollection> muons;
  iEvent.getByToken(muonToken_, muons);
  for (const pat::Muon &mu : *muons) 
    { 
      //correct the 4-momentum
      TLorentzVector p4;
      p4.SetPtEtaPhiM(mu.pt(),mu.eta(),mu.phi(),mu.mass());
      /* FIXME
      float qter(1.0);
      try {
        if(iEvent.isRealData()) {
	  rochcor_->momcor_data(p4, mu.charge(), 0, qter);
        }
        else {
          int ntrk=mu.innerTrack()->hitPattern().trackerLayersWithMeasurement();
	  rochcor_->momcor_data(p4, mu.charge(), ntrk, qter);
        }
      }
      catch(...) {
        //probably no inner track...
      }
      */

      //kinematics
      bool passPt( mu.pt() > 10 );
      bool passEta(fabs(mu.eta()) < 2.4 );
      if(!passPt || !passEta) continue;

      //ID
      bool isMedium(mu.passed(reco::Muon::CutBasedIdMedium));
      bool isTight(mu.passed(reco::Muon::CutBasedIdTight));
      bool isLoose(mu.passed(reco::Muon::CutBasedIdLoose));
      bool isSoft(mu.passed(reco::Muon::SoftCutBasedId));
      if(!isMedium) continue;

      //save it
      const reco::GenParticle * gen=mu.genLepton(); 
      isPromptFinalState[nl] = gen ? gen->isPromptFinalState() : false;
      isDirectPromptTauDecayProductFinalState[nl] = gen ? gen->isDirectPromptTauDecayProductFinalState() : false;
      l_id[nl] = mu.pdgId();
      l_charge[nl] = mu.charge();
      l_pt[nl] = mu.pt();
      l_eta[nl] = mu.eta();
      l_phi[nl] = mu.phi();
      l_mass[nl] = mu.mass();
      if(gen != nullptr) {
        //save the gen-matched muon
        l_g_pt[nl] = gen->pt();
        l_g_eta[nl] = gen->eta();
        l_g_phi[nl] = gen->phi();
        l_g_mass[nl] = gen->mass();
        l_g_id[nl] = gen->pdgId();
      }
      l_pid[nl] = (isTight | (isMedium<<1) | (isLoose<<2) | (isSoft<<3));
      l_chargedHadronIso[nl] = mu.pfIsolationR04().sumChargedHadronPt;
      l_relIso[nl] = (mu.passed(reco::Muon::PFIsoTight) |      // tight is l_relIso[imu]&0b1
                      mu.passed(reco::Muon::PFIsoMedium)<<1 | 
                      mu.passed(reco::Muon::PFIsoLoose)<<2);
      float t_l_ip3d(-9999.);
      float t_l_ip3dsig(-9999);
      if(mu.outerTrack().isNonnull()) {
        l_dxy[nl] = mu.dB();
        l_dxyE[nl] = mu.edB();
      }
      if(mu.innerTrack().isNonnull()) {
        //l_dxy[nl] = mu.dB();
        //l_dxyE[nl] = mu.edB();
        l_dxy[nl] = mu.innerTrack()->dxy(primVtx.position());
        l_dxyE[nl] = mu.innerTrack()->dxyError();
        l_dz[nl] = mu.innerTrack()->dz(primVtx.position());
        l_dzE[nl] = mu.innerTrack()->dzError();
        t_l_ip3d = sqrt(pow(l_dxy[nl], 2) + pow(l_dz[nl], 2));
        float l_ip3d_err = sqrt(pow(l_dxyE[nl], 2) + pow(l_dzE[nl], 2));
        t_l_ip3dsig = t_l_ip3d / l_ip3d_err;
        l_global[nl] = mu.isGlobalMuon();
        l_pf[nl] = mu.isPFMuon();
        l_nValTrackerHits[nl] = mu.innerTrack()->hitPattern().numberOfValidTrackerHits();
        l_nValPixelHits[nl] = mu.innerTrack()->hitPattern().numberOfValidPixelHits();
        l_nMatchedStations[nl] = mu.numberOfMatchedStations();
        l_pixelLayerWithMeasurement[nl] =  mu.innerTrack()->hitPattern().pixelLayersWithMeasurement();
        l_trackerLayersWithMeasurement[nl] = mu.innerTrack()->hitPattern().trackerLayersWithMeasurement();

        //Medium
        l_validFraction[nl] = mu.innerTrack()->validFraction();
        l_chi2LocalPosition[nl] = mu.combinedQuality().chi2LocalPosition;
        l_trkKink[nl] = mu.combinedQuality().trkKink;
      }
	  l_ip3d[nl] = t_l_ip3d;
	  l_ip3dsig[nl] = t_l_ip3dsig;

      if (mu.globalTrack().isNonnull()) {
        l_chi2norm[nl] = mu.normChi2();
        l_global[nl] = mu.isGlobalMuon();
        l_pf[nl] = mu.isPFMuon();
        l_globalTrackNumberOfValidHits[nl] = mu.globalTrack()->hitPattern().numberOfValidMuonHits();
        l_nMatchedStations[nl] = mu.numberOfMatchedStations();
      }
      nl++;
      nleptons += ( isTight && mu.pt()>25 && fabs(mu.eta())<2.5); 
    }
  // ELECTRON SELECTION: cf. https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
  edm::Handle<edm::View<pat::Electron> >    electrons;
  iEvent.getByToken(electronToken_, electrons);    
  edm::Handle<edm::ValueMap<bool> > veto_id_decisions;
  iEvent.getByToken(eleVetoIdMapToken_ ,veto_id_decisions);
  edm::Handle<edm::ValueMap<bool> > loose_id_decisions;
  iEvent.getByToken(eleLooseIdMapToken_ ,loose_id_decisions);
  edm::Handle<edm::ValueMap<bool> > medium_id_decisions;
  iEvent.getByToken(eleMediumIdMapToken_ ,medium_id_decisions);
  edm::Handle<edm::ValueMap<bool> > tight_id_decisions;
  iEvent.getByToken(eleTightIdMapToken_ ,tight_id_decisions);
  Int_t nele(0);
  for (const pat::Electron &el : *electrons) 
    {        
      const auto e = electrons->ptrAt(nele); 
      nele++;

      //kinematics cuts
      bool passPt(el.pt() > 15.0);
      bool passEta(fabs(el.eta()) < 2.5 && (fabs(el.superCluster()->eta()) < 1.4442 || fabs(el.superCluster()->eta()) > 1.5660));
      if(!passPt || !passEta) continue;
     
      //look up id decisions
      bool passVetoId   = el.electronID("cutBasedElectronID-Fall17-94X-V2-veto");
      bool passLooseId  = el.electronID("cutBasedElectronID-Fall17-94X-V2-loose");
      bool passMediumId = el.electronID("cutBasedElectronID-Fall17-94X-V2-medium");
      bool passTightId  = el.electronID("cutBasedElectronID-Fall17-94X-V2-tight");
      l_pid[nl] = passTightId | (passMediumId<<1) | (passLooseId<<2) | (passVetoId<<3);

      //save the electron
      const reco::GenParticle * gen=el.genLepton(); 
      isPromptFinalState[nl] = gen ? gen->isPromptFinalState() : false;
      isDirectPromptTauDecayProductFinalState[nl] = gen ? gen->isDirectPromptTauDecayProductFinalState() : false;
      l_id[nl] = el.pdgId();
      l_charge[nl] = el.charge();
      l_pt[nl] = el.pt();
      l_eta[nl] = el.eta();
      l_phi[nl] = el.phi();
      l_mass[nl] = el.mass();
      if(gen != nullptr) {
        //save the gen-matched electron
        l_g_pt[nl] = gen->pt();
        l_g_eta[nl] = gen->eta();
        l_g_phi[nl] = gen->phi();
        l_g_mass[nl] = gen->mass();
        l_g_id[nl] = gen->pdgId();
      }
      double neutral = el.pfIsolationVariables().sumNeutralHadronEt + el.pfIsolationVariables().sumPhotonEt  - 0.5*el.pfIsolationVariables().sumPUPt;
      if(neutral < 0) neutral = 0;
      l_relIso[nl] = (el.pfIsolationVariables().sumChargedHadronPt+ neutral)/el.pt();     
      l_chargedHadronIso[nl] = el.chargedHadronIso();
      float t_l_ip3d(-9999.);
      float t_l_ip3dsig(-9999);
      if(el.gsfTrack().get()) {
        l_dxy[nl] = el.gsfTrack()->dxy(primVtx.position());
        l_dxyE[nl] = el.gsfTrack()->dxyError();
        l_dz[nl] = el.gsfTrack()->dz(primVtx.position());
        l_dzE[nl] = el.gsfTrack()->dzError();
        t_l_ip3d = sqrt(pow(l_dxy[nl], 2) + pow(l_dz[nl], 2));
        //t_l_ip3d = fabs(el.dB(pat::Electron::PV3D))/el.edB(pat::Electron::PV3D);
        float l_ip3d_err = sqrt(pow(l_dxyE[nl], 2) + pow(l_dzE[nl], 2));
        t_l_ip3dsig = t_l_ip3d / l_ip3d_err;
	  }
	  l_ip3d[nl] = t_l_ip3d;
	  l_ip3dsig[nl] = t_l_ip3dsig;
      nl++;
      nleptons += (passTightId && el.pt()>25 && fabs(el.eta())<2.5);
    }

  if(nleptons == 0) return;

  // JETS
  using namespace edm;
  //Load jets
  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByToken(jetToken_,jets);
  edm::Handle<reco::GenJetCollection> genJets;
  iEvent.getByToken(genJetsToken_, genJets);


  bool matched[genJets->size()] = {false};

  // Fragmentation stuff
  nmeson = 0;
  nj = 0;
  ng = 0;
  npf = 0;
  for(auto jet = jets->begin();  jet != jets->end(); ++jet) {
    //saveJetConstituentPt(jet, recoJetConstituentPt, genJetConstituentPt, genJets);

    j_g[nj] = -1;
    float minDeltaR = 999.;
    float min_jet_dR = 0.01;
    float genPt = -1.;
    float genEta = -1.;
    float genPhi = -1.;
    j_pt[nj] = jet->pt();
    j_eta[nj] = jet->eta();
    j_phi[nj] = jet->phi();
    j_partflav[nj] = jet->partonFlavour();
    j_hadflav[nj] = jet->hadronFlavour();
    j_deepB[nj] = jet->bDiscriminator("pfDeepFlavourJetTags:probb") + jet->bDiscriminator("pfDeepFlavourJetTags:probbb") + jet->bDiscriminator("pfDeepFlavourJetTags:problepb");
    int igenjet = -1;
    bool good = false;
    for (const auto& genJet : *genJets) {
      igenjet++;
      if(matched[igenjet]) continue; // Already matched this jet
      //double jet_dR = pow(jet->eta() - genJet.eta(), 2) + pow(jet->phi() - genJet.phi(), 2);
      float jet_dR = reco::deltaR(*jet, genJet);
      if(jet_dR < min_jet_dR) {
        min_jet_dR = jet_dR;
        good = true;
        j_g[nj] = igenjet;
      }
    }
    if(good) {
      //j_g[nj] = igenjet;
      matched[igenjet] = true;
    }
    //else j_g[nj] = -1;
    //good = false;
    std::vector<const reco::Candidate*> pions;
    std::vector<const reco::Candidate*> muons;
    // Loop over the jet constituents
    for(unsigned int i = 0; i < jet->numberOfDaughters(); ++i) {
      const reco::Candidate* constituent = jet->daughter(i);
      if(constituent->pt() < 1) continue; // Only save pT >= 1 GeV
      if(constituent->charge() == 0) continue;

      // Save the reco level pt of the jet constituent

      // Find the gen jet constituent with the smallest delta R
      if(abs(constituent->pdgId()) == 211) pions.push_back(constituent);
      else if(abs(constituent->pdgId()) == 13) muons.push_back(constituent);
      for (const auto& genJet : *genJets) {
        g_j_id[ng] = genJet.pdgId();
        g_j_pt[ng] = genJet.pt();
        g_j_eta[ng] = genJet.eta();
        g_j_phi[ng] = genJet.phi();
        g_j_id[ng] = genJet.pdgId();
        for (unsigned int iGen = 0; iGen < genJet.numberOfDaughters(); ++iGen) {
          const reco::Candidate* genConstituent = genJet.daughter(iGen);
          float deltaR = reco::deltaR(*genConstituent, *constituent);
          if (deltaR < minDeltaR) {
              minDeltaR = deltaR;
              genPt = genConstituent->pt();
              genEta = genConstituent->eta();
              genPhi = genConstituent->phi();
          }
        }
        ng++;
      }
      if(constituent->charge() != 0) {
        pf_j[npf] = nj;
        pf_pt[npf] = constituent->pt();
        pf_eta[npf] = constituent->eta();
        pf_phi[npf] = constituent->phi();
        pf_id[npf] = constituent->pdgId();
        pf_g_pt[npf] = genPt;
        pf_g_eta[npf] = genEta;
        pf_g_phi[npf] = genPhi;
        pf_g_id[npf] = constituent->pdgId();
        pf_g_j[npf] = ng;
        npf++;
      }
    }

    // Loose check for charmed mesons
    if(pions.size() >= 2) {
      const float gMassK(0.4937),gMassPi(0.1396);
      for(size_t ipi = 0; ipi < pions.size(); ipi++) {
        for(size_t ik = 0; ik < pions.size(); ik++) { // Check all pairs for mass hypothesis (pi,K) and (K,pi)
          if(ipi == ik) continue;
          if(pions[ipi]->pdgId() * pions[ik]->pdgId() > 0) continue; //opposite sign only
          TLorentzVector pi;
          TLorentzVector k;
          pi.SetPtEtaPhiM(pions[ipi]->p4().Pt(), pions[ipi]->p4().eta(), pions[ipi]->p4().phi(), gMassPi);
          k.SetPtEtaPhiM(pions[ik]->p4().Pt(), pions[ik]->p4().eta(), pions[ik]->p4().phi(), gMassK);
          float mass = (pi+k).M();
          float pt = (pi+k).Pt();
          if(mass < 1.7 || mass > 2.0) continue; // Loose D0 mass window
          d0_mass[nmeson] = mass;
          d0_pt[nmeson] = pt;
          meson_j[nmeson] = nj;
          //xb.push_back(pt / jet->pt());
          xb[nmeson] = pt / jet->pt();
          nmeson++;
        }
      }
    }
    if(muons.size() >= 2) {
      const float gMassMu(0.1057);
      for(size_t imu1 = 0; imu1 < muons.size(); imu1++) {
        for(size_t imu2 = 0; imu2 < muons.size(); imu2++) { // Check all pairs for mass hypothesis (mu1,mu2) and (mu2,mu1)
          if(imu1 == imu2) continue;
          if(muons[imu1]->pdgId() * muons[imu2]->pdgId() > 0) continue; //opposite sign only
          TLorentzVector mu1;
          TLorentzVector mu2;
          mu1.SetPtEtaPhiM(muons[imu1]->p4().Pt(), muons[imu1]->p4().eta(), muons[imu1]->p4().phi(), gMassMu);
          mu2.SetPtEtaPhiM(muons[imu2]->p4().Pt(), muons[imu2]->p4().eta(), muons[imu2]->p4().phi(), gMassMu);
          float mass = (mu1+mu2).M();
          float pt = (mu1+mu2).Pt();
          if(mass < 2.8 || mass > 3.4) continue; // Loose J/Psi mass window
          jpsi_mass[nmeson] = mass;
          meson_j[nmeson] = nj;
          jpsi_pt[nmeson] = pt;
          //xb.push_back(pt / jet->pt());
          xb[nmeson] = pt / jet->pt();
          nmeson++;
        }
      }
    }
    nj++;
  }
  if(nj==0) return;
  tree_->Fill();


}


// ------------ method called once each job just before starting event loop  ------------
void
JetAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
JetAnalyzer::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
JetAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetAnalyzer);
