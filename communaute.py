#!/usr/bin/env python3
"""
Programme permettant de comprendre le fonctionnement d'une communauté 
scientifique à partir d'un jeu de données comportant les abstracts des 
articles et d'un fichier contenant les références des articles.
"""

########## Importation des modules ##########
import sys
# fonction pour traiter les fichiers de base
from pre_processing import pre_processing
# pour l'affichage des fonction 'cite' et 'est_cite'
import pprint
pp = pprint.PrettyPrinter(depth=4)
# importation les fichiers json uniquement après avoir init
try:
	if sys.argv[1] != 'init':
		from classes import Auteur, Communaute
except IndexError:
	print('Argument(s) invalide(s).')
	sys.exit()
except FileNotFoundError:
	print('Données manquantes. Veuillez fournir des données à l\'aide de la commande init.')
	print('Pour plus d\'informations taper \'./communaute aide\'')
	sys.exit()
#############################################



########## Documentation utilisateur ##########

liste_commandes = {'init' : 'Initialise deux nouveaux fichiers de données\n    argument 1: nom du fichier contenant les articles,\n    argument 2: nom du fichier contenant les références.',
				   'cite' : 'Affiche les auteurs cités par un auteur avec une profondeur donnée\n    argument 1: nom d\'un auteur,\n    argument 2: entier naturel définissant la profondeur.',
				   'est_cite' : 'Affiche les auteurs citant un auteur avec une profondeur donnée\n    argument 1: nom d\'un auteur,\n    argument 2: entier naturel définissant la profondeur.',
				   'communaute' : 'Affiche un graphe représentant les liens entre un auteur et sa communauté pour une profondeur donnée.\n    argument 1: nom d\'un auteur,\n    argument 2: entier naturel définissant la profondeur.',
				   }

def aide():
	"""Donne des information sur le fonctionnement de l'application."""
	print('> Liste des commandes:')
	print(list(liste_commandes.keys()),'\n')

	print('> Utiliser une commande:')
	print('./communaute.py maCommande argument1 argument2\n')

	print('> Information sur les commandes:')
	for commande, docu in liste_commandes.items():
		print(f'{commande} : {docu}')
	print("\nRemarque : Pour les fonction 'cite', 'est_cite' et 'communaute' veuillez respecter la casse, les caractères spéciaux et ne pas mettre d\'espace dans le nom de l\'auteur.")
#############################################



if __name__ == "__main__":

	# selection d'une commande		
	try:
		if sys.argv[1]=='aide':
			aide()

		elif sys.argv[1] == 'init':
			pre_processing(sys.argv[2], sys.argv[3])

		elif sys.argv[1] == 'cite':
			res = Auteur(sys.argv[2]).cite(sys.argv[3])
			# tri des valeurs du dictionnaire
			res = sorted(res.items(), key=lambda t: t[1])
			# affichage avec le module pretty print
			pp.pprint(res)

		elif sys.argv[1] == 'est_cite':
			res = Auteur(sys.argv[2]).est_cite(sys.argv[3])
			res = sorted(res.items(), key=lambda t: t[1])
			pp.pprint(res)

		elif sys.argv[1] == 'communaute1':
			Communaute(sys.argv[2],sys.argv[3]).graph_simple()

		elif sys.argv[1] == 'communaute2':
			Communaute(sys.argv[2],sys.argv[3]).graph_relations()

		else:
			raise KeyError

	except KeyError:
		print(f'La commande \'{sys.argv[1]}\' n\'est pas valide. Pour plus d\'informations taper \'./communaute aide\'')
	except IndexError:
		print('Argument(s) invalide(s).') 
