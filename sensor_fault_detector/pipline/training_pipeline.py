from sensor_fault_detector.entity.config_entity import TrainingPipelineConfig, DataIngestPipelineConfig
from sensor_fault_detector.entity.artifact_entity import DataIngestionArtifact
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging
import sys

class TrainingPipeline:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingest_config = DataIngestPipelineConfig(training_pipeline_config)
        self.training_pipeline_config = training_pipeline_config
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            logging.info("data ingestion complete")
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
        
    def run_pipeline(self):
        try:
             data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e, sys)
        