import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.tools import make_subplots
import argparse
def create_report(input1,input2,Sample,Date,Version,output):           
    
        data = pd.read_table(input1,sep=",")
        fig =make_subplots(rows = 3, cols = 3)
        fig.add_trace(go.Bar(x=data['Category'], y=data['TP'],name='TP'),row=1,col=1)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FN'],name='FN'),row=1,col=2)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FP'],name='FP'),row=1,col=3)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FNP'],name='FNP'),row=2,col=1)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FNT'],name='FNT'),row=2,col=2)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FPP'],name='FPP'),row=2,col=3)
        fig.add_trace(go.Bar(x=data['Category'], y=data['FPT'],name='FPT'),row=3,col=1)
        plt_div = plot(fig, output_type='div')
        data_to_html= data.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')
        data2=pd.read_table(input2,sep=",")
        data2=data2[["Type","Filter","TRUTH.TOTAL","TRUTH.TP","TRUTH.FN","QUERY.TOTAL","QUERY.FP" ,"QUERY.UNK",
                     "METRIC.Recall","METRIC.Precision","METRIC.F1_Score"]]
        data2=data2[data2.Filter!='ALL']
        fig2=make_subplots(rows =1 , cols = 3)
        fig2.add_trace(go.Bar(x=data2['Type'], y=data2['METRIC.Precision'],name='METRIC.Precision'),row=1,col=1)
        fig2.add_trace(go.Bar(x=data2['Type'], y=data2['METRIC.Recall'],name='METRIC.Recall'),row=1,col=2)
        fig2.add_trace(go.Bar(x=data2['Type'], y=data2['METRIC.F1_Score'],name='METRIC.F1_Score'),row=1,col=3)
        plt_div_2 = plot(fig2, output_type='div')
        data2_to_html= data2.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">')
        html_string = '''
        <html>
                <head>
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                        <style>body{ margin:0 100; background:whitesmoke; }</style>
                </head>
                <body>
                <h1>Variant calling benchmarking summary</h1>
                <h1> Sample Name : '''+Sample + '''</h1>
                <h2>Date : '''+Date+'''</h2>
                <h2>Pipeline Version : '''+Version+'''</h2>
                <h3>Summary Table</h3>
                '''+ data2_to_html + '''
                <h3>Metrics Bar Plots</h3>
                '''+ plt_div_2 + '''
                <h3>detailed Table</h3>
                '''+ data_to_html + '''
                <h3>Parameteres Bar Plots</h3>
                '''+ plt_div + '''
                </body>
        </html>'''
        with open(output,"w") as out:
                out.write(html_string)
        out.close()
