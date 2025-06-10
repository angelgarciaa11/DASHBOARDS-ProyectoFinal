import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from sqlalchemy import create_engine
import plotly.express as px

#CONEXIOONN
USER = "root"
PASSWORD = "12345678"
HOST = "localhost"
PORT = "3306"
DATABASE = "librosdash"
cadena_con = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(cadena_con)

#SIDEBAR
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem",
    "background-color": "#2c2f33",
    "color": "white"
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f5f5f5"
}

#SIDEBAR
sidebar = html.Div([
    html.Div([
        html.H2("BOOKSTORE", className="display-6", style={"color": "#f5c518", "marginBottom": "1rem", "textAlign": "center"}),
        html.Img(
            src="https://images.vexels.com/media/users/3/255333/isolated/preview/1ab1c05d2e8b34c0b0688b0de27fa540-dibujos-animados-de-libros-escolares.png",
            style={"height": "100px", "display": "block", "margin": "0 auto", "marginBottom": "20px"}
        )
    ]),
    html.Hr(style={"borderColor": "#f5c518"}),
    html.P("Navegación", className="lead", style={"textAlign": "center"}),

    dbc.Nav([
        dbc.NavLink("Bienvenida", href="/", active="exact"),
        dbc.NavLink("Top 50 Libros", href="/top50", active="exact"),
        dbc.NavLink("Libros por Género", href="/generos", active="exact"),
        dbc.NavLink("Análisis de Precios", href="/precios", active="exact"),
        dbc.NavLink("Editoriales", href="/editoriales", active="exact"),
        dbc.NavLink("Stock Disponible", href="/stock", active="exact"),
        dbc.NavLink("Libros con Rating Alto", href="/ratings", active="exact"),
        dbc.NavLink("Gráfica Comparativa", href="/comparativa", active="exact"),
        dbc.NavLink("Resumen General", href="/resumen", active="exact"),
        dbc.NavLink("Sitio Web", href="/sitioweb", active="exact"),
    ], vertical=True, pills=True),
], style=SIDEBAR_STYLE)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Bookstore Dashboard"

#LAYOUT_PRINCIPAL
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id="page-content", style=CONTENT_STYLE)
])

