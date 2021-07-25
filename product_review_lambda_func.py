import json
import base64
import boto3
import re

client = boto3.client("comprehend")

pattern = r'[\n\r\t]+'

def lambda_handler(event, context):
    
    output = []
    
    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data'])
        
        payload = json.loads(payload)
        
        review = payload['review_headline'] + '-' + payload['review_body']
        #print(review)
        
        sentiment = client.detect_sentiment(Text=review[:4000], LanguageCode = 'en')
        #print(sentiment['Sentiment'])
        
        payload['sentiment'] = sentiment['Sentiment']
        
        payload = json.dumps(payload, separators=(',',':'))
        
        payload = re.sub(pattern,' ',payload)+'\n'
        payload = payload.encode("ascii")
        output_record = {
                'recordId':record['recordId'],
                'result': 'Ok',
                'data':base64.b64encode(payload)
        }
        output.append(output_record)
    
    return {'records': output}