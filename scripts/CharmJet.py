#!/usr/bin/env python
# coding: utf-8

# In[1]:


import coffea
#from coffea import utils
import coffea.processor as processor
from coffea.analysis_tools import PackedSelection
import hist

import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

import cloudpickle
import gzip
import uproot


# In[2]:


fileset = {'ttbar': ['root://xrootd-cms.infn.it//store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_320.root']}


# In[3]:

import json
import argparse
parser = argparse.ArgumentParser(description='You can select which file to run over')
parser.add_argument('--ifile', default=-1 , help = 'File to run')
parser.add_argument('--json',  nargs='+'  , help = 'JSON of files', required=True)
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
print(fileset)
if ifile >= 0:
    fileset = {'ttbar': [fileset['ttbar'][ifile]]}
print(fileset)


# In[4]:


#from dask.distributed import Client

#client = Client("tls://localhost:8786")


# In[5]:


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
        jeta24 = abs(jets_eta) < 2.4
        leta24 = abs(leps_eta) < 2.4
        #is_ttbar = (ak.num(jets)>4)&(ak.num(bjets_tight)>1)&((ak.num(ele)>1)|(ak.num(mu)>1))# & (pad_jets[:,0].pt>30)# & ((pad_ele[:,0].pt>25) | (pad_mu[:,0].pt>25))#&(ht>180)
        return (nJets >= 1) & (nBJets >=1) & (nLep >= 1) & jpt30 & lpt25# & jeta24 & leta24


# In[6]:


