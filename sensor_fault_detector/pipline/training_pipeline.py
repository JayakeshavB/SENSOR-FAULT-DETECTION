from sensor_fault_detector.entity.config_entity import TrainingPipelineConfig, DataIngestPipelineConfig, DatavalidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor_fault_detector.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, DataValidationArtifact, ModelEvaluationArtifact
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging
from sensor_fault_detector.components.data_ingestion import DataIngestion
from sensor_fault_detector.components.data_validation import DataValidation
from sensor_fault_detector.components.model_evaluation import ModelEvaluation
from sensor_fault_detector.components.data_transformation import DataTransformation
from sensor_fault_detector.components.model_pusher import ModelPusher
from sensor_fault_detector.components.model_trainer import ModelTrainer
import os, sys
import shutil

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
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Starting model trainer")
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            self.model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = self.model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact,):
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            self.model_eval = ModelEvaluation(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = self.model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except  Exception as e:
            raise  SensorException(e,sys)
        
    def run_pipeline(self):
        try:
             data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
             data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
             data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
             model_trainer_artifact:ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
             model_eval_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
             if not model_eval_artifact.is_model_accepted:
                logging.info("Trained model is not better than the best model")
             model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
        except Exception as e:
            raise SensorException(e, sys)
        