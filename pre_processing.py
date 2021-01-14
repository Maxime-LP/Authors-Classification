from config import fp_articles, fp_ref, nom_dict
import json
import re
import os
import platform
from collections import defaultdict
from pylatexenc.latex2text import LatexNodes2Text
#Installation du module pylatexenc : pip install git+https://github.com/phfaist/pylatexenc.git



# Fonctions appellées pour nettoyer les données et les mettre en forme (json).

# pp := pre-processing



########### début clean ############

def clean(line_tmp):
	"""
	Enlève les éléments entre parenthèses.
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
				dict_ref_influence[line[1]].append(line[0]) # avec ou sans 30s
				nb_relations += 1

		return dict_ref_cite , dict_ref_influence

########### fin pp_references ############



########### début pp_articles ############

def pp_articles(chemin_articles,chemin_references): # amélioration à faire : utliser les regex dans la fonction clean et pour récupérer le nom des auteurs
	"""
	Pre-processing du dossier article.d
	Entrées : noms du fichiers contenant les résumés d'article (arborescence).
	Sorties : 
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


	# dict {papier: [auteur1, ...]}
	dict_p = defaultdict(list)
	# dict {auteur : [papier1, ...]}
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

	# Informations sur le dossier articles
	nb_articles = len(dict_p)
	nb_auteurs = len(dict_a)
	print(f'> Le dossier articles contient {nb_files} fichiers, {nb_articles} publications et {nb_auteurs} auteurs.')
	
	return dict_a, dict_p

########### fin pp_articles ############



########### début pre_processing ############

def pre_processing(articles, references):
	'''
	Pre-processing d'un nouveau jeu de données pour l'application.
	'''

	chemin_articles = fp_articles + articles
	chemin_references = fp_ref + references
	if os.path.exists(chemin_articles): # Test d'acces au fichier articles
		if os.path.exists(chemin_references): # Test d'acces au fichier references

			# créations de dictionnaires contenant les données triées
			dict_a, dict_p = pp_articles(chemin_articles,chemin_references)
			dict_cite, dict_est_cite = pp_references(chemin_references)
			
			os.makedirs('data', exist_ok=True)

			with open(f'data/{nom_dict[0]}.json', 'w',encoding='utf-32') as file:
				json.dump(dict_a, file)
			with open(f'data/{nom_dict[1]}.json', 'w',encoding='utf-32') as file:
				json.dump(dict_p, file)
			with open(f'data/{nom_dict[2]}.json', 'w',encoding='utf-8') as file:
				json.dump(dict_cite, file)
			with open(f'data/{nom_dict[3]}.json', 'w',encoding='utf-8') as file:
				json.dump(dict_est_cite, file)

			print("> Fin du chargement des données.")

		else:
			print(f'Problème d\'accès au fichier \'{references}\'')
			print('Veuillez vérifier le nom du fichier ainsi que les données du fichier \'config.py\'.')
	else:
		print(f'Problème d\'accès au fichier \'{articles}\'.')
		print('Veuillez vérifier le nom du fichier ainsi que les données du fichier \'config.py\'.')

########### fin pre_processing ############