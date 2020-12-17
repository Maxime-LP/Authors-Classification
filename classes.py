import pandas as pd
import numpy as np
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref
import time

data = pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF Article Auteurs
data2 = pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')   #DF Auteur Articles
ref = pd.read_csv(f'{article_ref}.csv',sep=',',usecols=['id_article','references'],index_col='id_article')    #DF Article ref


class Article: #OK
    """
    Un article = un id + une liste d'auteurs
    """
    def __init__(self,given_id):
        self.id=int(given_id)
        self.ref=ref.references[self.id]
        self.auteurs=data.auteurs[self.id]


class Auteur: #OK
    """
    Les éléments de la classe auteur ont deux attributs: name et liste_articles
    """

    def __init__(self, name):
        self.name=name
        self.liste_articles=data2.id_articles[f'{self.name}']
    
    def cite(self, N=1):
        """
        Retourne un dict {auteur : influence}
        L'argument influence détermine si on veut avoir les influences des auteurs
        """

        quoted_authors = {}

        try:
            N = int(N)

            if N==0: return self.name

            # on récupère les contributions de l'auteur
            next_step_papers = data2.id_articles[self.name]
            next_step_papers = re.split(", ",next_step_papers[1:-1]) #En attente de correction du problème des .csv en fin de processing

            for k in range(1,N+1):
                #print(f"Profondeur : {k}/{N}")
                written_papers = next_step_papers
                next_step_papers = []

                for paper in written_papers:
                    paper = int(paper)
                    #pour chaque article écrit, on récupère la liste des articles cités, puis on remonte les auteurs
                    try :
                        #On est à priori pas sûr que le papier considéré en cite au moins un autre
                        references=ref.references[paper][2:-2]
                        quoted_papers=re.split("', '",references)
                        quoted_authors_tmp  = []
                        for paper_tmp in quoted_papers:
                            quoted_authors_tmp+=re.split("', '", data.auteurs[int(paper_tmp)][2:-2])
                            #On en profite pour ajouter les papiers cités à la liste des papiers à traiter à la prochaine itération
                            if self.name not in data.auteurs[int(paper_tmp)] :
                                next_step_papers.append(paper_tmp)
                    except KeyError:
                        quoted_authors_tmp = []

                    for author in quoted_authors_tmp:
                        if author != self.name and author != "":
                            if author not in quoted_authors.keys():
                                quoted_authors[author] = 1/k
                            else:
                                quoted_authors[author] += 1/k
                #print(quoted_authors)
        except ValueError:
            print('Saisir un entier naturel pour la profondeur.')

        return quoted_authors



class Communaute(Auteur):

    """def __init__(self, name):
                    self.name = name
                    self.profondeur = profondeur"""

    def graph(self, N):
        # On récupère le dict {auteur : influence}
        dict_auteur = self.cite(N)

        dicts_inverse = defaultdict()
        for auteur in list(dict_auteur.keys()):
            dict_tmp = Auteur(auteur).cite(N)
            if auteur in dict_tmp.keys():
                print('ok')
            if self in dict_tmp.keys():
                print('ok')

    def mat_adj(self, N):
        n = len(data2)
        mat = np.zeros((n,n), int)
        auteurs = list(data2.index)
        # création d'un DF avec le nom des auteurs en index et colonnes
        mat_adj = pd.DataFrame(mat, index=auteurs, columns=auteurs, dtype=int) # memory_usage : 112608*2
        #for auteur in auteurs:
        dict_tmp = Auteur('C.Itzykson').cite(1)
        print(mat_adj.memory_usage())

    """def __str__(self):
                return f"La communauté autour de {self.auteur} ..."""


"""time0=time.time()
test=Auteur('N.Warner')
print(test.cite(4))
print(time.time()-time0)"""
