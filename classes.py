
import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, nom_articles1, nom_articles2, nom_references

df_articles = pd.read_csv(f'{nom_articles1}.csv',sep=',',usecols=['id_article','auteurs'],index_col='id_article', encoding='utf_32')
df_auteurs = pd.read_csv(f'{nom_articles2}.csv',sep=',',usecols=['auteur','references'],index_col='auteur', encoding='utf_32')
df_ref = pd.read_csv(f'{nom_references}.csv',sep=',',usecols=['id_article','references'],index_col='id_article', encoding='utf_32')

df_articles.sort_values(by='id_article',axis=0,inplace=True)
df_ref.sort_values(by='id_article',axis=0,inplace=True)

class Article:

    def __init__(self,given_id):
        self.id = int(given_id)
        self.ref = ref.ref_id[self.id]
        self.authors = data.Authors[self.id]



class Auteur:

    def __init__(self):
        # self = l'auteur donc pas besoin de créer self.name
        self.name = name
        self.list_articles = data.query('self.name in data.Authors')

    def cite(self, N):
        """
        fonction quote avec une profondeur N = 1
        """
        self = Auteur(N)
        N = int(N)
        author_quoted = []
        # on récupère les contributions de l'auteur
        paper_quoted = df_auteurs[sel.name]
        #dict_a[author]
        
        # pour chaque contribution, on regarde les papiers cités
        # on récupère les auteurs de chaque papier
        # et si un auteur n'est pas déjà dans les auteurs cités, on le rajoute à author_quoted
        for paper in paper_quoted: 
            for author in dict_p[paper]:
                if not author in author_quoted:
                    author_quoted.append(author)
                    
        return author_quoted

		
class Communaute:
	def __init__(self,auteur,profondeur):
		self.auteur=auteur
        self.profondeur=profondeur



'''
    def citeN(self, N):
        """
        Chercher pour chaque auteur qui la influencé à son 
        tour mais si auteur dans profondeur n-1 ne pas ajouter.
        Aussi voir la question de la pondération.
        """
        N = int(N)
        author_quoted = [[self]]
        tmp = []
        for i in range(N):
            for author in author_quoted[-1]:
                tmp.append(quote0(author))
                if i == N-1: print(tmp)
            for i in tmp:
                author_quoted.append([author for author in tmp if author not in author_quoted[-1]])
        print(author_quoted)
        return author_quoted

'''