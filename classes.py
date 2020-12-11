
import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref

data=pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article')
data2=pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','references'],index_col='auteur')
ref=pd.read_csv(f'{article_ref}.csv',sep=',',encoding='utf-32',usecols=['id_article'],index_col='id_article')
data.sort_values(by='id_article',axis=0,inplace=True)
ref.sort_values(by='id_article',axis=0,inplace=True) 
"""
class Article:
	def __init__(self,given_id):
		self.id=int(given_id)
		self.ref=ref.ref_id[self.id]
		self.authors=data.Authors[self.id]
"""
class Auteur:
	def __init__(self,name):
		self.name=name
		self.list_articles=data.query('self.name in data.Authors')

"""		
class Communaute:
	def __init__(self,auteur,profondeur):
		self.auteur=auteur
		self.profondeur=profondeur
"""
Itzy=Auteur('C. Itzykson')
print(Itzy.name,Itzy.list_articles) 
