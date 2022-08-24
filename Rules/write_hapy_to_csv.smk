#!/usr/bin/env python3
# Firas Akermi
rule write_hapy_to_csv:
    input:
        i1= expand("{output_path}/{analysis}/happy/Rapport.html",output_path=output_path,analysis=full_name+Time)
        
    output:
        o =  "{output_path}/{analysis}_happy_csv_done.txt"
    params:
        summary= lambda wildcards:"{}/".format(wildcards.output_path)+"{}/happy/".format(wildcards.analysis)+"{}".format(wildcards.analysis)+".summary.csv",
        script =config["scripts"]["hapy_S3_csv"],
        user = config["S3"]["USER"],
        adress_ip = config["S3"]["IP"],
        Bucket = config["S3"]["Bucket_name"],
        out= lambda wildcards:"{}/{}/happy/out.csv".format(wildcards.output_path,wildcards.analysis),
        version =config["general_information"]["Version"],
        env = config["general_information"]["Environnement"],
        date=config["general_information"]["Date"],
        ref = config["general_information"]["Reference"],
        tool=config["general_information"]["tool"],
        n2= lambda wildcards:"{}/{}/happy/data.csv".format(wildcards.output_path,wildcards.analysis),
        cluster_config=config["general_path"]["INPUT_PATH"]+"/"+"cluster_config/cluster_config.json"

    shell:
        '''
        python3 {params.script} -i {params.summary} -o {params.out} -v {params.version} -e {params.env} -d {params.date} -r {params.ref} -u {params.user} -ip {params.adress_ip} \
        -b {params.Bucket} -c {params.cluster_config} -t {params.tool} -n data.csv -f {params.out} -f2 data.csv -n2 {params.n2} > {output.o}
        '''