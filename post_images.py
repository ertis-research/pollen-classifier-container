# generate a post request that sends in FILES the zip images.zip

import requests
import os

url = "http://localhost:5000/predict"

# send images.zip in FILES
files = {'images.zip': open(os.path.join(os.getcwd(), 'images.zip'), 'rb')}

# send the post request
r = requests.post(url, files=files)

# print response headers
print(r.headers)