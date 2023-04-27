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


fileset = {'ttbar': ['/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_17.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_9.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_10.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_7.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_15.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_19.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_11.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_14.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_12.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_16.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_20.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_24.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_32.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_27.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_35.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_125.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_6.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_8.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_18.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_30.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_31.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_25.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_28.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_21.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_34.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_29.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_22.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_26.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_23.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_36.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_39.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_40.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_38.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_44.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_37.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_45.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_43.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_46.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_41.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_175.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_62.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_52.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_57.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_47.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_86.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_66.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_179.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_84.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_77.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_88.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_98.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_96.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_70.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_97.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_124.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_72.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_112.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_126.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_123.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_115.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_82.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_51.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_129.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_85.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_156.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_142.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_160.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_148.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_83.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_159.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_143.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_140.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_134.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_132.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_141.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_155.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_149.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_138.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_145.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_162.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_151.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_133.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_164.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_161.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_136.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_152.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_163.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_158.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_146.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_150.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_147.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_135.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_137.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_139.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_144.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_157.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_223.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_128.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_99.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_165.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_153.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_130.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_58.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_63.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_54.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_67.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_60.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_64.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_61.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_56.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_50.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_68.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_65.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_55.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_59.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_53.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_48.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_69.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_71.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_49.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_74.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_78.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_76.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_81.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_87.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_89.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_79.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_75.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_73.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_178.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_208.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_90.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_92.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_100.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_93.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_174.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_101.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_173.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_94.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_176.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_177.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_211.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_185.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_181.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_180.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_182.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_80.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_95.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_102.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_105.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_107.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_103.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_183.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_104.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_110.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_109.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_114.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_116.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_108.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_187.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_106.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_111.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_188.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_122.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_113.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_118.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_184.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_117.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_119.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_121.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_190.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_186.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_192.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_191.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_189.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_196.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_193.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_195.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_131.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_120.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_127.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_197.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_194.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_198.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_199.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_222.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_202.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_167.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_166.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_201.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_203.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_200.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_312.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_168.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_207.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_226.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_220.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_217.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_285.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_209.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_221.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_215.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_229.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_205.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_224.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_210.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_213.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_218.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_214.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_231.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_219.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_225.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_338.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_230.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_227.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_232.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_237.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_206.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_234.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_235.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_236.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_212.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_233.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_228.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_216.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_339.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_171.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_238.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_169.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_172.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_170.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_239.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_337.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_344.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_265.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_262.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_336.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_346.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_263.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_274.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_304.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_275.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_271.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_276.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_273.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_272.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_277.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_281.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_279.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_292.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_297.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_315.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_298.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_290.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_341.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_299.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_307.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_300.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_204.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_302.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_301.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_343.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_310.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_291.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_311.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_309.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_313.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_308.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_316.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_320.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_317.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_322.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_323.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_326.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_330.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_324.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_328.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_321.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_327.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_342.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_325.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_331.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_329.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_332.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_334.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_335.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_333.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_348.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_349.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_241.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_340.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_240.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_4.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_250.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_242.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_347.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_248.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_350.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_247.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_345.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_243.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_244.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_249.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_246.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_351.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_251.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_252.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_255.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_253.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_254.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_257.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_259.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_258.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_356.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_352.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_256.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_260.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_264.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_266.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_267.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_269.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_270.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_5.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-51.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_355.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_358.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_245.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_261.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_278.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-50.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_280.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_283.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_282.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_286.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_288.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_284.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_353.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_295.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_289.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_293.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_287.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_294.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_296.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_359.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-44.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_360.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_361.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_364.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_363.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_362.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-45.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-48.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-47.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-49.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-14.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_365.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_366.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-1.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_369.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-46.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_305.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-7.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-42.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_368.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_367.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_372.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-43.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_371.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_370.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_303.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_306.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_375.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_376.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-34.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_373.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_377.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_378.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_318.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-40.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-41.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-11.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-5.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_383.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-4.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_314.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-35.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_379.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-38.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-9.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-36.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-37.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_381.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-39.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_384.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_319.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-6.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-10.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_380.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-12.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-2.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-13.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-8.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-16.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_387.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-17.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_386.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-32.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_42.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_392.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-24.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_389.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_390.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-25.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-18.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-28.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-26.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_388.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-27.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_394.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-30.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-3.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_393.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_354.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-19.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-20.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-15.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_395.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-53.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_399.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-21.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-33.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-55.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_402.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_397.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_396.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_398.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_411.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_409.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_404.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_400.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_405.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_414.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_407.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_401.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_410.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_406.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_412.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_413.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-54.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_416.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_419.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-23.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_415.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-52.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_421.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_432.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_423.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_435.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-31.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_420.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_436.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_444.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_445.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_452.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_450.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_408.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_1-29.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_461.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_470.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_472.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_385.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_469.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_471.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_473.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_475.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_480.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_479.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_476.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_481.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_477.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_391.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_482.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_483.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_486.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_474.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_487.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_488.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_492.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_490.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_491.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_489.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_493.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_403.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_495.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_497.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_496.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_417.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_418.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_422.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_433.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_430.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_425.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_427.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_426.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_431.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_424.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_429.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_439.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_501.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_500.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_437.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_428.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_438.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_441.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_442.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_498.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_443.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_434.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_440.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_446.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_447.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_448.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_502.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_509.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_506.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_504.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_508.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_456.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_513.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_505.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_451.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_507.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_515.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_514.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_503.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_517.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_453.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_516.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_510.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_511.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-21.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_512.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_454.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_460.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_455.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-20.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_462.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_457.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_499.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_466.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_518.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_458.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_520.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_459.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_464.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_463.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_468.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_465.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_521.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_522.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_467.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_519.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_525.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_523.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_524.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-13.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-12.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_527.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_530.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-22.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-17.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_529.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_526.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_531.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-14.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-9.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-10.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-11.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_478.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-25.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-2.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-1.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-16.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-23.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-30.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-4.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-26.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-24.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-27.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_485.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_484.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_532.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-28.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-15.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-6.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_534.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_535.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_553.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_550.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_547.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_528.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_546.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-18.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_549.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_545.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_542.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_552.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_537.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_543.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_544.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_382.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-19.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-7.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_540.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-3.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-5.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_562.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_555.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-8.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_2-29.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_494.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_556.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_538.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_536.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_541.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_558.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_560.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_559.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_565.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_533.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_539.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_548.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_551.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_564.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_268.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_561.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_563.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_554.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-1.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-31.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-25.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-5.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-19.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-6.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-13.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-7.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-10.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-8.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-11.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-9.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-14.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-17.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-26.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-28.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-15.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-27.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-2.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-20.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-30.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-23.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-3.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-18.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-16.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-12.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-4.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-21.root',
                     '/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_3-24.root']}
