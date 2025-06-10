from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
#utilizamos 6 paginsa para sacar mas de 300 datos
def scrapear_rapido(genero, categoria, url_base, paginas=6):
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")

    
 
