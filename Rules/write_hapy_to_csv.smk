#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule write_hapy_to_csv:
    input:
        i1= expand("{output_path}/{analysis}/happy/{analysis}.summary.csv",output_path=output_path, analysis = full_name),
        i2=rules.Mise_en_forme_sous_format_csv.output,
        i3=rules.Comparaison_des_Haplotypes.output

    output:
        o =  "{output_path}/{analysis}_happy_csv_done.txt"
    params:
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
        n2= lambda wildcards:"{}/{}/happy/data.csv".format(wildcards.output_path,wildcards.analysis)


    shell:
        '''
        python3 {params.script} -i {input.i1} -o {params.out} -v {params.version} -e {params.env} -d {params.date} -r {params.ref} -u {params.user} -ip {params.adress_ip} \
        -b {params.Bucket} -t {params.tool} -n data.csv -f {params.out} -f2 data.csv -n2 {params.n2} > {output.o}
        '''