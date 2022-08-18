import boto3
import botocore
import argparse
import time
import json
import pandas as pd
def formating(input_file,output_file,version,env,date,ref,tool):
    data = pd.read_csv(input_file)
    data = data[data['Filter']=='PASS']
    data =data[["Type","TRUTH.TOTAL","TRUTH.TP","TRUTH.FN","QUERY.TOTAL","QUERY.FP",
                     "METRIC.Recall","METRIC.Precision","METRIC.F1_Score"]]
    data['Version']=[version,version]
    data['Environnement']=[env,env]
    data['Date']=[date,date]
    data['Reference']=[ref,ref]
    data['Outils']=[tool,tool]
    data.reset_index(inplace=True)
    data.drop(['index'],axis=1,inplace=True)
    New_name={'Type':'Categorie','TRUTH.TOTAL':'Total.Standard','TRUTH.TP':'VP.Standard','TRUTH.FN':'FN.Standard',
         'QUERY.TOTAL':'Total.Ech','QUERY.FP':'FP.Ech','METRIC.Recall':'Rappel','METRIC.Precision':"Precision",
         'METRIC.F1_Score':'Fscore'}
    data=data.rename(columns=New_name) 
    data.to_csv(output_file,index=False) 

def download(user,ip_file,file_path2,bucket_name,file_name2):
        boto3.setup_default_session(profile_name=user)
        with open(ip_file, 'r') as f:
                data = json.load(f)
        for adress in data["s3"]:
                try:
                        print('trying ip: {}'.format(adress))
                        s3client = boto3.client('s3', endpoint_url="http://"+adress)
                        
                        s3client.download_file(bucket_name,file_path2,file_name2)
                        print("Download succeded")
                        break
                except botocore.exceptions.ReadTimeoutError as error:                    
                        continue
def upload(user,ip_file,file_path,bucket_name,file_name,file_name2,output_file):
        df=pd.read_csv(file_name2)
        data= pd.read_csv(file_path)
        csv=pd.concat([df,data],sort=False)
        csv.to_csv(output_file,index=False)
        boto3.setup_default_session(profile_name=user)
        with open(ip_file, 'r') as f:
                data = json.load(f)
        for adress in data["s3"]:
                try:
                        print('trying ip: {}'.format(adress))
                        s3client = boto3.client('s3', endpoint_url="http://"+adress)
                        
                        s3client.upload_file(file_path,bucket_name,file_name)
                        print("Upload succeded")
                        break
                except botocore.exceptions.ReadTimeoutError as error:                    
                        continue
if __name__ == '__main__':
        parser = argparse.ArgumentParser(description = "Python script to edit file to aws s3")
        parser.add_argument("-i","--input", type = str, required= True)
        parser.add_argument("-o","--output", type = str, required= True)
        parser.add_argument("-v","--version", type = str, required= True)
        parser.add_argument("-e","--env", type = str, required= True)
        parser.add_argument("-d","--date", type = str, required= True)
        parser.add_argument("-r","--ref", type = str, required= True)
        parser.add_argument("-t","--tool", type = str, required= True)
        parser.add_argument("-u","--user", type = str, required= True)
        parser.add_argument("-ip","--endpoint", type = str, required= True)
        parser.add_argument("-f","--file_path", type = str, required= True)
        parser.add_argument("-b","--bucket_name", type = str, required= True)
        parser.add_argument("-n","--file_name", type = str, required= True)
        parser.add_argument("-f2","--file_path2", type = str, required= True)
        parser.add_argument("-n2","--file_name2", type = str, required= True)
        args = parser.parse_args()
        formating(args.input,args.output,args.version,
                        args.env,args.date,args.ref,args.tool)
        download(user= args.user,ip_file=args.endpoint,file_path2=args.file_path2,
                        bucket_name=args.bucket_name,file_name2=args.file_name2)
        upload(user= args.user,ip_file=args.endpoint,file_path=args.file_path,
                        bucket_name=args.bucket_name,file_name=args.file_name,file_name2=args.file_name2,output_file=args.output)