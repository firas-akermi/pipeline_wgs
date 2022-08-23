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
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Python script to create config file")
    parser.add_argument("-i1","--first_input_path", type = str, required= True)
    parser.add_argument("-i2","--second_input_path", type = str, required= True)
    parser.add_argument("-s","--Sample", type =str,required= True)
    parser.add_argument("-d","--Date", type =str,required= True)
    parser.add_argument("-o","--output_path", type =str, required= True)
    parser.add_argument("-v","--version", type =str, required= True)

    args = parser.parse_args()
    create_report(args.first_input_path,args.second_input_path,args.Sample,args.Date,args.version,args.output_path)
