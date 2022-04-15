import os
import pandas as pd
import numpy as np
import pickle
from File_Operations import FileOperations
from Data_Preprocessing import Preprocessing
from Data_Loader import DataLoader
from Logger.logger import appLogger

class prediction:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.dirname(__file__))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()
        self.model_directory = os.path.join(self.base_folder, 'Models')

    def modelPrediction(self, feature_pred):
        f = open(self.log_path, 'a+')
        msg = 'Started Model Prediction.'
        self.logger.log(f, msg)
        try:
            # applying log transformation to data
            features = []
            for feat in feature_pred:
                feat += 1
                feat = np.log(feat)
                features.append(feat)

            # loading kmeans model to find cluster
            file_op = FileOperations.fileOperation()
            kmeans = file_op.loadModel('KMeans')
            cluster_number = kmeans.predict([features])
            for file in os.listdir(self.model_directory):
                if file.endswith(str(cluster_number[0])):
                    # scaling the prediction features
                    scalar = file_op.loadModel('Scalar')
                    scaled_features = scalar.transform([features])
                    # loading model and making predictions
                    pred_model = file_op.loadModel(file)
                    pred = pred_model.predict(scaled_features)
                    f.close()
                    return "{:.2f}".format(pred[0])

        except Exception as e:
            msg = 'Error while making Prediction from file. ' \
                  'Error occurred in modelPrediction method of prediction class.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

if __name__== '__main__':
    a = prediction()
    # a.modelPrediction([540.0,0.0,0.0,162.0,2.5,1040.0,676.0,28])
    a.modelPrediction([10,10,10,10,10,10,10,10])
# 540.0","0.0","0.0","162.0","2.5","1040.0","676.0","28","79.99