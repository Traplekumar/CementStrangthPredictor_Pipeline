import os
import shutil
from Logger.logger import appLogger

class directoryHandling:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()

    def createLogDirectory(self):
        try:
            path = os.path.join(self.base_folder, 'General_Logs')
            if not os.path.isdir(path):
                os.makedirs(path)
                msg = 'Log Directory Created Successfully.'
            else:
                msg = 'Log Directory Present. Skipping creating new log directory.'

            file = open(os.path.join(path, 'GeneralLogs.txt'), 'a+')
            self.logger.log(file, msg)

        except Exception as e:
            path = os.path.join(self.base_folder, 'General_Logs')
            file = open(os.path.join(path, 'GeneralLogs.txt'), 'a+')
            msg = 'Log Directory already present. Skipping new creation. ' + str(e)
            self.logger.log(file, msg)
            raise e

        # self.log_path = os.path.join(self.base_folder, 'General_Logs')

    def createDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Good_Raw')
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Bad_Raw')
            if not os.path.isdir(path):
                os.makedirs(path)
            file = open(self.log_path, 'a+')
            msg = 'Successfully created New Good and Bad Raw directories.'
            self.logger.log(file, msg)

        except Exception as e:
            file = open(self.log_path, 'a+')
            msg = 'Error while creating Training_Raw_Files_Validated directory. ' + str(e)
            self.logger.log(file, msg)
            raise e

    def deleteExistingDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated')
            if os.path.isdir(path):
                shutil.rmtree(path)
                file = open(os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt'), 'a+')
                msg = 'Successfully deleted Good and Bad Raw directories before starting Validation.'
                self.logger.log(file, msg)

        except Exception as e:
            file = open(os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt'), 'a+')
            msg = 'Error while deleting Good and Bad Raw directories. ' + str(e)
            self.logger.log(file, msg)
            raise e

    def createArchiveBadDataDirectory(self):
        try:
            path = os.path.join(self.base_folder, 'Training_Archived_Bad_Data')
            if os.path.isdir(path):
                msg = "Training_Archived_Bad_Data directory already present."
            else:
                os.makedirs(path)
                msg = 'Training_Archived_Bad_Data directory created.'

            f = open(self.log_path, 'a+')
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = "Error while creating Training_Archived_Bad_Data directory. " + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createTrainingDatabaseDirectory(self):
        try:
            path = os.path.join(self.base_folder, 'Training_Data_Base')
            if os.path.isdir(path):
                msg = 'Training_Database directory already present.'
            else:
                os.makedirs(path)
                msg = 'Successfully created Training_Database directory.'

            f = open(self.log_path, 'a+')
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error while creating Training_Database directory. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createDbToCsvDirectory(self):
        try:
            path = os.path.join(self.base_folder, 'Training_CSV_From_DB')
            if os.path.isdir(path):
                msg = 'Training_CSV_From_DB directory already present.'
            else:
                os.makedirs(path)
                msg = 'Successfully created Training_CSV_From_DB directory.'

            f = open(self.log_path, 'a+')
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error while creating Training_CSV_From_DB directory. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createPreprocessingDataDirectory(self):
        f = open(self.log_path, 'a+')
        try:
            path = os.path.join(self.base_folder, 'Training_Preprocessing_Data')
            if not os.path.isdir(path):
                os.makedirs(path)
                msg = 'Successfully created Training_Preprocessing_Data directory.'
                self.logger.log(f, msg)
                f.close()

        except Exception as e:
            msg = 'Error while creating Training_Preprocessing_Data directory. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createModelsDirectory(self, filename):
        f = open(self.log_path, 'a+')
        try:
            path = os.path.join(self.base_folder, 'Models')
            if not os.path.isdir(path):
                os.makedirs(path)
                msg = 'Successfully created Models directory.'
                self.logger.log(f, msg)

            os.makedirs(os.path.join(path, filename))
            msg = f'Successfully created {filename} folder.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            msg = 'Error while creating Models Directory. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

if __name__ == '__main__':
    a = directoryHandling()
    a.createLogDirectory()
    a.deleteExistingDirectoryForGoodBadRawData()
    a.createDirectoryForGoodBadRawData()
    a.createArchiveBadDataDirectory()
    a.createTrainingDatabaseDirectory()
    a.createDbToCsvDirectory()
    a.createPreprocessingDataDirectory()
    a.createModelsDirectory()