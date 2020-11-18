# -*- coding: utf-8 -*-
import pandas as pd
import re
import os

#rawstring filepath
filepath=r"C:\Users\lepau\OneDrive\Desktop\abstracts" #Plus tard à mettre en input, pour le moment à varier selon la machine utilisée
links=r"C:\Users\lepau\OneDrive\Desktop\links"

###Première étape :
#Organisation des données dans des fichiers csv exploitables par les constructeurs de classes

##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
#Pre-processing
################
################

"""
####Construction d'un fichier data.csv
years = sorted(os.listdir(filepath))
files = []  # attribu en POO ?
nb_files = 0
i = 0
for year in years:
    files.append(os.listdir(f'{filepath}/{year}'))
    nb_files += len(files[i])
    i += 1

list_authors = []
list_papers = []
for year, file_by_year in zip(years, files): #à optimiser
    for file in sorted(file_by_year):
        with open(f"{filepath}/{year}/{file}","r",encoding="UTF-8")as f:
            j=0 # for pass when there is two lines with Authors => 9201039.abs
            code='[A-Za-z].- ' #je l'utiliserai peut etre

            for line in f:
                if j < 1:
                    if line[:9] == "Authors: ":
                        j += 1
                        tmp1=re.split(' and |, |& ', line[9:-1])
                        tmp2=[]
                        #Elimination du formatage LaTeX
                        for author in tmp1:
                            author=author.replace('\\"',"")
                            author=author.replace("\\'","")
                            author=author.replace('\"',"")
                            author=author.replace("\'","")
                            author=author.replace("\\~","")
                            author=author.replace("\~","")
                            author=author.replace("\`","")
                            author=author.replace("{","")
                            author=author.replace("}","")
                            tmp2.append(author)
                        list_authors.append(tmp2)

                    if line[:8] == "Author: ": 
                        j+= 1
                        tmp1=re.split(' and |, |& ', line[8:-1])
                        tmp2=[]
                        #Elimination du formatage LaTeX pour les accents
                        for author in tmp1:
                            author=author.replace('\\"',"")
                            author=author.replace("\\'","")
                            author=author.replace('\"',"")
                            author=author.replace("\'","")
                            author=author.replace("\\~","")
                            author=author.replace("\~","")
                            author=author.replace("\`","")
                            author=author.replace("{","")
                            author=author.replace("}","")
                            tmp2.append(author)
                        list_authors.append(tmp2)

                    if line[:7]=="Paper: ":
                        list_papers.append(int(line[14:21]))

data=pd.DataFrame({'paper_id':list_papers,'Authors':list_authors})

###Construction d'un fichier references.csv : une ligne = un id et une liste de ref
paper_id=[]
ref_id=[]
with open(f"{links}",'r') as ref:
    i=-1
    last_id=0
    for line in ref:
        current_id=line[0:7]
        current_ref=line[8:15]

        if current_id==last_id:
            ref_id[i].append(current_ref)
        else:
            ref_id.append([])
            paper_id.append(int(current_id))
            i+=1
            ref_id[i].append(current_ref)
            last_id=current_id
references=pd.DataFrame({'paper_id':paper_id,'ref_id':ref_id})

###Export
references.to_csv('references.csv',sep=',',encoding='utf8')
data.to_csv('data.csv',sep=',',encoding='utf8') #Ce csv est désormais utilisable par les constructeurs de classes
"""
######################
######################
#End of pre-processing
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

#Trouver un moyen de sauter le pre-processing dans certaines conditions par exemple avec une version du fichier : if name==f'data{current_version}'

from classes import Author
from classes import Article

data=pd.read_csv('data.csv',sep=',',usecols=['paper_id','Authors'],index_col='paper_id') #data.Authors['9201001'] : ['C. Itzykson', 'J.-B. Zuber']
ref=pd.read_csv('references.csv',sep=',',usecols=['paper_id','ref_id'],index_col='paper_id')

###Tests
Itzykson=Author('C. Itzykson')
print(Itzykson.list_articles)

Article0001002=Article(1002)
print(Article0001002.ref,Article0001002.authors)
