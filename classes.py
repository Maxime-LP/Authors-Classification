
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
	
	def cite(self, N):
		"""
		fonction quote avec une profondeur N = 1
		"""
		self = Auteur(N)
		N = int(N)
		author_quoted = []
		# on récupère les contributions de l'auteur
		paper_quoted = data2[self.name]
		
		# pour chaque contribution, on regarde les papiers cités
		# on récupère les auteurs de chaque papier
		# et si un auteur n'est pas déjà dans les auteurs cités, on le rajoute à author_quoted
		for paper in paper_quoted: 
			for author in data2[paper]:
				if not author in author_quoted:
					author_quoted.append(author)
					
		return author_quoted


class Communaute:

	def __init__(self,auteur,profondeur):
		self.auteur=auteur
		self.profondeur=profondeur

	def __str__(self):
		pass
	
	"""
	def citeN(self, N):
		Chercher pour chaque auteur qui la influencé à son 
		tour mais si auteur dans profondeur n-1 ne pas ajouter.
		Aussi voir la question de la pondération.
		N = int(N)
		author_quoted = [[self]]
		tmp = []
		for i in range(N):
			for author in author_quoted[-1]:
				tmp.append(quote0(author))
				if i == N-1: print(tmp)
			for i in tmp:
				author_quoted.append([author for author in tmp if author not in author_quoted[-1]])
		print(author_quoted)
		return author_quoted
	"""