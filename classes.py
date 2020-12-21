import pandas as pd
import numpy as np
import json
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, auteur_auteurs_cites, article_ref
import time
import networkx as nx
import matplotlib.pyplot as plt

data = pd.read_csv(f'{article_auteurs}.csv',sep=',',encoding='utf-32',usecols=['id_article','auteurs'],index_col='id_article') #DF {article:auteurs}
data2 = pd.read_csv(f'{auteur_articles}.csv',sep=',',encoding='utf-32',usecols=['auteur','id_articles'],index_col='auteur')   #DF {auteur:articles}
#data3 = pd.read_csv(f'{auteur_auteurs_cites}.csv',sep=',',encoding='utf-32',usecols=['auteur','auteurs_cités'],index_col='auteur')   #DF {auteur:auteurs_cités}
ref = pd.read_csv(f'{article_ref}.csv',sep=',',usecols=['id_article','references'],index_col='id_article')    #DF {article:references}

with open('dict_aa.txt', 'r', encoding='utf-32') as file:
        dict_aa = json.load(file)



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
        self.name = name
        try:
            self.liste_articles = data2.id_articles[f'{self.name}']
        except KeyError:
            pass
    
    def cite(self, N=1):
        """
        Retourne un dict {auteur : influence}
        L'argument influence détermine si on veut avoir les influences des auteurs
        """

        quoted_authors = {}

        try:
            N = int(N)

            if N == 0: return self.name

            # on récupère les contributions de l'auteur
            next_step_papers = data2.id_articles[self.name]
            next_step_papers = re.split(", ",next_step_papers[1:-1]) #En attente de correction du problème des .csv en fin de processing

            for k in range(1,N+1):
                print(k)
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
                            quoted_authors_tmp+=re.split("""', '|", "|', "|", '""", data.auteurs[int(paper_tmp)][2:-2])
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
        except ValueError:
            print('Saisir un entier naturel pour la profondeur.')

        print(quoted_authors.keys())
        return quoted_authors


<<<<<<< HEAD

    def influences(self, N=1):
        """
        Entrées : nom d'un auteur, profondeur des citations
        Sorties : dictionnaire de la forme {auteur : auteurs_cités}
        """

        auteurs_cites = {}

        try:
            if int(N) <= 0:
                raise ValueError

            N = int(N)
            
            auteurs_influence = defaultdict(float)

            for k in range(1, N+1):
                # in progress

                for auteur in dict_aa.keys():
                    if self.name in dict_aa[auteur]:
                        auteurs_influence[auteur]+= 1/k
            print(auteurs_influence)

        except ValueError:
            print('Saisir un entier naturel non nul pour la profondeur.')

        return

            

=======
>>>>>>> 46ca2b00a9041f3394151777b7501e83dfe7205a

class Communaute():

    #mat_adj = pd.DataFrame()

    def __init__(self, auteur, profondeur):
        self.auteur = Auteur(auteur)
        self.profondeur = profondeur
                    
    def graph(self, N):
        # initialisation du graphe de la commuanute
        g = nx.Graph()
        # On récupère le dict {auteur : influence}
        dict_auteur = self.auteur.cite(N)
        auteurs_cites = dict_auteur.keys()
        for n in range(1,N):
            g.add_edges_from([(self.auteur.name, i) for i in auteurs_cites])

        plt.figure()
        nx.draw(g)
        plt.show()
        return


    # la matrice d'adjacence exporté fais plus de 300Mo => FBI
    def mat_adj(self, N):
        mat_adj=pd.DataFrame()
        n = len(data2)
        mat = np.zeros((n,n), int)
        auteurs = list(data2.index)

        # création d'un DF avec le nom des auteurs en index et colonnes
        mat_adj = pd.DataFrame(mat, index=auteurs, columns=auteurs, dtype=float) # memory_usage : 112608*2
        return mat_adj

        '''# ligne par ligne on fait +1 lorsque un auteur est cité
        for auteur in auteurs:
            try:
                if '(' in auteur:
                    print(auteur)
            except TypeError:
                print(auteur)
            try:
                tmp = list(Auteur(auteur).cite(1).keys())
            except TypeError:
                pass
            if tmp != []:
                #print(tmp)
                try:
                    mat_adj.loc[auteur][tmp] = 1
                except KeyError:
                    pass
        mat_adj.to_csv('mat_adj.csv')
        return'''



"""test=Auteur('C.Itzykson')
print(test.cite(3))

test=Communaute('C.Itzykson',3)
test.mat_adj(3)
print(test.mat_adj(3))"""

