from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from azure.BlobStorage import BlobStorage

from array import array
import os
from PIL import Image
import sys
import time

import re
import json
import tqdm

subscription_key = "3d15d6dcd38a4481b760e63b4cfd6992" 
end_point = "https://cog-vision-dane-modsfc.cognitiveservices.azure.com/"
LOCAL_PATH = "/home/administrador/output-facebook/"

def get_id_file(text):
    #e.g. profile_100002422389615_pic_20211130.jpg
    found = None
    m = re.search('profile_(.+?)_pic', text)
    if m:
        found = m.group(1)
    return found

def get_date_file(text):
    #e.g. profile_100002422389615_pic_20211130.jpg
    found = None
    m = re.search('pic_(.+?).jpg', text)
    if m:
        found = m.group(1)
    return found


def analyze_faces(client, url_face, verbose=False):
    # Detect faces, gender, age and if is a celebrity    
    # Features
    remote_image_features = ["faces"]    
    detect_faces_results_remote = client.analyze_image(url_face, 
                                                       remote_image_features,
                                                       details=["celebrities"])
    results = []
    for face in detect_faces_results_remote.faces:
        results.append({"gender" : str(face.gender.name), "age":face.age})
    celebrities = []
    if len(detect_faces_results_remote.categories) > 0:
        if hasattr(detect_faces_results_remote.categories[0].detail, 'celebrities'):
            for celebrity in detect_faces_results_remote.categories[0].detail.celebrities:        
                celebrities.append(celebrity.name)

    if verbose:
        print("Rostros encontrados en la imagen: ")
        if (len(detect_faces_results_remote.faces) == 0):
            print("No se encontraron rostros")
        else:        
            print(f"{len(results)} faces: ", results)

    return {"faces" : results, "celebrities" : celebrities}

if __name__ == "__main__":
    #1.1 Set connection to the blob storage
    conf_param_azure = json.load(open('./azure/config_blob.json', 'r'))
    CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net'.format(
                            conf_param_azure['STORAGEACCOUNTNAME'], 
                            conf_param_azure['STORAGEACCOUNTKEY'])
    blobs = BlobStorage(CONNECTION_STRING, 
                        conf_param_azure['CONTAINERNAME'])
    #1.2 Set connetcion to Cognitive Computer Vision API
    vision_client = ComputerVisionClient(end_point, CognitiveServicesCredentials(subscription_key))

    #2. Get files url from Blob Storage
    files = blobs.ls_files(conf_param_azure['BLOBNAME-IMAGES'], recursive = True)
    print("Images: {}".format(files))
    # https://dlsdanemodsfc.blob.core.windows.net/socialnetworks-data/fb_profiles_images/profile_100002422389615_pic_20211130.jpg
    IMAGE_URL = "https://{}.blob.core.windows.net/{}/{}/".format(
        conf_param_azure['STORAGEACCOUNTNAME'],
        conf_param_azure['CONTAINERNAME'],
        conf_param_azure['BLOBNAME-IMAGES'])
    sas_token = blobs.create_sas_token()
    for f in files: # For each image
        #3. Analyze image content (faces)
        url_blob_sas = "{}{}?{}".format(IMAGE_URL, f, sas_token)
        print("Analizye image {}".format(url_blob_sas))        
        data_pic = analyze_faces(vision_client, url_blob_sas, verbose=True)
        data_pic['author_id'] = get_id_file(f)
        data_pic['_date'] = get_date_file(f)
        print(data_pic)
        #4. Save data from image
        print("Saving local")
        #filename = "{}{}_cv_data.json".format(LOCAL_PATH, f)
        filename = "{}{}_cv_data.json".format("", f)
        with open(filename, 'w') as fp:
            json.dump(data_pic, fp) 
        print("Saving in Blob storage")
        dest = "{}/{}_cv_data.json".format(conf_param_azure['BLOBNAME-IMAGES-CONTENT'], f)
        blobs.upload_file(filename, dest)


