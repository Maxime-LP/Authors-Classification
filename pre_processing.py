from config import fp_articles, fp_ref, nom_articles1, nom_articles2, nom_references
import pandas as pd
import numpy as np
import re
import os
from time import time
from collections import defaultdict
from pylatexenc.latex2text import LatexNodes2Text


# pp := pre-processing

########### début pp_articles ############

def pp_articles(chemin_articles):
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

	progression=1

	#construction du dict avec les id des articles en clés
	for year, file_by_year in zip(years, files):
		for file in sorted(file_by_year):
			with open(f"{chemin_articles}/{year}/{file}","r",encoding="utf-8") as f:
				nb_line_author = 0 # dans le cas ou il y a 2 lignes Auteur(s) => 9201039.abs
				for line in f:
					if nb_line_author < 1:
						if line[:7]=="Paper: ":
							# récupère id de l'article
							tmp_paper = int(line[14:21])

						if line[:9] == "Authors: ":
							# récupère nom des auteurs dans une liste
							nb_line_author += 1
							tmp =re.split(' and | | ,|,|, |& ',line[9:-1])
							dict_p[tmp_paper] = [LatexNodes2Text().latex_to_text(author) for author in tmp]

						if line[:8] == "Author: ":
							# récupère nom des auteurs dans une liste
							nb_line_author +=  1
							tmp = re.split(' and | | ,|,|, |& ', line[8:-1])
							dict_p[tmp_paper] = [LatexNodes2Text().latex_to_text(author) for author in tmp]

			progression_pct = progression / nb_files * 100
			if progression_pct%10 == 0 : 
				#os.system('cls')
				print(f'progression : {progression_pct} %')
			progression+=1


	# construction du dict avec les auteurs en clés
	for paper, authors in dict_p.items():
		for author in authors:
			dict_a[author].append(paper)

	# Informations sur le dossier articles
	nb_articles = len(dict_p)
	nb_auteurs = len(dict_a)
	print(f'> Le dossier articles contient {nb_files} fichiers.')
	print(f'> On y recence {nb_articles} publications et {nb_auteurs} auteurs.')

	return dict_p, dict_a

########### fin pp_articles ############



########### début pp_references ############

def pp_references(chemin_references):
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
				# on change le type des id: str vers int
				line = [int(line[i]) for i in [0,1]]
				dict_ref[line[0]].append(line[1])
				nb_relations += 1

		# Informations sur le fichier references
		print(f'> Le fichier references contient {nb_relations} relations.')

		return dict_ref

########### fin pp_references ############



def pre_processing(articles, references):
	'''
	Pre-processing d'un nouveau jeu'de données pour l'application.
	'''

	chemin_articles = fp_articles + articles
	chemin_references = fp_ref + references


	# créations de dictionnaires contenant les données triées
	dict_p, dict_a = pp_articles(chemin_articles)
	dict_ref = pp_references(chemin_references)


	# conversions en DataFrames et mis en forme de ces derniers
		# pour df_p
	df_p = pd.DataFrame({'id_article':dict_p.keys(), 'auteurs': dict_p.values()})
	df_p.set_index('id_article', inplace=True)
	df_p.sort_index(axis=0, inplace=True)

		# pour df_a
	df_a = pd.DataFrame({'auteur':dict_a.keys(), 'references':dict_a.values()})
	df_a.set_index('auteur', inplace=True)

		# pour df_ref
	df_ref = pd.DataFrame({'references':dict_ref.values(), 'id_article':dict_ref.keys()})
	df_ref.set_index('id_article', inplace=True)
	df_ref.sort_index(axis=0, inplace=True)


	# écriture des DataFrame dans des fichier format csv
	#les accents ne passent pas
	df_p.to_csv(f'{nom_articles1}.csv', sep=',', encoding='utf_32')
	df_a.to_csv(f'{nom_articles2}.csv', sep=',', encoding='utf_32')
	df_ref.to_csv(f'{nom_references}.csv', sep=',', encoding='utf_32')

	print("> Fin du chargement des données.")
	return 