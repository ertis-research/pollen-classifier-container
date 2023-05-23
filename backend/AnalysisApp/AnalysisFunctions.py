import cv2
import numpy as np
import javabridge
import bioformats as bf
import os
import zipfile
import asyncio
import subprocess

from DjangoAPI.settings import EXTENSION


def unzipFile(file, directory):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory)

def getImageInfo(input_image):    
    javabridge.attach()

    file_full_path = input_image # Ruta del fichero
    md = bf.get_omexml_metadata(file_full_path) 
    # Lectura de sus metadatos para obtener el ID de las series sin comprimir
    
    ome = bf.OMEXML(md)
    niceImages = []
    for serie in range(ome.get_image_count()):
        # Por cada serie que contenga nuestra imagen
        currentImage = ome.image(serie)

        acquisitionDate = None
        acquisitionDate = currentImage.get_AcquisitionDate() 
        
        if(acquisitionDate != None):
            # Nos quedamos unicamente con las que tengan fecha de captura, es decir, las que son sin comprimir
            
            niceImages.append( (serie, currentImage.get_Name()) )
            # Y almacenamos ese numero de serie en una lista que despues utilizaremos para la conversión
        
    javabridge.detach()
    return niceImages


async def parseImages(imageList, image_directory, output_directory):
    
    for image in imageList:
        stringScript  = os.path.join("bioformats", "bfconvert.") + EXTENSION + ' '
        stringScript += '-overwrite '
        stringScript += '-series '+ str(image) + ' '
        stringScript += '\"'+image_directory+'\" '

        if EXTENSION == 'nt':
            stringScript += '\"' + os.path.join(output_directory, "%%n.ome.tiff") + '\"'
        else:
            stringScript += '\"' + os.path.join(output_directory, "%n.ome.tiff") + '\"'

        # stringScript += '\"'+output_directory+'\\%%n.ome.tiff\"'
        
        # await os.system(stringScript)
        # await sp.create_subprocess_shell(stringScript,stdout=sp.STDOUT,stderr=sp.STDOUT)
        process = await asyncio.create_subprocess_shell(
            stringScript,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        return stdout, stderr

        # print(stringScript)

def listFiles(directory, extension):
    for (_, _, filenames) in os.walk(directory):
        files = []
        for filename in filenames:
            if(filename.endswith('.'+extension)):
                files.append(filename)
        return files

def analyseImage(image_name, image_directory, percentage=0.7):

    print('Image analyzed: '+image_name)

    im = cv2.imread(os.path.join(image_directory, image_name))

    # Splitting image in two different images for each day
    dims = im.shape

    cropped_images = []    
    cropped_images.append(im[0:int(dims[0]*percentage), 0:dims[1]])
    cropped_images.append(im[int(dims[0]*percentage):dims[0], 0:dims[1]])

    # Colors to Filter
    lower_pink  = np.array([135,19,89])
    higher_pink = np.array([179,255,255])

    res = []
    for cp_image in cropped_images: 
        
        # Color filtering
        hsv = cv2.cvtColor(cp_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_pink, higher_pink)
        cv2.bitwise_and(cp_image, cp_image, mask=mask)

        # Noise reduction
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel=kernel, iterations=2)

        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        res.append(len(cnts))

    return res