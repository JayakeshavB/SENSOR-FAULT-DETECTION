import os
from sensor_fault_detector.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))

class SensorModel:

    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e

class ModelResolver:
    def __init__(self, model_directory=SAVED_MODEL_DIR):
        try:
            self.model_directory = model_directory
        except Exception as e:
            raise e
    
    def get_best_model_path(self, )-> str:
        try:
            timestamps = list(map(int, os.listdir(self.model_directory)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_directory, str(latest_timestamp), MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise e
    
    def is_model_exists(self)->bool:
        try:
            if not os.path.exists(self.model_directory):
                return False

            timestamps = os.listdir(self.model_directory)
            if len(timestamps)==0:
                return False
            
            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as e:
            raise e