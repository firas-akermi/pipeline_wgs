#!/usr/bin/env python3
# Firas Akermi
rule stats_hapy_to_s3:
    input:
        i1=rules.Mise_en_forme_sous_format_csv.output,
    output:
        o="{output_path}/{analysis}_hapy_stats_done.txt",
        data= "{output_path}/{analysis}/happy/statistics.csv",
        tempf= "{output_path}/{analysis}/happy/statistics.temp.csv"
        
    params:
        script =config["scripts"]["hapy_stats_S3"],
        user = config["S3"]["USER"],
        adress_ip = config["S3"]["IP"],
        Bucket = config["S3"]["Bucket_name"],
        version =config["general_information"]["Version"],
        env = config["general_information"]["Environnement"],
        date=config["general_information"]["Date"],
        ref = config["general_information"]["Reference"],
        tool=config["general_information"]["tool"],
    shell:
        '''
        python3 {params.script} -i {input.i1} -o {output.tempf} -v {params.version} -e {params.env} -d {params.date} -r {params.ref} -u {params.user} -ip {params.adress_ip} \
        -b {params.Bucket} -t {params.tool} -n statistics.csv -f {output.tempf} -f2 statistics.csv -n2 {output.d} > {output.o}
        '''