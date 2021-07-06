# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: myNanoProdMc -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --no_exec --conditions 102X_upgrade2018_realistic_v15 --era Run2_2018,run2_nanoAOD_102Xv1 --customise_commands=process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Modifier_run2_nanoAOD_102Xv1_cff import run2_nanoAOD_102Xv1
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

process = cms.Process('NANO',Run2_2018,run2_nanoAOD_102Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(2)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIIAutumn18MiniAOD/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/100000/2A6B8F74-04C7-1B46-A56E-8C786D0C2E84.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('myNanoProdMc nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('myNanoProdMc_NANO.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
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

process.xconeJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    cut = cms.string(''),
    doc = cms.string('XCone Jets'),
    extension = cms.bool(False),
    name = cms.string('XConeJet'),
    singleton = cms.bool(False),
    src = cms.InputTag("xconePuppi"),
    variables = cms.PSet(
        eta = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('eta'),
            expr = cms.string('eta'),
            mcOnly = cms.bool(False),
            precision = cms.int32(12),
            type = cms.string('float')
        ),
        mass = cms.PSet(
            compression = cms.string('none'),
            doc = cms.string('mass'),
            expr = cms.string('mass'),
            mcOnly = cms.bool(False),
            precision = cms.int32(10),
            type = cms.string('float')
        ),
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
        )
    )
)

process.xconeSequence = cms.Sequence(process.xconePuppi + process.xconeJetTable)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC + process.xconeSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)


# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.


# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# End of customisation functions

# Customisation from command line

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

with open('pydump_mc_NANO.py', 'w') as f:
    f.write(process.dumpPython())
