import os
from RawDataValidation.DataValidation import rawDataValidation
from DataBase_Operation.DatabaseOperation import dbOperation
from Data_Transformation.DataTransformation import dataTransform
from Directory_Handling.DirectoryHandling import directoryHandling
from Logger.logger import appLogger

class trainValidation:
    def __init__(self, path):
        self.base_folder = os.path.realpath(os.path.dirname(__file__))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.raw_data = rawDataValidation(path)
        self.db_operation = dbOperation()
        self.directory = directoryHandling()
        self.data_transform = dataTransform()
        self.logger = appLogger()

    def necessaryDirectories(self):
        try:
            # creating directories in which data will be stored
            self.directory.createLogDirectory()
            self.directory.createDirectoryForGoodBadRawData()
            self.directory.createArchiveBadDataDirectory()
            self.directory.createTrainingDatabaseDirectory()
            self.directory.createDbToCsvDirectory()
            self.directory.createPreprocessingDataDirectory()
            # self.directory.createModelsDirectory()
            f = open(self.log_path, 'a+')
            msg = 'Successfully created all necessary directories.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error occurred while creating necessary directories. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def trainValidation(self):
        f = open(self.log_path, 'a+')
        msg = 'Start of Validation on files for Training.'
        self.logger.log(f, msg)
        try:
            # correcting the column names
            self.data_transform.replaceSpaceInColumnNames()
            # extracting values from Training_schema
            LengthOfDateStampInFile, LenghtOfTimeStampInFile, NoOfColumns, ColumnNames = self.raw_data.valuesFromSchema()
            # defining the regex to validate filename
            regex = self.raw_data.manualRegexCreation()
            # validating filename for Training files
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LenghtOfTimeStampInFile)
            # validating column length in file
            self.raw_data.validateColumnNumber(NoOfColumns)
            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            msg = 'Raw Data Validation Completed!!'
            self.logger.log(f, msg)

            msg = 'Creating Training_Database and tables on the basis of given schema!!'
            self.logger.log(f, msg)
            # create database train_db, if present open the connection!
            # Created table with columns given in Training Schema
            self.db_operation.createTableDb('train_db', ColumnNames)
            # inserting data into table
            self.db_operation.insertDataIntoTable('train_db')
            # moving bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            # deleting good and bad file folder
            self.directory.deleteExistingDirectoryForGoodBadRawData()
            # export database to csv
            self.db_operation.createCsvDataFromTable('train_db')
            msg = 'End of validation on training files.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            msg = 'Error occurred while validating train data.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e
