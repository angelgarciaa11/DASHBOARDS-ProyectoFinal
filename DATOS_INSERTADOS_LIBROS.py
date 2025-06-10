import pandas as pd
import mysql.connector
import re

class DBBooks:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="librosdash"
        )
        self.cur = self.con.cursor()

    
