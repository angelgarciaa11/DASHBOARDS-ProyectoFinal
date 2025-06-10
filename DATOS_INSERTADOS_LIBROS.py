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

    def insertar_categorias_y_ratings(self, df):
        categorias = df["Categoría"].unique()
        ratings = df["Rating"].unique()

        for cat in categorias:
            self.cur.execute("INSERT IGNORE INTO categorias (nombre_categoria) VALUES (%s)", (cat,))
        for r in ratings:
            self.cur.execute("INSERT IGNORE INTO rating (nombre_rating) VALUES (%s)", (r,))
        self.con.commit()

    def obtener_id(self, tabla, columna, valor):
        nombre_id = "id_categoria" if tabla == "categorias" else "id_rating"
        self.cur.execute(f"SELECT {nombre_id} FROM {tabla} WHERE {columna} = %s", (valor,))
        return self.cur.fetchone()[0]

    def insertar_libros(self, df):
        for _, fila in df.iterrows():
            id_cat = self.obtener_id("categorias", "nombre_categoria", fila["Categoría"])
            id_rat = self.obtener_id("rating", "nombre_rating", fila["Rating"])


            stock = int(re.findall(r'\d+', fila["Disponibilidad"])[0]) if re.findall(r'\d+', fila["Disponibilidad"]) else 0

            self.cur.execute("""
                INSERT INTO libros (titulo, precio, id_categoria, id_rating, stock_disponible, url_libro)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fila["Título"], fila["Precio"], id_cat, id_rat, stock, fila["URL"]))

        self.con.commit()
        print("✅ Libros insertados correctamente.")

    def eliminar_duplicados_libros(self):
        self.cur.execute("""
            DELETE l1 FROM libros l1
            INNER JOIN libros l2
            WHERE
                l1.id_libro > l2.id_libro AND
                l1.titulo = l2.titulo AND
                l1.precio = l2.precio AND
                l1.id_categoria = l2.id_categoria AND
                l1.id_rating = l2.id_rating AND
                l1.url_libro = l2.url_libro
        """)
        self.con.commit()
        print("🧹 Duplicados eliminados correctamente.")

    def cerrar(self):
        self.cur.close()
        self.con.close()

if __name__ == "__main__":
    df = pd.read_csv("books_completo.csv")
    db = DBBooks()
    db.insertar_categorias_y_ratings(df)
    db.insertar_libros(df)
    db.eliminar_duplicados_libros()
    db.cerrar()

