#-*- coding: utf-8 -*-
import pandas as pd
import re
import os
from time import time
from main import filepath


class Article:
    def __init__(self,id,prec):
        self.id=id
        self.prec=prec #
    def quote(self):
        pass
    def is_quoted(self):
        pass

class Author:
    def __init__(self,nom):
        self.nom=nom

print(filepath)