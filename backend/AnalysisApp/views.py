
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.core.files.storage import default_storage

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import jwt
import httpx
import zipfile
from pathlib import Path

import asyncio
from adrf.decorators import api_view 
from asgiref.sync import sync_to_async

from DjangoAPI.settings import SECRET_KEY, YOLO_EXECUTOR_URL

from AnalysisApp.models import Polen
from AnalysisApp.serializers import PolenSerializer

import AnalysisApp.AnalysisFunctions as af

import os
import numpy as np
from datetime import datetime

async def getUserDetails_fromJWT(request):
    jwt_token = request.META['HTTP_AUTHORIZATION'][len("Bearer "):]
    jwt_token_decoded = jwt.decode(str(jwt_token), SECRET_KEY, algorithms="HS256")

    UserId = jwt_token_decoded['user_id']
    username = jwt_token_decoded['username']
    email = jwt_token_decoded['email']
    
    try:
        await User.objects.aget(id=UserId, username = username, email = email)
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
        polen = await sync_to_async(list)(Polen.objects.filter(UserId=user))
        
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

    paths = {
        'unzip': unzip_path,
        'filename': vsiFiles[0]
    }

    responseList.append(paths)

    for image in af.getImageInfo(os.path.join(unzip_path, vsiFiles[0])):
        images = {
            'identifier': image[0],
            'name': image[1]
        }
        responseList.append(images)    
    return JsonResponse(responseList, safe=False)


async def saveParsedImages(selected_row_ids, reqStr, parsed_route):
    await af.parseImages(selected_row_ids, os.path.join(reqStr['PhotoFilePath'], reqStr['PhotoFileName']), parsed_route)
    
    if (len(selected_row_ids) > 0):        
        imageList = af.listFiles(parsed_route, 'ome.tiff')
        zip_path = os.path.join(parsed_route, 'images.zip')
        zip_file = zipfile.ZipFile(zip_path, 'w')
        for image in imageList:
            zip_file.write(os.path.join(parsed_route, image), image)

        zip_file.close()

        async with httpx.AsyncClient() as client:
            res = await client.post(f'{YOLO_EXECUTOR_URL}/predict', files={'file': open(zip_path, 'rb')}, timeout=None)
        
        polen_user = await User.objects.aget(id=reqStr['UserId'])

        new_pollen = {
            # 'AnalysisId': reqStr['UserId'],
            'UserId': polen_user,
            'AnalysisName': reqStr['AnalysisName'],
            'AnalysisDate': datetime.strptime(reqStr['AnalysisDate'], '%Y-%m-%d').date(),
            'SampleDate': datetime.strptime(reqStr['SampleDate'], '%Y-%m-%d').date(),
            'PhotoFileName': reqStr['PhotoFileName'],
            'PhotoFilePath': reqStr['PhotoFilePath'],
            'AnalysisResult': res.headers['pollen_count_report']
        }

        created_polen = await Polen.objects.acreate(**new_pollen)




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

    asyncio.get_event_loop().create_task(saveParsedImages(reqStr['SelectedRowsIds'], reqStr, parsed_route))
    
    return JsonResponse("Analysis request accepted", safe=False)