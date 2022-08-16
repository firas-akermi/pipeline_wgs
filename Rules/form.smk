#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule Mise_en_forme_sous_format_csv:
    input:
       expand("{output_path}/{analysis}/happy/{variant}/{score}.txt",output_path=output_path, analysis = full_name,variant= variants, score = scores)
    output:
        "{output_path}/{analysis}/happy/Statistics.csv",
    params:
        script = config["scripts"]["extract_script"],
        s = config["Variant_Scores"]["Scores"],
        v = config["Variant_Scores"]["Variant"]             
    shell:
        "python3 {params.script} -i {input} -o {output} -s {params.s} -v {params.v}" 
       



       



            
        

    

            


        



        
         
            
                                 
            
            
             
