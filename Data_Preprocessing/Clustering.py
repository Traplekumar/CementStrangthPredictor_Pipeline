import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operations.FileOperations import fileOperation
from Logger.logger import appLogger

class kMeansClustering:
    def __init__(self, ):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()

    def elbowPlot(self, data):
        f = open(self.log_path, 'a+')
        msg = 'Entered the elbowPlot method of the kMeansClustering class.'
        self.logger.log(f, msg)
        try:
            path = os.path.join(self.base_folder, 'Training_Preprocessing_Data')
            wcss = []
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=21)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1, 11), wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.savefig(path+'/'+'K_Means_Elbow.png')
            kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            msg = 'Optimum number of clusters is: ' + str(kn.knee) + '. ' \
                   'Exited the elbowPlot method of the kMeansClustering class.'
            self.logger.log(f, msg)
            f.close()
            return kn.knee

        except Exception as e:
            msg = 'Error occurred while finding the knee of elbow method.' \
                  'Error occurred in elbow method of the kMeansClustering class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createClusters(self, data, cluster_numbers):
        f = open(self.log_path, 'a+')
        msg = 'Entered the createClusters method of the kMeansClustering.'
        self.logger.log(f, msg)
        try:
            kmeans = KMeans(n_clusters=cluster_numbers, init='k-means++', random_state=21)
            y_kmeans = kmeans.fit_predict(data)
            file_op = fileOperation()
            file_op.saveModel(kmeans, 'KMeans')
            msg = 'Successfully created ' + str(cluster_numbers) + ' clusters. ' \
                  'Exited the createClusters method the kMeansClustering class.'
            self.logger.log(f, msg)
            f.close()
            return y_kmeans

        except Exception as e:
            msg = 'Error while creating cluster in dataset.' \
                  'Error occurred in createClusters method of the kMeansClustering class.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e
