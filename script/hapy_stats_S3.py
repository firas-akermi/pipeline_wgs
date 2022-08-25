from email.policy import default
import boto3
import botocore
import argparse
import time
import json
import pandas as pd
def formating(input_file,output_file,version,env,date,ref,tool):
    data = pd.read_csv(input_file,index_col=False)
    new_columns={"Category":"Categorie","FNP":"FNp","FNT":"FNt","FPP":"FPp","FPT":"FPt"}
    new_names={"SNP_INDEL_ALL":"SNP_DELINS_ALL","SNP_INDEL_het":"SNP_DELINS_het","SNP_INDEL_homalt":"SNP_DELINS_homalt",
          "SNP_INDEL_hetalt":"SNP_DELINS_hetalt","SNP_INDEL_het_homalt":"SNP_DELINS_het_homalt",
          "INDEL_ALL":"DELINS_ALL","INDEL_het":"DELINS_het","INDEL_homalt":"DELINS_homalt",
           "INDEL_hetalt":"DELINS_hetalt","INDEL_het_homalt":"DELINS_het_homalt"}
    data.rename(columns=new_columns,inplace=True)
    data['Categorie'].replace(new_names,inplace=True)
    data['Version']=[version for i in range(len(data["Categorie"]))]
    data['Environnement']=[env for i in range(len(data["Categorie"]))]
    data['Date']=[date for i in range(len(data["Categorie"]))]
    data['Reference']=[ref for i in range(len(data["Categorie"]))]
    data['Outils']=[tool for i in range(len(data["Categorie"]))]
    data.to_csv(input_file,index=False) 

def download(user,ip_file,file_path2,bucket_name,file_name2):
        boto3.setup_default_session(profile_name="default")
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

def upload(input_file,ip_file,file_path,bucket_name,file_name,file_name2,output_file):
        df=pd.read_csv(file_name2)
        data= pd.read_csv(input_file)
        csv=pd.concat([df,data],sort=False)
        csv.to_csv(output_file,index=False)
        boto3.setup_default_session(profile_name="default")
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
        upload(input_file= args.input,ip_file=args.endpoint,file_path=args.file_path,
                        bucket_name=args.bucket_name,file_name=args.file_name,file_name2=args.file_name2,output_file=args.output)