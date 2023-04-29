import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRFRegressor

from src.exception import Customexception
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join("artifacts","model.pkl")

class Model_Trainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split Tarining ang Test Input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models={
                "Random Forest": RandomForestRegressor(),
                "Decesion Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Liner Regression": LinearRegression(),
                "K-Neighbors Classifer": KNeighborsRegressor(),
                "XGBClassifier": XGBRFRegressor(),
                "Cat Boosting Classifier": CatBoostRegressor(),
                "AdaBoost Classifier": AdaBoostRegressor(),
            }
            model_report:dict=evaluate_model(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,models=models)

            best_model_score= max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise Customexception("No best Model Found")
            
            logging.info("Best Found model on both training and testing data")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted= best_model.predict(X_test)

            r2_scr=r2_score(y_test,predicted)
            return r2_scr


        except Exception as e:
            raise Customexception(e,sys)