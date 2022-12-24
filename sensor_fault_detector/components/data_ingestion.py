from sensor_fault_detector.logger import logging
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.entity.config_entity import DataIngestPipelineConfig
from sensor_fault_detector.entity.artifact_entity import DataIngestionArtifact
from sensor_fault_detector.data_access.sensor_data import SensorData
from sensor_fault_detector.constant.database import DATABASE_NAME, COLLECTION_NAME
import os, sys
from pandas import DataFrame
class DataIngestion:
    def __init__(self, data_ingestion_pipeline_config:DataIngestPipelineConfig):
        try:
            self.data_ingestion_pipeline_config = data_ingestion_pipeline_config
        except Exception as e:
            SensorException(e, sys)
    
    def export_data_into_feature_store(self)-> DataFrame:
        """
        This method is used to export mongoDB collection into feature store.
        """
        try:
            logging.info("export_data_into_feature_store")
            sensor_data =  SensorData()
            data_frame = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_pipeline_config.collection_name)
            feature_store_file_path = self.data_ingestion_pipeline_config.feature_store_file_path

            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            data_frame.to_csv(feature_store_file_path, index=False, header=True)
            return data_frame
        except Exception as e:
            SensorException(e, sys)


    def split_data_into_feature_store(self, data_frame:DataFrame)->None:
        """
        This method is used to split the data into train and test file.
        """    
        pass

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            data_frame = self.export_data_into_feature_store()
            self.split_data_into_feature_store(data_frame)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path= self.data_ingestion_pipeline_config.training_file_path
            ,test_file_path=self.data_ingestion_pipeline_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)