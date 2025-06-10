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
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opciones)
    datos = []

    for pag in range(1, paginas + 1):
        url = f"{url_base}?page={pag}"
        print(f"Scrapeando {categoria} - {genero} - Página {pag}")
        navegador.get(url)
        time.sleep(2)

        productos = navegador.find_elements(By.CSS_SELECTOR, "div.product-card__body")

        for p in productos:
            try:
                nombre = p.find_element(By.CLASS_NAME, "product-card__title").text.strip()
            except:
                nombre = "Sin nombre"

            try:
                precio_texto = p.find_element(By.CLASS_NAME, "product-price").text.strip()
                precio = float(precio_texto.replace("$", "").replace(",", "").split()[0])
            except:
                precio = None

            try:
                link = p.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = ""

            datos.append({
                "nombre": nombre,
                "precio": precio,
                "genero": genero,
                "categoria": categoria,
                "url_producto": link
            })

    navegador.quit()
    return datos

    
 