def old_vs_new(input1,pipeline_version,output):
    dic ={"Pipeline":[],"Type":[],"METRIC.Precision":[],"METRIC.Recall":[],"METRIC.F1_Score":[]}
    for file,version in zip(input1,pipeline_version):
        data2=pd.read_table(file)
        data2=data2[data2.Filter!='ALL']
        data2=data2[["Type","Filter","TRUTH.TOTAL","TRUTH.TP","TRUTH.FN","QUERY.TOTAL","QUERY.FP" ,"QUERY.UNK",
                     "METRIC.Recall","METRIC.Precision","METRIC.F1_Score"]]
        for j in data2["Type"]:
            dic["Type"].append(j)
            dic["Pipeline"].append(version)
            
        for k in data2['METRIC.Precision']:
            dic["METRIC.Precision"].append(k)
        for l in data2['METRIC.Recall']:
            dic["METRIC.Recall"].append(l)
        for n in data2['METRIC.F1_Score']:
            dic["METRIC.F1_Score"].append(n)
    df=pd.DataFrame(dic)
    df2=df[df.Type=='SNP']
    df=df[df.Type=='INDEL']
    df.reset_index(inplace=True)
    df2.reset_index(inplace=True)
    print(df)
    def loss(colname):
        loss_gain={"loss_precision":[],
               "gain_precision":[]
              }
        for v in range(len(colname)-1):
            if colname.values[v] == colname.values[v+1]:
                loss_gain['loss_precision'].append(0)
                loss_gain['gain_precision'].append(0)
            if colname.values[v]> colname.values[v+1]:
                loss_gain['loss_precision'].append(0)   
                loss_gain['loss_precision'].append(colname.values[v] - colname.values[v+1])
                loss_gain['gain_precision'].append(0)
            elif colname.values[v] < colname.values[v+1]:
                loss_gain['gain_precision'].append(0)   
                loss_gain['gain_precision'].append(colname.values[v+1] - colname.values[v])
                loss_gain['loss_precision'].append(0)
        return loss_gain
    
    p = pd.DataFrame.from_dict(loss(df["METRIC.Precision"]),orient='index')
    p= p.transpose()
    print(p)
    r = pd.DataFrame.from_dict(loss(df["METRIC.Recall"]),orient='index')
    r= r.transpose()
    f1 = pd.DataFrame.from_dict(loss(df["METRIC.F1_Score"]),orient='index')
    f1= f1.transpose()
    texte1=[]
    texte1_2=[]
    for i,j,k in zip(df["METRIC.Precision"],p["gain_precision"],p["loss_precision"]):
        texte1.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte1_2.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    print(texte1_2)
    texte2=[]
    texte2_2=[]
    for i,j,k in zip(df["METRIC.Recall"],r["gain_precision"],r["loss_precision"]):
        texte2.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte2_2.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    texte3=[]
    texte3_2=[]
    for i,j,k in zip(df["METRIC.F1_Score"],f1["gain_precision"],f1["loss_precision"]):
        texte3.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte3_2.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    fig = make_subplots(rows = 1, cols = 3,shared_yaxes=True,subplot_titles=('Précision', 
                                                           'Sensibilité',
                                                           'Score F1'),
                        horizontal_spacing = 0.15)
    
    fig.add_trace(go.Bar(x=df["METRIC.Precision"], y=df["Pipeline"],name="Valeur",orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df["METRIC.Precision"]-p["gain_precision"],legendgroup="group1",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman",color='black'),showlegend=True),row=1,col=1)
    #gain prec
    fig.add_trace(go.Bar(x=p["gain_precision"], y=df["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte1, 
                         textposition='inside',                                                    
                         hovertext=p["gain_precision"],legendgroup="group2",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=True,
                         base=df["METRIC.Precision"]-p["gain_precision"]),row=1,col=1)
    #loss_prec
    fig.add_trace(go.Bar(x=p["loss_precision"], y=df["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte1_2,  
                         textposition='inside',                                                        
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df["METRIC.Precision"]-p["gain_precision"],opacity=0.8),row=1,col=1)
    #recall
    fig.add_trace(go.Bar(x=df["METRIC.Recall"], y=df["Pipeline"],orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df["METRIC.Recall"]-r["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False),row=1,col=2)
   #gain recall
    fig.add_trace(go.Bar(x=r["gain_precision"], y=df["Pipeline"],
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte2,
                         textposition='inside',
                         hovertext=r["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df["METRIC.Recall"]-r["gain_precision"]),row=1,col=2)
    #loss_recall
    fig.add_trace(go.Bar(x=r["loss_precision"], y=df["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte2_2, 
                         textposition='inside',                                                         
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df["METRIC.Recall"]-r["gain_precision"],opacity=0.8),row=1,col=2)
    #f1
    fig.add_trace(go.Bar(x=df["METRIC.F1_Score"], y=df["Pipeline"],orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df["METRIC.F1_Score"]-f1["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False),row=1,col=3)
    
     #gain f1                       
    fig.add_trace(go.Bar(x=f1["gain_precision"], y=df["Pipeline"],
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte3,
                         textposition='inside',
                         hovertext=f1["gain_precision"], legendgroup="group2",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df["METRIC.F1_Score"]-f1["gain_precision"]),row=1,col=3)
    #loss_f1
    fig.add_trace(go.Bar(x=f1["loss_precision"], y=df["Pipeline"], name ='Delta',
                         width=0.5,
                         
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte3_2,                                                          
                         textposition='inside',
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df["METRIC.F1_Score"]-f1["gain_precision"],opacity=0.8),row=1,col=3)
                         
    fig.layout["xaxis1"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson' )
    fig.layout["xaxis2"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson')
    fig.layout["xaxis3"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson')
    fig.layout["yaxis1"].update(tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson' )
    #fig.layout["yaxis2"].update(tickangle=45,ticks="outside", 
    #                            tickwidth=1, tickcolor='crimson')
    #fig.layout["yaxis3"].update(tickangle=45,ticks="outside", 
    #                            tickwidth=1, tickcolor='crimson')
    fig['layout']['xaxis']['title']='Valeur'
    fig['layout']['yaxis']['title']='Version'
    fig['layout']['xaxis2']['title']='Valeur'
    #fig['layout']['yaxis2']['title']='Version'
    fig['layout']['xaxis3']['title']='Valeur'
    #fig['layout']['yaxis3']['title']='Version'
    fig.layout.update( width = 1500, height = 600, barmode='relative',hovermode= "y",
                     title='INDEL')
    plt_div= plot(fig, output_type='div')
    
    p_snp = pd.DataFrame.from_dict(loss(df2["METRIC.Precision"]),orient='index')
    p_snp= p_snp.transpose()
    print(p_snp)
    r_snp = pd.DataFrame.from_dict(loss(df2["METRIC.Recall"]),orient='index')
    r_snp= r_snp.transpose()
    f1_snp = pd.DataFrame.from_dict(loss(df2["METRIC.F1_Score"]),orient='index')
    f1_snp= f1_snp.transpose()
    texte1_snp=[]
    texte1_2_snp=[]
    for i,j,k in zip(df2["METRIC.Precision"],p_snp["gain_precision"],p_snp["loss_precision"]):
        texte1_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte1_2_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    print(texte1_2_snp)
    texte2_snp=[]
    texte2_2_snp=[]
    for i,j,k in zip(df2["METRIC.Recall"],r_snp["gain_precision"],r_snp["loss_precision"]):
        texte2_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte2_2_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    texte3_snp=[]
    texte3_2_snp=[]
    for i,j,k in zip(df2["METRIC.F1_Score"],f1_snp["gain_precision"],f1_snp["loss_precision"]):
        texte3_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(j,8))+'</b>')
        texte3_2_snp.append('<b>'+"Valeur:{},Delta:{}".format(round(i,8),round(-k,8))+'</b>')
    fig2 = make_subplots(rows = 1, cols = 3,shared_yaxes=True,subplot_titles=('Précision', 
                                                           'Sensibilité',
                                                           'Score F1'),
                        horizontal_spacing = 0.15)
    
    fig2.add_trace(go.Bar(x=df2["METRIC.Precision"], y=df2["Pipeline"],name="Valeur",orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df2["METRIC.Precision"]-p_snp["gain_precision"],legendgroup="group1",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman",color='black'),showlegend=True),row=1,col=1)
    #gain prec
    fig2.add_trace(go.Bar(x=p_snp["gain_precision"], y=df2["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte1_snp, 
                         textposition='inside',                                                    
                         hovertext=p_snp["gain_precision"],legendgroup="group2",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=True,
                         base=df2["METRIC.Precision"]-p_snp["gain_precision"]),row=1,col=1)
    #loss_prec
    fig2.add_trace(go.Bar(x=p_snp["loss_precision"], y=df2["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte1_2_snp,  
                         textposition='inside',                                                        
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df2["METRIC.Precision"]-p_snp["gain_precision"],opacity=0.8),row=1,col=1)
    #recall
    fig2.add_trace(go.Bar(x=df2["METRIC.Recall"], y=df2["Pipeline"],orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df2["METRIC.Recall"]-r_snp["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False),row=1,col=2)
   #gain recall
    fig2.add_trace(go.Bar(x=r_snp["gain_precision"], y=df2["Pipeline"],
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte2_snp,
                         textposition='inside',
                         hovertext=r_snp["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df2["METRIC.Recall"]-r_snp["gain_precision"]),row=1,col=2)
    #loss_recall
    fig2.add_trace(go.Bar(x=r_snp["loss_precision"], y=df2["Pipeline"], name ='Delta',
                         width=0.5,
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte2_2_snp, 
                         textposition='inside',                                                         
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df2["METRIC.Recall"]-r_snp["gain_precision"],opacity=0.8),row=1,col=2)
    #f1
    fig2.add_trace(go.Bar(x=df2["METRIC.F1_Score"], y=df2["Pipeline"],orientation="h",
                         width=0.5,
                         marker=dict(color='darkturquoise',line=dict(width=2, color='black')),
                         hovertext=df2["METRIC.F1_Score"]-f1_snp["gain_precision"],
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False),row=1,col=3)
    
     #gain f1                       
    fig2.add_trace(go.Bar(x=f1_snp["gain_precision"], y=df2["Pipeline"],
                         width=0.5,
                         marker=dict(color='aquamarine',line=dict(width=1, color='black')),orientation="h",
                         text=texte3_snp,
                         textposition='inside',
                         hovertext=f1_snp["gain_precision"], legendgroup="group2",
                         hoverinfo='text',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df2["METRIC.F1_Score"]-f1_snp["gain_precision"]),row=1,col=3)
    #loss_f1
    fig2.add_trace(go.Bar(x=f1_snp["loss_precision"], y=df2["Pipeline"], name ='Delta',
                         width=0.5,
                         
                         marker=dict(color='white',opacity=0.4,line=dict(width=0.5, color='red')),orientation="h",
                         text=texte3_2_snp,                                                          
                         textposition='inside',
                         legendgroup="group2",
                         hoverinfo='skip',textfont=dict(size=14,family="Times New Roman", color='black'),showlegend=False,
                         base=df2["METRIC.F1_Score"]-f1_snp["gain_precision"],opacity=0.8),row=1,col=3)
                         
    fig2.layout["xaxis1"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson' )
    fig2.layout["xaxis2"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson')
    fig2.layout["xaxis3"].update(type="log",tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson')
    fig2.layout["yaxis1"].update(tickangle=45,ticks="outside", 
                                tickwidth=1, tickcolor='crimson' )
    #fig2.layout["yaxis2"].update(tickangle=45,ticks="outside", 
    #                            tickwidth=1, tickcolor='crimson')
    #fig2.layout["yaxis3"].update(tickangle=45,ticks="outside", 
    #                            tickwidth=1, tickcolor='crimson')
    fig2['layout']['xaxis']['title']='Valeur'
    fig2['layout']['yaxis']['title']='Version'
    fig2['layout']['xaxis2']['title']='Valeur'
    #fig2['layout']['yaxis2']['title']='Version'
    fig2['layout']['xaxis3']['title']='Valeur'
    #fig2['layout']['yaxis3']['title']='Version'
    fig2.layout.update( width = 1500, height = 600, barmode='relative',hovermode= "y",
                     title='SNP')
    plt_div2= plot(fig2, output_type='div')
    html_string = '''
        <html>
                <head>
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                        <style>body{ margin:0 100; background:whitesmoke; }</style>
                </head>
                <body>
                <h3>Comparaison des versions du pipeline WGS-C, Maladies Rares</h3>
                '''+ plt_div + '''
                 <h4></h4>
                '''+ plt_div2 + '''
                </body>
        </html>'''
    with open(output,"a") as out:
        out.write(html_string)
    out.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Python script to create config file")
    parser.add_argument("-i1","--first_input_path", type = str, required= True)
    parser.add_argument("-i2","--second_input_path", type = str, required= True)
    parser.add_argument("-c", "--CSVs_path",type=str,nargs="+",required=True)
    parser.add_argument("-s","--Sample", type =str,required= True)
    parser.add_argument("-d","--Date", type =str,required= True)
    parser.add_argument("-v","--Version", type =str,required= True)
    parser.add_argument("-p","--pipeline_version",type=str, nargs="+",required=True)
    parser.add_argument("-o","--output_path", type =str, required= True)
    args = parser.parse_args()
    create_report(args.first_input_path,args.second_input_path,args.Sample,args.Date,args.Version,args.output_path)
    old_vs_new(args.CSVs_path,args.pipeline_version,args.output_path)