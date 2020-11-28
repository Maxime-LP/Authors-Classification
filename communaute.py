#!/usr/bin/env python3

"""
Programme permettant de comprendre le fonctionnement d'une commuanauté 
scientifique à partir d'un jeu de données comportant les résumé des 
articles et d'un fichier contenant les références des articles.
"""

import sys
from classes import Communaute


if __name__ == "__main__":

	# commandes disponible de l'application 
	dispatcher = {
		'init': Communaute.init,
		'help': Communaute.aide_generale
		}
	try:
		if sys.argv[1] == 'help':
			dispatcher[sys.argv[1]]()
		elif (sys.argv[1][:5] == 'help_') & (sys.argv[1][5:] in list(dispatcher.keys())):
			help(dispatcher[sys.argv[1][5:]])
		else:
			dispatcher[sys.argv[1]](sys.argv[2], sys.argv[3])
	except KeyError:
		print('Commande invalide. Pour plus d\'informations, entrer: ./communaute help')
	except IndexError:
		print('Argument(s) invalide(s).')
	print(Communaute.nb_auteurs)


# Anciennes fonctions:

'''if sys.argv[1] in operations:
									try:
										print(type(operations[sys.argv[1]]))
										return operations[sys.argv[1]]('olé')
									except IndexError:
										print(f'> Pour utiliser la commande {sys.argv[1]}, tapez:')
										print('wallah')'''


'''
	# initialiser un document
	elif sys.argv[1] == 'init':
		try:
			init(sys.argv[2]) # sys.argv[2] : chemin des fichiers
		except IndexError:
			print('> Pour utiliser la commande "init", tapez:')
			print('./commuanute init chemin_du_fichier')

	# obtenir les auteurs qui citent un auteur avec une profondeur N
	elif sys.argv[1] == 'quote':
		try:
			quote(sys.argv[2])
			# sys.argv[2] : nom d'un auteur
		except IndexError:
			print('> Pour utiliser la commande "quote", tapez:')
			print('./commuanute quote nom_auteur')

	# obtnir les références d'un auteurs avec une profondeur N
	elif sys.argv[1] == 'influence':
		try:
			influence(sys.argv[2])
			# sys.argv[2] : nom d'un auteur
		except IndexError:
			print('> Pour utiliser la commande "influence", tapez:')
			print('./commuanute influence nom_auteur')
	
	# représentation par un graphe d'une communauté autour d'un auteur
	elif sys.argv[1] == 'communaute':
		try:
			community(sys.argv[2])
			# sys.argv[2] : nom d'un auteur
			# sys.argv[3] : profondeur
		except IndexError:
			print('> Pour utiliser la commande "communautes", tapez:')
			print('./commuanute communautes nom_auteur profondeur')

	# si la commande n'existe pas
	else:
		print('> Commande inexistante.')
		print('> Utilisez l\'argument help pour plus d\'informations.')
'''