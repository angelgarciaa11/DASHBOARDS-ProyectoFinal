import pandas as pd
import mysql.connector

class DBNike:
   def __init__(self):
       self.con = mysql.connector.connect(
           host="localhost",
           user="root",
           password="12345678",
           database="nike_db"
       )
       self.cur = self.con.cursor()

   def insertar_generos_y_categorias(self, df):
       generos = df["genero"].unique()
       categorias = df["categoria"].unique()

       for g in generos:
           self.cur.execute("INSERT IGNORE INTO generos (nombre_genero) VALUES (%s)", (g,))
       for c in categorias:
           self.cur.execute("INSERT IGNORE INTO categorias (nombre_categoria) VALUES (%s)", (c,))
       self.con.commit()

   def obtener_id(self, tabla, columna, valor):
       nombre_id = "id_genero" if tabla == "generos" else "id_categoria"
       self.cur.execute(f"SELECT {nombre_id} FROM {tabla} WHERE {columna} = %s", (valor,))
       return self.cur.fetchone()[0]

   def insertar_productos(self, df):
       for _, fila in df.iterrows():
           id_gen = self.obtener_id("generos", "nombre_genero", fila["genero"])
           id_cat = self.obtener_id("categorias", "nombre_categoria", fila["categoria"])

           self.cur.execute("""
               INSERT INTO productos (nombre, precio, id_genero, id_categoria, url_producto)
               VALUES (%s, %s, %s, %s, %s)
           """, (fila["nombre"], fila["precio"], id_gen, id_cat, fila["url_producto"]))

       self.con.commit()
       print("Datos insertados correctamente.")

   def eliminar_duplicados_productos(self):
       self.cur.execute("""
           DELETE p1 FROM productos p1
           INNER JOIN productos p2
           WHERE
               p1.id_producto > p2.id_producto AND
               p1.nombre = p2.nombre AND
               p1.precio = p2.precio AND
               p1.id_genero = p2.id_genero AND
               p1.id_categoria = p2.id_categoria AND
               p1.url_producto = p2.url_producto
       """)
       self.con.commit()
       print("Duplicados eliminados correctamente.")

   def cerrar(self):
       self.cur.close()
       self.con.close()

if __name__ == "__main__":
   df = pd.read_csv("nike_datos_rapido_mas.csv")
   db = DBNike()
   db.insertar_generos_y_categorias(df)
   db.insertar_productos(df)
   db.eliminar_duplicados_productos()
   db.cerrar()