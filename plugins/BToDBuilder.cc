#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

#include <vector>
#include <memory>
#include <map>
#include <string>
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
//#include <DataFormats/JetReco/interface/GenJetMatching.h>
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/Statistics/interface/ChiSquaredProbability.h"
#include "helper.h"
#include <limits>
#include <algorithm>
#include "KinVtxFitter.h"

class BToDBuilder : public edm::global::EDProducer<> {

  // perhaps we need better structure here (begin run etc)
public:
  typedef std::vector<reco::TransientTrack> TransientTrackCollection;

  explicit BToDBuilder(const edm::ParameterSet &cfg):
    post_vtx_selection_{cfg.getParameter<std::string>("postVtxSelection")},
    isotracksToken_(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("tracks"))),
    isotrk_selection_{cfg.getParameter<std::string>("isoTracksSelection")},
    genIsotrk_selection_{cfg.getParameter<std::string>("genIsoTracksSelection")},
    genParticlesToken_(consumes<pat::PackedGenParticleCollection>(edm::InputTag("packedGenParticles"))),
    jetsToken_(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets"))),
    jets_selection_{cfg.getParameter<std::string>("jetsSelection")},
    genJetsToken_(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("genJets"))),
    beamspot_{consumes<reco::BeamSpot>( cfg.getParameter<edm::InputTag>("beamSpot") )},
    vertex_src_{consumes<reco::VertexCollection>( cfg.getParameter<edm::InputTag>("offlinePrimaryVertexSrc") )}
    {
      produces<pat::CompositeCandidateCollection>();
    }

  ~BToDBuilder() override {}
  
  void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions) {}
  
private:
  const StringCutObjectSelector<pat::CompositeCandidate> post_vtx_selection_; // cut on the di-lepton after the SV fit

  const edm::EDGetTokenT<pat::PackedCandidateCollection> isotracksToken_;
  const StringCutObjectSelector<pat::PackedCandidate> isotrk_selection_; 
  const StringCutObjectSelector<pat::PackedGenParticle> genIsotrk_selection_; 
  const edm::EDGetTokenT<pat::PackedGenParticleCollection> genParticlesToken_;


  const edm::EDGetTokenT<pat::JetCollection> jetsToken_;
  const StringCutObjectSelector<pat::Jet> jets_selection_; 
  const edm::EDGetTokenT<reco::GenJetCollection> genJetsToken_;

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_;  
  const edm::EDGetTokenT<reco::VertexCollection> vertex_src_;
};

