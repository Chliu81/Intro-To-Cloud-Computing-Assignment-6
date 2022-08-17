import json
import logging 
import boto3
from datetime import datetime
import requests

#Variables

###

###




#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

rekognition_client = boto3.client('rekognition')

def detect_labels(photo, bucket):

    response = rekognition_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=10)

    print('Detected labels for ' + photo) 
    print()   
    labels = []
    for label in response['Labels']:
        labels.append(label['Name'])
    return labels

def lambda_handler(event, context):
    
    print("event: ", event)
    
    # connect to s3 - assuming your creds are all set up and you have boto3 installed
    s3 = boto3.resource('s3')
    
    # identify the bucket - you can use prefix if you know what your bucket name starts with
    #for bucket in s3.buckets.all():
        #print(bucket.name)
        
    
    # get the bucket
    bucket = s3.Bucket('cc-store-photos')
    
    # use loop and count increment
    count_obj = 0
    for i in bucket.objects.all():
        count_obj = count_obj + 1
        
    print('object count: ', count_obj)

    # TODO implement
    records = event['Records']
    for record in records:

        s3object = record['s3']
        bucket = s3object['bucket']['name']
        objectKey = s3object['object']['key']


    print(objectKey, bucket)
    label_array = detect_labels(objectKey, bucket)
    
    now = datetime.now()
    datevar = now.strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "objectKey": objectKey,
        "bucket": bucket,
        "createdTimestamp": datevar,
        "labels": label_array
    }
    
    print('payload: ', payload)
    
    host = 'https://search-photos-6rvh5ktdd4gqn4pju66j6fdq7i.us-east-1.es.amazonaws.com/'
    path = 'photos/_doc/'
    USER = 'cloudcomputing'
    PASS = 'Aa12345!'

    
    url = host+path+str(count_obj)+'/'
    r = requests.post(url, auth=(USER, PASS), json = payload)
    
    print(r.text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
