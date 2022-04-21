from flask import Flask, request, render_template, url_for, redirect
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from ValidationInsertionTraining import trainValidation
from TrainingModel import trainModel
from PredictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)
@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def train():
    if request.method == "POST":
        if request.form.get('train') == 'Pre Trained':
            return redirect(url_for('pred'))
    else:
        return render_template('training.html')

@app.route('/predict/', methods=['GET', 'POST'])
@cross_origin()
def pred():
    if request.method=="POST":
        cement = float(request.form['cement'])
        blast_furnace = float(request.form['blastFurnaceSlag'])
        fly_ash = float(request.form['flyAsh'])
        water = float(request.form['water'])
        sup_plasticizer = float(request.form['Superplaticizer'])
        cor_aggre = float(request.form['coarseAggregate'])
        fin_aggre = float(request.form['fineAggregate'])
        age_day = float(request.form['ageDay'])
        feature_pred = [cement, blast_furnace, fly_ash, water, sup_plasticizer, cor_aggre, fin_aggre, age_day]
        predictor = prediction()
        pred = predictor.modelPrediction(feature_pred)
        return render_template('prediction.html', prediction=str(pred)+' MPa')
    else:
        return render_template('prediction.html', prediction='Enter the specified values.')

if __name__ == '__main__':
    # path = os.path.realpath(os.path.dirname(__file__))
    # path = os.path.join(path, 'Training_Batch_Files')
    # data_validation = trainValidation(path)
    #
    # data_validation.necessaryDirectories()
    # data_validation.trainValidation()
    # training = trainModel()
    # training.modelTrain()
    app.run(debug=True)

