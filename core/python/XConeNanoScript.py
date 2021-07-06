import datetime
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, StorageConfiguration, Workflow

project = 'XCone_' + datetime.datetime.now().strftime('%Y%m%d_%H%M')

storage = StorageConfiguration(
	
	#input=[
		#"hdfs://eddie.crc.nd.edu:19000/store/user/uname/directory/",
		#"file:///hadoop/store/user/username/directory/uname/directory/",
		#"root://deepthought.crc.nd.edu//store/user/uname/directory/",
		#"gsiftp://T3_US_NotreDame/store/user/uname/directory/",
		#"root://ndcms.crc.nd.edu/"
	#],

    output=[
        "hdfs://eddie.crc.nd.edu:19000/store/user/$USER/" + project,
        "file:///hadoop/store/user/$USER/" + project,
        "root://deepthought.crc.nd.edu//store/user/$USER/" + project,
        "gsiftp://T3_US_NotreDame/store/user/$USER/" + project,
        "srm://T3_US_NotreDame/store/user/$USER/" + project,
    ]
)

workflows = []

XCone = Workflow(
    label='XCone',
    sandbox=cmssw.Sandbox(release='/afs/crc.nd.edu/user/i/imcalist/Research/Ntuple_Prod/CMSSW_10_6_13'),
    dataset=cmssw.Dataset(
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v2/MINIAODSIM',
        events_per_task=15000
    ),
    category=Category(
        name='xcone',
        cores=2,
        memory=3500,
        disk=2000,
    ),
    command='cmsRun myNanoProdMc_NANO.py',
    publish_label='test',
    merge_size='2.5G',
    merge_command='./afs/crc.nd.edu/user/i/imcalist/Research/Ntuple_Prod/CMSSW_10_6_13/src/PhysicsTools/NanoAODTools/scripts/haddnano.py XConeNAOD.root @outputfiles',
    outputs=['XConettbar.root']
)
workflows.append(XCone)

config = Config(
    workdir='/tmpscratch/users/$USER/' + project,
    plotdir='/afs/crc.nd.edu/user/i/imcalist/www/lobster/' + project,
    label=project,
    storage=storage,
    workflows=workflows,
    advanced=AdvancedOptions(
    	dashboard = False,
        bad_exit_codes=[127, 160],
        log_level=2,
        threshold_for_failure=150,
        threshold_for_skipping=150,
        xrootd_servers = ['ndcms.crc.nd.edu','cmsxrootd.fnal.gov']
    )
)
