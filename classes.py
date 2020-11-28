from config import fp_articles, fp_ref
import pandas as pd
import numpy as np
import re
import os
from time import time
from collections import defaultdict


class Communaute:

	dict_p = defaultdict(list) # clés : id des articles, valeurs : auteurs ayant contribué à l'article
	dict_a = defaultdict(list) # clés : noms des auteurs, valeurs : articles auxquels l'auteur a contribué
	nb_articles = 0
	nb_auteurs = 0

	def aide_generale():
		print('> Liste des opérations:')
		print('init')
		print('> Pour voir la documentation des commandes, entrer:')
		print('./communaute help_maCommande')
		print()


	def init(articles, references):
		'''
		Pre-processing d'un nouveau jeu'de données pour l'application.
		'''
		chemin_articles = fp_articles + articles
		chemin_references = fp_ref + references

		def init_articles(chemin_articles):
			"""
			Pre-processing du dossier article.d
			Entrées : noms du fichiers contenant les résumés d'article (arborescence).
			Sorties : un dictionnaire avec id des articles en clé et nom des auteurs y ayant contribuéet un second avec le nom d'un auteur en clé et les articles de l'auteur en valeur.
			"""

			#récupération des fichiers dans l'arborescence
			years = sorted(os.listdir(chemin_articles))

			files = []
			nb_files = 0
			i = 0

			for year in years:
			    files.append(os.listdir(f'{chemin_articles}/{year}'))
			    nb_files += len(files[i])
			    i += 1


			# début du pre-processing
			dict_p = defaultdict(list)
			dict_a = defaultdict(list)

			#construction du dict avec les id des articles en clés
			for year, file_by_year in zip(years, files):
			    for file in sorted(file_by_year):
			        with open(f"{chemin_articles}/{year}/{file}","r") as f:
			            nb_line_author = 0 # for pass when there is two lines with Authors => 9201039.abs
			            for line in f:
			                if nb_line_author < 1:
			                    if line[:7]=="Paper: ":
			                        tmp_paper = line[14:21]

			                    if line[:9] == "Authors: ":
			                        nb_line_author += 1
			                        dict_p[tmp_paper] = re.split(' and |, |& ', line[9:-1])

			                    if line[:8] == "Author: ": 
			                        nb_line_author +=  1
			                        dict_p[tmp_paper] = re.split(' and |, |& ', line[8:-1])

			# construction du dict avec les auteurs en clés
			for paper, authors in dict_p.items():
			    for author in authors:
			        dict_a[author].append(paper)

			# Informations sur le dossier articles
			nb_articles = len(dict_p)
			nb_auteurs = len(dict_a)
			print(f'> Le fichier articles contient {nb_files} fichiers.')
			print(f'> On y recence {nb_articles} publications et {nb_auteurs} auteurs dans notre jeu de données.')

			return dict_p, dict_a, nb_articles, nb_auteurs


		def init_references(chemin_references):
			"""
			Pre_processing du fichier texte references.txt
			Entrées : noms du fichiers contenant les references (fichier txt)
			Sorties : dictionnaire avec id des articles en clé et id des articles références dans le-dit article en valeurs.
			"""

			nb_relations = 0
			dict_ref = defaultdict(list)

			# récupération et pre-processing du fichier
			with open(f'{chemin_references}',"r") as f:
			    for line in f:
			        line = line[:-1].split(' ')
			        dict_ref[line[0]].append(line[1])
			        nb_relations += 1

			# Informations sur le fichier references
			print(f'> Le fichier references contient {nb_relations} relations.')

			return dict_ref


		dict_p, dict_a, Communaute.nb_article, nb_auteurs = init_articles(chemin_articles)
		init_references(chemin_references)
		print("> Fin du chargement des données.")



class Article(Communaute):
	def __init__(self):
		return



"""class Auteur(Community):
 	def __init__(self,name):
         self.name = name # nom de l'auteur
         self.articles = data.query('self.name in data.Authors')"""
         # articles auxquels l'auteur a contribué