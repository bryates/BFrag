import FWCore.ParameterSet.Config as cms
from BFrag.BFrag.common_cff import *

electronPairsForKee = cms.EDProducer(
    'DiElectronBuilder',
    src = cms.InputTag('electronsForAnalysis', 'SelectedElectrons'),
    transientTracksSrc = cms.InputTag('electronsForAnalysis', 'SelectedTransientElectrons'),
    lep1Selection = cms.string('pt > 1.3'),
    lep2Selection = cms.string(''),
    preVtxSelection = cms.string(
        'abs(userCand("l1").vz - userCand("l2").vz) <= 1. && mass() < 5 '
        '&& mass() > 0 && charge() == 0 && userFloat("lep_deltaR") > 0.03 && userInt("nlowpt")<2'
        
    ),
    postVtxSelection = cms.string('userFloat("sv_chi2") < 998 && userFloat("sv_prob") > 1.e-5'),
)

BToKee = cms.EDProducer(
    'BToKLLBuilder',
    dileptons = cms.InputTag('electronPairsForKee', 'SelectedDiLeptons'),
    dileptonKinVtxs = cms.InputTag('electronPairsForKee', 'SelectedDiLeptonKinVtxs'),
    leptonTransientTracks = electronPairsForKee.transientTracksSrc,
    kaons = cms.InputTag('tracksBPark', 'SelectedTracks'),
    kaonsTransientTracks = cms.InputTag('tracksBPark', 'SelectedTransientTracks'),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    offlinePrimaryVertexSrc = cms.InputTag('offlineSlimmedPrimaryVertices'),
    tracks = cms.InputTag("packedPFCandidates"),
    lostTracks = cms.InputTag("lostTracks"),
    kaonSelection = cms.string(''),
    isoTracksSelection = cms.string('pt > 0.5 && abs(eta)<2.5'),
    isoTracksDCASelection = cms.string('pt > 0.5 && abs(eta)<2.5'),
    isotrkDCACut = cms.double(1.0),
    isotrkDCATightCut = cms.double(0.1),
    drIso_cleaning = cms.double(0.03),
    preVtxSelection = cms.string(
        'pt > 1.75 && userFloat("min_dr") > 0.03 '
        '&& mass < 7. && mass > 4.'
        ),
    postVtxSelection = cms.string(
         'userInt("sv_OK") == 1 && userFloat("fitted_mass") > 4.5 && userFloat("fitted_mass") < 6.'
    )
)

muonPairsForKmumu = cms.EDProducer(
    'DiMuonBuilder',
    src = cms.InputTag('muonTrgSelector', 'SelectedMuons'),
    transientTracksSrc = cms.InputTag('muonTrgSelector', 'SelectedTransientMuons'),
    lep1Selection = cms.string('pt > 1.5'),
    lep2Selection = cms.string(''),
    preVtxSelection = cms.string('abs(userCand("l1").vz - userCand("l2").vz) <= 1. && mass() < 5 '
                                 '&& mass() > 0 && charge() == 0 && userFloat("lep_deltaR") > 0.03'),
    postVtxSelection = electronPairsForKee.postVtxSelection,
)

BToKmumu = cms.EDProducer(
    'BToKLLBuilder',
    dileptons = cms.InputTag('muonPairsForKmumu', 'SelectedDiLeptons'),
    dileptonKinVtxs = cms.InputTag('muonPairsForKmumu', 'SelectedDiLeptonKinVtxs'),
    leptonTransientTracks = muonPairsForKmumu.transientTracksSrc,
    kaons = BToKee.kaons,
    kaonsTransientTracks = BToKee.kaonsTransientTracks,
    beamSpot = cms.InputTag("offlineBeamSpot"),
    offlinePrimaryVertexSrc = cms.InputTag('offlineSlimmedPrimaryVertices'),
    tracks = cms.InputTag("packedPFCandidates"),
    lostTracks = cms.InputTag("lostTracks"),
    kaonSelection = cms.string(''),
    isoTracksSelection = BToKee.isoTracksSelection,
    isoTracksDCASelection = BToKee.isoTracksDCASelection,
    isotrkDCACut = BToKee.isotrkDCACut,
    isotrkDCATightCut = BToKee.isotrkDCATightCut,
    drIso_cleaning = BToKee.drIso_cleaning,
    # This in principle can be different between electrons and muons
    preVtxSelection = cms.string(
        'pt > 1.75 && userFloat("min_dr") > 0.03 '
        '&& mass < 7. && mass > 4.'
        ),
    postVtxSelection = cms.string(
         'userInt("sv_OK") == 1 && userFloat("fitted_mass") > 4.5 && userFloat("fitted_mass") < 6.'
    )
)

