# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
from time import time

#rawstring filepath
filepath=r"C:\Users\lepau\OneDrive\Desktop\abstracts" #Plus tard à mettre en input, pour le moment à varier selon la machine utilisée
links=r"C:\Users\lepau\OneDrive\Desktop\links"

############################################
#Pre-processing
########################


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
            code='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. ' #je l'utiliserai peut etre
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
                            author=author.replace("\`","")
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
                            author=author.replace("\`","")
                            tmp2.append(author)
                        list_authors.append(tmp2)

                    if line[:7]=="Paper: ":
                        list_papers.append(line[14:21])


df=pd.DataFrame({'id_paper':list_papers,'Authors':list_authors})
print(df)
df.to_csv('process.csv',sep=',',encoding='utf8')


