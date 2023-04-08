import uproot
import awkward as ak
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.nanoevents.methods import base, vector, candidate


'''
fin = uproot.open("nano_mc2017_ULv2.root")
event = fin['Events']
j_pt = event['Jet_pt'].array()
j_eta = event['Jet_eta'].array()
j_phi = event['Jet_phi'].array()
t_vec = ak.zip({"pt" : j_pt, "eta" : j_eta, "phi" : j_phi, "mass" : j_mass}, with_name="Momentum4D")
'''
loose = 0.1355
medium = 0.4506      
tight = 0.7738

fname = '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230405_134841/0000/nano_mc2017_ULv2_101.root'
fname = 'root://ndcms.crc.nd.edu//store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230405_134841/0000/nano_mc2017_ULv2_101.root'
events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()
jets = events.Jet
#jet_const_mask = jets.nConstituents >= 4
b_med_jets_mask = jets['btagDeepFlavB'] > medium
b_med_jets = ak.pad_none(jets[b_med_jets_mask], 1)
pf = ak.with_name(events.PFCands._apply_global_index(b_med_jets.pFCandsIdxG), 'PtEtaPhiMCandidate')
#pf = events.PFCands[jets.pFCandsIdxG]
c = ak.cartesian([b_med_jets,pf], axis=0, nested=True)
#diags = c[ak.Array([[y for y in range(x+1) if x==y] for x in range(ak.num(c, axis=0))])]
#d0_cand = ak.combinations(pf, 2, fields=["pi","k"])
d0_cand = ak.cartesian({'pi':pf, 'k':pf})
pi = ak.flatten(d0_cand.pi)
k = ak.flatten(d0_cand.k)
pi = d0_cand.pi
k = d0_cand.k
k['mass'] = 0.4937
d0 = ak.flatten(pi, -1) + ak.flatten(k, -1)
#d0_mask = ((pi + k).mass > 1.7) & ((pi + k).mass < 2.0)
#d0 = d0[ak.num(d0, axis=-1)>0]
#d0 = d0[d0_mask]
#d0 = ak.pad_none(d0[d0_mask], 1)
#xb=(d0[:,0].pt / b_med_jets.pt)
#plt.hist(xb, bins=np.linspace(0, 1, 10))
#plt.show()
#d0 = ak.pad_none(d0, 1)[:,0] # Get first D0 only

#ak.flatten(pf.pt, axis=None)  / b_med_jets.pt[ak.flatten(ak.unzip(ak.zip([ak.local_index(pf,i) for i in range(pf.ndim)]))[1], axis=None)]
pf_j_pt = ak.unzip(ak.zip([pf.pt, b_med_jets.pt[ak.local_index(pf, -2)]]))[1]
d0_j_pt = ak.cartesian([d0.pt, b_med_jets.pt])
d0_mask = (ak.flatten(d0.mass)>1.7)&(ak.flatten(d0.mass)<2.0)
d0_mask = (d0.mass>1.8)&(d0.mass<1.9)
d0_lead_mass = ak.fill_none(ak.pad_none(d0.mass[d0_mask], 1), -1)[:,0]
d0_lead_pt = ak.fill_none(ak.pad_none(d0.pt[d0_mask], 1), -1)[:,0]
print(d0_lead_mass, ak.num(d0_lead_mass, axis=0))
print(ak.flatten(ak.fill_none(b_med_jets.pt, -1)[:,0], axis=0), ak.num(b_med_jets.pt[:,0], axis=0))
xb = d0_lead_pt / ak.flatten(ak.fill_none(b_med_jets.pt, -1)[:,0], axis=0)
print(xb[xb>0])
plt.hist(xb, np.linspace(0, 1, 10))
exit()
xb = ak.flatten(ak.unzip(d0_j_pt)[0])[d0_mask] / ak.flatten(ak.unzip(d0_j_pt)[1])[d0_mask]
plt.hist(xb, np.linspace(0, 1, 10))

'''
def update_mass(cands, mass=0.4937):
    px = cands.pt*np.cos(cands.phi)
    py = cands.pt*np.sin(cands.phi)
    pz = cands.pt*np.sinh(cands.eta)
    cands.mass = mass
    e = np.sqrt(np.square(px) + np.square(py) + np.square(pz) + np.square(mass))
    cands['e'] = e
    return cands

def inv_mass(cand1, cand2):
    px1 = cand1.pt*np.cos(cands.phi)
    py1 = cand1.pt*np.sin(cands.phi)
    pz1 = cand1.pt*np.sinh(cands.eta)
    e1 = cand1.e
    px2 = cand2.pt*np.cos(cands.phi)
    py2 = cand2.pt*np.sin(cands.phi)
    pz2 = cand2.pt*np.sinh(cands.eta)
    e2 = cand2.e
    return np.sqrt(np.square(e1+e2) - np.square(px+px) - np.square(py+py) - np.square(pz+pz))

def addCand(cand1, cand2):
    cand = ak.copy(cand1)
    cand.pt += cand2.pt
    cand.eta += cand2.eta
    cand.phi += cand2.phi
    cand.t += cand2.t

class PFfrag(vector.PtEtaPhiMLorentzVector, base.NanoCollection, base.Systematic):
    def __add__(self, rhs):
        pt = self.pt + rhs.pt
        eta = self.eta + rhs.eta
        phi = self.phi + rhs.phi
        e = self.E + rhs.E
        return ak.zip(
                      {
                          "pt": pt,
                          "eta": eta,
                          "phi": phi,
                          "t": e
                      },
                      with_name="PFfrag",
                      behavior=vector.behavior,
                     )
pi = ak.zip(
        {
            "pt": d0_cand.pi.pt,
            "eta": d0_cand.pi.eta,
            "phi": d0_cand.pi.phi,
            "mass": 0.1396
        },
        #with_name="PtEtaPhiMLorentzVector",
        with_name="PFfrag",
        behavior=vector.behavior,
    )
k = ak.zip(
        {
            "pt": d0_cand.k.pt,
            "eta": d0_cand.k.eta,
            "phi": d0_cand.k.phi,
            "mass": 0.4937
        },
        with_name="PFfrag",
        behavior=vector.behavior,
    )
'''