BToD = cms.EDProducer(
    'BToDBuilder',
    beamSpot = cms.InputTag("offlineBeamSpot"),
    offlinePrimaryVertexSrc = cms.InputTag('offlineSlimmedPrimaryVertices'),
    tracks = cms.InputTag("packedPFCandidates"),
    jets = cms.InputTag("slimmedJets"),
    genJets = cms.InputTag("slimmedGenJets"),
    isoTracksSelection = cms.string('pt > 0.5 && abs(eta)<2.5'),
    genIsoTracksSelection = cms.string('pt > 0.5 && abs(eta)<2.5 && (abs(pdgId)==211 || abs(pdgId)==13 || abs(pdgId)==321)'),# && (abs(motherRef->pdgId())!=5 || abs(motherRef->pdgId())%100!=5 || abs(motherRef->pdgId())%1000!=5)'),
    jetsSelection = cms.string('pt > 30 && abs(eta) < 2.5'),
    # This in principle can be different between electrons and muons
    postVtxSelection = cms.string(
         'userInt("sv_OK") == 1 && ((userFloat("fitted_mass") > 1.7 && userFloat("fitted_mass") < 2.0) || (userFloat("fitted_mass") > 2.5 && userFloat("fitted_mass") < 3.5))'
    )
)

BToDTable = cms.EDProducer(
    'SimpleCompositeCandidateFlatTableProducer',
    src = cms.InputTag("BToD"),
    cut = cms.string(""),
    name = cms.string("BToCharm"),
    doc = cms.string("BToD Variable"),
    singleton=cms.bool(False),
    extension=cms.bool(False),
    variables=cms.PSet(
        # pre-fit quantities
        CandVars,
        j_pt_ch = ufloat('j_pt_ch'),
        jetIdx = uint('jid'),
        piIdx = uint('pi_idx'),
        kIdx = uint('k_idx'),
        pigId = uint('pi_gid'),
        kgId = uint('k_gid'),
        pigIdx = uint('pi_gidx'),
        kgIdx = uint('k_gidx'),
        pi_mother = uint('pi_mother'),
        k_mother = uint('k_mother'),
        # fit and vtx info
        chi2 = ufloat('sv_chi2'),
        ndof = ufloat('sv_ndof'),
        svprob = ufloat('sv_prob'),
        l_xy = ufloat('l_xy'),
        l_xy_unc = ufloat('l_xy_unc'),
        vtx_x = ufloat('vtx_x'),
        vtx_y = ufloat('vtx_y'),
        vtx_z = ufloat('vtx_z'),
        vtx_ex = ufloat('vtx_ex'), ## only saving diagonal elements of the cov matrix
        vtx_ey = ufloat('vtx_ey'),
        vtx_ez = ufloat('vtx_ez'),
        vtx_l3d = ufloat('vtx_l3d'),
        vtx_el3d = ufloat('vtx_el3d'),
        # Mll
        mll_fullfit = ufloat('fitted_mll'),
        # Cos(theta)
        cos2D = ufloat('cos_theta_2D'),
        fit_cos2D = ufloat('fitted_cos_theta_2D'),
        # post-fit momentum
        fit_mass = ufloat('fitted_mass'),
        fit_massErr = ufloat('fitted_massErr'),
        fit_pt = ufloat('fitted_pt'),
        fit_eta = ufloat('fitted_eta'),
        fit_phi = ufloat('fitted_phi'),
        fit_pi_pt = ufloat('fitted_pi_pt'),
        fit_pi_eta = ufloat('fitted_pi_eta'),
        fit_pi_phi = ufloat('fitted_pi_phi'),
        fit_k_pt = ufloat('fitted_k_pt'),
        fit_k_eta = ufloat('fitted_k_eta'),
        fit_k_phi = ufloat('fitted_k_phi'),
        x_pt = ufloat('x_pt'),
        x_eta = ufloat('x_eta'),
        x_phi = ufloat('x_phi'),
        xIdx = uint('x_idx'),
        x_id = uint('x_id'),
        meson_id = uint('meson_id'),
        n_pi_used = uint('n_pi_used'),
        n_k_used = uint('n_k_used'),
    )
)

