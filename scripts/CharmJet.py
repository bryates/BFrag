#!/usr/bin/env python3
import coffea
import coffea.processor as processor
from coffea.analysis_tools import PackedSelection
import hist

import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

import json
import argparse
parser = argparse.ArgumentParser(description='You can select which file to run over')
parser.add_argument('--ifile', default=-1 , help = 'File to run')
parser.add_argument('--json',  nargs='+'  , help = 'JSON of files', required=True)
#parser.add_argument('--xsec', help = 'JSON file of xsecs', required=True)
parser.add_argument('--scaleout', type=int, default=6 , help = 'File to run')
parser.add_argument('--njobs', type=int, default=4, help='Nuber of jobs')
args = parser.parse_args()
ifile = int(args.ifile)
jfile = args.json
fileset = {}
for jname in jfile:
    with open(jname) as jf:
        jlist = json.load(jf)
        for k,v in jlist.items():
            if k in fileset:
                fileset[k].append(v)
            else:
                if not type(v) == list:
                    v = [v]
                fileset[k] = v
if ifile >= 0:
    fileset = {'ttbar': [fileset['ttbar'][ifile]]}
#lumi = 35.9
#j_xsec = open(args.xsec)
#xsecs = json.load(j_xsec)

def is_ttbar(jets, bjets, leptons):
    jets_pt = ak.fill_none(ak.pad_none(jets.pt, 1), 0)
    leps_pt  = ak.fill_none(ak.pad_none(leptons.pt, 1), 0)
    
    jets_eta = ak.fill_none(ak.pad_none(jets.eta, 1), 0)
    leps_eta  = ak.fill_none(ak.pad_none(leptons.eta, 1), 0)
    
    nJets = ak.num(jets)
    nBJets = ak.num(bjets)
    nLep = ak.num(leptons)
    jpt30 = jets_pt[:,0] > 30
    lpt25 = (leps_pt[:,0] > 25)
    jeta24 = np.abs(jets_eta) < 2.4
    leta24 = np.abs(leps_eta) < 2.4
    #is_ttbar = (ak.num(jets)>4)&(ak.num(bjets_tight)>1)&((ak.num(ele)>1)|(ak.num(mu)>1))# & (pad_jets[:,0].pt>30)# & ((pad_ele[:,0].pt>25) | (pad_mu[:,0].pt>25))#&(ht>180)
    return (nJets >= 1) & (nBJets >=1) & (nLep >= 1) & jpt30 & lpt25# & jeta24 & leta24


