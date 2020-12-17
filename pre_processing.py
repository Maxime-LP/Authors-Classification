from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref
import pandas as pd
import numpy as np
import re
import os
import platform
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
				for line in f:
					nb_line_author = 0 # dans le cas ou il y a 2 lignes Auteur(s) => 9201039.abs
					if nb_line_author < 1:
						if line[:7]=="Paper: ":
							# récupère id de l'article
							tmp_paper = int(line[14:21])

						if line[:9] == "Authors: ":
							# récupère nom des auteurs dans une liste
							nb_line_author += 1
							line_tmp=line[9:-1]
							#Suppression des noms d'universités
							while True:
								try:
									index1=line_tmp.index('(')
									index2=line_tmp.index(')')
									if index2==len(line_tmp)-1:
										line_tmp=line_tmp[0:index1]
									else:
										line_tmp=line_tmp[0:index1] + line_tmp[index2+1:-1] + line_tmp[-1]
								except ValueError:
									break

							# On crée une liste avec les noms d'auteurs en séparant avec certaines chaînes de caractères
							line_tmp = re.split(', and | and | nd | , | ,|, |,|& ',line_tmp)
							# On supprime aussi les espaces restant dans les noms d'auteurs et traduit les caractères spéciaux écrit en LaTeX
							dict_p[tmp_paper] = [LatexNodes2Text().latex_to_text(author).replace(" ","") for author in line_tmp]
							

						if line[:8] == "Author: ":
							# récupère nom des auteurs dans une liste
							nb_line_author +=  1
							line_tmp=line[8:-1]
							#Suppression des noms d'universités
							while True:
								try:
									index1=line_tmp.index('(')
									index2=line_tmp.index(')')
									if index2==len(line_tmp)-1:
										line_tmp=line_tmp[0:index1]
									else:
										line_tmp=line_tmp[0:index1] + line_tmp[index2+1:-1] + line_tmp[-1]
								except ValueError:
									break

							# pareil que plus haut
							line_tmp = re.split(', and | and | nd | , | ,|, |,|& ', line_tmp)
							dict_p[tmp_paper] = [LatexNodes2Text().latex_to_text(author).replace(" ","") for author in line_tmp]

			# affichage de la progression du traitement 
			progression_pct = progression / nb_files * 100
			if progression_pct%10 == 0 : 
				if platform.system() == "Windows":
					os.system("cls")
				elif platform.system() == "Linux":
					os.system("clear")
				print(f'progression : {progression_pct} %')
			progression+=1
	
	# Construction du dict avec les auteurs en clés
	for paper in dict_p.keys():
		authors=dict_p[paper]
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
				line = line[:-1].split(' ') #On crée une liste [id1,id2] où id1 et id2 sont de type str
				dict_ref[line[0]].append(line[1])
				nb_relations += 1

		# Informations sur le fichier references
		print(f'> Le fichier references contient {nb_relations} relations.')

		return dict_ref

########### fin pp_references ############



########### début pre_processing ############

def pre_processing(articles, references):
	'''
	Pre-processing d'un nouveau jeu'de données pour l'application.
	'''

	chemin_articles = fp_articles + articles
	chemin_references = fp_ref + references


	if os.path.exists(chemin_articles): # Test d'acces au fichier articles
		if os.path.exists(chemin_references): # Test d'acces au fichier references

			# créations de dictionnaires contenant les données triées
			dict_p, dict_a = pp_articles(chemin_articles)
			dict_ref = pp_references(chemin_references)

			# conversions en DataFrames et mise en forme de ces derniers
				# pour df_p

			df_p = pd.DataFrame({'id_article':dict_p.keys(), 'auteurs': dict_p.values()})
			df_p.set_index('id_article', inplace=True)
			df_p.sort_index(axis=0, inplace=True)

				# pour df_a
			df_a = pd.DataFrame({'auteur':dict_a.keys(), 'id_articles':dict_a.values()})
			df_a.set_index('auteur', inplace=True)

				# pour df_ref
			df_ref = pd.DataFrame({'references':dict_ref.values(), 'id_article':dict_ref.keys()})
			df_ref.set_index('id_article', inplace=True)
			df_ref.sort_index(axis=0, inplace=True)

			#Ecriture dans des fichiers csv
			df_p.to_csv(f'{article_auteurs}.csv',index='id_article', encoding='utf_32')
			df_a.to_csv(f'{auteur_articles}.csv',index='auteur', encoding='utf_32')
			df_ref.to_csv(f'{article_ref}.csv')


			#PROBLEME : les valeurs des DF sont bien des listes, mais apres export dans des csv ce sont des str !

			print("> Fin du chargement des données.")

		else:
			print(f'Problème d\'accès au fichier \'{references}\'. Veuillez vérifier le nom du fichier.')
	else:
		print(f'Problème d\'accès au fichier \'{articles}\'. Veuillez vérifier le nom du fichier.')

########### fin pre_processing ############