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

      std::vector<std::string> muTriggersToUse_, elTriggersToUse_;

      TTree *tree_;
      edm::Service<TFileService> fs;

      // ----------member data ---------------------------
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
  genJetsToken_(consumes<std::vector<reco::GenJet> >(edm::InputTag("pseudoTop:jets")))
{
   electronToken_ = mayConsume<edm::View<pat::Electron> >(iConfig.getParameter<edm::InputTag>("electrons"));
   elTriggersToUse_ = iConfig.getParameter<std::vector<std::string> >("elTriggersToUse");
   muTriggersToUse_ = iConfig.getParameter<std::vector<std::string> >("muTriggersToUse");
   //now do what ever initialization is needed
   //tree_ = new TTree("data","Tree with vectors");
   tree_ = fs->make<TTree>("JetData","JetData");

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
  //VERTICES
  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vtxToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  const reco::Vertex &primVtx = vertices->front();
  reco::VertexRef primVtxRef(vertices,0);
  std::vector<int> n_vtx;
  tree_->Branch("n_vtx",&n_vtx);
  n_vtx.push_back(vertices->size());
  if(n_vtx.size()==0) return;

  int nleptons(0);
  //MUON SELECTION: cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
  edm::Handle<pat::MuonCollection> muons;
  iEvent.getByToken(muonToken_, muons);
  std::vector<bool> isPromptFinalState;
  tree_->Branch("isPromptFinalState",&isPromptFinalState);
  std::vector<bool> isDirectPromptTauDecayProductFinalState;
  tree_->Branch("isDirectPromptTauDecayProductFinalState",&isDirectPromptTauDecayProductFinalState);
  std::vector<int> l_id;
  tree_->Branch("l_id",&l_id);
  std::vector<float> l_g;
  tree_->Branch("l_g",&l_g);
  std::vector<float> l_charge;
  tree_->Branch("l_charge",&l_charge);
  std::vector<float> l_pt;
  tree_->Branch("l_pt",&l_pt);
  std::vector<float> l_eta;
  tree_->Branch("l_eta",&l_eta);
  std::vector<float> l_phi;
  tree_->Branch("l_phi",&l_phi);
  std::vector<float> l_mass;
  tree_->Branch("l_mass",&l_mass);
  std::vector<float> l_g_pt;
  tree_->Branch("l_g_pt",&l_g_pt);
  std::vector<float> l_g_eta;
  tree_->Branch("l_g_eta",&l_g_eta);
  std::vector<float> l_g_phi;
  tree_->Branch("l_g_phi",&l_g_phi);
  std::vector<float> l_g_mass;
  tree_->Branch("l_g_mass",&l_g_mass);
  std::vector<float> l_g_id;
  tree_->Branch("l_g_id",&l_g_id);
  std::vector<int> l_pid;
  tree_->Branch("l_pid",&l_pid);
  std::vector<float> l_chargedHadronIso;
  tree_->Branch("l_chargedHadronIso",&l_chargedHadronIso);
  std::vector<float> l_relIso;
  tree_->Branch("l_relIso",&l_relIso);
  std::vector<float> l_ip3d;
  tree_->Branch("l_ip3d",&l_ip3d);
  std::vector<float> l_ip3dsig;
  tree_->Branch("l_ip3dsig",&l_ip3dsig);
  std::vector<float> l_dxy;
  tree_->Branch("l_dxy",&l_dxy);
  std::vector<float> l_dxyE;
  tree_->Branch("l_dxyE",&l_dxyE);
  std::vector<float> l_dz;
  tree_->Branch("l_dz",&l_dz);
  std::vector<float> l_dzE;
  tree_->Branch("l_dzE",&l_dzE);
  std::vector<bool> l_global;
  tree_->Branch("l_global",&l_global);
  std::vector<float> l_pf;
  tree_->Branch("l_pf",&l_pf);
  std::vector<float> l_nValTrackerHits;
  tree_->Branch("l_nValTrackerHits",&l_nValTrackerHits);
  std::vector<float> l_nValPixelHits;
  tree_->Branch("l_nValPixelHits",&l_nValPixelHits);
  std::vector<float> l_nMatchedStations;
  tree_->Branch("l_nMatchedStations",&l_nMatchedStations);
  std::vector<float> l_pixelLayerWithMeasurement;
  tree_->Branch("l_pixelLayerWithMeasurement",&l_pixelLayerWithMeasurement);
  std::vector<float> l_trackerLayersWithMeasurement;
  tree_->Branch("l_trackerLayersWithMeasurement",&l_trackerLayersWithMeasurement);
  std::vector<float> l_validFraction;
  tree_->Branch("l_validFraction",&l_validFraction);
  std::vector<float> l_chi2LocalPosition;
  tree_->Branch("l_chi2LocalPosition",&l_chi2LocalPosition);
  std::vector<float> l_trkKink;
  tree_->Branch("l_trkKink",&l_trkKink);
  std::vector<float> l_chi2norm;
  tree_->Branch("l_chi2norm",&l_chi2norm);
  std::vector<float> l_globalTrackNumberOfValidHits;
  tree_->Branch("l_globalTrackNumberOfValidHits",&l_globalTrackNumberOfValidHits);
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
      isPromptFinalState.push_back(gen ? gen->isPromptFinalState() : false);
      isDirectPromptTauDecayProductFinalState.push_back(gen ? gen->isDirectPromptTauDecayProductFinalState() : false);
      l_id.push_back(mu.pdgId());
      l_charge.push_back(mu.charge());
      l_pt.push_back(mu.pt());
      l_eta.push_back(mu.eta());
      l_phi.push_back(mu.phi());
      l_mass.push_back(mu.mass());
      if(gen != nullptr) {
        //save the gen-matched muon
        l_g_pt.push_back(gen->pt());
        l_g_eta.push_back(gen->eta());
        l_g_phi.push_back(gen->phi());
        l_g_mass.push_back(gen->mass());
        l_g_id.push_back(gen->pdgId());
      }
      l_pid.push_back((isTight | (isMedium<<1) | (isLoose<<2) | (isSoft<<3)));
      l_chargedHadronIso.push_back(mu.pfIsolationR04().sumChargedHadronPt);
      l_relIso.push_back(mu.passed(reco::Muon::PFIsoTight) |      // tight is l_relIso[imu]&0b1
                         mu.passed(reco::Muon::PFIsoMedium)<<1 | 
                         mu.passed(reco::Muon::PFIsoLoose)<<2);
      float t_l_ip3d(-9999.);
      float t_l_ip3dsig(-9999);
      if(mu.outerTrack().isNonnull()) {
        l_dxy.push_back(mu.dB());
        l_dxyE.push_back(mu.edB());
      }
      if(mu.innerTrack().isNonnull()) {
        //l_dxy.push_back(mu.dB());
        //l_dxyE.push_back(mu.edB());
        l_dxy.push_back(mu.innerTrack()->dxy(primVtx.position()));
        l_dxyE.push_back(mu.innerTrack()->dxyError());
        l_dz.push_back(mu.innerTrack()->dz(primVtx.position()));
        l_dzE.push_back(mu.innerTrack()->dzError());
        t_l_ip3d = sqrt(pow(l_dxy.back(), 2) + pow(l_dz.back(), 2));
        float l_ip3d_err = sqrt(pow(l_dxyE.back(), 2) + pow(l_dzE.back(), 2));
        t_l_ip3dsig = t_l_ip3d / l_ip3d_err;
        l_global.push_back(mu.isGlobalMuon());
        l_pf.push_back(mu.isPFMuon());
        l_nValTrackerHits.push_back(mu.innerTrack()->hitPattern().numberOfValidTrackerHits());
        l_nValPixelHits.push_back(mu.innerTrack()->hitPattern().numberOfValidPixelHits());
        l_nMatchedStations.push_back(mu.numberOfMatchedStations());
        l_pixelLayerWithMeasurement.push_back( mu.innerTrack()->hitPattern().pixelLayersWithMeasurement());
        l_trackerLayersWithMeasurement.push_back(mu.innerTrack()->hitPattern().trackerLayersWithMeasurement());

        //Medium
        l_validFraction.push_back(mu.innerTrack()->validFraction());
        l_chi2LocalPosition.push_back(mu.combinedQuality().chi2LocalPosition);
        l_trkKink.push_back(mu.combinedQuality().trkKink);
      }
	  l_ip3d.push_back(t_l_ip3d);
	  l_ip3dsig.push_back(t_l_ip3dsig);

      if (mu.globalTrack().isNonnull()) {
        l_chi2norm.push_back(mu.normChi2());
        l_global.push_back(mu.isGlobalMuon());
        l_pf.push_back(mu.isPFMuon());
        l_globalTrackNumberOfValidHits.push_back(mu.globalTrack()->hitPattern().numberOfValidMuonHits());
        l_nMatchedStations.push_back(mu.numberOfMatchedStations());
      }
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
      l_pid.push_back(passTightId | (passMediumId<<1) | (passLooseId<<2) | (passVetoId<<3));

      //save the electron
      const reco::GenParticle * gen=el.genLepton(); 
      isPromptFinalState.push_back(gen ? gen->isPromptFinalState() : false);
      isDirectPromptTauDecayProductFinalState.push_back(gen ? gen->isDirectPromptTauDecayProductFinalState() : false);
      l_id.push_back(el.pdgId());
      l_charge.push_back(el.charge());
      l_pt.push_back(el.pt());
      l_eta.push_back(el.eta());
      l_phi.push_back(el.phi());
      l_mass.push_back(el.mass());
      if(gen != nullptr) {
        //save the gen-matched electron
        l_g_pt.push_back(gen->pt());
        l_g_eta.push_back(gen->eta());
        l_g_phi.push_back(gen->phi());
        l_g_mass.push_back(gen->mass());
        l_g_id.push_back(gen->pdgId());
      }
      double neutral = el.pfIsolationVariables().sumNeutralHadronEt + el.pfIsolationVariables().sumPhotonEt  - 0.5*el.pfIsolationVariables().sumPUPt;
      if(neutral < 0) neutral = 0;
      l_relIso.push_back((el.pfIsolationVariables().sumChargedHadronPt+ neutral)/el.pt());     
      l_chargedHadronIso.push_back(el.chargedHadronIso());
      float t_l_ip3d(-9999.);
      float t_l_ip3dsig(-9999);
      if(el.gsfTrack().get()) {
        l_dxy.push_back(el.gsfTrack()->dxy(primVtx.position()));
        l_dxyE.push_back(el.gsfTrack()->dxyError());
        l_dz.push_back(el.gsfTrack()->dz(primVtx.position()));
        l_dzE.push_back(el.gsfTrack()->dzError());
        t_l_ip3d = sqrt(pow(l_dxy.back(), 2) + pow(l_dz.back(), 2));
        //t_l_ip3d = fabs(el.dB(pat::Electron::PV3D))/el.edB(pat::Electron::PV3D);
        float l_ip3d_err = sqrt(pow(l_dxyE.back(), 2) + pow(l_dzE.back(), 2));
        t_l_ip3dsig = t_l_ip3d / l_ip3d_err;
	  }
	  l_ip3d.push_back(t_l_ip3d);
	  l_ip3dsig.push_back(t_l_ip3dsig);
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


  std::vector<float> j_pt;
  std::vector<float> j_eta;
  std::vector<float> j_phi;
  std::vector<float> j_g;
  std::vector<float> j_deepB;
  std::vector<float> j_partflav;
  std::vector<float> j_hadflav;
  std::vector<float> pf_pt;
  std::vector<float> pf_eta;
  std::vector<float> pf_phi;
  std::vector<float> pf_id;
  std::vector<float> pf_j;
  std::vector<float> pf_g_pt;
  std::vector<float> pf_g_eta;
  std::vector<float> pf_g_phi;
  std::vector<float> pf_g_id;
  std::vector<float> pf_g_j;
  std::vector<float> g_j_pt;
  std::vector<float> g_j_eta;
  std::vector<float> g_j_phi;
  std::vector<float> g_j_id;
  std::vector<float> g_pt;
  std::vector<float> g_eta;
  std::vector<float> g_phi;
  std::vector<float> g_id;
  tree_->Branch("j_pt",&j_pt);
  tree_->Branch("j_eta",&j_eta);
  tree_->Branch("j_phi",&j_phi);
  tree_->Branch("j_g",&j_g);
  tree_->Branch("j_deepB",&j_deepB);
  tree_->Branch("j_partflav",&j_partflav);
  tree_->Branch("j_hadflav",&j_hadflav);
  tree_->Branch("pf_pt",&pf_pt);
  tree_->Branch("pf_eta",&pf_eta);
  tree_->Branch("pf_phi",&pf_phi);
  tree_->Branch("pf_id",&pf_id);
  tree_->Branch("pf_j",&pf_j);
  tree_->Branch("pf_g_pt",&pf_g_pt);
  tree_->Branch("pf_g_eta",&pf_g_eta);
  tree_->Branch("pf_g_phi",&pf_g_phi);
  tree_->Branch("pf_g_id",&pf_g_id);
  tree_->Branch("pf_g_j",&pf_g_j);
  tree_->Branch("g_j_pt",&g_j_pt);
  tree_->Branch("g_j_eta",&g_j_eta);
  tree_->Branch("g_j_phi",&g_j_phi);
  tree_->Branch("g_j_id",&g_j_id);
  tree_->Branch("g_pt",&g_pt);
  tree_->Branch("g_eta",&g_eta);
  tree_->Branch("g_phi",&g_phi);
  tree_->Branch("g_id",&g_id);
  bool matched[genJets->size()] = {false};
  for(auto jet = jets->begin();  jet != jets->end(); ++jet) {
    //saveJetConstituentPt(jet, recoJetConstituentPt, genJetConstituentPt, genJets);

    // Loop over the jet constituents
    //int j_g = -1;
    double minDeltaR = 999.;
    double min_jet_dR = 0.01;
    double genPt = -1.;
    double genEta = -1.;
    double genPhi = -1.;
    j_pt.push_back(jet->pt());
    j_eta.push_back(jet->eta());
    j_phi.push_back(jet->phi());
    j_partflav.push_back(jet->partonFlavour());
    j_hadflav.push_back(jet->hadronFlavour());
    j_deepB.push_back(jet->bDiscriminator("pfDeepFlavourJetTags:probb") + jet->bDiscriminator("pfDeepFlavourJetTags:probbb") + jet->bDiscriminator("pfDeepFlavourJetTags:problepb"));
    int igenjet = -1;
    bool good = false;
    for (const auto& genJet : *genJets) {
      igenjet++;
      if(matched[igenjet]) continue; // Already matched this jet
      //double jet_dR = pow(jet->eta() - genJet.eta(), 2) + pow(jet->phi() - genJet.phi(), 2);
      double jet_dR = reco::deltaR(*jet, genJet);
      if(jet_dR < min_jet_dR) {
        min_jet_dR = jet_dR;
        good = true;
      }
    }
    if(good) {
      j_g.push_back(igenjet);
      matched[igenjet] = true;
    }
    else j_g.push_back(-1);
    good = false;
    for(unsigned int i = 0; i < jet->numberOfDaughters(); ++i) {
      const reco::Candidate* constituent = jet->daughter(i);

      // Save the reco level pt of the jet constituent

      // Find the gen jet constituent with the smallest delta R
      for (const auto& genJet : *genJets) {
        g_j_id.push_back(genJet.pdgId());
        g_j_pt.push_back(genJet.pt());
        g_j_eta.push_back(genJet.eta());
        g_j_phi.push_back(genJet.phi());
        g_j_id.push_back(genJet.pdgId());
        for (unsigned int iGen = 0; iGen < genJet.numberOfDaughters(); ++iGen) {
          const reco::Candidate* genConstituent = genJet.daughter(iGen);
          double deltaR = reco::deltaR(*genConstituent, *constituent);
          if (deltaR < minDeltaR) {
              minDeltaR = deltaR;
              genPt = genConstituent->pt();
              genEta = genConstituent->eta();
              genPhi = genConstituent->phi();
          }
        }
      }
      if(constituent->charge() != 0) {
        pf_j.push_back(j_pt.size()-1);
        pf_pt.push_back(constituent->pt());
        pf_eta.push_back(constituent->eta());
        pf_phi.push_back(constituent->phi());
        pf_id.push_back(constituent->pdgId());
        pf_g_pt.push_back(genPt);
        pf_g_eta.push_back(genEta);
        pf_g_phi.push_back(genPhi);
        pf_g_id.push_back(constituent->pdgId());
        pf_g_j.push_back(g_pt.size()-1);
      }
    }
  }
  if(j_pt.size()==0) return;
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
