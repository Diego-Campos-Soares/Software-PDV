import sqlite3
from sqlite3 import Error


def connectarbd():
    
    try:
        conn = sqlite3.connect('bd/reserva_treinamento.db')
        return conn
    except Error as e:
        print("Erro ao conectar ao Banco de Dados:" + str(e))