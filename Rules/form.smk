#!/usr/bin/env python3
# Firas Akermi
rule Mise_en_forme_sous_format_csv:
    input:
       i1=expand("{output_path}/{analysis}/happy/{variant}/{score}.txt",output_path=output_path, analysis = full_name+Time,variant= variants, score = scores),
       i2=rules.Comparaison_des_Haplotypes.output
    output:
        "{output_path}/{analysis}/happy/Statistics.csv",
    params:
        script = config["scripts"]["extract_script"],
        s = config["Variant_Scores"]["Scores"],
        v = config["Variant_Scores"]["Variant"]             
    shell:
        "python3 {params.script} -i {input.i1} -o {output} -s {params.s} -v {params.v}" 
       



       



            
        

    

            


        



        
         
            
                                 
            
            
             
