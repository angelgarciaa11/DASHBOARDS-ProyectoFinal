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



             
