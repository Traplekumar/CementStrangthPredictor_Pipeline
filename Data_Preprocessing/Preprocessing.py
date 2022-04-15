import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import os
from Directory_Handling.DirectoryHandling import directoryHandling
from Logger.logger import appLogger


class preprocessor:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs/GeneralLogs.txt')
        self.logger = appLogger()

    def separateLabelFeature(self, data, label_column_name):
        f = open(self.log_path, 'a+')
        msg = 'Entered separate_label_feature method of the preprocessor class.'
        self.logger.log(f, msg)
        try:
            x = data.drop(label_column_name, axis=1)
            y = data[label_column_name]
            msg = 'Labels and Features Separation successful. ' \
                  'Exited the separate_label_feature method of the preprocessor class.'
            self.logger.log(f, msg)
            f.close()
            return x, y

        except Exception as e:
            msg = 'Error occurred while separating labels and features. ' \
                  'Error occurred in separate_label_feature method of the preprocessor class.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def isNullPresent(self, data):
        f = open(self.log_path, 'a+')
        msg = 'Entered isNullPresent method of the preprocessor class.'
        self.logger.log(f, msg)
        try:
            directory = directoryHandling()
            directory.createPreprocessingDataDirectory()
            null_counts = data.isnull().sum()
            cols = data.columns
            cols_with_missing_values = []
            null_present = False
            path = os.path.join(self.base_folder, 'Training_Preprocessing_Data')
            file_name = 'null_values.csv'
            for i in range(len(null_counts)):
                if null_counts[i] > 0:
                    null_present = True
                    cols_with_missing_values.append(cols[i])
            if null_present:
                df_with_null = pd.DataFrame()
                df_with_null['columns'] = data.columns
                df_with_null['missing_values_count'] = np.asarray(data.isnull.sum())
                df_with_null.to_csv(path+'/'+file_name)
                msg = 'Finding missing values is a success. Data written in:: ' + file_name
                self.logger.log(f, msg)
                f.close()
                return null_present, cols_with_missing_values
            return 0, 0

        except Exception as e:
            msg = 'Error while finding columns with null values. ' \
                  'Error in isNullPresent method of preprocessor class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def standardScaling(self, x):
        f = open(self.log_path, 'a+')
        msg = 'Entered standardScaling method of the preprocessor class.'
        self.logger.log(f, msg)
        try :
            scalar = StandardScaler()
            x_scaled = scalar.fit_transform(x)
            msg = 'Label scaling completed.'
            self.logger.log(f, msg)
            f.close()
            return x_scaled, scalar

        except Exception as e:
            msg = 'Error while Scaling Labels. Error in standardScaling method of preprocessor class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def standardScalingTest(self, x, scalar):
        f = open(self.log_path, 'a+')
        msg = 'Entered standardScaling for test dataset.'
        self.logger.log(f, msg)
        try:
            xtest_scaled = scalar.transform(x)
            msg = 'StandardScaling of test data completed.'
            self.logger.log(f, msg)
            f.close()
            return xtest_scaled

        except Exception as e:
            msg = 'Error while standard Scaling test data. ' \
                  'Error in standardScalingTest method of preprocessor class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def logTransformation(self, x):
        for col in x.columns:
            x[col] += 1
            x[col] = np.log(x[col])
        return x

    def imputeMissingValues(self, data):
        f = open(self.log_path, 'a+')
        msg = 'Entered imputeMissingValues method of the preprocessor class.'
        self.logger.log(f, msg)
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            imputed_data = imputer.fit_transform(data)
            new_df = pd.DataFrame(imputed_data, columns=data.colums)
            msg = 'Successfully imputed missing values. Exited the imputeMissingValues method of the preprocessor class.'
            self.logger.log(f, msg)
            f.close()
            return new_df

        except Exception as e:
            msg = 'Error while Imputing missing values in data. ' \
                  'Error in imputeMissingValues method of the preprocessor class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

if __name__ == '__main__':
    pass