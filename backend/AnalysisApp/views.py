from rest_framework.decorators import permission_classes #, api_view
from adrf.decorators import api_view # as async_api_view
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AnalysisApp.models import Polen
from django.contrib.auth.models import User
from AnalysisApp.serializers import PolenSerializer

from django.core.files.storage import default_storage

from DjangoAPI.settings import SECRET_KEY, YOLO_EXECUTOR_URL

import AnalysisApp.AnalysisFunctions as af
from pathlib import Path

import numpy as np
import zipfile
import httpx as requests
import os

from collections import OrderedDict

from asgiref.sync import sync_to_async

import jwt

# Create your views here.

# @sync_to_async
async def getUserDetails_fromJWT(request):
    jwt_token = request.META['HTTP_AUTHORIZATION'][len("Bearer "):]
    jwt_token_decoded = jwt.decode(str(jwt_token), SECRET_KEY, algorithms="HS256")

    UserId = jwt_token_decoded['user_id']
    username = jwt_token_decoded['username']
    email = jwt_token_decoded['email']
    
    try:
        await User.objects.aget(id=UserId, username = username, email = email)
        # User.objects.get(id=UserId, username = username, email = email)
    except:
        return -1, 401 # Unauthorized

    return UserId, 200 # OK


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
async def polenApi(request, id=0):
    """
    This view is used by the frontend module to obtain 
    the sample analysis list or delete one analysis from the list.

    """    
    user, code = await getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse([], safe=False)

    if request.method=='GET':  
        polen = await Polen.objects.filter(UserId=user)
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
async def uploadVSI(request):
    """
    This view is used by the frontend module to send to the backend the file with the sample to analyse.

    """    
    _, code = await getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse([], safe=False)

    # save the file in the server (async function)
    file=request.FILES['uploadedFile']    
    file_name = default_storage.save(file.name, file)
    file_path = default_storage.path(file_name)

    unzip_path = os.path.join("images", Path(file_name).stem)    

    if not os.path.exists("images"):
        os.makedirs("images")

    af.unzipFile(file_path, unzip_path)   

    vsiFiles = af.listFiles(unzip_path, 'vsi')
    if(len(vsiFiles) == 0 or len(vsiFiles) > 1):
        return JsonResponse('Error uploading file. The VSI file cannot be found or there is more than one.', safe=False)

    responseList = []
    paths = OrderedDict()
    paths['unzip']    = unzip_path
    paths['filename'] = vsiFiles[0]
    responseList.append(paths)

    for image in af.getImageInfo(os.path.join(unzip_path, vsiFiles[0])):
        images = OrderedDict()
        images['identifier'] = image[0]
        images['name'] = image[1]
        responseList.append(images)    
    return JsonResponse(responseList, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def analyseSelectedImages(request):
    """
    This view is used by the frontend module to send to the backend how it has to analyse the image previously sent.

    """
    userId, code = await getUserDetails_fromJWT(request)
    if code == 401:
        return JsonResponse("Analysis Failed - JWT", safe=False)

    reqStr  = JSONParser().parse(request)
    if reqStr['UserId'] != userId:        
        return JsonResponse("Analysis Failed - Auth", safe=False)
    
    parsed_route = os.path.join(reqStr['PhotoFilePath'], "parsed")    

    await af.parseImages(reqStr['SelectedRowsIds'], os.path.join(reqStr['PhotoFilePath'], reqStr['PhotoFileName']), parsed_route)
    
    if (len(reqStr['SelectedRowsIds']) > 0):        
        imageList = af.listFiles(parsed_route, 'ome.tiff')
        zip_path = os.path.join(parsed_route, 'images.zip')
        zip_file = zipfile.ZipFile(zip_path, 'w')
        for image in imageList:
            zip_file.write(os.path.join(parsed_route, image), image)

        zip_file.close()

        res = await requests.post(f'{YOLO_EXECUTOR_URL}/predict', files={'images.zip': open(zip_path, 'rb')})

    new_pollen = OrderedDict()
    new_pollen['AnalysisId'] = reqStr['AnalysisId']
    new_pollen['AnalysisName'] = reqStr['AnalysisName']
    new_pollen['SampleDate'] = reqStr['SampleDate']
    new_pollen['AnalysisDate'] = reqStr['AnalysisDate']
    new_pollen['PhotoFileName'] = reqStr['PhotoFileName']
    new_pollen['PhotoFilePath'] = reqStr['PhotoFilePath']
    new_pollen['UserId'] = reqStr['UserId']
    new_pollen['AnalysisResult']  = res.headers['AnalysisResult']

    polen_serializer = PolenSerializer(data=new_pollen)
    if polen_serializer.is_valid():
        polen_serializer.save()
        return JsonResponse("Analysis Okay", safe=False)
    return JsonResponse("Analysis Failed - Error", safe=False)