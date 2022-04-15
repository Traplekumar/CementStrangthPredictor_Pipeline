from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from Logger.logger import appLogger
from Directory_Handling.DirectoryHandling import directoryHandling

class rawDataValidation:
    def __init__(self, path):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.good_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Good_Raw')
        self.bad_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Bad_Raw')
        self.Batch_Directory = path
        self.schema_path = os.path.join(self.base_folder, "Training_schema.json")
        self.logger = appLogger()

    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()

            #pattern = dic["SampleFileName"]
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            NumberOfColumns = dic['NumberOfColumns']
            column_names = dic['ColName']
            file = open(self.log_path, 'a+')
            msg = f"LengthOfDateStampFile:: {LengthOfDateStampInFile} \t " \
                  f"LengthOfTimeStampInFile:: {LengthOfTimeStampInFile} \t NumberOfColumns:: {NumberOfColumns}"
            self.logger.log(file, msg)
            file.close()

            return LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberOfColumns, column_names

        except Exception as e:
            file = open(self.log_path, 'a+')
            msg = "Error in valuesFromSchema module of RawDataValidation. " + str(e)
            self.logger.log(file, msg)
            file.close()
            raise e

    def manualRegexCreation(self):
        regex = "(cement_strength)_[0-9]{8}_[0-9]{6}\.(csv)"
        return regex

    def moveBadFilesToArchiveBad(self):
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H%M%S')
        '''******************************************************************************************************
        Here we are moving Bad Raw data into Bad_Raw directory first and then, into 
        TrainingArchiveBadData/BadData_Date_Time. This is because -
        1.  Each new instance of BadData_Date_Time directory creates a new folder (because of date and time).
            If we move each file to TrainingArchiveBadData/BadData_Data_Time, we will have to store each file 
            into new BadData_Date_Time.
        2.  It will create multiple folders in just one Complete run on the application (if there are multilple
            bad files/data).
        *******************************************************************************************************'''
        try:
            source = self.bad_data_path
            if os.path.isdir(source):
                directory = directoryHandling()
                directory.createArchiveBadDataDirectory()
                # path = os.path.join(self.base_folder, 'Training_Archived_Bad_Data')
                # if not os.path.isdir(path):
                #     os.makedirs(path)
                dest = self.base_folder + '/' + 'Training_Archived_Bad_Data/BadData_' + str(date) + '_' + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(os.path.join(self.bad_data_path, f), dest)

                file = open(self.log_path, 'a+')
                msg = 'Bad files moved to archive folder.'
                self.logger.log(file, msg)
                if os.path.isdir(self.bad_data_path):
                    shutil.rmtree(self.bad_data_path)
                msg = 'Bad_Raw Data Folder Deleted Successfully after Archiving data.'
                self.logger.log(file, msg)
                file.close()

        except Exception as e:
            file = open(self.log_path, 'a+')
            msg = 'Error while moving bad files to archive. ' + str(e)
            self.logger.log(file, msg)
            file.close()
            raise e

    def validationFileNameRaw(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        directory = directoryHandling()
        directory.deleteExistingDirectoryForGoodBadRawData()
        directory.createDirectoryForGoodBadRawData()
        try:
            f = open(self.log_path, 'a+')
            for filename in listdir(self.Batch_Directory):
                filepath = self.Batch_Directory + '/' + filename
                if re.match(regex, filename):
                    splitDot = re.split('.csv', filename)
                    splitDot = re.split('_', splitDot[0])
                    if len(splitDot[2]) == LengthOfDateStampInFile and len(splitDot[3]) == LengthOfTimeStampInFile:
                        shutil.copy(filepath, self.good_data_path)
                        msg = 'Valid File name! File moved to Good_Raw folder :: ' + filename
                        self.logger.log(f, msg)
                    else:
                        shutil.copy(filepath, self.bad_data_path)
                        msg = 'Invalid File name! File moved to Bad_Raw folder :: ' + filename
                        self.logger.log(f, msg)
                else:
                    shutil.copy2(filepath, self.bad_data_path)
                    msg = 'Invalid File name! File moved to Bad_Raw folder :: ' + filename
                    self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = "Error occurred while validating FileNames" + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def validateColumnNumber(self, NumberOfColumns):
        try:
            f = open(self.log_path, 'a+')
            msg = 'Column Length Validation started'
            self.logger.log(f, msg)
            for file in listdir(self.good_data_path):
                df = pd.read_csv(os.path.join(self.good_data_path, file))
                if df.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move(os.path.join(self.good_data_path, file), self.bad_data_path)
                msg = 'Invalid number of Columns! File moved to Bad_Raw data folder::' + file
                self.logger.log(f, msg)

            msg = 'Column Length Validation Completed.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error occurred while validating the number of columns.'
            self.logger.log(f, msg)
            f.close()
            raise e

    def validateMissingValuesInWholeColumn(self):
        try:
            f = open(self.log_path, 'a+')
            msg = 'Missing whole column values Validation Started.'
            self.logger.log(f, msg)
            for file in listdir(self.good_data_path):
                df = pd.read_csv(os.path.join(self.good_data_path, file))
                count = 0
                null_values = df.isnull().sum()
                for i in range(df.shape[1]):
                    if null_values[i] == df.shape[0]:
                        shutil.move(os.path.join(self.good_data_path, file), self.bad_data_path)
                        msg = "Invalid Column! Missing whole values in column. File moved to Bad_Raw folder."
                        break
            msg = 'Missing whole column values validation ended.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error occurred while moving validating missing whole values in column. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

if __name__ == '__main__':
    a = rawDataValidation('E:\Documents\iNeuron\PROJECT\CementStrengthSelf\Training_Batch_Files')
    a.valuesFromSchema()
    a.manualRegexCreation()

    a.validationFileNameRaw('(cement_strength)_[0-9]{8}_[0-9]{6}\.(csv)', 8, 6)
    a.validateColumnNumber(9)
    a.validateMissingValuesInWholeColumn()
    a.moveBadFilesToArchiveBad()