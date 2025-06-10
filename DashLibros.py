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


             
