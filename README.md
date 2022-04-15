# CementStrangthPredictor

Solve the problem of poor quality of Cement Mixures.
This repository contains code and link to WebApp for 
predicting Cement Strength.
![image](https://user-images.githubusercontent.com/64093713/163631826-68a0c0ea-47ab-4e92-b78d-d0233c5dfa22.png)
![image](https://user-images.githubusercontent.com/64093713/163631881-635a3391-1989-40e2-83f7-0231dea9ee8d.png)


## Deployment
Model has been deployed on Heroku, using Rest API and 
Flask framework. Link to Webapp - 
https://cement-strength-predictor.herokuapp.com/


## Dataset and EDA
The dataset used is: https://drive.google.com/drive/folders/1fIMTz2B5t-8qMkM0bnKlbyYuIoJ9xHSF?usp=sharing

Link to Jupyter Notebook : 

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
    5. Perform EDA to check data distribution using KDE plot, 
       find optimum number of sub-clusters.
    6. Train model on each cluster separately and saving them.
    7. Hyper parameter tuning for fine tuning the models.
    8. Export the models via pickle.

## Project WebApp
    1. Used Rest API and flask framework, created route for home and prediction page.
    2. Used HTML and CSS to design the Webapp frontend.
    3. Created requirements.txt, Procfile, etc. and satisfied all requirements before deployment.
    4. Deployed the Model on Heroku using Git CLI.
