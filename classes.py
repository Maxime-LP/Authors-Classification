import json
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, nom_dict 
import time
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from math import sqrt



with open(f'data/{nom_dict[0]}.json', 'r', encoding='utf-32') as file:
    dict_a = json.load(file)
with open(f'data/{nom_dict[1]}.json', 'r', encoding='utf-32') as file:
    dict_p = json.load(file)
with open(f'data/{nom_dict[2]}.json', 'r', encoding='utf-8') as file:
    dict_cite = json.load(file)
with open(f'data/{nom_dict[3]}.json', 'r', encoding='utf-8') as file:
    dict_est_cite = json.load(file)


class Auteur: #OK

    """
    Les éléments de la classe auteur possèdent un attribut name
    """

    def __init__(self, name):
        self.name = name

    def cite(self, N=1):
        """
        Entrées : nom d'un auteur, profondeur des citations
        Sorties : dictionnaire de la forme {auteur_cité : influence_sur_l'auteur}
        """
        try:
            N = int(N)
        except ValueError:
            return print('Saisir un entier naturel non nul pour la profondeur.')

        if not int(N) > 0:
            print('Saisir un entier naturel non nul pour la profondeur.')
        
        else:
            # dict final
            auteurs_cites = defaultdict(lambda:0) #Par défaut le dict associe un 0 donc si un objet e n'y est pas, auteurs_cites[e]=0. Plus rapide à tester qu'un test in
            # liste des papiers à tester au prochain rang
            papiers_rang_suivant = dict_a[self.name]

            # boucle sur les profondeurs
            for k in range(1, N+1):
                # liste des papiers cités au rang courant
                papiers_rang_courant = papiers_rang_suivant
                papiers_rang_suivant = []

                for papier in papiers_rang_courant:
                    try : # exception déclenchée si le papiet n'en cite aucun autre
                        for papier_cite in dict_cite[papier]:
                            # on ajoute le papier cité pour le rang k+1
                            papiers_rang_suivant.append(papier_cite)
                            for auteur in dict_p[papier_cite]:
                                # on ajoute le nom d'un auteur à chaque fois qu'il apparait dans un un papier cité
                                if auteur!=self.name and auteur!="":
                                    #
                                    auteurs_cites[auteur] += 1/k
                    except KeyError:
                        pass

            return auteurs_cites

    def est_cite(self, N=1):
        """
        Entrés:nom d'un auteur (self), profondeur des citations
        Sorties : dictionnaire de la forme {auteur_influencé : influence_de_self_sur_l'auteur}
        """
        try:
            N = int(N)
        except ValueError:
            return print('Saisir un entier naturel non nul pour la profondeur.')

        if not int(N) > 0:
            print('Saisir un entier naturel non nul pour la profondeur.')
        
        else:
            # dict final
            auteurs_qui_citent = defaultdict(lambda:0) #Par défaut le dict associe un 0 donc si un objet e n'y est pas, auteurs_cites[e]=0. Plus rapide à tester qu'un test in
            # liste des papiers à tester au prochain rang
            papiers_rang_suivant = dict_a[self.name]

            # boucle sur les profondeurs
            for k in range(1, N+1):
                # liste des papiers cités au rang courant
                papiers_rang_courant = papiers_rang_suivant
                papiers_rang_suivant = []

                for papier in papiers_rang_courant:
                    try:
                        for papier_qui_cite in dict_est_cite[papier]:
                            papiers_rang_suivant.append(papier_qui_cite)
                            for auteur in dict_p[papier_qui_cite]:
                                # on ajoute le nom d'un auteur à chaque fois qu'il apparait dans un un papier cité
                                if auteur!=self.name and auteur!="":
                                    #
                                    auteurs_qui_citent[auteur] += 1/k
                    except KeyError:
                        pass

        return auteurs_qui_citent


class Communaute():

    def __init__(self, auteur, profondeur):
        self.auteur_central = Auteur(auteur)
        self.auteur = Auteur(auteur)
        self.profondeur = profondeur
        self.membres = {}
        
        dict_cite = self.auteur_central.cite(self.profondeur)
        dict_est_cite = self.auteur_central.est_cite(self.profondeur)

        """ #Ou on peut aussi utiliser cette méthode plus rapide pour construire self.membre
        dict_influences = defaultdict(lambda: 0)
        for auteur in dict_cite.keys():
            tmp=Auteur(auteur).cite(self.profondeur)  #C'est un defaultdict(lambda: 0), le test !=0 est plus rapide que le test in keys()
            if tmp[self.auteur_central.name]!=0:
                dict_influences[auteur]+=tmp[self.auteur_central.name]
        """

        #On a les liste des auteurs cités l'auteur central et ceux qui le citent, on cherche ensuite ceux qui sont dans les deux 
        liste_auteurs = list(set(dict_cite.keys()) & set(dict_est_cite.keys()))
        #Construisons ensuite le dictionnaire {auteur : influence}
        # L'influence est la moyenne des influences vers l'auteur et depuis l'auteur 
        # à laquelle on applique la fonction bijective sqrt(influence)+1 pour l'esthétisme de l'affichage
        for auteur in liste_auteurs:
            self.membres[auteur] = sqrt((dict_cite[auteur] + dict_est_cite[auteur]) / 2) + 1

                    
    def graph(self):
        """
        Affiche une représentation de la communauté autour de self pour un profondeur donnée.
        """
        print(self.membres)
        G = nx.Graph()
        #On trace les relations entre l'auteur central et les membres de la communautés (pour le moment j'utilise un attribut weight)
        G.add_edges_from([(self.auteur_central.name,membre_i,{'weight': self.membres[membre_i]}) for membre_i in self.membres.keys()])
        
        # on ajoute un attribut pos pour afficher le graph avec plotly
        pos = nx.spring_layout(G, k=0.5)
        for n, p in pos.items():
            G.nodes[n]['pos'] = p

        edge_trace = go.Scatter(
            x = [],
            y = [],
            line = dict(width=0.5, color='#888'),
            hoverinfo = 'none',
            mode = 'lines')

        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            
        node_trace = go.Scatter(
            x = [],
            y = [],
            text = [],
            mode = 'markers',
            hoverinfo = 'text',
            marker = dict(
                showscale = True,
                colorscale = 'Blues',
                color = [],
                size = 10,
                colorbar = dict(
                    thickness = 15,
                    title = 'Intensité moyenne des influences',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])


        for node in G.nodes():
            try:
                node_trace['marker']['color'] += tuple([self.membres[node]])
                node_info = node +' / Moyenne des influences : ' + str(round(self.membres[node],2))
                node_trace['text'] += tuple([node_info])
            except KeyError:
                #node_trace['marker']['color'] += tuple([self.membres[node]])
                node_info = node
                node_trace['text'] += tuple([node_info])

        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title = f'Communauté autour de l\'auteur {self.auteur_central.name}',
                titlefont = dict(size=16),
                showlegend = False,
                hovermode = 'closest',
                margin = dict(b=20,l=5,r=5,t=40),
                #annotations = [ dict(text="No. of connections",showarrow=False,xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        fig.show()
        return




# => Pour transformer un graph networkx en graph ploly:
#    https://medium.com/@anand0427/network-graph-with-at-t-data-using-plotly-a319f9898a02