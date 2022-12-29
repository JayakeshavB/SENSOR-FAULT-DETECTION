from sensor_fault_detector.exception import SensorException
from sensor_fault_detector.logger import logging
from sensor_fault_detector.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor_fault_detector.entity.config_entity import ModelEvaluationConfig
import os,sys
from sensor_fault_detector.ml.metric.classification_metric import get_classification_score
from sensor_fault_detector.ml.model.estimator import SensorModel
from sensor_fault_detector.utils.main_utils import save_object,load_object,write_yaml_file
from sensor_fault_detector.ml.model.estimator import ModelResolver
from sensor_fault_detector.constant.training_pipeline import TARGET_COLUMN
from sensor_fault_detector.ml.model.estimator import TargetValueMapping
import pandas  as  pd

class ModelEvaluation:


    def __init__(self,model_eval_config:ModelEvaluationConfig,
                    data_validation_artifact:DataValidationArtifact,
                    model_trainer_artifact:ModelTrainerArtifact):
        
        try:
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
            try:
                logging.info('Starting model evaluation')
                valid_train_file_path = self.data_validation_artifact.valid_train_file_path
                valid_test_file_path = self.data_validation_artifact.valid_test_file_path

                train_df = pd.read_csv(valid_train_file_path)
                test_df = pd.read_csv(valid_test_file_path)

                df = pd.concat([train_df,test_df])
                y_true = df[TARGET_COLUMN]
                y_true.replace(TargetValueMapping().to_dict(),inplace=True)
                df.drop(TARGET_COLUMN,axis=1,inplace=True)

                train_model_file_path = self.model_trainer_artifact.trained_model_file_path

                model_resolver = ModelResolver()
                is_model_accepted = True
                if not model_resolver.is_model_exists():
                    model_evaluation_artifact = ModelEvaluationArtifact(
                        is_model_accepted=is_model_accepted, 
                        improved_accuracy=None, 
                        best_model_path=None, 
                        trained_model_path=train_model_file_path, 
                        train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact, 
                        best_model_metric_artifact=None)
                    logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                    return model_evaluation_artifact 
                logging.info('model exists')
                latest_model_path = model_resolver.get_best_model_path()
                latest_model = load_object(file_path=latest_model_path)
                train_model = load_object(file_path=train_model_file_path)

                y_train_pred = train_model.predict(df)
                y_latest_pred = latest_model.predict(df)

                trained_metric = get_classification_score(y_true, y_train_pred)
                latest_metric = get_classification_score(y_true, y_latest_pred)

                improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
                if self.model_eval_config.change_threshold < improved_accuracy:
                    #0.02 < 0.03
                    is_model_accepted=True
                else:
                    is_model_accepted=False

                
                model_evaluation_artifact = ModelEvaluationArtifact(
                        is_model_accepted=is_model_accepted, 
                        improved_accuracy=improved_accuracy, 
                        best_model_path=latest_model_path, 
                        trained_model_path=train_model_file_path, 
                        train_model_metric_artifact=trained_metric, 
                        best_model_metric_artifact=latest_metric)

                model_eval_report = model_evaluation_artifact.__dict__

                #save the report
                write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
                
            except Exception as e:
                raise SensorException(e,sys)

