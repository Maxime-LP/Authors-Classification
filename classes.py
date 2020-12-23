#import pandas as pd
#import numpy as np
import json
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, file_data_name #article_auteurs, auteur_articles, auteur_auteurs_cites, article_ref
import time
import networkx as nx
import matplotlib.pyplot as plt

#data = pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF {article:auteurs}
#data2 = pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')   #DF {auteur:articles}
#data3 = pd.read_csv(f'{auteur_auteurs_cites}.csv',sep=',',encoding='utf-32',usecols=['auteur','auteurs_cités'],index_col='auteur')   #DF {auteur:auteurs_cités}
#ref = pd.read_csv(f'{article_ref}.csv',sep=',',usecols=['id_article','references'],index_col='id_article')    #DF {article:references}

with open('dict_aa.json', 'r', encoding='utf-32') as file:
	dict_aa = json.load(file)
with open('dict_a.json', 'r', encoding='utf-32') as file:
	dict_a = json.load(file)
with open('dict_p.json', 'r', encoding='utf-32') as file:
	dict_p = json.load(file)
with open('dict_ref.json', 'r', encoding='utf-8') as file:
	dict_ref = json.load(file)


'''class Article: #OK
	"""
	Un article = un id + une liste d'auteurs
	"""
	def __init__(self,given_id):
		self.id=int(given_id)
		self.ref=ref.references[self.id]
		self.auteurs=data.auteurs[self.id]'''


class Auteur: #OK

	"""
	Les éléments de la classe auteur ont deux attributs: name et liste_articles
	"""

	def __init__(self, name):
		self.name = name
		'''try:
			self.liste_articles = data2.id_articles[f'{self.name}']
		except KeyError:
			pass'''

	def cite(self, N=1):
		"""
		Entrées : nom d'un auteur, profondeur des citations
		Sorties : dictionnaire de la forme {auteur : auteurs_cités}
		"""
		try:
			N = int(N)
		except ValueError:
			return print('Saisir un entier naturel non nul pour la profondeur.')

		if not int(N) > 0:
			print('Saisir un entier naturel non nul pour la profondeur.')
		
		else:
			# dict final
			auteurs_cites = defaultdict(lambda: 0) #Par défaut le dict associe un 0 donc si un objet e n'y est pas, auteurs_cites[e]=0. Plus rapide à tester qu'un test in
			# liste des papiers à tester au prochain rang
			papiers_rang_suivant = dict_a[self.name]

			# boucle sur les profondeurs
			for k in range(1, N+1):
				# liste des papiers cités au rang courant
				papiers_rang_courant = papiers_rang_suivant
				papiers_rang_suivant = []

				for papier in papiers_rang_courant:
					try : #On est a priori pas sûr que la papier en cite un autre
						for papier_cite in dict_ref[papier]:
							# on ajoute le papier cité pour le rang k+1
							papiers_rang_suivant.append(papier_cite)
							for auteur in dict_p[papier_cite]:
								# on ajoute le nom d'un auteur à chaque fois qu'il apparait dans un un papier cité
								if auteur!=self.name and auteur!="":
									auteurs_cites[auteur] += 1/k
					except KeyError:
						pass

			return auteurs_cites



	def influences(self, N=1):
		"""
		Entrées : nom d'un auteur, profondeur des citations
		Sorties : dictionnaire de la forme {auteur : auteurs_influencés}
		"""

		try:
			N = int(N)
		except ValueError:
			return print('Saisir un entier naturel non nul pour la profondeur.')

		if not int(N) > 0:
			print('Saisir un entier naturel non nul pour la profondeur.')
		else:
			# dict final
			auteurs_influences = defaultdict(float)
			# list des auteurs influencé au rank précédant
			auteurs_rang_courant = [self.name]
			# liste des auteurs à tester au prochain rang
			auteurs_rang_suivant = []

			# boucle sur les profondeurs
			for k in range(1, N+1):
				for auteur_courant in auteurs_rang_courant:
					for auteur in dict_aa.keys():
						# test si l'auteur courant influence l'auteur
						if auteur_courant in dict_aa[auteur]:
							# laissez passer si k == 1
							if auteur != self.name:
								auteurs_rang_suivant.append(auteur)

							# ajout d'influence en fonction de la profondeur
							auteurs_influences[auteur]+= 1/k
				# on supprime les doublons
				auteurs_rang_courant = list(set(auteurs_rang_suivant))
				auteurs_rang_suivant = []
			
			#print(auteurs_influences)
			return auteurs_influences


class Communaute():

	#mat_adj = pd.DataFrame()

	def __init__(self, auteur, profondeur):
		self.auteur_central = Auteur(auteur)
		self.auteur = Auteur(auteur)
		self.profondeur = profondeur
		self.membres = {}
		
		dict_auteurs_1=self.auteur_central.cite(self.profondeur)
		dict_auteurs_2=self.auteur_central.influences(self.profondeur)
		#On a les liste des auteurs cités l'auteur central et ceux qui le citent, on cherche ensuite ceux qui sont dans les deux 
		liste_auteurs = list(set(dict_auteurs_1.keys()) & set(dict_auteurs_2.keys()))
		#Construisons ensuite le dictionnaire {auteur : influence} où influence est la moyenne des influences vers l'auteur et depuis l'auteur
		for auteur in liste_auteurs:
			self.membres[auteur] = (dict_auteurs_1[auteur] + dict_auteurs_2[auteur]) / 2
					
	def graph(self):
		"""
		"""
		g = nx.Graph()
		#On trace les relations entre l'auteur central et les membres de la communautés (pour le moment j'utilise un attribut weight)
		g.add_edges_from([(self.auteur_central,membre_i,{'weight': self.membres[membre_i]}) for membre_i in self.membres.keys()])

		plt.figure()
		nx.draw(g)
		plt.show()
		return


	'''# la matrice d'adjacence exporté fais plus de 300Mo => FBI
	def mat_adj(self, N):
		mat_adj=pd.DataFrame()
		n = len(data2)
		mat = np.zeros((n,n), int)
		auteurs = list(data2.index)

		# création d'un DF avec le nom des auteurs en index et colonnes
		mat_adj = pd.DataFrame(mat, index=auteurs, columns=auteurs, dtype=float) # memory_usage : 112608*2
		return mat_adj

		# ligne par ligne on fait +1 lorsque un auteur est cité
		for auteur in auteurs:
			try:
				if '(' in auteur:
					print(auteur)
			except TypeError:
				print(auteur)
			try:
				tmp = list(Auteur(auteur).cite(1).keys())
			except TypeError:
				pass
			if tmp != []:
				#print(tmp)
				try:
					mat_adj.loc[auteur][tmp] = 1
				except KeyError:
					pass
		mat_adj.to_csv('mat_adj.csv')
		return'''