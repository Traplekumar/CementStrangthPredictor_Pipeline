import pickle
import os
import shutil
from Directory_Handling import DirectoryHandling
from Logger.logger import appLogger

class fileOperation:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.model_directory = os.path.join(self.base_folder, 'Models')
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()


    def saveModel(self, model, filename):
        f = open(self.log_path, 'a+')
        msg = 'Entered saveModel method of the fileOperation class.'
        self.logger.log(f, msg)
        directory = DirectoryHandling.directoryHandling()
        try:
            path = os.path.join(self.model_directory, filename)
            if os.path.isdir(path):
                shutil.rmtree(path)
                directory.createModelsDirectory(filename)
            else:
                directory.createModelsDirectory(filename)

            with open(path+'\\'+filename+'.pickle', 'wb') as file:
                pickle.dump(model, file)
            msg = 'Successfully save model:: ' + filename + '. Exited the saveModel method of the fileOperation class.'
            self.logger.log(f, msg)
            f.close()

        except Exception as e:
            msg = 'Error while saving model. Error in saveModel method or the fileOperation class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def loadModel(self, filename):
        f = open(self.log_path, 'a+')
        msg = 'Entered loadModel method of the fileOperation class.'
        self.logger.log(f, msg)
        try:
            path = os.path.join(self.base_folder, 'Models', filename)
            with open(path+'/'+filename+'.pickle', 'rb') as model:
                msg = 'Successfully loaded model:: ' + filename + '. Exited the loadModel method of the fileOperation class.'
                self.logger.log(f, msg)
                f.close()
                return pickle.load(model)

        except Exception as e:
            msg = 'Error while loading saved model. ' + filename + ' model could not be loaded.' \
                  'Error occurred in loadModel method of the fileOperation class.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def findCorrectModelFile(self, cluster_number):
        f = open(self.base_folder, 'a+')
        msg = 'Entered the findCorrectModelFile method of the fileOperation class.'
        self.logger.log(f, msg)
        try:
            folder_name = self.model_directory
            model_name = 'Empty'
            list_of_files = os.listdir(folder_name)
            for file in list_of_files:
                try:
                    if file.index(str(cluster_number)) != -1:
                        model_name = file
                except:
                    continue
            model_name = model_name.split('.')[0]
            msg = 'Exited teh findCorrectModeFile method of the fileOperation class.'
            self.logger.log(f, msg)
            f.close()
            return model_name

        except Exception as e:
            msg = 'Error occurred in findCorrectModelFile method of fileOperation class. ' + str(e)
            self.logger.log(f, msg)
            raise e




