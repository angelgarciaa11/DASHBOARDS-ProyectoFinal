import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from sqlalchemy import create_engine
from dash import dash_table
from dash.dash_table.Format import Group

#nos conectamos a la base de datos que es nike en sql
USER = "root"
PASSWORD = "12345678"
HOST = "localhost"
PORT = "3306"
DATABASE = "nike_db"
cadena_con = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(cadena_con)

#cargamos los datos
query = """
SELECT p.nombre, p.precio, g.nombre_genero AS genero, c.nombre_categoria AS categoria
FROM productos p
JOIN generos g ON p.id_genero = g.id_genero
JOIN categorias c ON p.id_categoria = c.id_categoria
"""
df = pd.read_sql(query, engine)

#cargamos las vistas despues que tenemos
vista1 = pd.read_sql("SELECT * FROM vista_resumen_general", engine)
vista2 = pd.read_sql("SELECT * FROM vista_precio_categoria_genero", engine)
vista3 = pd.read_sql("SELECT * FROM vista_detalle_productos", engine)

#aqui se encuentran los datos en las graficas
conteo_categoria = df["categoria"].value_counts().reset_index()
conteo_categoria.columns = ["categoria", "count"]
conteo_genero = df["genero"].value_counts().reset_index()
conteo_genero.columns = ["genero", "count"]
precio_promedio = df.groupby("categoria")["precio"].mean().reset_index()
conteo_cross = df.groupby(["categoria", "genero"]).size().reset_index(name="count")
precio_cross = df.groupby(["categoria", "genero"])["precio"].mean().reset_index()
heatmap_data = precio_cross.pivot(index="categoria", columns="genero", values="precio")

#estilos para el dashboard
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem",
    "background-color": "#1c1c1c",
    "color": "white"
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f5f5f5"
}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Nike Dashboard"

#el sidebar que vamos a utilizar
sidebar = html.Div([
    html.Div([
        html.H2("Nike Dash", className="display-6", style={"color": "#ff5f00", "marginBottom": "0.5rem"}),
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg", style={"height": "50px", "marginBottom": "10px"})
    ], style={"textAlign": "center"}),
    html.Hr(style={"borderColor": "#ff5f00"}),
    html.P("Navegación", className="lead"),
    dbc.Nav([
        dbc.NavLink("Bienvenida", href="/", active="exact"),
        dbc.NavLink("Datos Generales", href="/datos", active="exact"),
        dbc.NavLink("Comparativa por Género", href="/comparativa", active="exact"),
        dbc.NavLink("Vista General", href="/vista1", active="exact"),
        dbc.NavLink("Precios por Categoría y Género", href="/vista2", active="exact"),
        dbc.NavLink("Detalle de Productos", href="/vista3", active="exact"),
        dbc.NavLink("Sucursales", href="/sucursales", active="exact"),
    ], vertical=True, pills=True),
], style=SIDEBAR_STYLE)


content = html.Div(id="page-content", style=CONTENT_STYLE)

