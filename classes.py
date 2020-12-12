import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref

data=pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF Article Auteurs
data2=pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')	#DF Auteur Articles
ref=pd.read_csv(f'{article_ref}.csv',sep=',',usecols=['id_article','references'],index_col='id_article')	#DF Article ref

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
		Retourne la liste des auteurs cités sous la forme (auteur,k) où k est la profondeur de la citation
		"""
		N = int(N)
		authors_quoted = []
		# on récupère les contributions de l'auteur
		paper_quoted = data2.id_articles[self.name]
		print(paper_quoted[1])
		for k in range(1,N+1):
			next_step_paper_quoted=[]
			for paper in paper_quoted:
				current_authors_list=data.auteurs[paper]
				for current_author in current_authors_list:
					if current_author not in authors_quoted :
						authors_quoted.append(current_author)
					next_step_paper_quoted.append(current_author)

			paper_quoted=next_step_paper_quoted
			
					
		return authors_quoted


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

"""
test=Auteur('C. Itzykson')
print(test.cite(1))
"""