BToKeeTable = cms.EDProducer(
    'SimpleCompositeCandidateFlatTableProducer',
    src = cms.InputTag("BToKee"),
    cut = cms.string(""),
    name = cms.string("BToKEE"),
    doc = cms.string("BToKEE Variable"),
    singleton=cms.bool(False),
    extension=cms.bool(False),
    variables=cms.PSet(
        # pre-fit quantities
        CandVars,
        l1Idx = uint('l1_idx'),
        l2Idx = uint('l2_idx'),
        kIdx = uint('k_idx'),
        minDR = ufloat('min_dr'),
        maxDR = ufloat('max_dr'),
        # fit and vtx info
        #chi2 = ufloat('sv_chi2'),
        svprob = ufloat('sv_prob'),
        l_xy = ufloat('l_xy'),
        l_xy_unc = ufloat('l_xy_unc'),
        vtx_x = ufloat('vtx_x'),
        vtx_y = ufloat('vtx_y'),
        vtx_z = ufloat('vtx_z'),
        vtx_ex = ufloat('vtx_ex'), ## only saving diagonal elements of the cov matrix
        vtx_ey = ufloat('vtx_ey'),
        vtx_ez = ufloat('vtx_ez'),
        # Mll
        mll_raw = Var('userCand("dilepton").mass()', float),
        mll_llfit = Var('userCand("dilepton").userFloat("fitted_mass")', float), # this might not work
        mllErr_llfit = Var('userCand("dilepton").userFloat("fitted_massErr")', float), # this might not work
        mll_fullfit = ufloat('fitted_mll'),
        # Cos(theta)
        cos2D = ufloat('cos_theta_2D'),
        fit_cos2D = ufloat('fitted_cos_theta_2D'),
        # post-fit momentum
        fit_mass = ufloat('fitted_mass'),
        fit_massErr = ufloat('fitted_massErr'),
        fit_pt = ufloat('fitted_pt'),
        fit_eta = ufloat('fitted_eta'),
        fit_phi = ufloat('fitted_phi'),
        fit_l1_pt = ufloat('fitted_l1_pt'),
        fit_l1_eta = ufloat('fitted_l1_eta'),
        fit_l1_phi = ufloat('fitted_l1_phi'),
        fit_l2_pt = ufloat('fitted_l2_pt'),
        fit_l2_eta = ufloat('fitted_l2_eta'),
        fit_l2_phi = ufloat('fitted_l2_phi'),
        fit_k_pt = ufloat('fitted_k_pt'),
        fit_k_eta = ufloat('fitted_k_eta'),
        fit_k_phi = ufloat('fitted_k_phi'),
        k_svip2d = ufloat('k_svip2d'),
        k_svip2d_err = ufloat('k_svip2d_err'),
        k_svip3d = ufloat('k_svip3d'),
        k_svip3d_err = ufloat('k_svip3d_err'),
        l1_iso03 = ufloat('l1_iso03'),
        l1_iso04 = ufloat('l1_iso04'),
        l2_iso03 = ufloat('l2_iso03'),
        l2_iso04 = ufloat('l2_iso04'),
        k_iso03  = ufloat('k_iso03'),
        k_iso04  = ufloat('k_iso04'),
        b_iso03  = ufloat('b_iso03'),
        b_iso04  = ufloat('b_iso04'),
        l1_n_isotrk = uint('l1_n_isotrk'),
        l2_n_isotrk = uint('l2_n_isotrk'),
        k_n_isotrk = uint('k_n_isotrk'),
        b_n_isotrk = uint('b_n_isotrk'),
        l1_iso03_dca = ufloat('l1_iso03_dca'),
        l1_iso04_dca = ufloat('l1_iso04_dca'),
        l2_iso03_dca = ufloat('l2_iso03_dca'),
        l2_iso04_dca = ufloat('l2_iso04_dca'),
        k_iso03_dca  = ufloat('k_iso03_dca'),
        k_iso04_dca  = ufloat('k_iso04_dca'),
        b_iso03_dca  = ufloat('b_iso03_dca'),
        b_iso04_dca  = ufloat('b_iso04_dca'),
        l1_n_isotrk_dca = uint('l1_n_isotrk_dca'),
        l2_n_isotrk_dca = uint('l2_n_isotrk_dca'),
        k_n_isotrk_dca = uint('k_n_isotrk_dca'),
        b_n_isotrk_dca = uint('b_n_isotrk_dca'),
        l1_iso03_dca_tight = ufloat('l1_iso03_dca_tight'),
        l1_iso04_dca_tight = ufloat('l1_iso04_dca_tight'),
        l2_iso03_dca_tight = ufloat('l2_iso03_dca_tight'),
        l2_iso04_dca_tight = ufloat('l2_iso04_dca_tight'),
        k_iso03_dca_tight  = ufloat('k_iso03_dca_tight'),
        k_iso04_dca_tight  = ufloat('k_iso04_dca_tight'),
        b_iso03_dca_tight  = ufloat('b_iso03_dca_tight'),
        b_iso04_dca_tight  = ufloat('b_iso04_dca_tight'),
        l1_n_isotrk_dca_tight = uint('l1_n_isotrk_dca_tight'),
        l2_n_isotrk_dca_tight = uint('l2_n_isotrk_dca_tight'),
        k_n_isotrk_dca_tight = uint('k_n_isotrk_dca_tight'),
        b_n_isotrk_dca_tight = uint('b_n_isotrk_dca_tight'),
        n_k_used = uint('n_k_used'),
        n_l1_used = uint('n_l1_used'),
        n_l2_used = uint('n_l2_used'),
    )
)

BToKmumuTable = BToKeeTable.clone(
    src = cms.InputTag("BToKmumu"),
    name = cms.string("BToKMuMu"),
    doc = cms.string("BToKMuMu Variable")
)


CountBToD = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("BToD")
)    
CountBToKee = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("BToKee")
)    
CountBToKmumu = CountBToKee.clone(
    minNumber = cms.uint32(1),
    src = cms.InputTag("BToKmumu")
)


BToKMuMuSequence = cms.Sequence(
    (muonPairsForKmumu * BToKmumu)
)
BToKEESequence = cms.Sequence(
    (electronPairsForKee * BToKee)
)

BToDSequence = cms.Sequence(
    (BToD)
)

