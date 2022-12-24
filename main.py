from sensor_fault_detector.configuration.mongo_db_connection import MongoDBClient
from sensor_fault_detector.entity.config_entity import TrainingPipelineConfig, DataIngestPipelineConfig
from sensor_fault_detector.logger import logging
from sensor_fault_detector.exception import SensorException
import os, sys
from sensor_fault_detector.pipline.training_pipeline import TrainingPipeline

if __name__ == '__main__':
    training_pipeline = TrainingPipeline()
    training_pipeline.run_pipeline()