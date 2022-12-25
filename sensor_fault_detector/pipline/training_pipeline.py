from sensor_fault_detector.entity.config_entity import TrainingPipelineConfig, DataIngestPipelineConfig, DatavalidationConfig, DataTransformationConfig
from sensor_fault_detector.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging
from sensor_fault_detector.components.data_ingestion import DataIngestion
from sensor_fault_detector.components.data_validation import DataValidation
from sensor_fault_detector.components.data_transformation import DataTransformation
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
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            self.data_validation_config = DatavalidationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = self.data_validation.initiate_data_validation()
            logging.info(f"data validation complete and artifact {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Starting data transformation")
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_transformation = DataTransformation(data_validation_artifact= data_validation_artifact, data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = self.data_transformation.initiate_data_transformation()
            logging.info(f"data transformation complete and artifact {data_transformation_artifact}")
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
             data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
             data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise SensorException(e, sys)
        