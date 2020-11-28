#!/usr/bin/env python3

"""
Programme permettant de comprendre le fonctionnement d'une commuanauté 
scientifique à partir d'un jeu de données comportant les résumé des 
articles et d'un fichier contenant les références des articles.
"""

import sys
import classes
from pre_processing import pre_processing


def aide():
	print('> Liste des commandes:')
	print('init')
	print('> Utiliser une commande:')
	print('./communaute.py maCommande argument1 argument2')



if __name__ == "__main__":

	# commandes disponible de l'application 
	dispatcher = {
		'init': pre_processing,
		'help': aide
		}


	# selection d'une commande		
	try:
		if sys.argv[1] == 'help':
			dispatcher[sys.argv[1]]()
		elif (sys.argv[1][:5] == 'help_') & (sys.argv[1][5:] in list(dispatcher.keys())):
			help(dispatcher[sys.argv[1][5:]])
		else:
			dispatcher[sys.argv[1]](sys.argv[2], sys.argv[3])
	except KeyError:
		print('Commande invalide. Pour plus d\'informations: ./communaute help')
	except IndexError:
		print('Argument(s) invalide(s).')