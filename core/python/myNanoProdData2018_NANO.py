# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: myNanoProdData2018 -s NANO --data --eventcontent NANOAOD --datatier NANOAOD --no_exec --conditions 106X_dataRun2_v32 --era Run2_2018,run2_nanoAOD_106Xv1 --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv1_cff import run2_nanoAOD_106Xv1
from Configuration.EventContent.EventContent_cff import *
from RecoJets.Configuration.RecoPFJets_cff import *
from RecoJets.JetProducers.fixedGridRhoProducerFastjet_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *
from RecoBTag.SecondaryVertex.trackSelection_cff import *
from UHH2.core.muon_pfMiniIsolation_cff import *
from UHH2.core.electron_pfMiniIsolation_cff import *
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

process = cms.Process('NANO',Run2_2018,run2_nanoAOD_106Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# load the standard PAT config
#process.load("PhysicsTools.PatAlgos.patSequences_cff")

# load the coreTools of PAT
#from PhysicsTools.PatAlgos.tools.coreTools import runOnData
#runOnData(process)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2018B/SingleMuon/MINIAOD/12Nov2019_UL2018-v3/00000/006332C4-470B-A44B-A281-8B0B10A7D591.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('myNanoProdData2018 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('XConettbar_data.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition

#XCONE
usePseudoXCone = cms.bool(True)
process.xconePuppi = cms.EDProducer("XConeProducer",
    src=cms.InputTag("packedPFCandidates"),
    usePseudoXCone=usePseudoXCone,  # use PseudoXCone (faster) or XCone
    NJets = cms.uint32(9),          # number of fatjets
    RJets = cms.double(0.4),        # cone radius of fatjets
    BetaJets = cms.double(2.0),     # conical mesure (beta = 2.0 is XCone default)
    NSubJets = cms.uint32(0),       # number of subjets in each fatjet
    RSubJets = cms.double(0.4),     # cone radius of subjetSrc
    BetaSubJets = cms.double(2.0),  # conical mesure for subjets
    printWarning = cms.bool(False), # set True if you want warnings about missing jets
    doRekey = cms.bool(True),       # set True if you want to rekey jet & subjets so that
    rekeyCandidateSrc = cms.InputTag("packedPFCandidates") # constituents point to rekeyCandidateSrc
)

#Jet Collection
addJetCollection(
					process,
					jetSource = cms.InputTag("xconePuppi"),
					labelName = "XConewithbtag",
					jetCorrections = None,
					btagDiscriminators = ['pfDeepCSVJetTags:probb','pfDeepCSVJetTags:probbb','pfDeepCSVJetTags:probc', 
										  'pfCombinedMVAV2BJetTags','pfCombinedInclusiveSecondaryVertexV2BJetTags',
										  'pfDeepFlavourJetTags:probb','pfDeepFlavourJetTags:probbb',
										  'pfDeepFlavourJetTags:problepb','pfDeepFlavourJetTags:probc'],
					getJetMCFlavour = False,
					pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
					svSource = cms.InputTag("slimmedSecondaryVertices"),
					muSource = cms.InputTag("slimmedMuons"),
					elSource = cms.InputTag("slimmedElectrons"),
					pfCandidates = cms.InputTag("packedPFCandidates"),
					#genJetCollection = cms.InputTag("slimmedGenJets"),
					#genParticles = cms.InputTag("prunedGenParticles")
				 )

process.xconeJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    cut = cms.string(''),
    doc = cms.string('XCone Jets'),
    extension = cms.bool(False),
    #externalVariables = cms.PSet(
        #bRegCorr = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('pt correction for b-jet energy regression'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(12),
        #    src = cms.InputTag("bjetNN","corr"),
        #    type = cms.string('float')
        #),
        #bRegRes = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('res on pt corrected with b-jet regression'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(8),
        #    src = cms.InputTag("bjetNN","res"),
        #    type = cms.string('float')
        #)
    #),
    name = cms.string('XConeJet'),
    singleton = cms.bool(False),
    src = cms.InputTag("selectedPatJetsXConewithbtag"),
    variables = cms.PSet(
        area = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('jet catchment area, for JECs'),
            expr = cms.string('jetArea()'),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagCMVA = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('CMVA V2 btag discriminator'),
            expr = cms.string("bDiscriminator(\'pfCombinedMVAV2BJetTags\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagCSVV2 = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string(' pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)'),
            expr = cms.string("bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagDeepB = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('DeepCSV b+bb tag discriminator'),
            expr = cms.string("bDiscriminator(\'pfDeepCSVJetTags:probb\')+bDiscriminator(\'pfDeepCSVJetTags:probbb\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagDeepC = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('DeepCSV charm btag discriminator'),
            expr = cms.string("bDiscriminator(\'pfDeepCSVJetTags:probc\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagDeepFlavB = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('DeepFlavour b+bb+lepb tag discriminator'),
            expr = cms.string("bDiscriminator(\'pfDeepFlavourJetTags:probb\')+bDiscriminator(\'pfDeepFlavourJetTags:probbb\')+bDiscriminator(\'pfDeepFlavourJetTags:problepb\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        btagDeepFlavC = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('DeepFlavour charm tag discriminator'),
            expr = cms.string("bDiscriminator(\'pfDeepFlavourJetTags:probc\')"),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        #chEmEF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('charged Electromagnetic Energy Fraction'),
        #    expr = cms.string('chargedEmEnergyFraction()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #chHEF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('charged Hadron Energy Fraction'),
        #    expr = cms.string('chargedHadronEnergyFraction()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #electronIdx1 = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('index of first matching electron'),
        #    expr = cms.string("?overlaps(\'electrons\').size()>0?overlaps(\'electrons\')[0].key():-1"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #electronIdx2 = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('index of second matching electron'),
        #    expr = cms.string("?overlaps(\'electrons\').size()>1?overlaps(\'electrons\')[1].key():-1"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        eta = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('eta'),
            expr = cms.string('eta'),
            mcOnly = cms.bool(False),
            precision = cms.int32(12),
            type = cms.string('float')
        ),
        #jercCHF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Charged Hadron Energy Fraction with the JERC group definition'),
        #    expr = cms.string("userFloat(\'jercCHF\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #jercCHPUF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Pileup Charged Hadron Energy Fraction with the JERC group definition'),
        #    expr = cms.string("userFloat(\'jercCHPUF\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #jetId = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto'),
        #    expr = cms.string("userInt(\'tightId\')*2+4*userInt(\'tightIdLepVeto\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        mass = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('mass'),
            expr = cms.string('mass'),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
        #muEF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('muon Energy Fraction'),
        #    expr = cms.string('muonEnergyFraction()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #muonIdx1 = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('index of first matching muon'),
        #    expr = cms.string("?overlaps(\'muons\').size()>0?overlaps(\'muons\')[0].key():-1"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #muonIdx2 = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('index of second matching muon'),
        #    expr = cms.string("?overlaps(\'muons\').size()>1?overlaps(\'muons\')[1].key():-1"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #muonSubtrFactor = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('1-(muon-subtracted raw pt)/(raw pt)'),
        #    expr = cms.string("1-userFloat(\'muonSubtrRawPt\')/(pt()*jecFactor(\'Uncorrected\'))"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #nConstituents = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Number of particles in the jet'),
        #    expr = cms.string('numberOfDaughters()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #nElectrons = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('number of electrons in the jet'),
        #    expr = cms.string("?hasOverlaps(\'electrons\')?overlaps(\'electrons\').size():0"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #nMuons = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('number of muons in the jet'),
        #    expr = cms.string("?hasOverlaps(\'muons\')?overlaps(\'muons\').size():0"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #neEmEF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('neutral Electromagnetic Energy Fraction'),
        #    expr = cms.string('neutralEmEnergyFraction()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        #neHEF = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('neutral Hadron Energy Fraction'),
        #    expr = cms.string('neutralHadronEnergyFraction()'),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        #),
        phi = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('phi'),
            expr = cms.string('phi'),
            mcOnly = cms.bool(False),
            precision = cms.int32(12),
            type = cms.string('float')
        ),
        pt = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('pt'),
            expr = cms.string('pt'),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        #),
        #puId = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Pilup ID flags'),
        #    expr = cms.string("userInt(\'pileupJetId:fullId\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(-1),
        #    type = cms.string('int')
        #),
        #qgl = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('Quark vs Gluon likelihood discriminator'),
        #    expr = cms.string("userFloat(\'qgl\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(10),
        #    type = cms.string('float')
        #),
        #rawFactor = cms.PSet(
        #    compression = cms.string('none'),
        #    doc = cms.string('1 - Factor to get back to raw pT'),
        #    expr = cms.string("1.-jecFactor(\'Uncorrected\')"),
        #    mcOnly = cms.bool(False),
        #    precision = cms.int32(6),
        #    type = cms.string('float')
        )
    )
)

process.xconeSequence = cms.Sequence(process.xconePuppi + process.xconeJetTable)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v32', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeData 

#call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeData(process)

# End of customisation functions

# Customisation from command line

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
with open('pydump_data_NANO.py', 'w') as f:
    f.write(process.dumpPython())
