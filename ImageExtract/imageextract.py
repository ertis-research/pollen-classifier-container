import numpy as np
import os, zipfile, re
import bioformats as bf
import javabridge
import typer

def start_java():
    # Start CellProfiler's JVM via Javabridge   

    javabridge.start_vm(class_path=bf.JARS, max_heap_size='6G') # Sobremesa "ps3aj"
    javabridge.attach()

    """
    # This is so that Javabridge doesn't spill out a lot of DEBUG messages during runtime. From CellProfiler/python-bioformats.
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger", "ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory", "getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level", "WARN", "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel)
    """
    
def stop_java():
    javabridge.detach()
    javabridge.kill_vm()

def unzipFile(file, directory):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory)

def listFiles(directory, extension):
    for (_, _, filenames) in os.walk(directory):
        files = []
        for filename in filenames:
            if(filename.endswith('.'+extension)):
                files.append(filename)
        return files

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
            total_pixel = currentImage.Pixels.get_SizeX()*currentImage.Pixels.get_SizeY()
            niceImages.append((serie, currentImage.get_Name(), total_pixel))
            # Y almacenamos ese numero de serie en una lista que despues utilizaremos para la conversión
        
    javabridge.detach()
    return niceImages


def parseImages(imageList, image_directory, output_directory, regex_filter, tam_filter):
    try:
        max_pixel_amount = int(tam_filter)
    except:
        max_pixel_amount = max([image[2] for image in imageList])
        
    for image in imageList:
        if (regex_filter == "" or re.match(regex_filter, image[1])) and image[2] >= max_pixel_amount:
            stringScript  = '../bioformats/bfconvert '
            stringScript += '-overwrite '
            stringScript += '-series '+ str(image[0]) + ' '
            stringScript += '\"'+image_directory+'\" '
            stringScript += '\"'+output_directory+'/%n.ome.tiff\"'
            os.system(stringScript)
            print(stringScript)

def compressImages(zipname):
    zf = zipfile.ZipFile(zipname+".zip", "w")
    for dirname, subdirs, files in os.walk("images"):
        for filename in files:
            print("images/"+filename)
            zf.write("images/"+filename, filename)
    zf.close()

def imageExtract(filePath: str = typer.Option(..., help = "Path to the images"),
                 fileExtension: str = typer.Option(..., help = "Microscope file extension"),
                 imagename_regex: str = typer.Option(..., help = "Image Name filter by Regular Expression"),
                 min_image_size: str = typer.Option(..., help = "Image filter by size")): 

    os.chdir("data")

    directory = "vsi"

    unzipFile(filePath, directory)
    vsiFiles = listFiles(directory, fileExtension)

    vsiFile = vsiFiles[0]
    
    start_java()
    
    selectedImages = [x for x in getImageInfo(directory+"/"+vsiFile)]

    parseImages(selectedImages, directory+"/"+vsiFile, "images", imagename_regex, min_image_size)
    
    stop_java()

    compressImages("imagesZipped")


if __name__ == '__main__':
    typer.run(imageExtract)