
import pandas as pd
import re
import os
from collections import defaultdict
from config import fp_articles, fp_ref, nom_articles1, nom_articles2, nom_references

data=pd.read_csv(f'{nom_articles1}',sep=',',usecols=['paper_id','Authors'],index_col='paper_id')
ref=pd.read_csv(f'{nom_articles2}',sep=',',usecols=['paper_id','ref_id'],index_col='paper_id')
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



