from collections import namedtuple

DataIngestArtifact = namedtuple('DataIngestArtifact',
['ingested_dir_path','message'])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", [ "message", "trained_model_file_path"])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])
