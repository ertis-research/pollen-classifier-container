# PollenImage Analyzer

This repository contains the code of PollenImage Analyzer, a web application capable of analysing pollen samples in the format of the microscope from which the samples are taken, thus promoting automatic analysis. 

## Table of Contents
- [Deployment](#Deployment)
- [Installation and development](#Installation-and-development)
    - [Requirements](#requirements) 
    - [Steps to build and the application](#Steps-to-build-and-the-application)
- [License](#license)

## Deployment
In order to deploy the application, Kubernetes YAMLs are provided in order to make a simple deploy. Applying all those YAMLs in the same namespace should be enough to have the application running at port 8520.

## Installation and development

### Requirements

- [Python 3.6–3.8](https://www.python.org/)
- [Node.js](https://nodejs.org/)

### Steps to build the application

1. Install the libraries and execute the frontend:
    ```
    cd frontend/angular10
    npm install
    npm i -g @angular/cli
    
    ng serve --open
    ```

2. Install the libraries and execute the backend:
    ```
    cd DjangoAPI
    pip3 install -r ../requirements_django.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manate.py createsuperuser
    
    python3 manage.py runserver
    ```


Finally, you will be able to access the application: http://localhost:4200/


## License
MIT
