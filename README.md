# Pipeline de validation de détection des variants

Ce pipeline permet d'effectuer la validation de detection des variants (SNP,INDEL et SV) en utilisant 3 outils:

 [Hap.py](https://github.com/Illumina/hap.py): pour les SNPs et les INDELs


 [ClinSV](https://github.com/KCCG/ClinSV) et [Wittyer](https://github.com/Illumina/witty.er): pour les SVs.

 Le pipeline lance l'analyse selon l'outil spécifié dans le fichier config:

 Le nom de l'outil(tool) doit être mentionné dans le fichier config soit "Hap.py" ou "ClinSV" ou "Witty" pour Witty.er.

# Cloner le Repository:
```
git clone https://gitlab-bioinfo.aphp.fr/Seqoia-Diag-Pipelines/pipeline_validation_wgs.git
```
## I. Création du fichier config
 Le script argconfig_json.py permet de créer le fichier json de configuration de pipeline:

 La discription des arguments est disponible en entrant la commande suivante:
```
python3 argconfig_json.py -h
```
### I.1. Arguments obligatoires pour tous les outils

|Arguments obligatoires|  Description|                  Exemple|
|:----:|:----:|:----:|
|-i|input path|/scratch3/spim-preprod/pipeline_validation_wgs|
|-o|output path|/scratch3/spim-preprod/pipeline_validation_wgs/data|
|-s|Rules path|/scratch3/spim-preprod/pipeline_validation_wgs/Rules|
|-Enviro|Execution environment|scratch3|
|-tool|tool to launch|Hap.py or Witty or ClinSV|
|-ref|reference|NA12878|
|-V|version|3.3.1|
|-R|Run id|A00666|
|-A|Alias|0012|
|-T|Target|WGS|
|-D|Disease|MR|
|-S|Sample id|FS00505001|
|-t|type|index|
|-d|date|21/04/2022|
|-an|Full analysis name|A00666_0012_WGS_MR_FS00505001_index_21042022_final|
|-u|S3 user name|spim-dev|
|-bn|S3 Bucket name|validation|

### I.2. Arguments spécifiques à Hap.py

|Arguments|   Description|    Exemple|
|:----:|:----:|:----:|
|-r|gold standard vcf path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-b|gold standard bed path|/data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2|
|-e|vcf sample path|/scratch2/tmp/fakermi|
|-f|fasta path|/data/annotations/Human/GRCh38/index/sorted_primary_assemblies|
|-GSF|fasta file name|GRCh38.92|
|-GSB|standard bed file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7|
|-GSV|standard vcf file name|HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer|

### I.3. Arguments spécifiques à Witty.er
Arguments|   Description|     Exemple|
|:----:|:----:|:----:|
|-pvcfhg002|Standard vcf hg002|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-nvcfhg002|standard hg002 VCf file name|HG002_GRCh38_1_22_v4.2.1_benchmark|
|-nbedhg002|standard hg002 bed file name|HG002_GRCh38_1_22_v4.2.1_benchmark_noinconsistent|
|-pbedhg002|standard hg002 bed file path|/data/annotations/Human/hg38/references/NA24385_HG002/NISTv4.2.1|
|-query_sv_path|path to  vcf query for witty|/scratch2/tmp/vsaillour/tmp/20220704_wittyer_test/A00666_0012_WGS_MR_FS00505001_index_21042022|
|-query_sv_name|query vcf name for witty|A00666_0012_WGS_MR_FS00505001_index_21042022_SV-CNV|

### I.4. Arguments spécifiques à ClinSV
Arguments|    Description|      Exemple|
|:----:|:----:|:----:|
|-bam|bam files base directory|/scratch3/spim-preprod/pipeline_trio_wgs/data|
|-prefix|bam files subdirectory|A00666_0012_WGS_MR_FS00505001_21042022|
|-suffix|bam files directory|FS00505001_S6|



### I.5. Remarques:

 Il ne faut pas spécifier les extensions des fichiers: Si on a un fichier Name.vcf.gz on donne uniquement le nom du fichier dans ce cas (Name), de même pour toutes les autres extensions (e.g bam,fa,bed...). 


 Il ne faut pas aussi ajouter un "/" à la fin d'un chemin d'accés d'un fichier: si on a un chemin "/path/to/folder/" il faut éliminer le dernier "/" -----> "/path/to/folder"


### I.6. Exemple de création du fichier config:
Ouvrir [Godocker]()

Copier la commande ci-dessous en modifiant les arguments en fonction de l'analyse souhaitée.
Choisir les paramètres suivants:

###### Contairner image: sequoia-docker-tools/snakemake:3.9.0-4
###### Mount  volumes: snakemake, scratch2, scratch3, home
###### CPU et RAM : Valeurs Par défaut

##### Cliquer "Submit"

#### - Pour Hap.py:
```
#!/bin/bash

python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool Hap.py \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-r /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-b /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-e /scratch2/tmp/shared_files_tmp/spim \
-f /data/annotations/Human/GRCh38/index/sorted_primary_assemblies \
-GSF GRCh38.92 \
-GSB HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7 \
```
#### - Pour witty.er:

```
#!/bin/bash

python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool Witty \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-pvcfhg002 /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-nvcfhg002 HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_PGandRTGphasetransfer \
-nbedhg002 HG001_GRCh38_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-10X-SOLID_CHROM1-X_v.3.3.2_highconf_nosomaticdel_noCENorHET7 \
-pbedhg002 /data/annotations/Human/GRCh38/references/NA12878_HG001/NISTv3.3.2 \
-query_sv_path [path to vcf query for witty] \
-query_sv_name [query vcf name for witty] \

```
#### - Pour ClinSV:

```
#!/bin/bash
python3 /scratch3/spim-preprod/pipeline_validation_wgs/script/argconfig_json.py \
-i /scratch3/spim-preprod/pipeline_validation_wgs \
-o /scratch3/spim-preprod/pipeline_validation_wgs/data \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Rules \
-Enviro scratch3 \
-tool ClinSV \
-ref NA12878 \
-V 3.3.1 \
-R A00666 \
-A 0012 \
-T WGS \
-D MR \
-S FS00505001 \
-t index \
-d 22/08/2022 \
-an A00666_0012_WGS_MR_FS00505001_index_21042022_final \
-u spim-preprod \
-bn validation  \
-bam /scratch3/spim-preprod/pipeline_trio_wgs/data \
-prefix A00666_0012_WGS_MR_FS00505001_21042022 \
-suffix FS00505001_S6 \

```
## II. Exécution du pipeline

### II.1. Paramètres Go_docker

#### Mount volumes :
##### scratch2
##### scratch3
##### irods
##### annotations
##### home
##### snakemake

#### Container Image: sequoia-docker-tools/snakemake:3.9.0-4
#### CPU: 4
#### RAM: 5

### II.2. Commande:
Copier la commande ci-dessous dans go-docker en sécifiant les paramètres entre crochés 
```
#!/bin/bashset -o pipefail;
/data/snakemake/miniconda3/envs/snakemake/bin/snakemake \
-s /scratch3/spim-preprod/pipeline_validation_wgs/Snakefile_validation.smk \
-k --rerun-incomplete \
--configfile /scratch3/spim-preprod/pipeline_validation_wgs/pipeline_config/config.json \
--cluster-config /scratch3/spim-preprod/pipeline_validation_wgs/cluster_config/cluster_config.json \
--cluster 'godjob.py create -n {cluster.name}_[Sample id] -t {cluster.tags} --external_image -v {cluster.volume_snakemake} -v {cluster.volume_home} -v {cluster.volume_scratch2} -v {cluster.volume_irods} -v {cluster.volume_scratch3} -v {cluster.volume_annotations} -c {cluster.cpu} -r {cluster.mem} -i {cluster.image} -s' \
-j 40 -w 60 2>&1 | tee /scratch3/spim-preprod/pipeline_validation_wgs/log/[Full analysis name].log
```
### II.3. AWS_S3

 Le pipeline permet la compression et le stockage des résultats sur aws_S3,après chaque analyse. Pour cela la [configuration](https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-configure-files.html) de S3 doit être spécifiée sous :
```
/home/.aws/credentials
```


 