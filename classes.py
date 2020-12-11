
import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, article_auteurs, auteur_articles, article_ref

data=pd.read_csv(f'{article_auteurs}',sep=',',usecols=['paper_id','Authors'],index_col='paper_id')
data2=pd.read_csv(f'{auteur_articles}',sep=',',usecols=['paper_id','Authors'],index_col='paper_id')
ref=pd.read_csv(f'{auteur_articles}',sep=',',usecols=['paper_id','ref_id'],index_col='paper_id')
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

		
class Communaute:
	def __init__(self,auteur,profondeur):
		self.auteur=auteur
        self.profondeur=profondeur



