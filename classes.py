import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref
import time
import networkx as nx
import matplotlib.pyplot as plt

data = pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF {article:auteurs}
data2 = pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')   #DF {auteur:articles}
ref = pd.read_csv(f'{article_ref}.csv',sep=',',usecols=['id_article','references'],index_col='id_article')    #DF {article:references}

class Auteur:
	"""
	Les éléments de la classe auteur ont deux attributs: name et liste_articles
	"""

	def __init__(self, name):
		self.name = name
		try:
			self.liste_articles = data2.id_articles[f'{self.name}']
		except KeyError:
			pass
	
	def cite(self, N=1):
		"""
		Retourne un dict {auteur : influence}
		L'argument influence détermine si on veut avoir les influences des auteurs
		"""
		quoted_authors = defaultdict(lambda: 0)
		N = int(N)

		# on récupère les contributions de l'auteur
		next_step_papers = data2.id_articles[self.name]
		next_step_papers = re.split(", ",next_step_papers[1:-1]) #En attente de correction du problème des .csv en fin de processing

		for k in range(1,N+1):
			written_papers = next_step_papers
			next_step_papers = []

			for paper in written_papers:
				paper = int(paper)
				#pour chaque article écrit, on récupère la liste des articles cités, puis on remonte les auteurs

				try :
					#On est à priori pas sûr que le papier considéré en cite au moins un autre
					references=ref.references[paper][1:-1]
					quoted_papers=re.split(", ",references)
					for paper_tmp in quoted_papers:
						paper_tmp=int(paper_tmp)
						#On en profite pour ajouter les papiers cités à la liste des papiers à traiter à la prochaine itération
						if self.name not in data.auteurs[paper_tmp] :
							next_step_papers.append(paper_tmp)
						try :
							quoted_authors_tmp=re.split("""', '|", "|', "|", '""", data.auteurs[paper_tmp][2:-2])
							for author in quoted_authors_tmp:
								if author != self.name and author != "":
									quoted_authors[author] += 1/k
						except KeyError:
							pass
				except KeyError:
					pass

		return quoted_authors


class Communaute():

	def __init__(self, auteur, profondeur):
		self.auteur_central = Auteur(auteur)
		self.profondeur = profondeur
		self.membres = {}
		
		#Dictionnaire des auteurs cités par l'auteur central
		dict_cite=self.auteur_central.cite(self.profondeur)  #C'est un defaultdict(lambda: 0) donc si un élément e n'y est pas on adict_cite[e]=0
		#Dictionnaire des auteurs de dict_cite qui citent également l'auteur central
		dict_est_cite_par = defaultdict(lambda: 0)

		for auteur in dict_cite.keys():
			tmp=Auteur(auteur).cite(self.profondeur)  #C'est aussi un defaultdict(lambda: 0), le test !=0 est plus rapide que le test in keys()
			if tmp[self.auteur_central.name]!=0:
				dict_est_cite_par[auteur]+=tmp[self.auteur_central.name]

		#On a les listes des auteurs cités l'auteur central et ceux qui le citent, on cherche ensuite ceux qui sont dans les deux 
		liste_auteurs = list(set(dict_cite.keys()) & set(dict_est_cite_par.keys()))
		#Construisons ensuite le dictionnaire {auteur : influence} où influence est la moyenne des influences vers l'auteur et depuis l'auteur
		for auteur in liste_auteurs:
			self.membres[auteur] = (dict_cite[auteur] + dict_est_cite_par[auteur]) / 2
		

	def graph(self):
		g = nx.Graph()
		#On trace les relations entre l'auteur central et les membres de la communautés (pour le moment j'utilise un attribut weight)
		g.add_edges_from([(self.auteur_central.name,membre_i,{'weight': self.membres[membre_i]}) for membre_i in self.membres.keys()])
		nx.draw(g,with_labels=True)
		plt.show()

		return
"""
test=Communaute('C.Itzykson',3)
print(test.membres)
test.graph()
"""