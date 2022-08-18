import boto3
import botocore
import argparse
import time
import json
def archive(user,ip_file,file_path,bucket_name,file_name,key):
        boto3.setup_default_session(profile_name=user)
        with open(ip_file, 'r') as f:
                data = json.load(f)
        for adress in data["s3"]:
                try:
                        print('trying ip: {}'.format(adress))
                        s3client = boto3.client('s3', endpoint_url="http://"+adress)
                        s3client.put_object(Bucket = bucket_name, Key= (key))
                        s3client.upload_file(file_path,bucket_name,key+file_name)
                        print('Connected to: {}'.format(adress))
                        break
                except Exception as e:
                        print('Unable to connect to ip: {}...'.format(adress))                    
                        continue
if __name__ == '__main__':
        parser = argparse.ArgumentParser(description = "Python script to copy file to aws s3")
        parser.add_argument("-u","--user", type = str, required= True)
        parser.add_argument("-ip","--endpoint", type = str, required= True)
        parser.add_argument("-f","--file_path", type = str, required= True)
        parser.add_argument("-b","--bucket_name", type = str, required= True)
        parser.add_argument("-n","--file_name", type = str, required= True)
        parser.add_argument("-k","--key", type = str, required= True)

        args = parser.parse_args()
        archive(user= args.user,ip_file=args.endpoint,file_path=args.file_path,
                        bucket_name=args.bucket_name,file_name=args.file_name,key = args.key)
        
                