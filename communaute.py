#!/usr/bin/env python3

"""
Programme permettant de comprendre le fonctionnement d'une commuanauté 
scientifique à partir d'un jeu de données comportant les résumé des 
articles et d'un fichier contenant les références des articles.
"""

import sys
import numpy as np
from pre_processing import pre_processing
if sys.argv[1]!='init': #Pour eviter d'essayer d'importer les fichiers csv lorsqu'on a pas encore init
	from classes import Article, Auteur, Communaute


def aide():
	print('> Liste des commandes:')
	print('init  cite  communaute')
	print('> Utiliser une commande:')
	print('./communaute.py maCommande argument1 argument2')


if __name__ == "__main__":

	"""# commandes disponible de l'application 
				dispatcher = {
					'init': pre_processing,		# non-utilisé
					'help': aide,
					}"""


	# selection d'une commande		
	#try:
	if sys.argv[1] == 'test':
		test_df()

	if sys.argv[1] == 'aide':
		aide()

	elif sys.argv[1] == 'init':
		pre_processing(sys.argv[2], sys.argv[3])

	elif sys.argv[1] == 'cite':
		Auteur(sys.argv[2]).cite(sys.argv[3])

	elif sys.argv[1] == 'communaute':
		Communaute(sys.argv[2]).graph(sys.argv[3])

	else:
		print('Saisie non-valide. Tapez \'./communaute aide\' pour plus d\'informations.')
		#dispatcher[sys.argv[1]](sys.argv[2], sys.argv[3])

	#except KeyError:
		#print('Commande invalide. Pour plus d\'informations taper \'./communaute help\'')
	#except IndexError:
		#print('Argument(s) invalide(s).')