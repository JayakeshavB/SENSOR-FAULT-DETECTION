import os

# defining common constant variable for training pipleine
TARGET_COLUMN = "class"
PIPELINE_NAME: str = "sensor_pipleine"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "sensor.csv"

TRAINING_FILE_NAME: str = "training.csv"
TESTING_FILE_NAME: str = "testing.csv"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_NAME = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"

"""
Data Ingestion related constant start with DATA_INGESTION VARIABLES NAMES
"""
DATA_INGESTION_COLLECTION_NAME: str = "sensor"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

