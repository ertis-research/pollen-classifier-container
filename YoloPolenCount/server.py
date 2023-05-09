import os
import zipfile
import random
import string
import cv2
import pathlib
import yaml
import json

import torch
import detect

from flask import Flask, make_response, send_file, request

server = Flask(__name__)

def crop_images(random_string, crop_size=25, file_type='tif'):
    files = []
    for r, d, f in os.walk(os.path.join(os.getcwd(), 'images', random_string, 'received_images')):
        for file in f:
            if f'.{file_type}' in file:
                files.append(os.path.join(r, file))

    for x in files:
        print('Cropping Image: '+x)

        im = cv2.imread(x)

        dims = im.shape

        for i in range(1,crop_size+1):
            for j in range(1,crop_size+1):
                temp_img = im[int(dims[0]*(i-1)/crop_size):int(dims[0]*i/crop_size), int(dims[1]*(j-1)/crop_size):int(dims[1]*j/crop_size)]

                new_file_name = pathlib.Path(x).stem + '_crop-' + str(i) + '-' + str(j) + '.png'

                cv2.imwrite(os.path.join(os.getcwd(), 'images', random_string, 'cropped_images', new_file_name), temp_img)



def extract_images(random_string):
    with zipfile.ZipFile(os.path.join(os.getcwd(), 'images', random_string + '.zip'), 'r') as zip_ref:        
        zip_ref.extractall(os.path.join(os.getcwd(), 'images', random_string, 'received_images'))

    # Delete the zip file
    os.remove(os.path.join(os.getcwd(), 'images', random_string + '.zip'))


def predict_pollen_count(random_string):
    files = []
    for r, d, f in os.walk(os.path.join(os.getcwd(), 'images', random_string, 'cropped_images')):
        for file in f:
            if '.png' in file:
                files.append(os.path.join(r, file))

    arguments = {
        'weights': os.path.join('trained_models', 'v1', 'weights', 'best.pt'),
        'source': os.path.join('images', random_string, 'cropped_images'),
        'img_size': 640,
        'conf_thres': 0.4,
        'iou_thres': 0.45,
        'device': torch.cuda.device_count()-1 if torch.cuda.is_available() else "cpu",
        'view_img': False,
        'save_txt': True,
        'save_conf': False,
        'nosave': False,
        'classes': None,
        'agnostic_nms': False,
        'augment': False,
        'update': False,
        'project': os.path.join('images', random_string),
        'name': 'predicted_images',
        'exist_ok': False,
        'no_trace': False
    }

    detect.detect(arguments)


def generate_pollen_report(random_string, model_version='v1'):
    # Count different pollen types and generate a report
    
    # Load data yaml in trained_models/model_version/data/data.yaml
    with open(os.path.join('trained_models', model_version, 'data', 'data.yaml')) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    # Get classes from data
    classes = data['names']

    # Create a dictionary with classes as keys and count as values
    pollen_count = {}
    for c in classes:
        pollen_count[c] = 0
    
    # Get all files in images/random_string/predicted_images/labels
    files = []
    for r, d, f in os.walk(os.path.join(os.getcwd(), 'images', random_string, 'predicted_images', 'labels')):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    
    # For each file in files, open file and for each line in file, get the class and count it
    for f in files:
        with open(f) as file:
            for line in file:
                pollen_count[classes[int(line.split()[0])]] += 1

    return pollen_count

def export_predictions(random_string):
    # Zip the predicted images folder
    with zipfile.ZipFile(os.path.join(os.getcwd(), 'images', random_string, 'predicted_images.zip'), 'w') as zip_ref:
        # Write each file in predicted_images folder (just in that directory)
        for r, d, f in os.walk(os.path.join(os.getcwd(), 'images', random_string, 'predicted_images')):
            for file in f:
                zip_ref.write(os.path.join(r, file), arcname=file)    



@server.route('/predict', methods=['POST'])
def predict_pollen():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    if not os.path.exists(os.path.join(os.getcwd(), 'images', random_string)):
        os.makedirs(os.path.join(os.getcwd(), 'images', random_string))
        os.makedirs(os.path.join(os.getcwd(), 'images', random_string, 'received_images'))
        os.makedirs(os.path.join(os.getcwd(), 'images', random_string, 'cropped_images'))

    zip_file = request.files['images.zip']
    zip_file.save(os.path.join(os.getcwd(), 'images', f"{random_string}.zip"))
    
    extract_images(random_string)

    crop_images(random_string, crop_size=2, file_type='jpg')

    result = predict_pollen_count(random_string)

    # Count different pollen types and generate a report
    report = generate_pollen_report(random_string) 

    # clear directory and zip
    export_predictions(random_string) 

    
    filename = os.path.join(os.getcwd(), 'images', random_string, 'predicted_images.zip')
    response = make_response(send_file(filename, as_attachment=True))    
    response.headers['pollen_count_report'] = json.dumps(report)

    return response