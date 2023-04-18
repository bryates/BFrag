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
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
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
    jetsToken_(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets"))),
    jets_selection_{cfg.getParameter<std::string>("jetsSelection")},
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

  const edm::EDGetTokenT<pat::JetCollection> jetsToken_;
  const StringCutObjectSelector<pat::PackedCandidate> jets_selection_; 

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_;  
  const edm::EDGetTokenT<reco::VertexCollection> vertex_src_;
};

void BToDBuilder::produce(edm::StreamID, edm::Event &evt, edm::EventSetup const &iSetup) const {

  //input
  edm::Handle<reco::BeamSpot> beamspot;
  evt.getByToken(beamspot_, beamspot);  

  edm::Handle<reco::VertexCollection> pvtxs;
  evt.getByToken(vertex_src_, pvtxs);

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

  //for jets
  edm::Handle<pat::JetCollection> jets;
  evt.getByToken(jetsToken_, jets);

  std::vector<size_t> used_pi_id, used_k_id;


  // output
  std::unique_ptr<pat::CompositeCandidateCollection> ret_val(new pat::CompositeCandidateCollection());
  size_t ijet = 0;
  for(auto jet = jets->begin();  jet != jets->end(); ++jet) {
    unsigned int ndau = jet->numberOfDaughters();

    for(size_t iTrk=0; iTrk < ndau; ++iTrk) {
    //for( size_t iTrk=0; iTrk<nTracks; ++iTrk ) {
        //if(iTrk > 100) continue;

      const pat::PackedCandidate &trk1 = dynamic_cast<const pat::PackedCandidate &>(*jet->daughter(iTrk));
      //const pat::PackedCandidate & trk1 = (*iso_tracks)[iTrk];
      if(abs(trk1.pdgId()) != 211) continue; // Charged hadrons

      for(size_t jTrk=0; jTrk < ndau; ++jTrk) {
      //for( size_t jTrk=0; jTrk<nTracks; ++jTrk ) {
        //if(jTrk > 100) continue;
        
        const pat::PackedCandidate &trk2 = dynamic_cast<const pat::PackedCandidate &>(*jet->daughter(jTrk));
        //const pat::PackedCandidate & trk2 = (*iso_tracks)[jTrk];
        if(iTrk == jTrk) continue; // Need to check all (i,j) and (j,i), skip (i,i)
        if(abs(trk2.pdgId()) != 211) continue; // Charged hadrons
        if(trk1.charge() * trk2.charge() > 0) continue; // Opposite-signed pairs

        math::PtEtaPhiMLorentzVector k_p4( // k mass hypothesis for jTrk
          trk2.pt(), 
          trk2.eta(),
          trk2.phi(),
          K_MASS
        );

        pat::CompositeCandidate cand;
        cand.addUserInt("pi_idx", iTrk);
        cand.addUserInt("k_idx", jTrk);
        cand.setP4(trk1.p4() + k_p4);
        cand.setCharge(trk1.charge() + trk2.charge());
        // define selections for iso tracks (pT, eta, ...)
        if( !jets_selection_(trk1) ) continue;
        if( !jets_selection_(trk2) ) continue;
        //if( !isotrk_selection_(trk1) ) continue;
        //if( !isotrk_selection_(trk2) ) continue;
        if(!trk1.trackHighPurity()) continue;
        if(!trk2.trackHighPurity()) continue;
        //if(cand.mass() < 1.7 || cand.mass() > 2.0) continue; // Loose D0 window
        
        auto pi_ttrack = reco::TransientTrack( (*trk1.bestTrack()) , &(*fieldHandle));
        auto k_ttrack = reco::TransientTrack( (*trk2.bestTrack()) , &(*fieldHandle));
        if(trk1.bestTrack() == nullptr || trk2.bestTrack() == nullptr) continue; // No transient track

        KinVtxFitter fitter(
          {pi_ttrack, k_ttrack},
          {PI_MASS, K_MASS},
          {PI_SIGMA, K_SIGMA} //some small sigma for the lepton mass
        );
        if(!fitter.success()) continue; // hardcoded, but do we need otherwise?
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

        float sigmax = sqrt(fitter.fitted_vtx_uncertainty().cxx());
        float sigmay = sqrt(fitter.fitted_vtx_uncertainty().cyy());
        float sigmaz = sqrt(fitter.fitted_vtx_uncertainty().czz());

        float sigmaL3D = 1.0 / sqrt( pow( (fit_p4.Px()/fit_p4.M())/sigmax,2 ) +
                                     pow( (fit_p4.Py()/fit_p4.M())/sigmay,2 ) +
                                     pow( (fit_p4.Pz()/fit_p4.M())/sigmaz,2 ) );

        float L3D = (fit_p4.Px()/fit_p4.M()) * pow(sigmaL3D/sigmax,2) * (cand.vx()) +
                    (fit_p4.Py()/fit_p4.M()) * pow(sigmaL3D/sigmay,2) * (cand.vy()) +
                    (fit_p4.Pz()/fit_p4.M()) * pow(sigmaL3D/sigmaz,2) * (cand.vz());

        cand.addUserFloat("vtx_l3d", L3D);
        cand.addUserFloat("vtx_el3d", sigmaL3D);

        cand.addUserFloat("fitted_pi_pt" , fitter.daughter_p4(0).pt()); 
        cand.addUserFloat("fitted_pi_eta", fitter.daughter_p4(0).eta());
        cand.addUserFloat("fitted_pi_phi", fitter.daughter_p4(0).phi());
        cand.addUserFloat("fitted_k_pt" , fitter.daughter_p4(1).pt()); 
        cand.addUserFloat("fitted_k_eta", fitter.daughter_p4(1).eta());
        cand.addUserFloat("fitted_k_phi", fitter.daughter_p4(1).phi());
      
        // kaon 3D impact parameter from dilepton SV
        /* Play with this for D* -> D0 + pi
        TrajectoryStateOnSurface tsos = extrapolator.extrapolate(kaons_ttracks->at(k_idx).impactPointState(), dileptons_kinVtxs->at(ll_idx).fitted_vtx());
        std::pair<bool,Measurement1D> cur2DIP = signedTransverseImpactParameter(tsos, dileptons_kinVtxs->at(ll_idx).fitted_refvtx(), *beamspot);
        std::pair<bool,Measurement1D> cur3DIP = signedImpactParameter3D(tsos, dileptons_kinVtxs->at(ll_idx).fitted_refvtx(), *beamspot, (*pvtxs)[0].position().z());

        cand.addUserFloat("k_svip2d" , cur2DIP.second.value());
        cand.addUserFloat("k_svip2d_err" , cur2DIP.second.error());
        cand.addUserFloat("k_svip3d" , cur3DIP.second.value());
        cand.addUserFloat("k_svip3d_err" , cur3DIP.second.error());
        */

        if( !post_vtx_selection_(cand) ) continue;        

        ret_val->push_back(cand);

      } // jTrk
    } // iTrk
    ijet++;
  } // jet

  for (auto & cand: *ret_val){
    cand.addUserInt("n_pi_used", std::count(used_pi_id.begin(),used_pi_id.end(),cand.userInt("pi_idx"))+std::count(used_k_id.begin(),used_k_id.end(),cand.userInt("pi_idx")));
    cand.addUserInt("n_k_used", std::count(used_pi_id.begin(),used_pi_id.end(),cand.userInt("k_idx"))+std::count(used_k_id.begin(),used_k_id.end(),cand.userInt("k_idx")));
  }

  evt.put(std::move(ret_val));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(BToDBuilder);
