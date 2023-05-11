from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AnalysisApp.models import Polen
from django.contrib.auth.models import User
from AnalysisApp.serializers import PolenSerializer

from django.core.files.storage import default_storage

from DjangoAPI.settings import SECRET_KEY

import AnalysisApp.AnalysisFunctions as af
from pathlib import Path

import numpy as np
import zipfile
import requests

from collections import OrderedDict

import jwt

# Create your views here.

def getUserDetails_fromJWT(request):
    jwt_token = request.META['HTTP_AUTHORIZATION'][4:]
    jwt_token_decoded = jwt.decode(str(jwt_token), SECRET_KEY, algorithms="HS256")    
    UserId = jwt_token_decoded['user_id']
    username = jwt_token_decoded['username']
    email = jwt_token_decoded['email']
    
    try:
        User.objects.get(id=UserId, username = username, email = email)
    except:
        return -1, 401 # Unauthorized

    return UserId, 200 # OK


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def polenApi(request, id=0):
    """
    This view is used by the frontend module to obtain 
    the sample analysis list or delete one analysis from the list.

    """    
    user, code = getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse([], safe=False)

    if request.method=='GET':  
        polen = Polen.objects.filter(UserId=user)
        polen_serializer = PolenSerializer(polen, many=True)
        return JsonResponse(polen_serializer.data, safe=False)

    elif request.method=='DELETE':
        try:
            polen = Polen.objects.get(AnalysisId=id, UserId_id = user)
            polen.delete()
            return JsonResponse("Deleted Successfully!", safe= False)
        except:
            return JsonResponse("", safe= False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadVSI(request):
    """
    This view is used by the frontend module to send to the backend the file with the sample to analyse.

    """
    _, code = getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse([], safe=False)

    file=request.FILES['uploadedFile']    
    file_name = default_storage.save(file.name, file)
    file_path = default_storage.path(file_name)

    unzip_path = 'images\\'+Path(file_name).stem
    af.unzipFile(file_path, unzip_path)   

    vsiFiles = af.listFiles(unzip_path, 'vsi')
    if(len(vsiFiles) == 0 or len(vsiFiles) > 1):
        return JsonResponse('Error uploading file. The VSI file cannot be found or there is more than one.', safe=False)

    responseList = []
    paths = OrderedDict()
    paths['unzip']    = unzip_path
    paths['filename'] = vsiFiles[0]
    responseList.append(paths)
    for image in af.getImageInfo(unzip_path+'\\'+vsiFiles[0]):
        images = OrderedDict()
        images['identifier'] = image[0]
        images['name'] = image[1]
        responseList.append(images)    
    return JsonResponse(responseList, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyseSelectedImages(request):
    """
    This view is used by the frontend module to send to the backend how it has to analyse the image previously sent.

    """
    userId, code = getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse("Analysis Failed", safe=False)

    reqStr  = JSONParser().parse(request)
    if reqStr['UserId'] != userId:        
        return JsonResponse("Analysis Failed", safe=False)
    
    parsed_route = reqStr['PhotoFilePath']+'\\parsed'
    af.parseImages(reqStr['SelectedRowsIds'], reqStr['PhotoFilePath']+'\\'+reqStr['PhotoFileName'], parsed_route)
    
    totalBlobsDetected = [0,0]   
    if (len(reqStr['SelectedRowsIds']) != 0):
        # old method
        imageList = af.listFiles(parsed_route, 'ome.tiff')
        for image in imageList:
            res = af.analyseImage(image, parsed_route, 0.5833) 
            totalBlobsDetected = np.add(totalBlobsDetected, res )
        
        # new method: zip images in imagelst and post to api as FILES
        imageList = af.listFiles(parsed_route, 'ome.tiff')
        zip_path = parsed_route+'\\images.zip'
        zip_file = zipfile.ZipFile(zip_path, 'w')
        for image in imageList:
            zip_file.write(parsed_route+'\\'+image, image)

        zip_file.close()

        res = requests.post('http://localhost:8091/predict', files={'images.zip': open(zip_path, 'rb')})




    
    new_pollen = OrderedDict()
    new_pollen['AnalysisId'] = reqStr['AnalysisId']
    new_pollen['AnalysisName'] = reqStr['AnalysisName']
    new_pollen['SampleDate'] = reqStr['SampleDate']
    new_pollen['AnalysisDate'] = reqStr['AnalysisDate']
    new_pollen['PhotoFileName'] = reqStr['PhotoFileName']
    new_pollen['PhotoFilePath'] = reqStr['PhotoFilePath']
    new_pollen['UserId'] = reqStr['UserId']
    new_pollen['AnalysisResult']  = res.headers['AnalysisResult']

    polen_serializer = PolenSerializer(data= new_pollen)
    if polen_serializer.is_valid():
        polen_serializer.save()
        return JsonResponse("Analysis Okay", safe=False)
    return JsonResponse("Analysis Failed", safe=False)