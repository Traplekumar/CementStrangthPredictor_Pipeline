import os
import re
from Logger.logger import appLogger
import pandas as pd

class dataTransform:

    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.good_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Good_Raw')
        self.bad_data_path = os.path.join(self.base_folder, 'Training_Raw_Files_Validated', 'Bad_Raw')
        self.logger = appLogger()

    def replaceSpaceInColumnNames(self):
        f = open(self.log_path, 'a+')
        msg = 'Started replacing Whitespaces in Columns names.'
        self.logger.log(f, msg)
        try:
            for file in os.listdir(self.good_data_path):
                file_path = os.path.join(self.good_data_path, file)
                df = pd.read_csv(file_path)
                column_headers = df.columns
                new_columns = []
                for c in column_headers:
                    regex = re.compile(r' _| ')
                    replace = re.sub(regex, '_', c)
                    new_columns.append(replace)
                df.set_axis(new_columns, axis=1, inplace=True)
                df.to_csv(file_path, index=False, header=True)
                msg = 'Successfully replaced whitespace in column names.'
                self.logger.log(f, msg)
                f.close()

        except Exception as e:
            msg = "Error while replacing whitespace in column names."
            self.logger.log(f, msg)
            f.close()
            raise e


if __name__ == '__main__':
    a = dataTransform()
    a.replaceSpaceInColumnNames()