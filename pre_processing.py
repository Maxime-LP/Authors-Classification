from config import fp_articles, fp_ref, file_data_name #, article_auteurs, auteur_articles, auteur_auteurs_cites, article_ref
#import pandas as pd
import json
#import numpy as np
import re
import os
import platform
from time import time
from collections import defaultdict
from pylatexenc.latex2text import LatexNodes2Text
#Installation du module pylatexenc : pip install git+https://github.com/phfaist/pylatexenc.git

# pp := pre-processing

########### début clean ############
def clean(line_tmp):
	"""
	Entrées: ligne contenant les auteurs
	Sorties : liste conteannt le nom des auteurs
	"""
	# Suppression des éléments entre parenthèses
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
	if '(' in line_tmp:
		index = line_tmp.index('(')
		line_tmp = line_tmp[:index]

	# On crée une liste avec les noms d'auteurs en séparant avec certaines chaînes de caractères
	line_tmp = re.split(', and | and | nd | , | ,|, |,|& ',line_tmp)
	# On supprime aussi les espaces restant dans les noms d'auteurs et traduit les caractères spéciaux écrit en LaTeX
	line_tmp = [LatexNodes2Text().latex_to_text(author).replace(" ","") for author in line_tmp]
	return line_tmp
########### fin clean ############


########### début pp_references ############
def pp_references(chemin_references):
		"""
		Pre_processing du fichier texte references.txt
		Entrées : noms du fichiers contenant les references (fichier txt)
		Sorties : dictionnaire avec id des articles en clé et id des articles références dans le-dit article en valeurs.
		"""

		nb_relations = 0
		# dict {papier_qui_cite : [papier_cite1, ...]}
		dict_ref_cite = defaultdict(list)
		# dict {papier_cite : [papier_qui_cite1, ...]}
		dict_ref_influence = defaultdict(list)

		# récupération et pre-processing du fichier
		with open(f'{chemin_references}',"r") as f:
			for line in f:
				#On crée une liste [id1,id2] avec type(idx)=str
				line = line[:-1].split(' ')
				
				dict_ref_cite[line[0]].append(line[1])
				#On crée une liste [id1,id2] avec type(idx)=str
				dict_ref_influence[line[1]].append(line[0])
				nb_relations += 1

		return dict_ref_cite #, dict_ref_influence
########### fin pp_references ############


########### début pp_articles ############
def pp_articles(chemin_articles,chemin_references):
	"""
	Pre-processing du dossier article.d
	Entrées : noms du fichiers contenant les résumés d'article (arborescence).
	Sorties : 
	"""

	# on recupère dict_ref_cite
	dict_ref = pp_references(chemin_references)

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
	# dict {auteur : [papier1, ...]}
	dict_a = defaultdict(list)
	dict_aa = defaultdict(list) # à supprimer et tout ce qui s'y rapporte
	
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
							tmp_paper = line[14:21] #####

						if line[:9] == "Authors: ":
							# récupère nom des auteurs dans une liste
							nb_line_author += 1
							line_tmp=line[9:-1]
							# ajout d'une nouvelle clé dans dict_p
							dict_p[tmp_paper] = clean(line_tmp)
							

						if line[:8] == "Author: ":
							# récupère nom des auteurs dans une liste
							nb_line_author +=  1
							line_tmp=line[8:-1]
							# ajout d'une nouvelle clé dans dict_p
							dict_p[tmp_paper] = clean(line_tmp)

			# affichage de la progression du traitement 
			progression_pct = progression / nb_files * 100
			if progression_pct%10 == 0 :
				if platform.system() == "Windows":
					os.system("cls")
				elif platform.system() in ["Darwin","Linux"]:
					os.system("clear")
				print(f'Progression : {progression_pct} %')
			progression+=1
	
	# construction dict_a
	for paper in dict_p.keys():
		authors = dict_p[paper]
		for author in authors:
			dict_a[author].append(paper)

	# à supprimer
	for auteur in dict_a.keys():
		auteurs_cites = []
		# pour les papiers d'un auteur
		for papier in dict_a[auteur]:
			# on récupère les papiers cités par l'auteur
			papiers_cites = dict_ref[int(papier)]
			for papier_cite in papiers_cites:
				auteurs_cites = list(set(auteurs_cites) | set(dict_p[papier_cite]))
		try:
			auteurs_cites.remove(auteur)
		except ValueError:
			pass
		dict_aa[auteur] = auteurs_cites

	# Informations sur le dossier articles
	nb_articles = len(dict_p)
	nb_auteurs = len(dict_a)
	print(f'> Le dossier articles contient {nb_files} fichiers, {nb_articles} publications et {nb_auteurs} auteurs.')
	
	return dict_a, dict_p, dict_aa
########### fin pp_articles ############



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
			dict_a, dict_p, dict_aa = pp_articles(chemin_articles,chemin_references)
			dict_ref = pp_references(chemin_references)
			with open(f'dict_a.json', 'w',encoding='utf-32') as file:
				json.dump(dict_a, file)
			with open(f'dict_p.json', 'w',encoding='utf-32') as file:
				json.dump(dict_p, file)
			with open(f'dict_aa.json', 'w',encoding='utf-32') as file:
				json.dump(dict_aa, file)
			with open(f'dict_ref.json', 'w',encoding='utf-8') as file:
				json.dump(dict_ref, file)

			'''# conversions en DataFrames et mise en forme de ces derniers
				# pour df_p
			df_p = pd.DataFrame({'id_article':dict_p.keys(), 'auteurs': dict_p.values()})
			df_p.set_index('id_article', inplace=True)
			df_p.sort_index(axis=0, inplace=True)

				# pour df_a
			df_a = pd.DataFrame({'auteur':dict_a.keys(), 'id_articles':dict_a.values()})
			df_a.set_index('auteur', inplace=True)

				# pour df_aa
			df_aa = pd.DataFrame({'auteur':dict_aa.keys(), 'auteurs cités':dict_aa.values()})
			df_aa.set_index('auteur', inplace=True)

				# pour df_ref
			df_ref = pd.DataFrame({'references':dict_ref.values(), 'id_article':dict_ref.keys()})
			df_ref.set_index('id_article', inplace=True)

			#Ecriture dans des fichiers csv
			df_p.to_csv(f'{article_auteurs}.csv',index='id_article', encoding='utf_32')
			df_a.to_csv(f'{auteur_articles}.csv',index='auteur', encoding='utf_32')
			df_aa.to_json(f'{auteur_auteurs_cites}.json', orient='columns')
			df_ref.to_csv(f'{article_ref}.csv')


			#PROBLEME : les valeurs des DF sont bien des listes, mais apres export dans des csv ce sont des str !
			'''
			
			print("> Fin du chargement des données.")

		else:
			print(f'Problème d\'accès au fichier \'{references}\'. Veuillez vérifier le nom du fichier.')
	else:
		print(f'Problème d\'accès au fichier \'{articles}\'. Veuillez vérifier le nom du fichier.')
########### fin pre_processing ############