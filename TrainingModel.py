import os
import shutil
from sklearn.model_selection import train_test_split
from Data_Loader.DataLoader import dataGetter
from Data_Preprocessing.Preprocessing import preprocessor
from Data_Preprocessing.Clustering import kMeansClustering
from Training_BestModelFinder.ModelFinder import modelFinder
from File_Operations.FileOperations import fileOperation
from Directory_Handling.DirectoryHandling import directoryHandling
from Logger.logger import appLogger

class trainModel:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.dirname(__file__))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()

    def modelTrain(self):
        f = open(self.log_path, 'a+')
        msg = 'Starting model Training.'
        self.logger.log(f, msg)
        try:
            # getting cleaned data after data validation
            get_data = dataGetter()
            data = get_data.getData()

            # preprocessing the data
            preprocess_data = preprocessor()
            is_null_present, cols_with_missing_values = preprocess_data.isNullPresent(data)
            if is_null_present:
                data = preprocess_data.imputeMissingValues(data)
            # creating label and features
            x, y = preprocess_data.separateLabelFeature(data, label_column_name='Concrete_compressive_strength')
            # applying log transformation on data
            x = preprocess_data.logTransformation(x)

            # applying clustering approach
            clusters = kMeansClustering()
            number_of_clusters = clusters.elbowPlot(x)
            # creating new column in dataset corresponding to clusters and adding labels
            y_kmeans = clusters.createClusters(x, number_of_clusters)
            x['cluster'] = y_kmeans
            x['label'] = y
            # getting unique clusters from our data
            list_of_clusters = x['cluster'].unique()

            # parsing all clusters and finding the best ML model for each
            for clust in list_of_clusters:
                cluster_data = x[x['cluster']==clust]
                clust_features = cluster_data.drop(['label', 'cluster'], axis=1)
                clust_labels = cluster_data['label']
                # splitting dataset into train and test
                xtrain, xtest, ytrain, ytest = train_test_split(clust_features, clust_labels)

                # scaling the dataset
                xtrain_scaled, scalar = preprocess_data.standardScaling(xtrain)
                xtest_scaled = preprocess_data.standardScalingTest(xtest, scalar)

                #saving standard scalar
                file_op = fileOperation()
                file_op.saveModel(scalar, 'Scalar')

                # finding best model for the cluster
                model_finder = modelFinder()
                model_name, model = model_finder.getBestModel(xtrain_scaled, ytrain, xtest_scaled, ytest)
                # print(model)
                # saving the model
                file_op.saveModel(model, model_name+str(clust))

            msg = 'End of model Training.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            msg = 'Error while model training. ' \
                  'Error occurred in trainingModel method of the trainModel class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e



