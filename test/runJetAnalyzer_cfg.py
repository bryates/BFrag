import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register('runOnData', False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Run this on real data"
                 )
options.register('outFilename', 'MiniEvents.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output file name"
                 )
options.register('inputDir', '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "input directory with files to process"
                 )
options.register('saveTree', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "save summary tree"
                 )
options.register('savePF', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 'save PF candidates'
                 )
options.register('skipEvents', 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 'skip events'
                 )
options.parseArguments()

process = cms.Process("JetAnalysis")


# Load the standard set of configuration modules
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')


# global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016SeptRepro_v5' if options.runOnData else '94X_mc2017_realistic_v14')

#message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000


# set input to process
#from TopLJets2015.TopAnalysis.Compressed_T2tt_cfi import *
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
if options.maxEvents > 0:
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring('file://eos/user/b/byates/D458D37A-263C-7B47-8850-46CE3E8A4C2F.root'),
                            fileNames = cms.untracked.vstring('/store/mc/RunIISummer20UL16MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/280000/D458D37A-263C-7B47-8850-46CE3E8A4C2F.root'),
                            #fileNames = cms.untracked.vstring(Compressed_T2tt_2),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
                            #skipEvents = cms.untracked.uint32(options.skipEvents)
                            )
#if options.skipEvents > 0: process.skipEvents = cms.untracked.uint32(options.skipEvents)
if options.runOnData:
    process.source.fileNames = cms.untracked.vstring('/store/data/Run2016B/SingleMuon/MINIAOD/23Sep2016-v3/00000/00AE0629-1F98-E611-921A-008CFA1112CC.root')
    #process.source.fileNames = cms.untracked.vstring('/store/data/Run2016B/SingleElectron/MINIAOD/23Sep2016-v3/00000/00099863-E799-E611-A876-141877343E6D.root')
    #process.source.fileNames = cms.untracked.vstring('/store/data/Run2016G/DoubleMuon/MINIAOD/23Sep2016-v1/50000/0ADAF1EC-808D-E611-8B6C-008CFA056400.root')
    #process.source.fileNames = cms.untracked.vstring('file://pickevents.root')
    #process.source.fileNames = cms.untracked.vstring('/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/281/639/00000/3A55AB69-8E85-E611-B299-02163E0119BB.root')
    #/store/data/Run2016B/SingleElectron/MINIAOD/PromptReco-v2/000/273/158/00000/06277EC1-181A-E611-870F-02163E0145E5.root')

#this make the process crash ?!
#if options.inputDir!='': 
#    from TopLJets2015.TopAnalysis.storeTools import getEOSlslist 
#    print 'Will process files from',options.inputDir
#    process.source.fileNames=cms.untracked.vstring(getEOSlslist(directory=options.inputDir))

######### Pre-skim weight counter
#FIXME
#process.weightCounter = cms.EDAnalyzer('WeightCounter')

######### Skim Filter
process.selectedMuons = cms.EDFilter("CandPtrSelector",
                                     src = cms.InputTag("slimmedMuons"),
                                     cut = cms.string("pt>9.8 && abs(eta)<2.4"))

process.selectedElectrons = cms.EDFilter("CandPtrSelector",
                                         src = cms.InputTag("slimmedElectrons"),
                                         cut = cms.string("pt>9.8 && abs(eta)<2.5"))

process.selectedJets = cms.EDFilter("CandPtrSelector",
                                         src = cms.InputTag("slimmedJets"),
                                         cut = cms.string("pt>20 && abs(eta)<2.5"))

process.allLeps = cms.EDProducer("CandViewMerger",
                                 src = cms.VInputTag(
                                                        cms.InputTag("selectedElectrons"),
                                                        cms.InputTag("selectedMuons")))

process.countLeps = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("allLeps"),
                                 minNumber = cms.uint32(1))

process.countJets = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("selectedJets"),
                                 minNumber = cms.uint32(2))

