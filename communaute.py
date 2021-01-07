#!/usr/bin/env python3

"""
Programme permettant de comprendre le fonctionnement d'une commuanauté 
scientifique à partir d'un jeu de données comportant les résumés des 
articles et d'un fichier contenant les références des articles.
"""

import sys

# fonction pour traiter les fichiers de base
from pre_processing import pre_processing

# pour l'affichage des fonction 'cite' et 'est_cite'
import pprint
pp = pprint.PrettyPrinter(depth=4)

# importation les fichiers json uniquement après avoir init
try:
	if sys.argv[1] != 'init':
		from classes import Auteur, Communaute, mat_adj
except IndexError:
	print('Argument(s) invalide(s).')
	sys.exit()
except FileNotFoundError:
	print('Veuillez fournir des données à l\'aide de la commande init.')
	print('Pour plus d\'informations taper \'./communaute aide\'')
	sys.exit()




def aide():
	print('> Liste des commandes:')
	print('init  cite  influences communaute')
	print('> Utiliser une commande:')
	print('./communaute.py maCommande argument1 argument2')


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

		elif sys.argv[1] == 'communaute':
			Communaute(sys.argv[2],sys.argv[3]).graph()

		elif sys.argv[1] == 'communaute_info':
			mat_adj()

		else:
			raise KeyError

	except KeyError:
		print(f'La commande \'{sys.argv[1]}\' n\'est pas valide. Pour plus d\'informations taper \'./communaute aide\'')
	except IndexError:
		print('Argument(s) invalide(s).')