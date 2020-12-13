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
		index_list est la liste des index du DF ref, on l'utilise pour savoir si un article dépend d'un autre ou non (si son id n'est pas dans index_list, alors il ne cite aucun article)
		"""
		index_list=list(ref.index.values)
		N = int(N)
		quoted_authors = []
		# on récupère les contributions de l'auteur
		next_step_papers = data2.id_articles[self.name]
		next_step_papers = re.split(", ",next_step_papers[1:-1]) #En attente de correction du problème des .csv en fin de processing
		
		for k in range(1,N+1):
			print(f"{k}/{N}")
			written_papers=next_step_papers
			next_step_papers=[]

			for paper in written_papers:
				paper=int(paper)
				#pour chaque article écrit, on récupère la liste des articles cités, puis on remonte les auteurs
				if paper in index_list:
					quoted_papers=re.split("', '",ref.references[paper][2:-2])
					quoted_authors_tmp=[]
					for paper_tmp in quoted_papers:
						quoted_authors_tmp+=re.split("', '", data.auteurs[int(paper_tmp)][2:-2])
						#On en profite pour ajouter les papiers cités à la liste des papiers à traiter à la prochaine itération
						next_step_papers.append(paper_tmp)
				else:
					quoted_authors_tmp=[]

				for author in quoted_authors_tmp:
					if author not in quoted_authors and author!=self.name:
						quoted_authors.append((author,k))

		return quoted_authors


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


test=Auteur('R.Giachetti')
print(test.cite(4))