process.preYieldFilter = cms.Sequence(process.selectedMuons+process.selectedElectrons+process.allLeps+process.countLeps+process.selectedJets+process.countJets)

######### Kalman Filter
#process.kalman = cms.EDAnalyzer("KalmanFilter",
    #electrons = cms.InputTag("slimmedElectrons"),
    #muons = cms.InputTag("slimmedMuons"),
    #jets = cms.InputTag("slimmedJets"),
    #pfCands = cms.InputTag("packedPFCandidates::PAT"),
#)


#analysis
process.load('BFrag.BFrag.jetAnalyzer_cfi')
if not options.saveTree:
    print 'Summary tree won\'t be saved'
    process.analysis.saveTree=cms.bool(False)
if not options.savePF:
    print 'Summary PF info won\'t be saved'
    process.analysis.savePF=cms.bool(False)

#pseudo-top
if not options.runOnData:
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
        inputPruned = cms.InputTag("prunedGenParticles"),
        inputPacked = cms.InputTag("packedGenParticles"),
    )
    process.load('GeneratorInterface.RivetInterface.genParticles2HepMC_cfi')
    process.genParticles2HepMC.genParticles = cms.InputTag("mergedGenParticles")
    process.genParticles2HepMC.genEventInfo = cms.InputTag("generator")
    process.load('TopQuarkAnalysis.TopEventProducers.producers.pseudoTop_cfi')
    process.pseudoTop.leptonMinPt=cms.double(20)
    process.pseudoTop.leptonMaxEta=cms.double(2.5)
    process.pseudoTop.jetMaxEta=cms.double(5.0)

# b-frag weight producer
#process.load('TopLJets2015.TopAnalysis.bfragWgtProducer_cfi')

# Set up electron ID (VID framework)
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
'''
#my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff']
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
'''

#jet energy corrections
'''
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
from JetMETCorrections.Configuration.DefaultJEC_cff import *
from JetMETCorrections.Configuration.JetCorrectionServices_cff import *
from TopLJets2015.TopAnalysis.customizeJetTools_cff import *
jecLevels=['L1FastJet','L2Relative','L3Absolute']
jecFile='Summer19UL18_V5_MC.db'
jecTag='106X_upgrade2018_realistic_v15_L1v1'
#jecTag='106X_upgrade2018_realistic_v15_L1v1'
if options.runOnData : 
    #print 'Warning we\'re still using Spring16 MC corrections for data - to be updated'
    jecLevels.append( 'L2L3Residual' )
    jecFile='Summer16_23Sep2016AllV4_DATA.db'
    jecTag='Summer16_23Sep2016AllV4_DATA_AK4PFchs'
customizeJetTools(process=process,jecLevels=jecLevels,jecFile=jecFile,jecTag=jecTag)
'''

#tfile service
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('histo.root')
                                   )

if options.runOnData:
    #process.p = cms.Path(process.egmGsfElectronIDSequence*process.customizeJetToolsSequence*process.analysis)
    process.p = cms.Path(process.preYieldFilter*process.egmGsfElectronIDSequence*process.customizeJetToolsSequence*process.analysis)
else:
    #process.p = cms.Path(process.egmGsfElectronIDSequence*process.customizeJetToolsSequence*process.pseudoTop*process.analysis)
    process.p = cms.Path(process.egmGsfElectronIDSequence*process.mergedGenParticles*process.genParticles2HepMC*process.pseudoTop*process.analysis)
    #process.p = cms.Path(process.preYieldFilter*process.egmGsfElectronIDSequence*process.mergedGenParticles*process.genParticles2HepMC*process.pseudoTop*process.analysis)
    #process.p = cms.Path(process.weightCounter*process.preYieldFilter*process.egmGsfElectronIDSequence*process.customizeJetToolsSequence*process.mergedGenParticles*process.genParticles2HepMC*process.pseudoTop*process.bfragWgtProducer*process.analysis)