#fileset = {'ttbar': ['/eos/cms/store/group/phys_top/byates/PFNano/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1_PFtestNano/230420_165513/0000/nano_mc2017_ULv2_320.root']}


import argparse
parser = argparse.ArgumentParser(description='You can select which file to run over')
parser.add_argument('--ifile', default=0 , help = 'File to run')
args = parser.parse_args()
ifile = int(args.ifile)
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
        self.jpsi_mass_bins = np.linspace(2.8, 3.4, 30)
        self.mass_bins = np.linspace(1.7, 2.0, 30)
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
        jpsi_mass_axis = hist.axis.Regular(name='jpsi_mass', label='J/Psi mass [GeV]', bins=30, start=self.jpsi_mass_bins[0], stop=self.jpsi_mass_bins[-1])
        d0_mass_axis = hist.axis.Regular(name='d0_mass', label='D0 mass [GeV]', bins=30, start=self.mass_bins[0], stop=self.mass_bins[-1])
        mass_tag_axis = hist.axis.Regular(name='d0_mu_mass', label='D0 mu-tag mass [GeV]', bins=30, start=self.mass_bins[0], stop=self.mass_bins[-1])
        mass_axes = [hist.axis.Regular(name=f'd0_{int(xb_bin*10)}', label='D0 mass [GeV] (' + str(round(self.xb_bins[ibin], 2)) + ' < $x_{\mathrm{b}}$ < ' + str(round(self.xb_bins[ibin+1], 2)) + ')', bins=30, start=1.7, stop=2.0) for ibin,xb_bin in enumerate(self.xb_bins[:-1])]
        self.output = processor.dict_accumulator({
            'j0pt': hist.Hist(dataset_axis, jpt_axis),
            'b0pt': hist.Hist(dataset_axis, bpt_axis),
            'l0pt': hist.Hist(dataset_axis, lpt_axis),
            'D0pt': hist.Hist(dataset_axis, D0pt_axis),
            'D0pipt': hist.Hist(dataset_axis, D0pipt_axis),
            'D0kpt': hist.Hist(dataset_axis, D0kpt_axis),
            'xb_mass_jpsi'  : hist.Hist(dataset_axis, xb_axis, jpsi_mass_axis),
            'xb_mass_d0'  : hist.Hist(dataset_axis, xb_axis, d0_mass_axis),
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
            'jpsi_mass': hist.Hist(dataset_axis, jpsi_mass_axis),
            'd0_mass': hist.Hist(dataset_axis, d0_mass_axis),
            'd0_mu_mass': hist.Hist(dataset_axis, mass_tag_axis),
            # FIXME make these dynamically
            'd0_0' : hist.Hist(dataset_axis, mass_axes[0]),
            'd0_1' : hist.Hist(dataset_axis, mass_axes[1]),
            'd0_2' : hist.Hist(dataset_axis, mass_axes[2]),
            'd0_3' : hist.Hist(dataset_axis, mass_axes[3]),
            'd0_4' : hist.Hist(dataset_axis, mass_axes[4]),
            'd0_5' : hist.Hist(dataset_axis, mass_axes[5]),
            'd0_6' : hist.Hist(dataset_axis, mass_axes[6]),
            'd0_7' : hist.Hist(dataset_axis, mass_axes[7]),
            'd0_8' : hist.Hist(dataset_axis, mass_axes[8]),
            'd0_9' : hist.Hist(dataset_axis, mass_axes[9]),
            'd0_mu_0' : hist.Hist(dataset_axis, mass_axes[0]),
            'd0_mu_1' : hist.Hist(dataset_axis, mass_axes[1]),
            'd0_mu_2' : hist.Hist(dataset_axis, mass_axes[2]),
            'd0_mu_3' : hist.Hist(dataset_axis, mass_axes[3]),
            'd0_mu_4' : hist.Hist(dataset_axis, mass_axes[4]),
            'd0_mu_5' : hist.Hist(dataset_axis, mass_axes[5]),
            'd0_mu_6' : hist.Hist(dataset_axis, mass_axes[6]),
            'd0_mu_7' : hist.Hist(dataset_axis, mass_axes[7]),
            'd0_mu_8' : hist.Hist(dataset_axis, mass_axes[8]),
            'd0_mu_9' : hist.Hist(dataset_axis, mass_axes[9]),
            #'d0_10' : hist.Hist(dataset_axis, mass_axes[10]),
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
        leptons = leptons[ak.argsort(leptons.pt, axis=1)][::-1]
        
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
        j0pt = ak.fill_none(ak.pad_none(jets.pt, 1), 0)[:,0]
        l0pt = ak.fill_none(ak.pad_none(ak.pad_none(leptons.pt, 1), -1)[:,0], -1)
        b0pt = ak.fill_none(bjets_tight.pt[:,0], -1)
        
        # Charm meson candidates from b-jets
        charm_cand = events.BToCharm
        #chi2_mask = ((charm_cand.chi2 / charm_cand.ndof) < 5) & (charm_cand.svprob>0.02) # Normalized chi^2 and vertex probability
        chi2_mask = charm_cand.svprob>0.02
        b_mask = jets[charm_cand.jetIdx].btagDeepFlavB > tight
        d0_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 411)
        jpsi_mask = chi2_mask & b_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        d0_mask = chi2_mask & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 411)
        jpsi_mask = chi2_mask  & (charm_cand.jetIdx>-1) & (np.abs(charm_cand.meson_id) == 443)
        d0 = charm_cand[d0_mask]
        selections.add('jpsi', ak.any(jpsi_mask, axis=1))
        selections.add('d0', ak.any(d0_mask, axis=1))
        d0mass = ak.fill_none(ak.flatten(d0.fit_mass[events.is_ttbar]), -1)
        ptsort = ak.argsort(charm_cand.pt, ascending=False)
        mass = ak.fill_none(ak.firsts(charm_cand[ptsort].fit_mass), -1)
        xb = ak.fill_none(ak.flatten((d0.fit_pt / jets[d0.jetIdx].pt)[events.is_ttbar]), -1)
        xb = ak.fill_none(ak.firsts((charm_cand.fit_pt / jets[charm_cand.jetIdx].pt)[ptsort]), -1)
        weight  = events.Generator.weight

        #binned_masses = [d0mass[(xb > low) & (xb < high)] for low,high in zip(self.xb_bins[:-1], self.xb_bins[1:])]
        # D0 mu tagged
        d0_mu_mask = abs(d0.x_id)==13
        d0_mu = d0[d0_mu_mask]
        d0_mu = d0_mu[ak.argsort(d0_mu.pt, ascending=False)] # Sort in case we just want the hardest muon
        xb_d0mu = ak.flatten((d0_mu.pt + d0_mu.x_pt)[events.is_ttbar] / jets.pt[d0_mu.jetIdx][events.is_ttbar])
        d0_mu_mass = ak.fill_none(ak.flatten(d0_mu.fit_mass[events.is_ttbar]), -1)
        #d0mu_binned_masses = [d0_mu_mass[(xb_d0mu > low) & (xb_d0mu < high)] for low,high in zip(self.xb_bins[:-1], self.xb_bins[1:])]

        self.output['j0pt'].fill(dataset=dataset, j0pt=j0pt[events.is_ttbar])
        self.output['b0pt'].fill(dataset=dataset, b0pt=b0pt[events.is_ttbar])
        self.output['l0pt'].fill(dataset=dataset, l0pt=l0pt[events.is_ttbar])
        self.output['njets'].fill(dataset=dataset, njets=ak.num(jets[events.is_ttbar]))
        self.output['nbjets'].fill(dataset=dataset, nbjets=ak.num(bjets_tight[events.is_ttbar]))
        self.output['nleps'].fill(dataset=dataset, nleps=ak.num(leptons[events.is_ttbar]))
        self.output['HT'].fill(dataset=dataset, HT=ht)
        #self.output['D0pt'].fill(dataset=dataset, D0pt=d0pt)
        #self.output['xb_ch'].fill(dataset=dataset, xb_ch=xb_ch[events.is_ttbar])
        #self.output['d0'].fill(dataset=dataset, d0=d0_imp)
        # mu_tag is at jet level, cartesian associates each PF in a jet with the jet-level flag
        #d0_tag, is_tag = ak.unzip(ak.cartesian([d0_mass, mu_tag]))
        #self.output['d0_mu_mass'].fill(dataset=dataset, d0_mu_mass=ak.fill_none(ak.flatten(d0_tag[is_tag]), 0))
        jpsi_sel = selections.all(*['ttbar', 'jpsi'])
        self.output['xb_jpsi'].fill(dataset=dataset, xb_jpsi=xb[jpsi_sel])
        self.output['jpsi_mass'].fill(dataset=dataset, jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        d0_sel = selections.all(*['ttbar', 'd0'])
        self.output['xb_d0'].fill(dataset=dataset, xb=xb[d0_sel])
        self.output['xb_mass_jpsi'].fill(dataset=dataset, xb=xb[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['xb_mass_d0'].fill(dataset=dataset, xb=xb[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['vtx_mass_d0'].fill(dataset=dataset, vtx=ak.fill_none(ak.firsts(charm_cand.svprob[ptsort]), -1)[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['chi_mass_d0'].fill(dataset=dataset, chi=ak.fill_none(ak.firsts(charm_cand.chi2[ptsort]), -1)[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        #self.output['chi_mass_d0'].fill(dataset=dataset, chi=ak.fill_none(ak.firsts(charm_cand.chi2[ptsort] / charm_cand.ndof[ptsort]), -1)[d0_sel], d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['vtx_mass_jpsi'].fill(dataset=dataset, vtx=ak.fill_none(ak.firsts(charm_cand.svprob[ptsort]), -1)[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        self.output['chi_mass_jpsi'].fill(dataset=dataset, chi=ak.fill_none(ak.firsts(charm_cand.chi2[ptsort]), -1)[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        #self.output['chi_mass_jpsi'].fill(dataset=dataset, chi=ak.fill_none(ak.firsts(charm_cand.chi2[ptsort] / charm_cand.ndof[ptsort]), -1)[jpsi_sel], jpsi_mass=mass[jpsi_sel], weight=weight[jpsi_sel])
        #self.output['xb_d0mu'].fill(dataset=dataset, xb=xb_d0mu)
        self.output['d0_mass'].fill(dataset=dataset, d0_mass=mass[d0_sel], weight=weight[d0_sel])
        self.output['d0_mu_mass'].fill(dataset=dataset, d0_mu_mass=d0_mu_mass)
        for ibin in range(len(self.xb_bins)-1):
            xb_mask = d0_sel & (xb > self.xb_bins[ibin]) & (xb < self.xb_bins[ibin+1])
            self.output[f'd0_{ibin}'].fill(**{'dataset': dataset, f'd0_{ibin}': mass[xb_mask], 'weight': weight[xb_mask]})
            #self.output[f'd0_{ibin}'].fill(**{'dataset': dataset, f'd0_{ibin}': binned_masses[ibin]})
            '''
            if ak.any(d0_mu_mask):
                self.output[f'd0_mu_{ibin}'].fill(**{'dataset': dataset, f'd0_{ibin}': d0mu_binned_masses[ibin]})
            '''
        '''
        # FIXME make these dynamically
        self.output['d0_0'].fill(dataset=dataset, d0_0=binned_masses[0])
        self.output['d0_1'].fill(dataset=dataset, d0_1=binned_masses[1])
        self.output['d0_2'].fill(dataset=dataset, d0_2=binned_masses[2])
        self.output['d0_3'].fill(dataset=dataset, d0_3=binned_masses[3])
        self.output['d0_4'].fill(dataset=dataset, d0_4=binned_masses[4])
        self.output['d0_5'].fill(dataset=dataset, d0_5=binned_masses[5])
        self.output['d0_6'].fill(dataset=dataset, d0_6=binned_masses[6])
        self.output['d0_7'].fill(dataset=dataset, d0_7=binned_masses[7])
        self.output['d0_8'].fill(dataset=dataset, d0_8=binned_masses[8])
        #self.output['d0_9'].fill(dataset=dataset, d0_9=binned_masses[9])
        '''
        #self.output['D0pipt'].fill(dataset=dataset, D0pipt=d0pi_lead_pt)
        #self.output['D0kpt'].fill(dataset=dataset, D0kpt=d0pi_lead_pt)
        self.output['sumw'][dataset]  = ak.sum(events.Generator.weight)
        self.output['sumw2'][dataset] = ak.sum(np.square(events.Generator.weight))
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
