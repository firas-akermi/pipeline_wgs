#!/usr/bin/env python3
# Firas Akermi
#akermi1996@gmail.com
rule witty_csv:
    input:
        i1 = rules.witty.output,
        i2 = rules.witty.output[0]+'Wittyer.Stats.json'
    output:
        o = "{output_path}/{analysis}_Witty_csv_done.txt"
    params:
        script =config["scripts"]["witty_S3_csv"],
        user = config["S3"]["USER"],
        adress_ip = config["S3"]["IP"],
        Bucket = config["S3"]["Bucket_name"],
        out= lambda wildcards:"{}/{}/Witty/Witty.csv".format(wildcards.output_path,wildcards.analysis),
        version =config["general_information"]["Version"],
        env = config["general_information"]["Environnement"],
        date=config["general_information"]["Date"],
        ref = config["general_information"]["Reference"],
        tool=config["general_information"]["tool"],
        n2= lambda wildcards:"{}/{}/Witty/data.csv".format(wildcards.output_path,wildcards.analysis)

    shell:
        '''
        python3 {params.script} -i {input.i2} -o {params.out} -v {params.version} -e {params.env} -d {params.date} -r {params.ref} -u {params.user} -ip {params.adress_ip} \
        -b {params.Bucket} -t {params.tool} -n data.csv -f {params.out} -f2 data.csv -n2 {params.n2} > {output.o}
        '''