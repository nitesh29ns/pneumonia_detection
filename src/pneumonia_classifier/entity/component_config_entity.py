from collections import namedtuple

dataingestionconfig = namedtuple('dataingestionconfig',
['dataset_download_url','tgz_download_dir','ingested_dir'])

modeltrainerconfig = namedtuple("modelTrainerconfig",["trained_model_file_path","model_config_file_path"])

modelevaluationconfig = namedtuple("modelevaluationconfig",['model_evaluation_report_dir','model_evaluation_file_path'])

modelPusherconfig = namedtuple("modelPusherconfig",["saved_model_path"])

trainingpipelineconfig = namedtuple('trainingpipelineconfig',
['artifact_dir'])