class Processor(processor.ProcessorABC):
    def __init__(self):
        self.jpsi_mass_bins = np.linspace(2.8, 3.4, 61)
        self.d0_mass_bins = np.linspace(1.7, 2.0, 61)
        self.xb_bins = np.linspace(0, 1, 11)

        dataset_axis = hist.axis.StrCategory(name="dataset", label="", categories=[], growth=True)
        # Split data into 50 bins, ranging from 0 to 100.
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
        meson_axis = hist.axis.IntCategory(name="meson_id", label="Meson pdgId (411 D0, 41113 D0mu, 443 J/Psi, 443211 J/Psi+K)", categories=[411, 41113, 443])
        jet_axis = hist.axis.IntCategory(name="jet_id", label="Jet flavor", categories=list(range(1,7)))
        gen_axis = hist.axis.IntCategory(name="g_id", label="Gen-matched flavor", categories=[], growth=True)
        ctau_axis = hist.axis.Regular(name='ctau', label='Meson time of flight', bins=100, start=0, stop=100)
        self.output = processor.dict_accumulator({
            'j0pt': hist.Hist(dataset_axis, jpt_axis),
            'b0pt': hist.Hist(dataset_axis, bpt_axis),
            'l0pt': hist.Hist(dataset_axis, lpt_axis),
            'D0pt': hist.Hist(dataset_axis, D0pt_axis),
            'D0pipt': hist.Hist(dataset_axis, D0pipt_axis),
            'D0kpt': hist.Hist(dataset_axis, D0kpt_axis),
            'jet_id'  : hist.Hist(dataset_axis, meson_axis, jet_axis),
            'xb_mass_jpsi'  : hist.Hist(dataset_axis, meson_axis, xb_axis, jpsi_mass_axis),
            'xb_mass_d0'  : hist.Hist(dataset_axis, meson_axis, xb_axis, d0_mass_axis),
            'xb_mass_d0_gen'  : hist.Hist(dataset_axis, meson_axis, gen_axis, xb_axis, d0_mass_axis),
            'xb_jpsi'  : hist.Hist(dataset_axis, xb_jpsi_axis),
            'xb_d0'  : hist.Hist(dataset_axis, xb_axis),
            'xb_d0mu'  : hist.Hist(dataset_axis, xb_axis),
            'xb_ch'  : hist.Hist(dataset_axis, xb_ch_axis),
            'HT'  : hist.Hist(dataset_axis, HT_axis),
            'pdgid'  : hist.Hist(dataset_axis, pdgid_axis),
            'd0'  : hist.Hist(dataset_axis, d0_axis),
            'njets' : hist.Hist(dataset_axis, njets_axis),
            'nbjets' : hist.Hist(dataset_axis, nbjets_axis),
            'nleps' : hist.Hist(dataset_axis, nleps_axis),
            'jpsi_mass': hist.Hist(dataset_axis, meson_axis, jpsi_mass_axis),
            'd0_mass': hist.Hist(dataset_axis, meson_axis, d0_mass_axis),
            'ctau': hist.Hist(dataset_axis, ctau_axis, meson_axis),
            'vtx_mass_d0' : hist.Hist(dataset_axis, hist.axis.Regular(name='vtx', label='Vertex prob.', bins=100, start=0, stop=.1), d0_mass_axis),
            'chi_mass_d0' : hist.Hist(dataset_axis, hist.axis.Regular(name='chi', label='$\chi^2$ prob.', bins=100, start=0, stop=.1), d0_mass_axis),
            'vtx_mass_jpsi' : hist.Hist(dataset_axis, hist.axis.Regular(name='vtx', label='Vertex prob.', bins=100, start=0, stop=.1), jpsi_mass_axis),
            'chi_mass_jpsi' : hist.Hist(dataset_axis, hist.axis.Regular(name='chi', label='$\chi^2$ prob.', bins=100, start=0, stop=.1), jpsi_mass_axis),
            'sumw'  : processor.defaultdict_accumulator(int),
            'sumw2' : processor.defaultdict_accumulator(int),
            
        })


    def process(self, events):
        dataset = events.metadata["dataset"]
        selections = PackedSelection(dtype='uint64')
        #events = events[events.is_ttbar]
        jets = events.Jet
        ele  = events.Electron
        mu   = events.Muon
        leptons = ak.with_name(ak.concatenate([ele, mu], axis=1), 'PtEtaPhiMCandidate')
        leptons = leptons[ak.argsort(leptons.pt, axis=1, ascending=False)]
        
        '''
        jets_pt = ak.fill_none(ak.pad_none(jets.pt, 1), 0)
        ele_pt  = ak.fill_none(ak.pad_none(ele.pt, 1), 0)
        mu_pt   = ak.fill_none(ak.pad_none(mu.pt, 1), 0)
        
        jets_eta = ak.fill_none(ak.pad_none(jets.eta, 1), 0)
        ele_eta  = ak.fill_none(ak.pad_none(ele.eta, 1), 0)
        mu_eta   = ak.fill_none(ak.pad_none(mu.eta, 1), 0)
        '''
        
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
        #ctau_mask = ak.fill_none((charm_cand.l_xy / charm_cand.l_xy_unc) > 10, False) # Just d_xy for now
        #ctau = ak.firsts((charm_cand.l_xy / charm_cand.l_xy_unc)) # Just d_xy for now
        #l3d = np.sqrt(np.square(charm_cand.vtx_x) + np.square(charm_cand.vtx_y) + np.square(charm_cand.vtx_z))
        #l3d_e = np.sqrt(np.square(charm_cand.vtx_ex) + np.square(charm_cand.vtx_ey) + np.square(charm_cand.vtx_ez))
        #ctau_mask = ak.fill_none((l3d / l3d_e) > 10, False) # Just d_xy for now
        #ctau = ak.firsts(l3d / l3d_e)
        ctau_mask = ak.fill_none((charm_cand.vtx_l3d / charm_cand.vtx_el3d) > 10, False) # Just d_xy for now
        ctau = ak.firsts((charm_cand.vtx_l3d / charm_cand.vtx_el3d)) # Just d_xy for now
        chi2_mask = charm_cand.svprob>0.02
        b_mask = jets[charm_cand.jetIdx].btagDeepFlavB > tight
        d0_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 411)
        jpsi_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        d0_mask = chi2_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 411)
        jpsi_mask = chi2_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        selections.add('jpsi', ak.firsts(jpsi_mask, axis=1))
        selections.add('d0', ak.firsts(d0_mask, axis=1))
        #selections.add('d0', ak.firsts(d0_mask, axis=1) & (ht>180))
        selections.add('ctau', ak.firsts(ctau_mask, axis=1))
        mass = ak.firsts(charm_cand.fit_mass)

        print(g_kid, '\n\n\n\n')
        #g_pid_mask = ak.fill_none(g_pid == pid, False)
        #g_kid_mask = ak.fill_none(g_kid == kid, False)
        #pid[g_pid_mask] = g_pid
        #kid[g_kid_mask] = g_kid
        #pid[~g_pid_mask] = 0
        #kid[~g_kid_mask] = 0
        d0_gid = g_pid*1000 + g_kid
        weight  = events.Generator.weight

        # D0 mu tagged
        d0_mu_mask = abs(charm_cand.x_id)==13
        #selections.add('d0mu', ak.any(d0_mask, axis=1))
        charm_cand[d0_mu_mask]['meson_id'] = 41113
        d0_mu = charm_cand[d0_mu_mask]
        d0_mu = d0_mu[ak.argsort(d0_mu.pt, ascending=False)] # Sort in case we just want the hardest muon
        #xb_d0mu = ak.flatten((d0_mu.pt + d0_mu.x_pt)[events.is_ttbar] / jets.pt[d0_mu.jetIdx][events.is_ttbar])

        # Define xb
        xb = (charm_cand.fit_pt / jets[charm_cand.jetIdx].pt)
        xb_mu = (charm_cand.x_pt / jets[charm_cand.jetIdx].pt)
        #xb[d0_mu_mask] += xb_mu
        #xb = ak.fill_none(ak.firsts((charm_cand.fit_pt / jets[charm_cand.jetIdx].pt)[ptsort]), -1)
        xb = ak.firsts(xb)
        #xb = ak.fill_none(ak.firsts(xb), -1)

        meson_id = ak.firsts(charm_cand.meson_id)
        jet_id = ak.firsts(jets[charm_cand.jetIdx].partonFlavour)
        vtx = ak.firsts(charm_cand.svprob)
        chi = ak.firsts(charm_cand.chi2)

        ttbar_sel = selections.all('ttbar')
        cuts = {'ttbar': ['ttbar'], 'ctau': ['ttbar', 'ctau'], 'd0': ['ttbar', 'ctau', 'd0'], 'jpsi': ['ttbar', 'ctau', 'jpsi']}
        jpsi_sel = selections.all('ttbar', 'jpsi', 'ctau')
        d0_sel = selections.all('ttbar', 'd0', 'ctau')
        self.output['j0pt'].fill(dataset=dataset, j0pt=j0pt[d0_sel], weight=weight[d0_sel])
        self.output['b0pt'].fill(dataset=dataset, b0pt=b0pt[d0_sel], weight=weight[d0_sel])
        self.output['l0pt'].fill(dataset=dataset, l0pt=l0pt[d0_sel], weight=weight[d0_sel])
        self.output['njets'].fill(dataset=dataset, njets=ak.fill_none(ak.num(jets), -1)[d0_sel], weight=weight[d0_sel])
        self.output['nbjets'].fill(dataset=dataset, nbjets=ak.fill_none(ak.num(bjets_tight), -1)[d0_sel], weight=weight[d0_sel])
        self.output['nleps'].fill(dataset=dataset, nleps=ak.fill_none(ak.num(leptons), -1)[d0_sel], weight=weight[d0_sel])
        self.output['HT'].fill(dataset=dataset, HT=ht[ttbar_sel], weight=weight[ttbar_sel])
        self.output['xb_jpsi'].fill(dataset=dataset, xb_jpsi=xb[jpsi_sel], weight=weight[jpsi_sel])
        self.output['jpsi_mass'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['jet_id'].fill(dataset=dataset, jet_id=jet_id[d0_sel], meson_id=meson_id[d0_sel], weight=weight[d0_sel])
        self.output['jet_id'].fill(dataset=dataset, jet_id=jet_id[jpsi_sel], meson_id=meson_id[jpsi_sel], weight=weight[jpsi_sel])
        self.output['xb_d0'].fill(dataset=dataset, xb=xb[d0_sel], weight=weight[d0_sel])
        self.output['xb_mass_jpsi'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], xb=xb[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['xb_mass_d0'].fill(dataset=dataset, meson_id=meson_id[d0_sel], xb=xb[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['xb_mass_d0_gen'].fill(dataset=dataset, meson_id=meson_id[d0_sel], g_id=d0_gid[d0_sel], xb=xb[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['vtx_mass_d0'].fill(dataset=dataset, vtx=vtx[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['chi_mass_d0'].fill(dataset=dataset, chi=chi[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['vtx_mass_jpsi'].fill(dataset=dataset, vtx=vtx[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['chi_mass_jpsi'].fill(dataset=dataset, chi=chi[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['d0_mass'].fill(dataset=dataset, meson_id=meson_id[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['ctau'].fill(dataset=dataset, meson_id=meson_id[d0_sel], ctau=ctau[d0_sel], weight=weight[d0_sel])
        self.output['ctau'].fill(dataset=dataset, meson_id=meson_id[jpsi_sel], ctau=ctau[jpsi_sel], weight=weight[jpsi_sel])
        self.output['sumw'][dataset]  = ak.sum(events.Generator.weight, axis=0)
        self.output['sumw2'][dataset] = ak.sum(np.square(events.Generator.weight), axis=0)
        return self.output

    def postprocess(self, accumulator):
        return accumulator


# In[ ]:

'''
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
'''
futures_run = processor.Runner(
    executor = processor.FuturesExecutor(compression=None, workers=4),
    schema=processor.NanoAODSchema,
    #maxchunks=10,
    chunksize=2500000
)

output = futures_run(
    fileset=fileset,
    treename="Events",
    processor_instance=Processor()
)

#with gzip.open('xb.pkl.gz', "wb") as fout:
#    cloudpickle.dump(output, fout)

coffea.util.save(output, f'/afs/cern.ch/user/b/byates/CMSSW_10_6_18/src/BFrag/BFrag/histos/coffea_{ifile}.pkl')

'''


# In[21]:


output['d0_mass'].plot1d()
#output['d0_mu_mass'].plot1d()


# In[10]:


output['njets'].plot1d(label='njets')
output['nbjets'].plot1d(label='nbjets')
output['nleps'].plot1d(label='nleps')
plt.legend()


# In[11]:


output['l0pt'].plot1d(label='l0 pt')
output['j0pt'].plot1d(label='j0 pt')
plt.legend()


# In[12]:


output['HT'].plot1d(label='HT')


# In[13]:


#output['j0pt'].plot1d()
output['b0pt'].plot1d()
output['D0pt'].plot1d()


# In[14]:


output['xb'].plot1d()
output['xb_ch'].plot1d()


# In[15]:


output['HT'].plot1d()


# In[16]:


output['pdgid'].plot1d()


# In[17]:


output['d0'].plot1d()


# In[18]:


output.keys()


# In[19]:


import matplotlib.pyplot as plt


# In[42]:


xb_bins = np.linspace(0, 1, 11)
#output['d0_1'].plot1d(label='d0_1')
#output['d0_2'].plot1d(label='d0_2')
#output['d0_3'].plot1d(label='d0_3')
#output['d0_4'].plot1d(label='d0_4')
#output['d0_5'].plot1d(label='d0_5')
#output['d0_6'].plot1d(label='d0_6')
#output['d0_7'].plot1d(label='d0_7')
#output['d0_8'].plot1d(label='d0_8')
for ibin in range(len(xb_bins)-1):
    key = f'd0_{ibin}'
    if 'd0_' in key and len(output[key].view()) != 0 and 'd0_' in key and 'mass' not in key:
    #if 'd0_' in key and 'd0_9' not in key:
        output[key].plot1d(label=f'{xb_bins[ibin]:.2f}' + ' < $x_{b}$ < ' + f'{xb_bins[ibin+1]:.2f}')
plt.legend()
xb_bins


# In[21]:


output['d0_mu_mass'].plot1d()


# In[22]:


output['xb'][{'dataset': sum}][0:len(output['xb'].axes['xb'].edges)]


# In[146]:


def d0_mass_fit(mass, mean, sigma, nsig, mean_kk, sigma_kk, nkk, mean_pp, sigma_pp, npp, l, nbkg):
    return \
    nsig * np.exp(-1/2 * (np.square(mass - mean) / np.square(sigma))) + \
    nkk  * np.exp(-1/2 * (np.square(mass - mean_kk) / np.square(sigma_kk))) + \
    npp  * np.exp(-1/2 * (np.square(mass - mean_pp) / np.square(sigma_pp))) + \
    nbkg * np.exp(l * mass)


# In[149]:


from scipy.optimize import curve_fit

mass_bins = np.linspace(1.7, 2.0, 31)
d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0 = 1.87, .01, 1, 1.78, 0.02, 100, 1.9, 0.02, 10, -2.27, 30
xb_mass = []
for ibin in range(len(xb_bins)-1):
    h = output[f'd0_{ibin}'].values()[0]
    plt.step(mass_bins[:-1], h, label=f'D0 {ibin}')
    g = [d0_mass_fit(x, d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0) for x in mass_bins]
    popt, pcov = curve_fit(d0_mass_fit, mass_bins[:-1], h, p0=[d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0], bounds=([1.85, 0, 0, 1.77, 0, 0, 1.88, 0, 0, -10, 0], [1.88, .02, 1000, 1.79, .02, 100, 1.91, .02, 10, 10, 10000]))
    plt.plot(mass_bins, d0_mass_fit(mass_bins, *popt), label=f'Fit {i}')
    #print(*popt)
    #print({name: round(val,2) for name,val in zip(('D0 mean', 'D0 width', 'N D0', 'lambda', 'N bkg'), popt)})
    print(f'N D0 {round(popt[2])} +/- {round(np.sqrt(pcov[2][2]))}, N bkg {round(popt[4])} +/- {round(np.sqrt(pcov[4][4]))}')
    xb_mass.append(popt[2])
plt.legend()

output['xb_mass'] = xb_mass

# In[134]:


xb_center = [np.average([low, high]) for low,high in zip(xb_bins[:-1], xb_bins[1:])]
plt.step(x=xb_bins[:-1], y=xb_mass, label='$x_{\mathrm{b}}$ signal')
plt.legend()
'''