#usamos un layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1("NIKE DASHBOARD", style={"textAlign": "center", "fontWeight": "bold"}),
            html.H5("Just scrape it. ", style={"textAlign": "center", "color": "#ff5f00", "marginBottom": "30px"}),
            html.Img(src="https://png.pngtree.com/png-vector/20230817/ourmid/pngtree-orange-and-grey-nike-sneaker-illustration-clipart-vector-png-image_7005184.png",
                     style={"display": "block", "margin": "0 auto", "height": "150px"}),
            html.Br(),
            html.P("Este dashboard es educativo para analizar productos de la tienda oficial de Nike México.",
                   style={"textAlign": "center", "fontSize": "1.1rem"}),
            html.Br(),
            html.Div(style={
                "backgroundColor": "#ffe5d0",
                "padding": "30px",
                "borderRadius": "10px",
                "marginTop": "30px"
            }, children=[
                html.H2("Acerca de Nosotros", style={"textAlign": "center", "color": "#1c1c1c", "marginBottom": "20px"}),
                html.P("En nuestra compañía, creemos que el deporte tiene el poder de transformar vidas. Nos dedicamos a ofrecer productos que no solo representan rendimiento y estilo, sino que también impulsan una cultura global basada en el movimiento, la superación y la autenticidad.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("Desde nuestros inicios, nos hemos enfocado en algo más que solo ropa y calzado: creamos identidad. Cada uno de nuestros diseños está inspirado en atletas, artistas y comunidades que desafían lo establecido y marcan el ritmo del presente y del futuro.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("A lo largo de los años, hemos tenido el orgullo de colaborar con algunos de los nombres más influyentes del deporte y la cultura urbana. Michael Jordan, leyenda del baloncesto, marcó un antes y un después con la icónica línea Air Jordan. Travis Scott, uno de los artistas más creativos de su generación, ha llevado nuestros diseños a nuevas dimensiones con sus ediciones especiales que rompen esquemas. Y figuras como Ousmane Dembélé, entre otros atletas de élite, han confiado en nuestra marca dentro y fuera de la cancha.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("También hemos trabajado junto a otras marcas y diseñadores para crear colecciones únicas que fusionan innovación, arte y funcionalidad. Nuestra presencia no solo se siente en los estadios y escenarios, sino también en las calles, en el día a día de millones de personas que eligen destacar con cada paso que dan.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("Hoy, nuestro objetivo sigue siendo el mismo: inspirar a cada persona a alcanzar su máximo potencial. Ya sea que estés entrenando, compitiendo o simplemente expresándote a través de tu estilo, estamos contigo en cada movimiento.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("Bienvenido a nuestra plataforma de análisis, donde podrás explorar de forma visual cómo evoluciona el mundo de nuestros productos, tendencias y categorías más destacadas.", style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                dbc.Row([
                    dbc.Col(html.Img(src="https://www.flexdog.com/_next/image?url=https%3A%2F%2Fstatic.flexdog.cz%2Fflexdog%2Fbusiness%2Fimages%2Fb3a3ef74-5575-46c3-b22a-40e4059c0e4e.png&w=2400&q=90", style={"width": "100%", "borderRadius": "8px"}), md=4),
                    dbc.Col(html.Img(src="https://imagenes.elpais.com/resizer/v2/BKZDZY4PVBBW5PB3C4AK52OIDY.jpg?auth=f4b1f0ed6fe3310c02b521356820bd12a0f470da68bdb8c520c20435aa62ddc8&width=1200", style={"width": "100%", "borderRadius": "8px"}), md=4),
                    dbc.Col(html.Img(src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjH6k2BnKshfuZTM6_needoTjy33_2RIFo6E6oEHlnq6Mls54AXoFS-TV_R9e7ychb9Kkw0xSmuUqKlInPLl6O-Rh_UckuyLewB1qwSFblAwdPBIpbv6ef1FQ4V2G0oKCWi2NUhekbdojk/s1600/dembele-boots+%25284%2529.jpg", style={"width": "100%", "borderRadius": "8px"}), md=4),
                ])
            ])
        ])

    elif pathname == "/datos":
        return html.Div([
            html.Img(src="https://images.seeklogo.com/logo-png/55/1/nike-logo-png_seeklogo-550585.png", style={"width": "120px", "float": "right"}),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.pie(df, names="genero", title="Distribución por género", color_discrete_sequence=["#ff5f00", "#1c1c1c"])), md=6),
                dbc.Col(dcc.Graph(figure=px.bar(conteo_categoria, x="categoria", y="count", title="Cantidad por categoría", color_discrete_sequence=["#1c1c1c"])), md=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.bar(conteo_genero, x="genero", y="count", title="Total por género", color_discrete_sequence=["#ff5f00"])), md=6),
                dbc.Col(dcc.Graph(figure=px.bar(precio_promedio, x="categoria", y="precio", title="Precio promedio", color_discrete_sequence=["#1c1c1c"])), md=6),
            ]),
        ])

    elif pathname == "/comparativa":
        return html.Div([
            html.Img(src="https://images.seeklogo.com/logo-png/9/2/nike-logo-png_seeklogo-99486.png",
                     style={"width": "120px", "float": "right"}),

            #grafico de barras
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.bar(
                    conteo_cross,
                    x="categoria",
                    y="count",
                    color="genero",
                    barmode="group",
                    title="Productos por género",
                    color_discrete_sequence=["#1c1c1c", "#ff5f00"]
                )), md=12)
            ]),

            #grafica dos
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.pie(
                    conteo_genero,
                    names="genero",
                    values="count",
                    title="Distribución de Productos por Género",
                    color_discrete_sequence=["#1c1c1c", "#ff5f00"]
                )), md=12)
            ]),

            #grafica tres
            dbc.Row([
                dbc.Col(dcc.Graph(figure=px.bar(
                    precio_cross,
                    x="categoria",
                    y="precio",
                    color="genero",
                    title="Precio Promedio por Categoría y Género",
                    barmode="stack",
                    color_discrete_sequence=["#1c1c1c", "#ff5f00"]
                )), md=12)
            ])
        ])


    elif pathname == "/vista1":
        return html.Div([
            html.Div([
                html.Img(
                    src="https://png.pngtree.com/png-vector/20230728/ourmid/pngtree-nike-clipart-cartoon-nike-logo-graphic-vector-cartoon-illustration-of-nike-png-image_6811260.png",
                    style={"width": "100px", "float": "right"}
                ),
                html.H2("Vista General de Resumen", style={
                    "textAlign": "center",
                    "color": "#1c1c1c",
                    "marginBottom": "1.5rem",
                    "fontWeight": "bold"
                }),
            ]),

            dbc.Row([
                dbc.Col(html.Div([
                    html.Img(
                        src="https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/051d4f65-bf73-4814-b47c-ce62dc74bfc0/M+NK+DF+STD+ISS+PO+HOODIE.png",
                        style={
                            "width": "100%",
                            "borderRadius": "15px",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                            "marginBottom": "20px"
                        }
                    )
                ]), md=6),

                dbc.Col(html.Div([
                    html.Img(
                        src="https://beatnightmx.com/wp-content/uploads/2019/09/Nike-Air-Max-270-React-750x400.jpg",
                        style={
                            "width": "100%",
                            "borderRadius": "15px",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                            "marginBottom": "20px"
                        }
                    )
                ]), md=6)
            ]),

            html.Br(),

            html.Div([
                html.H4("Resumen General", style={
                    "textAlign": "center",
                    "marginBottom": "1rem",
                    "color": "#ff5f00"
                }),
                dbc.Table.from_dataframe(
                    vista1,
                    striped=True,
                    bordered=False,
                    hover=True,
                    responsive=True,
                    color=None,
                    className="table table-hover table-sm"
                )
            ], style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                "marginTop": "2rem"
            }),

            html.Div([
                html.Br(),
                html.Img(
                    src="https://www.lavanguardia.com/files/og_thumbnail/uploads/2019/03/14/5fa521c8100fc.jpeg",
                    style={
                        "width": "100%",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)",
                        "marginTop": "2rem"
                    }
                )
            ]),

            html.Div([
                html.Br(),
                html.H4("Explora más", style={
                    "textAlign": "center",
                    "color": "#1c1c1c",
                    "marginBottom": "1.5rem"
                }),
                dbc.Row([
                    dbc.Col(html.A([
                        html.Img(
                            src="https://static.nike.com/a/images/w_1280,q_auto,f_auto/354d14df-3286-44e6-afbf-debaf283d320/fecha-de-lanzamiento-del-air-jordan-1-low-x-travis-scott-sail-and-ridgerock-dm7866-162.jpg",
                            style={
                                "width": "100%",
                                "borderRadius": "15px",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                                "transition": "transform 0.3s",
                                "cursor": "pointer"
                            }
                        )
                    ], href="https://www.nike.com/", target="_blank"), md=6),

                    dbc.Col(html.A([
                        html.Img(
                            src="https://static.vecteezy.com/system/resources/thumbnails/049/668/138/small_2x/nike-air-max-exceed-running-shoes-orange-and-blue-comfortable-and-stylish-with-a-transparent-background-png.png",
                            style={
                                "width": "100%",
                                "borderRadius": "15px",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                                "transition": "transform 0.3s",
                                "cursor": "pointer",
                                "backgroundColor": "#ffffff",
                                "padding": "10px"
                            }
                        )
                    ], href="https://www.nike.com/mx/", target="_blank"), md=6)
                ], style={"marginTop": "2rem", "marginBottom": "2rem"})
            ])
        ])




    elif pathname == "/vista2":
        try:

            columnas_requeridas = ["nombre", "url_producto", "precio", "genero", "categoria"]
            if all(col in vista2.columns for col in columnas_requeridas):
                df_v2 = vista2.dropna(subset=["nombre", "url_producto"]).copy()
                df_v2["nombre_link"] = df_v2.apply(
                    lambda row: f"[{row['nombre']}]({row['url_producto']})", axis=1
                )

                return html.Div([
                    html.H3("Precios Promedio por Categoría y Género", style={"color": "#1c1c1c"}),

                    dash_table.DataTable(
                        columns=[
                            {"name": "Producto", "id": "nombre_link", "presentation": "markdown"},
                            {"name": "Precio", "id": "precio"},
                            {"name": "Género", "id": "genero"},
                            {"name": "Categoría", "id": "categoria"},
                        ],
                        data=df_v2[["nombre_link", "precio", "genero", "categoria"]].to_dict("records"),
                        style_table={"overflowX": "auto", "marginTop": "20px"},
                        style_cell={"textAlign": "left", "fontFamily": "Arial", "padding": "10px", "fontSize": "15px"},
                        style_header={"backgroundColor": "#1c1c1c", "color": "white", "fontWeight": "bold"},
                    )
                ])
            else:
                return html.Div([
                    html.H4("La vista2 no contiene todas las columnas requeridas.", style={"color": "red"}),
                    html.Pre(f"Columnas actuales: {list(vista2.columns)}")
                ])
        except Exception as e:
            return html.Div([
                html.H4("Error inesperado en vista2.", style={"color": "red"}),
                html.Pre(str(e))
            ])




    elif pathname == "/vista3":
        return html.Div([
            html.H3("Detalle de Productos", style={"color": "#1c1c1c"}),
            dbc.Table.from_dataframe(vista3.head(50), striped=True, bordered=True, hover=True, color="dark"),
            html.P("Mostrando los primeros 50 productos."),
        ])

    elif pathname == "/sucursales":
        sucursales_df = pd.read_sql("SELECT * FROM sucursales", engine)
        return html.Div([
            html.Div([
                html.H1("SUCURSALES NIKE MÉXICO", style={
                    "color": "white",
                    "textAlign": "center",
                    "padding": "1.5rem",
                    "fontWeight": "bold",
                    "fontSize": "2.5rem",
                    "backgroundColor": "rgba(0, 0, 0, 0.6)"
                }),
                html.Img(
                    src="https://media.fashionnetwork.com/cdn-cgi/image/fit=contain,width=1000,height=1000,format=auto/m/3e33/79d7/a885/c85f/d9bf/d3e7/3e4a/304b/da1d/fc11/fc11.jpeg",
                    style={
                        "width": "100%",
                        "height": "auto",
                        "marginBottom": "1rem",
                        "borderRadius": "10px"
                    }
                )
            ], style={"position": "relative"}),

            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Img(
                        src="https://static.nike.com/a/images/f_auto/6cec080e-ee9d-4889-b668-6a36fedd8f7f/image.jpg",
                        style={"width": "100%", "borderRadius": "10px"}
                    ), md=6),
                    dbc.Col(html.Img(
                        src="https://static.nike.com/a/images/f_auto/dc5326f0-b1b3-4af9-8d4e-94f404b30f0a/image.jpeg",
                        style={"width": "100%", "borderRadius": "10px"}
                    ), md=6)
                ], style={"marginTop": "2rem"}),

                html.Br(),

                html.H4("Listado de Sucursales", style={
                    "textAlign": "center",
                    "marginTop": "2rem",
                    "color": "#1c1c1c"
                }),
                dbc.Table.from_dataframe(sucursales_df, striped=True, bordered=True, hover=True, color="dark"),

                html.Br(),

                html.Div([
                    html.H5("📍 Sucursal Destacada: Tijuana", style={
                        "textAlign": "center",
                        "color": "#ff5f00",
                        "marginTop": "2rem"
                    }),
                    html.P("Tijuana - Blvd. Gustavo Díaz Ordaz 13325, Fracc. Las Palmas. Tel: +52 664 621 1507", style={
                        "textAlign": "center",
                        "color": "#1c1c1c",
                        "fontSize": "1rem"
                    }),
                    html.Div([
                        html.A(
                            html.Img(
                                src="https://lh3.googleusercontent.com/gps-cs-s/AC9h4nrB7zdrQCqyHlrOl1TNDJgxoJzsmjyMhHVYz34qt5MxQhdk9GULlGby3gvcIFaZvPaP5qsSAuZAgDkig5wLNgewN28YorJujeIQ3vooAWiNnle50EEFiwKVyD2GJrP5wtCo64_I5Q=s1360-w1360-h1020-rw",
                                style={
                                    "width": "100%",
                                    "maxWidth": "600px",
                                    "borderRadius": "10px",
                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.2)",
                                    "margin": "0 auto",
                                    "display": "block",
                                    "cursor": "pointer"
                                }
                            ),
                            href="https://www.nike.com/mx/retail/s/nike-factory-store-tijuana",
                            target="_blank"
                        )
                    ])
                ])
            ])
        ])

    return html.Div([
        html.H1("Página no encontrada", className="text-danger"),
        html.P(f"la ruta {pathname} no existe."),
    ])

if __name__ == "__main__":
    app.run(debug=True)
