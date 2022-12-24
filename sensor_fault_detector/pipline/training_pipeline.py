from sensor_fault_detector.entity.config_entity import TrainingPipelineConfig, DataIngestPipelineConfig
from sensor_fault_detector.entity.artifact_entity import DataIngestionArtifact
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging
from sensor_fault_detector.components.data_ingestion import DataIngestion
import os, sys

class TrainingPipeline:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.training_pipeline_config = training_pipeline_config
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            self.data_ingest_config = DataIngestPipelineConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_pipeline_config=self.data_ingest_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion complete and artifact {data_ingestion_artifact}")
            return data_ingestion_artifact
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
        