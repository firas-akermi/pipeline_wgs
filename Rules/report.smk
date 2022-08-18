#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule Analyse_des_resultats_et_generation_du_rapport_html:
    input:
        i="{output_path}/{analysis}/happy/Statistics.csv"
    output:
        o1="{output_path}/{analysis}/happy/Rapport.html",
        o2="{output_path}/{analysis}/happy/"
    params:
        s = config["general_information"]["Sample"],
        d = config["general_information"]["Date"],
        v= config["general_information"]["Version"],
        script= config["scripts"]["create_form"],
        summary= lambda wildcards:"{}/".format(wildcards.output_path)+"{}/happy/".format(wildcards.analysis)+"{}".format(wildcards.analysis)+".summary.csv",
        old_data= config["general_path"]["old_pipelines"],
        old_pipes_v= config["general_path"]["old_pipelines"]

    shell: 
        "python3 {params.script} -i1 {input.i} -i2 {params.summary} -s {params.s} -d {params.d} -v {params.v} -c {params.old_data} -p {params.old_pipes_v} -o {output.o1}"