class Processor(processor.ProcessorABC):
    def __init__(self):
        self.jpsi_mass_bins = np.linspace(2.8, 3.4, 61)
        self.d0_mass_bins = np.linspace(1.7, 2.0, 61)
        self.xb_bins = np.linspace(0, 1, 11)
        self.systematics = ['nominal', 'FSRup', 'FSRdown', 'ISRup', 'ISRdown']

        dataset_axis = hist.axis.StrCategory(name="dataset", label="", categories=[], growth=True)
        jpt_axis = hist.axis.Regular(name="j0pt", label="Leading jet $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=300)
        bpt_axis = hist.axis.Regular(name="b0pt", label="Leading b jet $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=300)
        lpt_axis = hist.axis.Regular(name="l0pt", label="Leading lepotn $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=100)
        D0pt_axis= hist.axis.Regular(name="D0pt", label="Leading D0 $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=100)
        D0pipt_axis= hist.axis.Regular(name="D0pipt", label="Leading D0 pi $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=100)
        D0kpt_axis= hist.axis.Regular(name="D0kpt", label="Leading D0 k $p_{\mathrm{T}}$ [GeV]", bins=50, start=0, stop=100)
        xb_jpsi_axis  = hist.axis.Regular(name="xb_jpsi",   label="$x_{\mathrm{b}}$", bins=10, start=0, stop=1)
        xb_axis  = hist.axis.Regular(name="xb",   label="$x_{\mathrm{b}}$", bins=10, start=0, stop=1)
        xb_ch_axis  = hist.axis.Regular(name="xb_ch",   label="$x_{\mathrm{b}} \Sigma p_{\mathrm{T}}^{\mathrm{charged}}$", bins=10, start=0, stop=1)
        HT_axis  = hist.axis.Regular(name="HT",   label="$H_{\mathrm{T}}$", bins=50, start=0, stop=1000)
        pdgid_axis= hist.axis.Regular(name="pdgid",   label="D0 id's", bins=10, start=0, stop=250)
        d0_axis  = hist.axis.Regular(name='d0',   label="$d_0$", bins=10, start=0, stop=100)
        njets_axis = hist.axis.Regular(name='njets', label='$N_{\mathrm{jets}}$', bins=10, start=0, stop=10)
        nbjets_axis = hist.axis.Regular(name='nbjets', label='$N_{\mathrm{b-jets}}$', bins=10, start=0, stop=10)
        nleps_axis = hist.axis.Regular(name='nleps', label='$N_{\mathrm{leps}}$', bins=10, start=0, stop=10)
        jpsi_mass_axis = hist.axis.Regular(name='jpsi_mass', label='J/Psi mass [GeV]', bins=len(self.jpsi_mass_bins), start=self.jpsi_mass_bins[0], stop=self.jpsi_mass_bins[-1])
        d0_mass_axis = hist.axis.Regular(name='d0_mass', label='D0 mass [GeV]', bins=len(self.d0_mass_bins), start=self.d0_mass_bins[0], stop=self.d0_mass_bins[-1])
        mass_axes = [hist.axis.Regular(name=f'd0_{int(xb_bin*10)}', label='D0 mass [GeV] (' + str(round(self.xb_bins[ibin], 2)) + ' < $x_{\mathrm{b}}$ < ' + str(round(self.xb_bins[ibin+1], 2)) + ')', bins=len(self.d0_mass_bins), start=self.d0_mass_bins[0], stop=self.d0_mass_bins[-1]) for ibin,xb_bin in enumerate(self.xb_bins[:-1])]
        meson_axis = hist.axis.IntCategory(name="meson_id", label="Meson pdgId (421 D0, 42113 D0mu, 443 J/Psi, 443211 J/Psi+K)", categories=[421, 42113, 443])
        jet_axis = hist.axis.IntCategory(name="jet_id", label="Jet flavor", categories=list(range(1,7)))
        pi_gen_axis = hist.axis.IntCategory(name="pi_gid", label="Gen-matched flavor", categories=[], growth=True)
        k_gen_axis = hist.axis.IntCategory(name="k_gid", label="Gen-matched flavor", categories=[], growth=True)
        pi_mother_gen_axis = hist.axis.IntCategory(name="pi_mother", label="Gen-matched flavor", categories=[], growth=True)
        k_mother_gen_axis = hist.axis.IntCategory(name="k_mother", label="Gen-matched flavor", categories=[], growth=True)
        ctau_axis = hist.axis.Regular(name='ctau', label='Meson time of flight', bins=100, start=0, stop=100)
        systematic_axis = hist.axis.StrCategory(name='systematic', categories=['nominal'],growth=True)
        self.output = processor.dict_accumulator({
            'j0pt': hist.Hist(dataset_axis, jpt_axis, systematic_axis),
            'b0pt': hist.Hist(dataset_axis, bpt_axis, systematic_axis),
            'l0pt': hist.Hist(dataset_axis, lpt_axis, systematic_axis),
            'D0pt': hist.Hist(dataset_axis, D0pt_axis, systematic_axis),
            'D0pipt': hist.Hist(dataset_axis, D0pipt_axis, systematic_axis),
            'D0kpt': hist.Hist(dataset_axis, D0kpt_axis, systematic_axis),
            'jet_id'  : hist.Hist(dataset_axis, meson_axis, jet_axis, systematic_axis),
            'xb_mass_jpsi'  : hist.Hist(dataset_axis, meson_axis, xb_axis, jpsi_mass_axis, systematic_axis),
            'xb_mass_d0mu'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0_pik'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0_kk'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0_pipi'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0_unmatched'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_mass_d0_gen'  : hist.Hist(dataset_axis, meson_axis, pi_gen_axis, k_gen_axis, pi_mother_gen_axis, k_mother_gen_axis, xb_axis, d0_mass_axis, systematic_axis),
            'xb_jpsi'  : hist.Hist(dataset_axis, xb_jpsi_axis, systematic_axis),
            'xb_d0'  : hist.Hist(dataset_axis, xb_axis, systematic_axis),
            'xb_d0mu'  : hist.Hist(dataset_axis, xb_axis, systematic_axis),
            'xb_ch'  : hist.Hist(dataset_axis, xb_ch_axis, systematic_axis),
            'HT'  : hist.Hist(dataset_axis, HT_axis, systematic_axis),
            'pdgid'  : hist.Hist(dataset_axis, pdgid_axis, systematic_axis),
            'd0'  : hist.Hist(dataset_axis, d0_axis, systematic_axis),
            'njets' : hist.Hist(dataset_axis, njets_axis, systematic_axis),
            'nbjets' : hist.Hist(dataset_axis, nbjets_axis, systematic_axis),
            'nleps' : hist.Hist(dataset_axis, nleps_axis, systematic_axis),
            'jpsi_mass': hist.Hist(dataset_axis, meson_axis, jpsi_mass_axis, systematic_axis),
            'd0_mass': hist.Hist(dataset_axis, meson_axis, d0_mass_axis, systematic_axis),
            'ctau': hist.Hist(dataset_axis, ctau_axis, meson_axis, systematic_axis),
            'vtx_mass_d0' : hist.Hist(dataset_axis, hist.axis.Regular(name='vtx', label='Vertex prob.', bins=100, start=0, stop=.1), d0_mass_axis, systematic_axis),
            'chi_mass_d0' : hist.Hist(dataset_axis, hist.axis.Regular(name='chi', label='$\chi^2$ vtx', bins=100, start=0, stop=5), d0_mass_axis, systematic_axis),
            'vtx_mass_jpsi' : hist.Hist(dataset_axis, hist.axis.Regular(name='vtx', label='Vertex prob.', bins=100, start=0, stop=.1), jpsi_mass_axis, systematic_axis),
            'chi_mass_jpsi' : hist.Hist(dataset_axis, hist.axis.Regular(name='chi', label='$\chi^2$ vtx', bins=100, start=0, stop=5), jpsi_mass_axis, systematic_axis),
            'sumw'  : processor.defaultdict_accumulator(int),
            'sumw2' : processor.defaultdict_accumulator(int),
            #'sumw_syst' : hist.Hist(hist.axis.Regular(name='weight', label='weight', bins=2, start=0, stop=2), systematic_axis),
            'sumwFSRup'  : processor.defaultdict_accumulator(int),
            'sumwFSRdown'  : processor.defaultdict_accumulator(int),
            'sumwISRup'  : processor.defaultdict_accumulator(int),
            'sumwISRdown'  : processor.defaultdict_accumulator(int),
        })


    def process(self, events):
        dataset = events.metadata["dataset"]
        selections = PackedSelection(dtype='uint32')
        jets = events.Jet
        ele  = events.Electron
        mu   = events.Muon
        leptons = ak.with_name(ak.concatenate([ele, mu], axis=1), 'PtEtaPhiMCandidate')
        leptons = leptons[ak.argsort(leptons.pt, axis=1, ascending=False)]
        j0pt = ak.fill_none(ak.firsts(jets.pt), -1)
        l0pt = ak.fill_none(ak.firsts(leptons.pt), -1)

        loose = 0.1355
        medium = 0.4506
        tight = 0.7738
        is_bjets_tight = jets['btagDeepFlavB'] > tight
        bjets_tight = ak.pad_none(jets[is_bjets_tight], 1)
        events['is_ttbar'] = is_ttbar(jets, bjets_tight, leptons)
        selections.add('ttbar', events.is_ttbar)
        ht = ak.sum(jets.pt, axis=-1)
        j0pt = ak.fill_none(ak.firsts(jets.pt), -1)
        l0pt = ak.fill_none(ak.firsts(leptons.pt), -1)
        b0pt = ak.fill_none(ak.firsts(bjets_tight.pt), -1)

        # Charm meson candidates from b-jets
        charm_cand = events.BToCharm
        ptsort = ak.argsort(charm_cand.pt, ascending=False)
        charm_cand = events.BToCharm[ptsort]
        ctau_mask = ak.fill_none((charm_cand.vtx_l3d / charm_cand.vtx_el3d) > 10, False)
        ctau = ak.firsts((charm_cand.vtx_l3d / charm_cand.vtx_el3d))
        chi2_mask = (charm_cand.svprob>0.02) & (charm_cand.chi2<5)
        b_mask = jets[charm_cand.jetIdx].btagDeepFlavB > tight
        d0_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 421)
        jpsi_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        d0_mask = chi2_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 421)
        jpsi_mask = chi2_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        selections.add('jpsi', ak.firsts(jpsi_mask, axis=1))
        #selections.add('d0', ak.firsts(d0_mask, axis=1) & (ht>180))
        selections.add('ctau', ak.firsts(ctau_mask, axis=1))
        selections.add('vtx', ak.firsts(chi2_mask, axis=1))
        #mass = ak.firsts(charm_cand.mass)
        mass = ak.firsts(charm_cand.fit_mass)

        pi_gid = ak.firsts(ak.fill_none(charm_cand.pigId, 0))
        k_gid = ak.firsts(ak.fill_none(charm_cand.kgId, 0))
        pi_mother = ak.firsts(ak.fill_none(charm_cand.pi_mother, 0))
        k_mother = ak.firsts(ak.fill_none(charm_cand.k_mother, 0))
        #d0_gid = np.abs(pi_gid)*1e6 + np.abs(k_gid)*1e3 + np.abs(
        maskpik = ((abs(pi_gid)==211) & (abs(k_gid)==321))
        maskkk = ((abs(pi_gid)==321) & (abs(k_gid)==321))
        maskpipi = ((abs(pi_gid)==211) & (abs(k_gid)==211))
        selections.add('d0_pik', maskpik)
        selections.add('d0_kk', maskkk)
        selections.add('d0_pipi', maskpipi)
        selections.add('d0_unmatched', (~maskpik & ~maskkk & ~maskpipi))
        weight = events.Generator.weight
        #weight = 1000.0 * lumi * xsec[dataset] / events.Generator.weight

        # D0 mu tagged
        d0_mu_mask = ak.any(np.abs(charm_cand.x_id)==13, -1)
        #d0_mu_mask = (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 421) & ak.any(np.abs(charm_cand.x_id)==13, -1)
        selections.add('d0', ak.firsts(d0_mask & ~d0_mu_mask, axis=-1))
        selections.add('d0mu', ak.firsts(d0_mask & d0_mu_mask, axis=-1))
        charm_cand[d0_mu_mask]['meson_id'] = 42113
        d0_mu = charm_cand[d0_mu_mask]
        d0_mu = d0_mu[ak.argsort(d0_mu.pt, ascending=False)] # Sort in case we just want the hardest muon
        #xb_d0mu = ak.flatten((d0_mu.pt + d0_mu.x_pt)[events.is_ttbar] / jets.pt[d0_mu.jetIdx][events.is_ttbar])

        # Define xb
        xb = (charm_cand.pt / jets[charm_cand.jetIdx].pt)
        xb_ch = (charm_cand.fit_pt / charm_cand.j_pt_ch)
        #xb = (charm_cand.fit_pt / jets[charm_cand.jetIdx].pt)
        #xb_mu = (charm_cand.x_pt / jets[charm_cand.jetIdx].pt)
        #xb[d0_mu_mask] += xb_mu
        #xb = ak.fill_none(ak.firsts((charm_cand.fit_pt / jets[charm_cand.jetIdx].pt)[ptsort]), -1)
        xb_d0mu = xb + charm_cand.x_pt / jets.pt[charm_cand.jetIdx]
        xb_d0mu_ch = xb + charm_cand.x_pt / charm_cand.j_pt_ch
        #xb_d0mu = xb[d0_mu_mask] + charm_cand.x_pt[d0_mu_mask] / jets.pt[charm_cand.jetIdx][d0_mu_mask]
        #print(xb[d0_mu_mask] + charm_cand.x_pt[d0_mu_mask] / jets.pt[charm_cand.jetIdx][d0_mu_mask], '\n\n\n\n')
        #xb[d0_mu_mask] = xb[d0_mu_mask] + charm_cand.x_pt[d0_mu_mask] / jets.pt[charm_cand.jetIdx][d0_mu_mask]
        xb = ak.firsts(xb)
        xb_ch = ak.firsts(xb_ch)
        xb_d0mu = ak.firsts(xb_d0mu)
        xb_d0mu_ch = ak.firsts(xb_d0mu_ch)
        #xb = ak.fill_none(ak.firsts(xb), -1)

        meson_id = ak.firsts(charm_cand.meson_id)
        jet_id = ak.firsts(jets[charm_cand.jetIdx].partonFlavour)
        vtx = ak.firsts(charm_cand.svprob)
        chi = ak.firsts(charm_cand.chi2)

        ttbar_sel = selections.all('ttbar')
        cuts = {'ttbar': ['ttbar'], 'ctau': ['ttbar', 'ctau'], 'd0': ['ttbar', 'ctau', 'vtx', 'd0'], 'jpsi': ['ttbar', 'ctau', 'vtx', 'jpsi']}
        jpsi_sel = selections.all('ttbar', 'jpsi', 'ctau', 'vtx')
        d0mu_sel = selections.all('ttbar', 'd0mu', 'ctau', 'vtx')
        d0_sel = selections.all('ttbar', 'd0', 'ctau', 'vtx')
        d0_pik = selections.all('ttbar', 'd0', 'd0_pik', 'ctau', 'vtx')
        d0_kk = selections.all('ttbar', 'd0', 'd0_kk', 'ctau', 'vtx')
        d0_pipi = selections.all('ttbar', 'd0', 'd0_pipi', 'ctau', 'vtx')
        d0_unmatched = selections.all('ttbar', 'd0', 'd0_unmatched', 'ctau', 'vtx')
        #self.output['j0pt'].fill(dataset=dataset, j0pt=j0pt[d0_sel], weight=weight[d0_sel])
        #self.output['b0pt'].fill(dataset=dataset, b0pt=b0pt[d0_sel], weight=weight[d0_sel])
        #self.output['l0pt'].fill(dataset=dataset, l0pt=l0pt[d0_sel], weight=weight[d0_sel])
        #self.output['njets'].fill(dataset=dataset, njets=ak.fill_none(ak.num(jets), -1)[d0_sel], weight=weight[d0_sel])
        #self.output['nbjets'].fill(dataset=dataset, nbjets=ak.fill_none(ak.num(bjets_tight), -1)[d0_sel], weight=weight[d0_sel])
        #self.output['nleps'].fill(dataset=dataset, nleps=ak.fill_none(ak.num(leptons), -1)[d0_sel], weight=weight[d0_sel])
        #self.output['HT'].fill(dataset=dataset, HT=ht[ttbar_sel], weight=weight[ttbar_sel])
        #self.output['xb_jpsi'].fill(dataset=dataset, xb_jpsi=xb[jpsi_sel], weight=weight[jpsi_sel])
        #self.output['jpsi_mass'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        #self.output['jet_id'].fill(dataset=dataset, jet_id=jet_id[d0_sel], meson_id=meson_id[d0_sel], weight=weight[d0_sel])
        #self.output['jet_id'].fill(dataset=dataset, jet_id=jet_id[jpsi_sel], meson_id=meson_id[jpsi_sel], weight=weight[jpsi_sel])
        #self.output['xb_d0'].fill(dataset=dataset, xb=xb[d0_sel], weight=weight[d0_sel])

        #Float_t PS weights (w_var / w_nominal); [0] is ISR=0.5 FSR=1; [1] is ISR=1 FSR=0.5; [2] is ISR=2
        syst_table = {
            'ISRdown': 0,
            'FSRdown': 1,
            'ISRup': 2,
            'FSRup': 3,
        }
        for syst in self.systematics:
            syst_weight = ak.ones_like(weight)
            if syst != 'nominal':
                syst_weight = events.PSWeight[:, syst_table[syst]]
                self.output[f'sumw{syst}'] = ak.sum(syst_weight*weight, axis=0)
                #self.output[f'sumw_syst']  = ak.sum(syst_weight, axis=0)
            self.output['xb_mass_jpsi'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], xb=xb_ch[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel]*syst_weight[jpsi_sel], systematic=syst)
            self.output['xb_mass_d0mu'].fill(dataset=dataset, meson_id=meson_id[d0mu_sel], xb=xb_d0mu_ch[d0mu_sel], d0_mass=mass[d0mu_sel], weight=weight[d0mu_sel]*syst_weight[d0mu_sel], systematic=syst)
            self.output['xb_mass_d0'].fill(dataset=dataset, meson_id=meson_id[d0_sel], xb=xb_ch[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel]*syst_weight[d0_sel], systematic=syst)
            self.output['xb_mass_d0_pik'].fill(dataset=dataset, meson_id=meson_id[d0_pik], xb=xb_ch[d0_pik], d0_mass=mass[d0_pik], weight=weight[d0_pik]*syst_weight[d0_pik], systematic=syst)
            self.output['xb_mass_d0_kk'].fill(dataset=dataset, meson_id=meson_id[d0_kk], xb=xb_ch[d0_kk], d0_mass=mass[d0_kk], weight=weight[d0_kk]*syst_weight[d0_kk], systematic=syst)
            self.output['xb_mass_d0_pipi'].fill(dataset=dataset, meson_id=meson_id[d0_pipi], xb=xb_ch[d0_pipi], d0_mass=mass[d0_pipi], weight=weight[d0_pipi]*syst_weight[d0_pipi], systematic=syst)
            self.output['xb_mass_d0_unmatched'].fill(dataset=dataset, meson_id=meson_id[d0_unmatched], xb=xb_ch[d0_unmatched], d0_mass=mass[d0_unmatched], weight=weight[d0_unmatched]*syst_weight[d0_unmatched], systematic=syst)
            #self.output['xb_mass_d0_gen'].fill(dataset=dataset, meson_id=meson_id[d0_sel], pi_gid=pi_gid[d0_sel], k_gid=k_gid[d0_sel], pi_mother=pi_mother[d0_sel], k_mother=k_mother[d0_sel], xb=xb[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel]*syst_weight[d0_sel], systematic=syst)
            self.output['vtx_mass_d0'].fill(dataset=dataset, vtx=vtx[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel]*syst_weight[d0_sel], systematic=syst)
            self.output['chi_mass_d0'].fill(dataset=dataset, chi=chi[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel]*syst_weight[d0_sel], systematic=syst)
            self.output['vtx_mass_jpsi'].fill(dataset=dataset, vtx=vtx[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel]*syst_weight[jpsi_sel], systematic=syst)
            self.output['chi_mass_jpsi'].fill(dataset=dataset, chi=chi[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel]*syst_weight[jpsi_sel], systematic=syst)
        #self.output['d0_mass'].fill(dataset=dataset, meson_id=meson_id[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        #self.output['ctau'].fill(dataset=dataset, meson_id=meson_id[d0_sel], ctau=ctau[d0_sel], weight=weight[d0_sel])
        #self.output['ctau'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], ctau=ctau[jpsi_sel], weight=weight[jpsi_sel])
        self.output['sumw'][dataset]  = ak.sum(events.Generator.weight, axis=0)
        self.output['sumw2'][dataset] = ak.sum(np.square(events.Generator.weight), axis=0)
        return self.output

    def postprocess(self, accumulator):
        return accumulator


from distributed import Client
from dask_jobqueue import HTCondorCluster
import socket

def hname():
    import socket
    return socket.gethostname()


def run_futures():
    output = processor.run_uproot_job(fileset=fileset, 
                       treename="Events",
                       processor_instance=Processor(),
                       #executor=processor.dask_executor,
                       #executor_args={'client': client, 'schema': processor.NanoAODSchema},
                       executor=processor.FuturesExecutor,
                       executor_args={'schema': processor.NanoAODSchema},
                       #maxchunks=50,
                       #chunksize=50)
                       chunksize=2500000)
    coffea.util.save(output, f'/afs/cern.ch/user/b/byates/CMSSW_10_6_18/src/BFrag/BFrag/histos/coffea_dask.pkl')

def run_dask():
    n_port = 8786
    with HTCondorCluster(
            cores=1,
            #memory='10000MB',
            memory='8GB',
            disk='1000MB',
            death_timeout = '300',
            #lcg = True,
            nanny = False,
            #container_runtime = "none",
            #container_runtime = "singularity",
            log_directory = "/afs/cern.ch/user/b/byates/CMSSW_10_6_18/src/BFrag/BFrag/logs",
            #log_directory = "/eos/user/b/byates/condor/log",
            scheduler_options={
                'port': n_port,
                'host': socket.gethostname(),
                },
            job_extra_directives={
                '+JobFlavour': '"longlunch"',
                },
            worker_extra_args = ['--worker-port 10000:10100']
            ) as cluster:
        print(cluster.job_script())
        with Client(cluster) as client:
            futures = []
            cluster.scale(args.njobs)
            for i in range(args.njobs):
              f = client.submit(hname)
              futures.append(f)
            print('Result is {}'.format(client.gather(futures)))
            print("Waiting for at least one worker...")
            client.wait_for_workers(1)
            from dask.distributed import performance_report
            with performance_report(filename="dask-report.html"):
                output = processor.run_uproot_job(
                    fileset,
                    treename="Events",
                    processor_instance=Processor(),
                    executor=processor.dask_executor,
                    executor_args={
                        "client": client,
                        #"skipbadfiles": args.skipbadfiles,
                        "schema": processor.NanoAODSchema,
                        "retries": 4,
                    },
                    chunksize=30_000,
                    #maxchunks=args.max,
                )
                coffea.util.save(output, f'/eos/cms/store/user/byates/bfrag/coffea_dask.pkl')

if __name__ == '__main__':
    run_dask()
    #run_futures()
:q	
