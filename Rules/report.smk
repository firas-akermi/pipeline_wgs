#!/usr/bin/env python3
# Firas Akermi
rule Analyse_des_resultats_et_generation_du_rapport_html:
    input:
        i="{output_path}/{analysis}/happy/Statistics.csv"
    output:
        o1="{output_path}/{analysis}/happy/Rapport.html"
    params:
        s = config["general_information"]["Sample"],
        d = config["general_information"]["Date"],
        script= config["scripts"]["create_form"],
        summary= lambda wildcards:"{}/".format(wildcards.output_path)+"{}/happy/".format(wildcards.analysis)+"{}".format(wildcards.analysis)+".summary.csv",
        v=config["general_information"]["Version"]
    shell: 
        "python3 {params.script} -i1 {input.i} -i2 {params.summary} -s {params.s} -d {params.d} -v {params.v}  -o {output.o1}"
