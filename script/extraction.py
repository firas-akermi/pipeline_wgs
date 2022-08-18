#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
import argparse
import os
def extract_stat(input,output, scores,variants):
    for out in output:
        with open(out,"a") as outfile:
            outfile.writelines("Category")
            statistic =[]
            for files in input:
                direct = os.path.basename(files).split(".txt")[0]
                docs = os.path.split(files)[0]
                v = os.path.split(docs)[1]              
                with open(files,'r') as f:
                    nb=0
                    for line in f.readlines():
                        nb+=1
                f.close()
                statistic.append(v)
                statistic.append(direct)
                statistic.append(nb)
            for i in scores:
                outfile.writelines(","+i)
            outfile.writelines("\n")
            for elt in variants:
                outfile.writelines(elt) 
                for j in range(len(statistic)):
                    if statistic[j]== elt:
                        outfile.writelines(","+str(statistic[j+2]))
                outfile.writelines("\n")          
        outfile.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Python script to create statistics file")
    parser.add_argument("-i","--input", type = str,nargs='*', required= True)
    parser.add_argument("-o","--output", type =str, nargs='*',required=True)
    parser.add_argument("-s","--score", type =str, nargs='*', required= True)
    parser.add_argument("-v","--variant", type =str, nargs='*',required= True)
    args = parser.parse_args()
    extract_stat(args.input,args.output,args.score, args.variant)
    
