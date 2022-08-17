import json
import requests
import boto3



region = 'us-east-1' # For example, us-west-1
service = 'es'
host = 'https://search-post1-xx3ised4hmqhtgwx22ar7o5lsa.us-east-1.es.amazonaws.com/' # The OpenSearch domain endpoint with https://
index = 'posts'
url = host + '/' + index + '/_search'


headers = { "Content-Type": "application/json"}

def lambda_handler(event, context):
    # TODO implement
    
    lex_client = boto3.client('lex-runtime')
    
    print ('event: ', json.dumps(event))
    
    '''
    query = event['queryStringParameters']['q']
    
    processed_query1 = lex_client.post_text(
        botName = 'assignment_six_lex',
        botAlias = 'Dev',
        userId = 'cl5522',
        inputText = query
    )
    
    print('lex response: ', processed_query1)
    
    processed_query = processed_query1['slots']['Tag']
    
    
    print('Processed Query: ', processed_query)
    '''
    
    processed_query = event['queryStringParameters']['q']
    
    path = 'https://search-photos-6rvh5ktdd4gqn4pju66j6fdq7i.us-east-1.es.amazonaws.com/photos/_doc/_search?q='
    elasticsearch_client = boto3.client('es')
    tag_idx = 0
    dict_return = {}
    number_of_tags = len(processed_query)
    
    for tag in processed_query:
        
        search_path = path + tag
        
        response = requests.get(search_path, headers=headers, auth=('cloudcomputing', 'Aa12345!'))
        
        test_response = type(response)
        print("tag: ", tag_idx, " type: ", test_response,"\n")
        dict1 = json.loads(response.text)
        
        print("tag: ", tag_idx, "response: ", dict1)
        
        tag_idx += 1
        
        elastic_resp_list = dict1['hits']['hits']
        
        
        for ele in elastic_resp_list:
            object_key = ele['_source']['objectKey']
            if object_key in dict_return:
                dict_return[object_key] += 1
            else:
                dict_return[object_key] = 1
                
    
    print("Dict_Return: ",dict_return)
    
    object_key_list = []
    
    for key in dict_return:
        if dict_return[key] == number_of_tags:
            object_key_list.append(key)
    
    print("Object_Key_List: ", object_key_list)
    
    result = json.dumps({'Successfully Searched': object_key_list})
    
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "multiValueHeaders": {},
        "body": result,
        "isBase64Encoded": False
    }
