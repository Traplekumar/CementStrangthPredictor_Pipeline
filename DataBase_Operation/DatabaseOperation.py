import sqlite3
import os
import pandas as pd
import csv
from Logger.logger import  appLogger
from Directory_Handling.DirectoryHandling import directoryHandling

class dbOperation:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.good_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Good_Raw')
        self.bad_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Bad_Raw')
        self.path = os.path.join(self.base_folder, 'Training_Data_base')
        self.logger = appLogger()

    def dataBaseConnection(self, DatabaseName):
        try:
            conn = sqlite3.connect(self.path + "/" + DatabaseName + '.db')
            f = open(self.log_path, 'a+')
            msg = 'Successfully opened database:: ' + DatabaseName
            self.logger.log(f, msg)
            f.close()
            return conn

        except Exception as e:
            f = open(self.log_path, 'a+')
            msg = 'Error while connecting to database. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def createTableDb(self, DatabaseName, column_names):
        conn = self.dataBaseConnection(DatabaseName)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")
            # "sqlite_master" is an internal table that is present in all SQLite databases. The content of this
            # table describes the database's schema.
            if cursor.fetchone()[0] == 1:
                conn.close()
                f = open(self.log_path, 'a+')
                msg = 'Tables already present.'
                self.logger.log(f, msg)
                msg = 'Database closed Successfully:: ' + DatabaseName
                self.logger.log(f, msg)
                f.close()

            else:
                for key in column_names.keys():
                    type = column_names[key]
                    try:
                        conn.execute(f'ALTER TABLE Good_Raw_Data ADD COLUMN "{key}" {type}')
                    except:
                        cursor.execute(f'CREATE TABLE Good_Raw_Data ({key} {type})')

                conn.close()
                f = open(self.log_path, 'a+')
                msg = 'Tables created Successfully.'
                self.logger.log(f, msg)
                msg = 'Database closed Successfully:: ' + DatabaseName
                self.logger.log(f, msg)
                f.close()

        except Exception as e:
            conn.close()
            f = open(self.log_path, 'a+')
            msg = 'Error while creating database table. ' + str(e)
            self.logger.log(f, msg)
            msg = 'Database closed successfully.'
            self.logger.log(f, msg)
            f.close()
            raise e

    def insertDataIntoTable(self, DatabaseName):
        conn = self.dataBaseConnection(DatabaseName)
        cursor = conn.cursor()
        for file in os.listdir(self.good_data_path):
            file_path = os.path.join(self.good_data_path, file)
            reader = pd.read_csv(file_path)
            try:
                for r in range(reader.shape[0]):
                    # row = tuple([i for i in reader.iloc[r]])

                    row = tuple([i if str(i) != 'nan' else 'NULL' for i in reader.iloc[r] ])
                    cursor.execute(f'INSERT INTO Good_Raw_Data VALUES {row}')
                conn.commit()
                conn.close()
                f = open(self.log_path, 'a+')
                msg = 'File loaded successfully in Database.'
                self.logger.log(f, msg)
                msg = 'Database closed Successfully:: ' + DatabaseName
                self.logger.log(f, msg)
                f.close()

            except Exception as e:
                conn.close()
                f = open(self.log_path, 'a+')
                msg = 'Error while loading file in database. ' + str(e)
                self.logger.log(f, msg)
                msg = 'Database closed Successfully:: ' + DatabaseName
                self.logger.log(f, msg)
                f.close()
                raise e

    def createCsvDataFromTable(self, DatabaseName):
        directory = directoryHandling()
        directory.createDbToCsvDirectory()
        filename = "InputFile.csv"
        file_path = os.path.join(self.base_folder, 'Training_CSV_From_DB', filename)
        conn = self.dataBaseConnection(DatabaseName)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Good_Raw_Data")
            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]
            csv_file = csv.writer(open(file_path, 'w', newline=''), delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')
            csv_file.writerow(headers)
            csv_file.writerows(results)

            conn.close()
            f = open(self.log_path, 'a+')
            msg = 'Successfully exported database as CSV file:: ' + filename
            self.logger.log(f, msg)
            msg = 'Database closed successfully.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            conn.close()
            f = open(self.log_path, 'a+')
            msg = 'Error while exporting database as CSV file. ' + str(e)
            self.logger.log(f, msg)
            msg = 'Database closed successfully.'
            self.logger.log(f, msg)
            f.close()
            raise e

if __name__ == '__main__':
    from RawDataValidation.DataValidation import rawDataValidation
    a = rawDataValidation('E:\Documents\iNeuron\PROJECT\CementStrengthSelf\Training_Batch_Files')
    _, _, _, column_names = a.valuesFromSchema()

    b = dbOperation()
    b.createTableDb('train_db', column_names)
    b.insertDataIntoTable('train_db')

    c = b.dataBaseConnection('train_db').cursor()
    c.execute("SELECT * FROM Good_Raw_Data")
    b.createCsvDataFromTable('train_db')