#-*- coding: utf-8 -*-
import pandas as pd
import re
import os
from collections import defaultdict

data=pd.read_csv('data.csv',sep=',',usecols=['paper_id','Authors'],index_col='paper_id')
ref=pd.read_csv('references.csv',sep=',',usecols=['paper_id','ref_id'],index_col='paper_id')
data.sort_values(by='paper_id',axis=0,inplace=True)
ref.sort_values(by='paper_id',axis=0,inplace=True) 

class Article:
    def __init__(self,given_id):
        self.id=int(given_id)
        self.ref=ref.ref_id[self.id]
        self.authors=data.Authors[self.id]

class Author:
    def __init__(self,name):
        self.name=name
        self.list_articles=data.query('self.name in data.Authors')
        """
        for paper_id in data.index:
            if self.name in data.Authors[paper_id]:
                list_articles.append(paper_id)
        self.list_articles=list_articles
        """

    def quote0(self):
        """
        Auteurs cités directement par self (prof 1)
        Retourne la liste des tuple (auteur,profondeur de la citation)
        """
        authors_quoted=[]
        for article in self.list_articles:
            for author in article.citation.authors:
                if author not in authors_quoted:
                    authors_quoted.append((author,1))
        return authors_quoted

    def quote(self,N=1):
        """
        Auteurs cités avec profondeur au plus égale à 1
        Retourne la liste des tuple (auteur,profondeur de la citation)
        """
        if N==1:
            return self.quote0()
        else:
            authors_quoted_tmp=[]
            for article in self.list_articles:
                for author in article.citation.authors:
                   authors_quoted_tmp+=author.quote(N-1)
        #suppression des doublons
        return authors_quoted_tmp

