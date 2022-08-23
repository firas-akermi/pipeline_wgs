#!/usr/bin/env python3
# Firas Akermi
rule Extraction_des_informations:
        input:
            "{output_path}/{analysis}/happy/{variant}/{score}.vcf"
        output:
            "{output_path}/{analysis}/happy/{variant}/{score}.txt",
        shell:'''
            set +e
            grep -Pv "^#" {input} > {output}
             exitcode=$?
             if [ $exitcode -eq 1 ]
            then
                exit 0
            elif  [ $exitcode -eq 0 ]
            then
                exit 0
            else
                exit 1
            fi
              '''
           
                     
            