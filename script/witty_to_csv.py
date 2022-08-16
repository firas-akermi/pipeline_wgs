#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
import json 
import pandas as pd
import argparse
import boto3
def from_json_to_csv(input_file,output_file,version,env,date,ref,tool):
    with open(input_file, 'r') as file:
        data=file.read()
    obj = json.loads(data)
    df=[i['DetailedStats'] for i in obj['PerSampleStats']]
    Variant_stats_event={"VariantType":[],'StatsType':[],"TruthTpCount":[],
              "TruthFnCount":[],"TruthTotalCount":[],"Recall":[],"QueryTpCount":[],"QueryFpCount":[],
               'QueryTotalCount':[],"Precision":[],'Fscore':[]}
    Variant_stats_base={"VariantType":[],'StatsType':[],"TruthTpCount":[],
              "TruthFnCount":[],"TruthTotalCount":[],"Recall":[],"QueryTpCount":[],"QueryFpCount":[],
               'QueryTotalCount':[],"Precision":[],'Fscore':[]}
    varianttype_event=[i['VariantType'] for i in df[0]]
    overall=[i['OverallStats'][0] for i in df[0]]
    base=[i['OverallStats'][1] for i in df[0] if len(i['OverallStats'])>1]
    varianttype_base= [e for e in varianttype_event if e not in ('Insertion',
                                                             'IntraChromosomeBreakend', 
                                                             'Inversion', 
                                                             'TranslocationBreakend')]
    for i, j in zip(varianttype_event, overall):
        Variant_stats_event['VariantType'].append(i)
        Variant_stats_event['StatsType'].append(j['StatsType'])
        Variant_stats_event['TruthTpCount'].append(j['TruthTpCount'])
        Variant_stats_event['TruthFnCount'].append(j['TruthFnCount'])
        Variant_stats_event['TruthTotalCount'].append(j['TruthTotalCount'])
        Variant_stats_event['Recall'].append(j['Recall'])
        Variant_stats_event['QueryTpCount'].append(j['QueryTpCount'])
        Variant_stats_event['QueryFpCount'].append(j['QueryFpCount'])
        Variant_stats_event['QueryTotalCount'].append(j['QueryTotalCount'])
        Variant_stats_event['Precision'].append(j['Precision'])
        Variant_stats_event['Fscore'].append(j['Fscore'])
    for i, j in zip(varianttype_base, base):
        Variant_stats_base['VariantType'].append(i)
        Variant_stats_base['StatsType'].append(j['StatsType'])
        Variant_stats_base['TruthTpCount'].append(j['TruthTpCount'])
        Variant_stats_base['TruthFnCount'].append(j['TruthFnCount'])
        Variant_stats_base['TruthTotalCount'].append(j['TruthTotalCount'])
        Variant_stats_base['Recall'].append(j['Recall'])
        Variant_stats_base['QueryTpCount'].append(j['QueryTpCount'])
        Variant_stats_base['QueryFpCount'].append(j['QueryFpCount'])
        Variant_stats_base['QueryTotalCount'].append(j['QueryTotalCount'])
        Variant_stats_base['Precision'].append(j['Precision'])
        Variant_stats_base['Fscore'].append(j['Fscore'])
    df_event=pd.DataFrame.from_dict(Variant_stats_event)
    df_base=pd.DataFrame.from_dict(Variant_stats_base)
    df_event=df_event.astype({'Recall': 'float32','Precision':'float32',"Fscore":"float32"})
    df_base=df_base.astype({'Recall': 'float32','Precision':'float32',"Fscore":"float32"})
    df_event=df_event.fillna(0)
    df_base=df_base.fillna(0)
    df_event.drop(columns=['StatsType',"QueryTpCount"],axis=1,inplace=True)
    df_base.drop(columns=['StatsType',"QueryTpCount"],axis=1,inplace=True)
    new_cols = ["VariantType","TruthTpCount","TruthFnCount","TruthTotalCount","QueryFpCount",
                "QueryTotalCount","Precision","Fscore","Recall"]
    df_event=df_event.reindex(columns=new_cols)
    df_base=df_base.reindex(columns=new_cols)
    New_name={'VariantType':'Categorie','TruthTotalCount':'Total.Standard','TruthTpCount':'VP.Standard','TruthFnCount':'FN.Standard',
         'QueryTotalCount':'Total.Ech','QueryFpCount':'FP.Ech','Recall':'Rappel','Precision':"Precision",
         'Fscore':'Fscore'}
    df_event=df_event.rename(columns=New_name)
    df_base=df_base.rename(columns=New_name)
    df_event['Version']=list((version,) * len(df_event['Categorie'].values))
    df_event['Environnement']=list((env,) * len(df_event['Categorie'].values))
    df_event['Date']=list((date,) * len(df_event['Categorie'].values))
    df_event['Reference']=list((ref,) * len(df_event['Categorie'].values))
    df_event['Outils']=list((tool,) * len(df_event['Categorie'].values))
    df_event.reset_index(inplace=True)
    df_event.drop(['index'],axis=1,inplace=True)
    df_base['Version']=list((version,) * len(df_base['Categorie'].values))
    df_base['Environnement']=list((env,) * len(df_base['Categorie'].values))
    df_base['Date']=list((date,) * len(df_base['Categorie'].values))
    df_base['Reference']=list((ref,) * len(df_base['Categorie'].values))
    df_base['Outils']=list((tool,) * len(df_base['Categorie'].values))
    df_base.reset_index(inplace=True)
    df_base.drop(['index'],axis=1,inplace=True)
    df_event.to_csv(output_file,index=False)
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
        from_json_to_csv(args.input,args.output,args.version,
                        args.env,args.date,args.ref,args.tool)
        download(user= args.user,ip_file=args.endpoint,file_path2=args.file_path2,
                        bucket_name=args.bucket_name,file_name2=args.file_name2)
        upload(user= args.user,ip_file=args.endpoint,file_path=args.file_path,
                        bucket_name=args.bucket_name,file_name=args.file_name,file_name2=args.file_name2,output_file=args.output)