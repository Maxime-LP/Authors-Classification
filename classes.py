
import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref

data=pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF Article Auteurs
data2=pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')	#DF Auteur Articles
ref=pd.read_csv(f'{article_ref}.csv',sep=',',encoding='utf-32',usecols=['id_article','references'],index_col='id_article')	#DF Article ref

class Article: #OK
	"""
	Un article = un id + une liste d'auteurs
	"""

	def __init__(self,given_id):
		self.id=int(given_id)
		self.ref=ref.references[self.id]
		self.auteurs=data.auteurs[self.id]

class Auteur: #OK
	"""
	Un auteur = un nom + une liste d'article
	"""
	def __init__(self,name):
		self.name=name
		self.liste_articles=data2.id_articles[f'{self.name}']
	
class Communaute:

	def __init__(self,auteur,profondeur):
		self.auteur=auteur
		self.profondeur=profondeur

	def __str__(self):
		pass

print(Auteur('C. Itzykson').name)