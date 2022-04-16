# CementStrangthPredictor

Solve the problem of poor quality of Cement Mixures.
This repository contains code and link to WebApp for 
predicting Cement Strength.

![Home Page](https://user-images.githubusercontent.com/64093713/163632720-8f0145c1-fd38-4085-8029-ae957523a7d8.png)
![Predict Page](https://user-images.githubusercontent.com/64093713/163632712-a632c512-adec-4049-89a6-5b208edbbc42.png)

## Deployment
Model has been deployed on Heroku, using Rest API and 
Flask framework. Link to Webapp - 
https://cement-strength-predictor.herokuapp.com/


## Dataset
The dataset used is: https://drive.google.com/drive/folders/1fIMTz2B5t-8qMkM0bnKlbyYuIoJ9xHSF?usp=sharing

## Tech Stack
- Python3
- Flask
- Rest API
- SQLite
- Heroku
- Html
- CSS
- Jupyter Notebook
- PyCharm

## Description
### Problem Statement
To determine the strength of cement mixture.

### Models used
- Random Forest
- Linear Regression


## Project Automated Pipeline
    1. Validation of the Raw Data by simulating data coming from client.
    2. Perform various data checks, filename, column name & datatype validation.
    3. Creation of SQLite Database containg good data.
    4. Preprocessing the data to, impute missing values, perform Scaling, and One Hot Encoding.
    5. Perform EDA to, find optimum number of sub-clusters.
    6. Train model on each cluster separately and saving them.
    7. Hyper parameter tuning for fine tuning the models.
    8. Export the models via pickle.

## Project WebApp
    1. Used Rest API and flask framework, created route for home and prediction page.
    2. Used HTML and CSS to design the Webapp frontend.
    3. Created requirements.txt, Procfile, etc. and satisfied all requirements before deployment.
    4. Deployed the Model on Heroku using Git CLI.