#caLLback que utilizaremos
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1("¡Bienvenido a BOOKSTORE!", style={"textAlign": "center", "fontWeight": "bold", "color": "#2c2f33"}),
            html.P("Somos una plataforma apasionada por los libros y la tecnología.", style={"textAlign": "center", "fontSize": "1.1rem"}),
            html.Br(),
            html.Div(style={
                "backgroundColor": "#fdf6e3",
                "padding": "30px",
                "borderRadius": "10px",
                "marginTop": "30px"
            }, children=[
                html.H2("Acerca de Nosotros", style={"textAlign": "center", "color": "#2c2f33"}),
                html.P("En BOOKSTORE creemos que un buen libro puede cambiar tu mundo. Somos una plataforma que no solo vende libros, sino que permite hacer scraping y análisis de datos para descubrir tendencias en la literatura.",
                       style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("Nuestra pasión por los libros va más allá de las ventas. Nos enfocamos en ofrecer acceso a los títulos más relevantes, más vendidos y mejor calificados en el mercado, con herramientas digitales que hacen de la experiencia algo interactivo.",
                       style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                html.P("Desde novelas clásicas hasta lanzamientos recientes, tenemos algo para todos los gustos. ¡Explora, analiza y encuentra tu próximo libro favorito!",
                       style={"textAlign": "justify", "margin": "0 auto", "maxWidth": "900px"}),
                html.Br(),
                dbc.Row([
                    dbc.Col(html.A(html.Img(
                        src="https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg",
                        style={"width": "100%", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)", "cursor": "pointer"}
                    ), href="https://books.toscrape.com/index.html", target="_blank"), md=4),
                    dbc.Col(html.A(html.Img(
                        src="https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg",
                        style={"width": "100%", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)", "cursor": "pointer"}
                    ), href="https://books.toscrape.com/index.html", target="_blank"), md=4),
                    dbc.Col(html.A(html.Img(
                        src="https://books.toscrape.com/media/cache/97/27/97275841c81e66d53bf9313cba06f23e.jpg",
                        style={"width": "100%", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)", "cursor": "pointer"}
                    ), href="https://books.toscrape.com/index.html", target="_blank"), md=4),
                ], style={"marginTop": "2rem"})
            ])
        ])

    elif pathname == "/top50":
        try:
            query = """
                SELECT titulo, precio, url_libro
                FROM libros
                WHERE titulo IS NOT NULL AND precio IS NOT NULL
                ORDER BY precio DESC
                LIMIT 50
            """
            top50_df = pd.read_sql(query, engine)

            if top50_df.empty:
                return html.Div([html.H4("No hay datos disponibles para el Top 50.", style={"color": "red", "textAlign": "center"})])
                df_plot = top50_df.copy()
            df_plot["titulo_corto"] = df_plot["titulo"].str.slice(0, 30) + "..."

            fig_top50 = px.bar(
                df_plot.sort_values(by="precio", ascending=True),
                x="precio", y="titulo_corto",
                orientation="h",
                title="Top 50 Libros más Caros",
                labels={"precio": "Precio", "titulo_corto": "Título"},
                height=900,
                template="plotly_white"
            )

            return html.Div([
                html.H2("Top 50 Libros", style={"textAlign": "center", "marginBottom": "2rem", "color": "#2c2f33"}),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src="https://media.transformanceadvisors.com/unique/top-50-03.png",
                                style={"width": "160px", "display": "block", "margin": "0 auto 15px", "borderRadius": "10px", "boxShadow": "0 2px 6px rgba(0,0,0,0.2)"}
                            ),
                            html.P("Representación Top 50", style={"textAlign": "center", "fontSize": "0.85rem", "color": "#666", "marginBottom": "20px"}),
                            html.Div([
                                html.H5("Listado de Libros", style={"marginBottom": "1rem", "color": "#2c2f33"}),
                                dbc.Table.from_dataframe(
                                    top50_df[["titulo", "precio", "url_libro"]],
                                    striped=True, bordered=True, hover=True, responsive=True,
                                    style={"fontSize": "0.9rem"}
                                )
                            ], style={
                                "maxHeight": "720px",
                                "overflowY": "auto",
                                "backgroundColor": "#ffffff",
                                "padding": "10px",
                                "borderRadius": "8px",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.05)"
                            })
                        ])
                    ], md=6),

                    dbc.Col([
                        html.Div([dcc.Graph(figure=fig_top50)], style={
                            "backgroundColor": "#ffffff",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.05)"
                        })
                    ], md=6),
                ], style={"marginBottom": "2rem"})
            ], style={"backgroundColor": "#fdf6e3", "padding": "30px", "borderRadius": "10px", "boxShadow": "0 4px 10px rgba(0,0,0,0.05)"})

        except Exception as e:
            return html.Div([
                html.H4("Error al cargar Top 50", style={"color": "red"}),
                html.Pre(str(e))
            ])

    elif pathname == "/generos":
        try:
            query = """
                SELECT c.nombre_categoria AS categoria, COUNT(*) AS total
                FROM libros l
                JOIN categorias c ON l.id_categoria = c.id_categoria
                GROUP BY c.nombre_categoria
                ORDER BY total DESC
            """
            df_categorias = pd.read_sql(query, engine)
            top20 = df_categorias.head(20)

            fig_bar = px.bar(
                top20.sort_values(by="total", ascending=True),
                x="total", y="categoria",
                orientation="h",
                title="Top 20 Categorías con Más Libros",
                labels={"total": "Cantidad", "categoria": "Categoría"},
                template="plotly_white",
                height=500
            )

            fig_pie = px.pie(
                top20,
                values="total", names="categoria",
                title="Distribución Porcentual (Top 20 Categorías)",
                template="plotly_white",
                hole=0.3
            )

            return html.Div([
                html.H2("Libros por Categoría", style={"textAlign": "center", "marginBottom": "1.5rem", "color": "#2c2f33"}),
                dcc.Graph(figure=fig_bar),
                dcc.Graph(figure=fig_pie)
            ], style={"backgroundColor": "#fdf6e3", "padding": "30px", "borderRadius": "10px"})

        except Exception as e:
            return html.Div([
                html.H4("Error al cargar datos de categoría", style={"color": "red"}),
                html.Pre(str(e))
            ])

    elif pathname == "/precios":
        try:
            query = """
                SELECT l.titulo, l.precio, c.nombre_categoria AS categoria
                FROM libros l
                JOIN categorias c ON l.id_categoria = c.id_categoria
                WHERE l.precio IS NOT NULL
            """
            df_precios = pd.read_sql(query, engine)

            df_prom = df_precios.groupby("categoria").agg(precio_promedio=("precio", "mean")).reset_index()

            fig_prom = px.bar(
                df_prom.sort_values(by="precio_promedio", ascending=True),
                x="precio_promedio", y="categoria",
                orientation="h",
                title="Precio Promedio por Categoría",
                labels={"precio_promedio": "Precio Promedio", "categoria": "Categoría"},
                height=500,
                color="categoria",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig_hist = px.histogram(
                df_precios,
                x="precio",
                nbins=20,
                title="Distribución de Precios de Libros",
                labels={"precio": "Precio"},
                height=400,
                color_discrete_sequence=["#f4a261"]
            )

            return html.Div([
                html.H2("Análisis de Precios",
                        style={"textAlign": "center", "color": "#2c2f33", "marginBottom": "2rem"}),
                dcc.Graph(figure=fig_prom),
                dcc.Graph(figure=fig_hist)
            ], style={"backgroundColor": "#fdf6e3", "padding": "30px", "borderRadius": "10px"})

        except Exception as e:
            return html.Div([
                html.H4("Error al cargar Análisis de Precios", style={"color": "red"}),
                html.Pre(str(e))
            ])


    elif pathname == "/editoriales":
        try:
            query = """
                    SELECT titulo, url_libro
                    FROM libros
                    WHERE titulo IS NOT NULL AND url_libro IS NOT NULL
                    ORDER BY titulo ASC
                    LIMIT 100
                """
            df_catalogo = pd.read_sql(query, engine)

            #]
            filas = []
            for _, row in df_catalogo.iterrows():
                filas.append(html.Tr([
                    html.Td(html.A(row["titulo"], href=row["url_libro"], target="_blank"))
                ]))

            return html.Div([
                html.H2("Catálogo de Libros",
                        style={"textAlign": "center", "color": "#2c2f33", "marginBottom": "2rem"}),

                dbc.Row([
                    dbc.Col(html.Img(
                        src="https://books.toscrape.com/media/cache/91/a4/91a46253e165d144ef5938f2d456b88f.jpg",
                        style={"width": "100%", "borderRadius": "10px", "marginBottom": "15px",
                               "boxShadow": "0 2px 6px rgba(0,0,0,0.2)"}
                    ), md=4),
                    dbc.Col(html.Img(
                        src="https://books.toscrape.com/media/cache/b1/0e/b10eabab1e1c811a6d47969904fd5755.jpg",
                        style={"width": "100%", "borderRadius": "10px", "marginBottom": "15px",
                               "boxShadow": "0 2px 6px rgba(0,0,0,0.2)"}
                    ), md=4),
                    dbc.Col(html.Img(
                        src="https://books.toscrape.com/media/cache/6b/07/6b07b77236b7c80f42bd90bf325e69f6.jpg",
                        style={"width": "100%", "borderRadius": "10px", "marginBottom": "15px",
                               "boxShadow": "0 2px 6px rgba(0,0,0,0.2)"}
                    ), md=4),
                ], style={"marginBottom": "2rem"}),

                html.Div([
                    html.H5("Listado interactivo de libros", style={"marginBottom": "1rem", "color": "#2c2f33"}),
                    dbc.Table([
                        html.Thead(html.Tr([html.Th("Título")])),
                        html.Tbody(filas)
                    ], bordered=True, hover=True, responsive=True, striped=True, className="table-sm")
                ], style={
                    "backgroundColor": "#ffffff",
                    "padding": "15px",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 10px rgba(0,0,0,0.05)"
                })
            ], style={"backgroundColor": "#fdf6e3", "padding": "30px", "borderRadius": "10px"})

        except Exception as e:
            return html.Div([
                html.H4("Error al cargar el catálogo de libros", style={"color": "red"}),
                html.Pre(str(e))
            ])

    elif pathname == "/stock":
        try:
            query = """
                SELECT l.titulo, l.stock_disponible, c.nombre_categoria AS categoria
                FROM libros l
                JOIN categorias c ON l.id_categoria = c.id_categoria
                WHERE l.stock_disponible IS NOT NULL
            """
            df_stock = pd.read_sql(query, engine)

            #cateogira top 10
            df_stock_agg = (
                df_stock.groupby("categoria")
                .agg(stock_total=("stock_disponible", "sum"))
                .reset_index()
                .sort_values(by="stock_total", ascending=False)
                .head(10)
            )

            #libros con mayor stockkkkkk
            top_libros = df_stock.sort_values(by="stock_disponible", ascending=False).head(10)

            #graficaaa
            fig_bar_stock = px.bar(
                df_stock_agg,
                x="categoria", y="stock_total",
                title="Top 10 Categorías con Más Stock",
                labels={"stock_total": "Stock Disponible", "categoria": "Categoría"},
                template="simple_white",
                color_discrete_sequence=["#4682B4"]
            )

            #grafica de cake
            fig_pie_stock = px.pie(
                df_stock_agg,
                names="categoria", values="stock_total",
                title="Distribución del Stock por Categoría (Top 10)",
                hole=0.3,
                template="simple_white",
                color_discrete_sequence=px.colors.sequential.RdBu
            )

            return html.Div([
                html.H2("Stock Disponible", style={"textAlign": "center", "color": "#2c2f33", "marginBottom": "2rem"}),

                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig_bar_stock), md=6),
                    dbc.Col(dcc.Graph(figure=fig_pie_stock), md=6),
                ], style={"marginBottom": "2rem"}),

                html.Div([
                    html.H5("Top 10 Libros con Mayor Stock", style={"marginBottom": "1rem", "color": "#2c2f33"}),
                    dbc.Table.from_dataframe(
                        top_libros[["titulo", "categoria", "stock_disponible"]],
                        striped=True, bordered=True, hover=True, responsive=True,
                        style={"fontSize": "0.9rem"},
                        class_name="table-sm"
                    )
                ], style={
                    "backgroundColor": "#ffffff",
                    "padding": "15px",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 10px rgba(0,0,0,0.05)"
                })

            ], style={"backgroundColor": "#fdf6e3", "padding": "30px", "borderRadius": "10px"})

        except Exception as e:
            return html.Div([
                html.H4("Error al cargar análisis de stock", style={"color": "red"}),
                html.Pre(str(e))
            ])
    elif pathname == "/ratings":
        try:
            query = """
                SELECT l.titulo, r.nombre_rating, c.nombre_categoria AS categoria, l.precio
                FROM libros l
                JOIN rating r ON l.id_rating = r.id_rating
                JOIN categorias c ON l.id_categoria = c.id_categoria
                WHERE r.nombre_rating IS NOT NULL
            """
            df_rating = pd.read_sql(query, engine)


            rating_map = {"One": 2, "Two": 4, "Three": 6, "Four": 8, "Five": 10}
            df_rating["rating_num"] = df_rating["nombre_rating"].map(rating_map)






             