void BToDBuilder::produce(edm::StreamID, edm::Event &evt, edm::EventSetup const &iSetup) const {

  //input
  edm::Handle<reco::BeamSpot> beamspot;
  evt.getByToken(beamspot_, beamspot);  

  edm::Handle<reco::VertexCollection> pvtxs;
  evt.getByToken(vertex_src_, pvtxs);
  if (pvtxs->empty()) return; // skip the event if no PV found
  const reco::Vertex &primVtx = pvtxs->front();
  reco::VertexRef primVtxRef(pvtxs,0);
  int nvtx = pvtxs->size();
  if(nvtx==0) return;

  edm::ESHandle<MagneticField> fieldHandle;
  iSetup.get<IdealMagneticFieldRecord>().get(fieldHandle);
  const MagneticField *fMagneticField = fieldHandle.product();
  AnalyticalImpactPointExtrapolator extrapolator(fMagneticField);

  edm::ESHandle<TransientTrackBuilder> theB ;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);

  //for isolation
  edm::Handle<pat::PackedCandidateCollection> iso_tracks;
  evt.getByToken(isotracksToken_, iso_tracks);
  unsigned int nTracks     = iso_tracks->size();

  // for gen paricles
  edm::Handle<pat::PackedGenParticleCollection> genParticles;
  evt.getByToken(genParticlesToken_,genParticles);

  //for jets
  edm::Handle<pat::JetCollection> jets;
  evt.getByToken(jetsToken_, jets);

  //for gen jets
  edm::Handle<reco::GenJetCollection> genJets;
  evt.getByToken(genJetsToken_, genJets);
  // Match reco jets to gen jets
  /*
  std::vector<std::pair<const reco::PFJet*, const reco::GenJet*>> jetMatches;
  reco::GenJetMatcher matcher(*genJets, *jets, true, true, 0.4);
  matcher.getJetMatches(jetMatches);
  */

  std::vector<size_t> used_pi_id, used_k_id, used_x_id;


  // output
  std::unique_ptr<pat::CompositeCandidateCollection> ret_val(new pat::CompositeCandidateCollection());
  size_t ijet = 0;
  //bool extraFound = false;
  for(auto jet = jets->begin();  jet != jets->end(); ++jet) {
    if( !jets_selection_(*jet) ) continue;
    size_t ndau = jet->numberOfDaughters();
    //ndau = ndau > 4 ? 4 : ndau; // Fit sometimes crashes at large candidates, low pT not modeled well anyway

    for(size_t iTrk=0; iTrk < ndau; ++iTrk) {

      const pat::PackedCandidate &trk1 = dynamic_cast<const pat::PackedCandidate &>(*jet->daughter(iTrk));
      //const pat::PackedCandidate & trk1 = (*iso_tracks)[iTrk];
      //if(abs(trk1.pdgId()) != 211) continue; // Charged hadrons
      if(abs(trk1.pdgId()) != 211 && abs(trk1.pdgId()) != 13) continue; // Charged hadrons or muons

      for(size_t jTrk=0; jTrk < ndau; ++jTrk) {
        
        const pat::PackedCandidate &trk2 = dynamic_cast<const pat::PackedCandidate &>(*jet->daughter(jTrk));
        //const pat::PackedCandidate & trk2 = (*iso_tracks)[jTrk];
        if(iTrk == jTrk) continue; // Need to check all (i,j) and (j,i), skip (i,i)
        //if(abs(trk2.pdgId()) != 211) continue; // Charged hadrons
        if(abs(trk2.pdgId()) != 211 && abs(trk2.pdgId()) != 13) continue; // Charged hadrons or muons
        if(trk1.pdgId()*trk2.pdgId() != -211*211 && trk1.pdgId()*trk2.pdgId() != -13*13) continue; // pi(K) K(pi) or mu mu
        if(trk1.charge() * trk2.charge() > 0) continue; // Opposite-signed pairs
        const float mass1 = abs(trk1.pdgId()) == 13 ? MUON_MASS : PI_MASS;
        const float mass2 = abs(trk2.pdgId()) == 13 ? MUON_MASS : K_MASS;
        const float sigma1 = abs(trk1.pdgId()) == 13 ? LEP_SIGMA : K_SIGMA; // K and pi have same sigma in helper.h
        const int meson_id = abs(trk1.pdgId()) == 13 ? 443 : 411;

        math::PtEtaPhiMLorentzVector k_p4( // k mass hypothesis for jTrk
          trk2.pt(), 
          trk2.eta(),
          trk2.phi(),
          mass2
        );

        pat::CompositeCandidate cand;
        cand.addUserInt("pi_idx", iTrk);
        cand.addUserInt("k_idx", jTrk);
        cand.setP4(trk1.p4() + k_p4);
        cand.setCharge(trk1.charge() + trk2.charge());
        // define selections for iso tracks (pT, eta, ...)
        //if( !jets_selection_(trk1) ) continue;
        //if( !jets_selection_(trk2) ) continue;
        if( !isotrk_selection_(trk1) ) continue;
        if( !isotrk_selection_(trk2) ) continue;
        if(!trk1.trackHighPurity()) continue;
        if(!trk2.trackHighPurity()) continue;
        /*
        */
        if(abs(trk1.pdgId()) == 13) { // J/Psi -> mu mu
          if(cand.mass() < 2.5 || cand.mass() > 3.5) continue; // Loose J/Psi window
        }
        else if(abs(trk1.pdgId()) == 211) { // D0 -> pi K
          if(cand.mass() < 1.7 || cand.mass() > 2.0) continue; // Loose D0 window
        }
        
        if(trk1.bestTrack() == nullptr || trk2.bestTrack() == nullptr) continue; // No transient track
        auto pi_ttrack = reco::TransientTrack( (*trk1.bestTrack()) , &(*fieldHandle));
        auto k_ttrack = reco::TransientTrack( (*trk2.bestTrack()) , &(*fieldHandle));

        KinVtxFitter fitter;
        try {
          fitter = KinVtxFitter(
            {pi_ttrack, k_ttrack},
            {mass1, mass2},
            {sigma1, sigma1} //some small sigma for the lepton mass
          );
        }
        catch (...) {
          std::cout << "Problem computing vertex" << std::endl;
          continue;
        }
        try {
        if(!fitter.success()) continue; // hardcoded, but do we need otherwise?
        }
        catch (...) {
           continue;
        }
        cand.setVertex( 
          reco::Candidate::Point( 
            fitter.fitted_vtx().x(),
            fitter.fitted_vtx().y(),
            fitter.fitted_vtx().z()
          )  
        );
        used_pi_id.emplace_back(iTrk);
        used_k_id.emplace_back(jTrk);
        cand.addUserInt("jid" , ijet);
        cand.addUserInt("meson_id" , meson_id);
        cand.addUserInt("sv_OK" , fitter.success());
        cand.addUserFloat("sv_chi2", fitter.chi2());
        cand.addUserFloat("sv_ndof", fitter.dof()); // float??
        cand.addUserFloat("sv_prob", fitter.prob());
        cand.addUserFloat("fitted_mll" , (fitter.daughter_p4(0) + fitter.daughter_p4(1)).mass());
        auto fit_p4 = fitter.fitted_p4();
        cand.addUserFloat("fitted_pt"  , fit_p4.pt()); 
        cand.addUserFloat("fitted_eta" , fit_p4.eta());
        cand.addUserFloat("fitted_phi" , fit_p4.phi());
        cand.addUserFloat("fitted_mass", fitter.fitted_candidate().mass());      
        cand.addUserFloat("fitted_massErr", sqrt(fitter.fitted_candidate().kinematicParametersError().matrix()(6,6)));      
        cand.addUserFloat(
          "cos_theta_2D", 
          cos_theta_2D(fitter, *beamspot, cand.p4())
          );
        cand.addUserFloat(
          "fitted_cos_theta_2D", 
          cos_theta_2D(fitter, *beamspot, fit_p4)
          );
        auto lxy = l_xy(fitter, *beamspot);
        cand.addUserFloat("l_xy", lxy.value());
        cand.addUserFloat("l_xy_unc", lxy.error());
        cand.addUserFloat("vtx_x", cand.vx());
        cand.addUserFloat("vtx_y", cand.vy());
        cand.addUserFloat("vtx_z", cand.vz());
        cand.addUserFloat("vtx_ex", sqrt(fitter.fitted_vtx_uncertainty().cxx()));
        cand.addUserFloat("vtx_ey", sqrt(fitter.fitted_vtx_uncertainty().cyy()));
        cand.addUserFloat("vtx_ez", sqrt(fitter.fitted_vtx_uncertainty().czz()));

        float sigmax = sqrt(fitter.fitted_vtx_uncertainty().cxx() + pow(primVtx.x(),2));
        float sigmay = sqrt(fitter.fitted_vtx_uncertainty().cyy() + pow(primVtx.y(),2));
        float sigmaz = sqrt(fitter.fitted_vtx_uncertainty().czz() + pow(primVtx.z(),2));

        float sigmaL3D = 1.0 / sqrt( pow( (fit_p4.Px()/fit_p4.M())/sigmax,2 ) +
                                     pow( (fit_p4.Py()/fit_p4.M())/sigmay,2 ) +
                                     pow( (fit_p4.Pz()/fit_p4.M())/sigmaz,2 ) );

        float L3D = (fit_p4.Px()/fit_p4.M()) * pow(sigmaL3D/sigmax,2) * (cand.vx() - primVtx.x()) +
                    (fit_p4.Py()/fit_p4.M()) * pow(sigmaL3D/sigmay,2) * (cand.vy() - primVtx.y()) +
                    (fit_p4.Pz()/fit_p4.M()) * pow(sigmaL3D/sigmaz,2) * (cand.vz() - primVtx.z());

        cand.addUserFloat("vtx_l3d", L3D);
        cand.addUserFloat("vtx_el3d", sigmaL3D);

        cand.addUserFloat("fitted_pi_pt" , fitter.daughter_p4(0).pt()); 
        cand.addUserFloat("fitted_pi_eta", fitter.daughter_p4(0).eta());
        cand.addUserFloat("fitted_pi_phi", fitter.daughter_p4(0).phi());
        cand.addUserFloat("fitted_k_pt" , fitter.daughter_p4(1).pt()); 
        cand.addUserFloat("fitted_k_eta", fitter.daughter_p4(1).eta());
        cand.addUserFloat("fitted_k_phi", fitter.daughter_p4(1).phi());
      
        // kaon 3D impact parameter from dilepton SV
        /*
        */
        bool extraFound = false;
        for(size_t kTrk = 0; kTrk < ndau; ++kTrk) {
          if(kTrk == iTrk) continue;
          if(kTrk == jTrk) continue;
          const pat::PackedCandidate &trk3 = dynamic_cast<const pat::PackedCandidate &>(*jet->daughter(kTrk));
          if( !isotrk_selection_(trk3) ) continue;
          if(trk3.bestTrack() == nullptr) continue; // No transient track
          auto x_ttrack = reco::TransientTrack( (*trk3.bestTrack()) , &(*fieldHandle));
          if(abs(trk3.pdgId()) != 211 && abs(trk3.pdgId()) != 13) continue; // Charged hadrons
          const float mass3 = abs(trk3.pdgId()) == 13 ? MUON_MASS : K_MASS;
          const float sigma3 = abs(trk3.pdgId()) == 13 ? LEP_SIGMA : K_SIGMA;
          if(!trk3.trackHighPurity()) continue;
          if(abs(trk3.pdgId()) == 13 && !trk3.isTrackerMuon() && !trk3.isGlobalMuon()) continue; // global muons only
          //TrajectoryStateOnSurface tsos = extrapolator.extrapolate(x_ttrack.impactPointState(), fitter.fitted_vtx());
          //std::pair<bool,Measurement1D> cur2DIP = signedTransverseImpactParameter(tsos, fitter.fitted_refvtx(), *beamspot);
          //std::pair<bool,Measurement1D> cur3DIP = signedImpactParameter3D(tsos, fitter.fitted_refvtx(), *beamspot, (*pvtxs)[0].position().z());
          cand.addUserFloat("x_pt" , trk3.pt()); 
          cand.addUserFloat("x_eta", trk3.eta());
          cand.addUserFloat("x_phi", trk3.phi());
          cand.addUserInt("x_idx", kTrk);
          cand.addUserInt("x_id", trk3.pdgId());
          /*
          KinVtxFitter fitter3(
            {pi_ttrack, k_ttrack, x_ttrack},
            {mass1, mass2, mass},
            {sigma1, sigma1, sigma} //some small sigma for the lepton mass
          );
          if(!fitter3.success()) continue; // hardcoded, but do we need otherwise?
          pat::CompositeCandidate cand3;
          cand3.setVertex( 
            reco::Candidate::Point( 
              fitter3.fitted_vtx().x(),
              fitter3.fitted_vtx().y(),
              fitter3.fitted_vtx().z()
            )  
          );
          used_x_id.emplace_back(kTrk);
          cand.addUserInt("x_idx", kTrk);
          cand.addUserInt("x_id", trk3.pdgId());
          cand.addUserFloat("fitted_mass3", fitter3.fitted_candidate().mass());      
          cand.addUserFloat("fitted_massErr3", sqrt(fitter3.fitted_candidate().kinematicParametersError().matrix()(6,6)));      
          cand.addUserFloat("fitted_x_pt" , fitter3.daughter_p4(2).pt()); 
          cand.addUserFloat("fitted_x_eta", fitter3.daughter_p4(2).eta());
          cand.addUserFloat("fitted_x_phi", fitter3.daughter_p4(2).phi());
          */
          
          extraFound = true;
          //cand.addUserFloat("x_svip2d" , cur2DIP.second.value());
          //cand.addUserFloat("x_svip2d_err" , cur2DIP.second.error());
          //cand.addUserFloat("x_svip3d" , cur3DIP.second.value());
          //cand.addUserFloat("x_svip3d_err" , cur3DIP.second.error());
        } // kTrk
        /*
        */
        if(!extraFound) {
          cand.addUserFloat("x_pt" , -1); 
          cand.addUserFloat("x_eta", -1);
          cand.addUserFloat("x_phi", -1);
          cand.addUserInt("x_id", 0);
          cand.addUserInt("x_idx", -1);
        } 

        if( !post_vtx_selection_(cand) ) continue;
        float best_pi_dR = 0.1;
        float best_k_dR = 0.1;
        int best_pi_id = 0;
        int best_k_id = 0;
        int best_pi_idx = -1;
        int best_k_idx = -1;
        int best_pi_mother = -1;
        int best_k_mother = -1;
        for(size_t igen = 0; igen < genParticles->size(); igen++) {
          const pat::PackedGenParticle & genIt = (*genParticles)[igen];
          if( !genIsotrk_selection_(genIt) ) continue;
          if(abs(genIt.motherRef()->pdgId())!=5 && abs(genIt.motherRef()->pdgId())%100!=5 && abs(genIt.motherRef()->pdgId())%1000!=5) continue; // Not from b or B hadron
          if(reco::deltaR(trk1, genIt) > best_pi_dR && reco::deltaR(trk2, genIt) > best_k_dR) continue; // no match found
          if(reco::deltaR(trk1, genIt) < best_pi_dR) {
            best_pi_id = genIt.pdgId();
            best_pi_idx = igen;
            best_pi_mother = genIt.motherRef()->pdgId();
          }
          if(reco::deltaR(trk1, genIt) < best_pi_dR) {
            best_pi_dR = reco::deltaR(trk1, genIt);
            best_pi_id = genIt.pdgId();
            best_pi_idx = igen;
            best_pi_mother = genIt.motherRef()->pdgId();
          }
          else if(reco::deltaR(trk2, genIt) < best_k_dR) {
            best_k_dR = reco::deltaR(trk2, genIt);
            best_k_id = genIt.pdgId();
            best_k_idx = igen;
            best_k_mother = genIt.motherRef()->pdgId();
          }
        } // igen
        /*
        for(auto genJet = genJets->begin();  genJet != genJets->end(); ++genJet) {
          if( !jets_selection_(*genJet) ) continue;
          if(1 - jet->pt() / genJet->pt() > 0.2) continue;
          if(reco::deltaR(*jet, *genJet) > 0.4) continue;
          size_t ngdau = jet->numberOfDaughters();
          //ngdau = ngdau > 4 ? 4 : ngdau; // Fit sometimes crashes at large candidates, low pT not modeled well anyway

          for(size_t gTrk=0; gTrk < ngdau; ++gTrk) {
            if(genJet->daughter(iTrk) == nullptr) continue;
            const reco::Candidate &trkg = dynamic_cast<const reco::Candidate &>(*genJet->daughter(iTrk));
            if(abs(trkg.pdgId()) != 13 && abs(trkg.pdgId()) != 211 && abs(trkg.pdgId()) != 321) continue; // Only check mu, pi, and K
            if(trkg.mother(0) == nullptr) continue;
            if(abs(trkg.mother(0)->pdgId())!=5 && abs(trkg.mother(0)->pdgId())%100!=5 && abs(trkg.mother(0)->pdgId())%1000!=5) continue; // Not from b or B hadron
            if(reco::deltaR(trk1, trkg) > best_pi_dR && reco::deltaR(trk2, trkg) > best_k_dR) continue; // no match found
            if(reco::deltaR(trk1, trkg) < best_pi_dR) {
              best_pi_id = trkg.pdgId();
              best_pi_idx = gTrk;
              if(trkg.mother(0) != nullptr)
                best_pi_mother = trkg.mother(0)->pdgId();
            }
            if(reco::deltaR(trk1, trkg) < best_pi_dR) {
              best_pi_dR = reco::deltaR(trk1, trkg);
              best_pi_id = trkg.pdgId();
              best_pi_idx = gTrk;
              if(trkg.mother(0) != nullptr)
                best_pi_mother = trkg.mother(0)->pdgId();
            }
            else if(reco::deltaR(trk2, trkg) < best_k_dR) {
              best_k_dR = reco::deltaR(trk2, trkg);
              best_k_id = trkg.pdgId();
              best_k_idx = gTrk;
              if(trkg.mother(0) != nullptr)
                best_k_mother = trkg.mother(0)->pdgId();
            }
          } // gTrk
        } // genJet
        */
        cand.addUserInt("pi_gidx", best_pi_idx);
        cand.addUserInt("pi_gid", best_pi_id);
        cand.addUserInt("pi_mother", best_pi_mother);
        cand.addUserInt("k_gidx", best_k_idx);
        cand.addUserInt("k_gid", best_k_id);
        cand.addUserInt("k_mother", best_k_mother);

        ret_val->push_back(cand);

      } // jTrk
    } // iTrk
    ijet++;
  } // jet

  for (auto & cand: *ret_val){
    cand.addUserInt("n_pi_used", std::count(used_pi_id.begin(),used_pi_id.end(),cand.userInt("pi_idx"))+std::count(used_k_id.begin(),used_k_id.end(),cand.userInt("pi_idx")));
    cand.addUserInt("n_k_used", std::count(used_pi_id.begin(),used_pi_id.end(),cand.userInt("k_idx"))+std::count(used_k_id.begin(),used_k_id.end(),cand.userInt("k_idx")));
    //cand.addUserInt("n_x_used", std::count(used_pi_id.begin(),used_pi_id.end(),cand.userInt("x_idx"))+std::count(used_x_id.begin(),used_x_id.end(),cand.userInt("x_idx")));
  }

  evt.put(std::move(ret_val));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(BToDBuilder);
