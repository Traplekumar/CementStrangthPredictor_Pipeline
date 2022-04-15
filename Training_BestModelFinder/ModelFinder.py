import os
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from Logger.logger import appLogger

class modelFinder:
    def __init__(self):
        self.base_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.linearReg = LinearRegression()
        self.randomForestReg = RandomForestRegressor()
        self.log_path = os.path.join(self.base_folder, 'General_Logs', 'GeneralLogs.txt')
        self.logger = appLogger()

    def getBestParamsForRandomForestReg(self, xtrain, ytrain):
        f = open(self.log_path, 'a+')
        msg = 'Entered the RandomForestReg method of the modelFinder class.'
        self.logger.log(f, msg)
        try:
            param_grid = {
                'n_estimators': [10, 20, 30, 40, 50],
                'max_features': ['auto', 'sqrt', 'log2'],
                'min_samples_split': range(2, 10),
                'bootstrap': [True, False]
            }
            grid = GridSearchCV(self.randomForestReg, param_grid, cv=5, n_jobs=-1)
            grid.fit(xtrain, ytrain)
            n_estimators = grid.best_params_['n_estimators']
            max_features = grid.best_params_['max_features']
            min_samples_split = grid.best_params_['min_samples_split']
            bootstrap = grid.best_params_['bootstrap']

            random_forest_final = RandomForestRegressor(n_estimators=n_estimators, max_features=max_features,
                                                        min_samples_split=min_samples_split, bootstrap=bootstrap)
            random_forest_final.fit(xtrain, ytrain)
            msg = 'Random Forest Regressor best params: ' + str(grid.best_params_) + '. ' \
                  'Exited the RandomForestReg method of the modelFinder class.'
            self.logger.log(f, msg)
            f.close()
            return random_forest_final

        except Exception as e:
            msg = 'Error while finding best parameters for Random Forest Regressor. ' \
                  'Error in RandomForestReg method of the modelFinder class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def getBestParamsForLinearReg(self, xtrain, ytrain):
        f = open(self.log_path, 'a+')
        msg = 'Entered LinearRegressor method of the modelFinder class.'
        self.logger.log(f, msg)
        try:
            param_grid = {
                'fit_intercept' : [True, False],
                # 'copy_x' : [True, False]
            }
            grid = GridSearchCV(self.linearReg, param_grid, cv=5, n_jobs=-1)
            grid.fit(xtrain, ytrain)
            fit_intercept = grid.best_params_['fit_intercept']
            # normalize = grid.best_params_['normalize']
            # copy_x = grid.best_params_['copy_x']
            linear_reg_final = LinearRegression(fit_intercept=fit_intercept)
            linear_reg_final.fit(xtrain, ytrain)
            msg = 'Linear Regression best params: ' + str(grid.best_params_) + '. ' \
                  'Exited the LinearRegressor method of the modelFinder class.'
            self.logger.log(f, msg)
            f.close()
            return linear_reg_final

        except Exception as e:
            msg = 'Error while finding best parameters for Linear Regressor.' \
                  'Error occurred in LinearRegressor method of the modelFinder class.' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e

    def getBestModel(self, xtrain, ytrain, xtest, ytest):
        f = open(self.log_path, 'a+')
        msg = 'Entered getBestModel method of the modelFinder class.'
        self.logger.log(f, msg)
        try:
            linear_reg = self.getBestParamsForLinearReg(xtrain, ytrain)
            pred_linear_reg = linear_reg.predict(xtest)
            linear_reg_error = r2_score(ytest, pred_linear_reg)

            random_forest_reg = self.getBestParamsForRandomForestReg(xtrain, ytrain)
            pred_random_forest = random_forest_reg.predict(xtest)
            random_forest_error = r2_score(ytest, pred_random_forest)
            # print('linear_reg_error: ', linear_reg_error)
            # print('random_forest_error: ', random_forest_error)

            if linear_reg_error < random_forest_error:
                msg = 'Random Forest Regressor works better.'
                self.logger.log(f, msg)
                f.close()
                return 'RandomForestRegressor', random_forest_reg
            else:
                msg = 'Linear Regressor works better.'
                self.logger.log(f, msg)
                f.close()
                return 'LinearRegression', linear_reg

        except Exception as e:
            msg = 'Error in getBestModel method of modelFinder class. ' + str(e)
            self.logger.log(f, msg)
            f.close()
            raise e