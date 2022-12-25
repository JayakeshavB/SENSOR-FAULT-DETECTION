import yaml
import os, sys
from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging

def read_yaml_file(filename)->dict:
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        SensorException(e, sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)

        