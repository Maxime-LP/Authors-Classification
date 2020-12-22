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

        print(quoted_authors)
        return #quoted_authors

    def cite_bis(self, N=1):

        """
        Entrées : nom d'un auteur, profondeur des citations
        Sorties : dictionnaire de la forme {auteur : auteurs_cités}
        """

        try:
            # on veut une profondeur d'au moins 1
            if int(N) <= 0:
                raise ValueError

            N = int(N)
            
            # dict final
            auteurs_cites = defaultdict(float)
            # list des auteurs influencé au rank précédant
            auteurs_rang_courant = [self.name]
            # liste des auteurs à tester au prochain rang
            auteurs_rang_suivant = []

            # boucle sur les profondeurs
            for k in range(1, N+1):
                for auteur_courant in auteurs_rang_courant:
                    for auteur in dict_aa[auteur_courant]:
                        # ajout d'influence en fonction de la profondeur
                        auteurs_cites[auteur]+= 1/k
                        auteurs_rang_suivant.append(auteur)
                # on supprime les doublons
                auteurs_rang_courant = list(set(auteurs_rang_suivant))
                auteurs_rang_suivant = []
            
        # QUESTION : Comment gérer la citation de self lui même?!

            print(auteurs_cites)

        except ValueError:
            print('Saisir un entier naturel non nul pour la profondeur.')

        return #auteurs_cites



    def influences(self, N=1):
        """
        Entrées : nom d'un auteur, profondeur des citations
        Sorties : dictionnaire de la forme {auteur : auteurs_influencés}
        """

        try:
            # on veut une profondeur d'au moins 1
            if int(N) <= 0:
                raise ValueError

            N = int(N)
            
            # dict final
            auteurs_influence = defaultdict(float)
            # list des auteurs influencé au rank précédant
            auteurs_rang_courant = [self.name]
            # liste des auteurs à tester au prochain rang
            auteurs_rang_suivant = []

            # boucle sur les profondeurs
            for k in range(1, N+1):
                for auteur_courant in auteurs_rang_courant:
                    for auteur in dict_aa.keys():
                        # test si l'auteur courant influence l'auteur
                        if auteur_courant in dict_aa[auteur]:
                            # laissez passer si k == 1
                            if auteur != self.name:
                                auteurs_rang_suivant.append(auteur)

                            # ajout d'influence en fonction de la profondeur
                            auteurs_influence[auteur]+= 1/k
                # on supprime les doublons
                auteurs_rang_courant = list(set(auteurs_rang_suivant))
                auteurs_rang_suivant = []
            
            #print(auteurs_influence)

        except ValueError:
            print('Saisir un entier naturel non nul pour la profondeur.')

        return


class Communaute():

    #mat_adj = pd.DataFrame()

    def __init__(self, auteur, profondeur):
        self.auteur_central = Auteur(auteur)
        self.auteur = Auteur(auteur)
        self.profondeur = profondeur
        self.membres = {}
        
        dict_auteurs_1=self.auteur_central.cite(self.profondeur)
        dict_auteurs_2=self.auteur_central.influences(self.profondeur)
        #On a les liste des auteurs cités l'auteur central et ceux qui le citent, on cherche ensuite ceux qui sont dans les deux 
        liste_auteurs = list(set(dict_auteurs_1.keys()) & set(dict_auteurs_2.keys()))
        #Construisons ensuite le dictionnaire {auteur : influence} où influence est la moyenne des influences vers l'auteur et depuis l'auteur
        for auteur in liste_auteurs:
            self.membres[auteur] = (dict_auteurs_1[auteur] + dict_auteurs_2[auteur]) / 2
                    
    def graph(self):
        """
        """
        g = nx.Graph()
        #On trace les relations entre l'auteur central et les membres de la communautés (pour le moment j'utilise un attribut weight)
        g.add_edges_from([(self.auteur_central,membre_i,{'weight': self.membres[membre_i]}) for membre_i in self.membres.keys()])

        plt.figure()
        nx.draw(g)
        plt.show()
        return


    '''# la matrice d'adjacence exporté fais plus de 300Mo => FBI
    def mat_adj(self, N):
        mat_adj=pd.DataFrame()
        n = len(data2)
        mat = np.zeros((n,n), int)
        auteurs = list(data2.index)

        # création d'un DF avec le nom des auteurs en index et colonnes
        mat_adj = pd.DataFrame(mat, index=auteurs, columns=auteurs, dtype=float) # memory_usage : 112608*2
        return mat_adj

        # ligne par ligne on fait +1 lorsque un auteur est cité
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
test=Auteur('C.Itzykson')
test.cite(3)

