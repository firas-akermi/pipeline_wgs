# Pipeline de validation de détection de variant
Ce pipeline permet d'effectuer la validation de detection des variants (SNP,INDEL et SV) en utilisant 3 outils:
 [Hap.py](https://github.com/Illumina/hap.py) pour les SNPs et les INDELs
 [ClinSV](https://github.com/KCCG/ClinSV) et [Wittyer](https://github.com/Illumina/witty.er) pour les SVs.

 Le pipeline lance l'analyse selon l'outil spécifié dans le fichier config:
 Le nom de l'outil(tool) doit être mentionné dans le fichier config soit "Hap.py" ou "ClinSV" ou "Witty" pour Witty.er.

 Le script argconfig_json.py permet de créer le fichier json de configuration de pipeline:
 La discription des arguments est disponible en entrant la commande suivante:
```
python3 argconfig_json.py -h
```
 Le pipeline permet la compression et le stockage des résultats sur aws S3,après chaque analyse. Pour cela la configuration de S3 doit être spécifiée sous :
```
/home/.aws/credentials
```


 