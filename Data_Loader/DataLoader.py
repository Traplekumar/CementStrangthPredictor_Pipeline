import os
import pandas as pd
from Logger.logger import appLogger

class dataGetter:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs/GeneralLogs.txt')
        self.training_file = os.path.join(self.base_folder, 'Training_CSV_From_DB/InputFile.csv')
        self.logger = appLogger()

    def getData(self):
        f = open(self.log_path, 'a+')
        msg = 'Entered the getData method of the fileOperation class.'
        self.logger.log(f, msg)
        try:
            data = pd.read_csv(self.training_file)
            msg = 'Data Loaded successful. Exited the getData method of fileOperation class.'
            self.logger.log(f, msg)
            f.close()
            return data

        except Exception as e:
            msg = 'Error while loading data for model training. ' \
                  'Error occurred in getData method of fileOperation class. ' + str(e)
            self.logger.log(f, msg)
            raise e

if __name__ == '__main__':
    a = dataGetter()
    a.getData()