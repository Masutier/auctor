import os
import pandas as pd
import sqlite3 as sql3


def db_conn():
    conn = sql3.connect('dbs/auctor.db')
    conn.row_factory = sql3.Row
    return conn


def askOne(sqlquery, add):
    try:
        conn = db_conn()
        objects = conn.execute(sqlquery, (add,)).fetchone()
        conn.commit()
        conn.close()
    except:
        
        objects = []
    return objects


def askAll(sqlquery):
    try:
        conn = db_conn()
        objects = conn.execute(sqlquery).fetchall()
        conn.close()
    except:
        objects = []
    return objects


def dbCreateLocation(location):
    contry = "Colombia"
    try:
        conn = db_conn()
        conn.execute("CREATE TABLE Location (id INTEGER PRIMARY KEY ASC, espacio, nivel, lugar, direccion, depto, ciudad, contry)")
        conn.commit()
        conn.execute("INSERT INTO Location (espacio, nivel, lugar, direccion, depto, ciudad, contry) VALUES (?, ?, ?, ?, ?, ?, ?)", (location['espacio'], location['nivel'], location['lugar'], location['direccion'], location['ciudad'], location['depto'], contry))
        conn.commit()
        conn.close()
    except:
        conn = db_conn()
        conn.execute("INSERT INTO Location (espacio, nivel, lugar, direccion, depto, ciudad, contry) VALUES (?, ?, ?, ?, ?, ?, ?)", (location['espacio'], location['nivel'], location['lugar'], location['direccion'], location['ciudad'], location['depto'], contry))
        conn.commit()
        conn.close()


def dbCreateShelf(shelf):
    try:
        conn = db_conn()
        conn.execute("CREATE TABLE Shelf (id INTEGER PRIMARY KEY ASC, estante, entrepano, id_location)")
        conn.commit()
        conn.execute("INSERT INTO Shelf (estante, entrepano, id_location) VALUES (?, ?, ?)", (shelf['estante'], shelf['entrepano'], shelf['id_location']))
        conn.commit()
        conn.close()
    except:
        conn = db_conn()
        conn.execute("INSERT INTO Shelf (estante, entrepano, id_location) VALUES (?, ?, ?)", (shelf['estante'], shelf['entrepano'], shelf['id_location']))
        conn.commit()
        conn.close()


def dbCreateContainer(container):
    try:
        conn = db_conn()
        conn.execute("CREATE TABLE Container (id INTEGER PRIMARY KEY ASC, indice, numero, contenedor, id_shelf, id_location)")
        conn.commit()
        conn.execute("INSERT INTO Container (indice, numero, contenedor, id_shelf, id_location) VALUES (?, ?, ?, ?, ?)", (container['indice'], container['numero'], container['contenedor'], container['id_shelf'], container['id_location']))
        conn.commit()
        conn.close()
    except:
        conn = db_conn()
        conn.execute("INSERT INTO Container (indice, numero, contenedor, id_shelf, id_location) VALUES (?, ?, ?, ?, ?)", (container['indice'], container['numero'], container['contenedor'], container['id_shelf'], container['id_location']))
        conn.commit()
        conn.close()


def dbCreateArticle(article):
    try:
        conn = db_conn()
        conn.execute("CREATE TABLE Article (id INTEGER PRIMARY KEY ASC, photo, name, description, type, id_container, id_shelf, id_location)")
        conn.commit()
        conn.execute("INSERT INTO Article (photo, name, description, type, id_container, id_shelf, id_location) VALUES (?, ?, ?, ?, ?, ?, ?)", (article['photo'], article['name'], article['description'], article['type'], article['id_container'], article['id_shelf'], article['id_location']))
        conn.commit()
        conn.close()
    except:
        conn = db_conn()
        conn.execute("INSERT INTO Article (photo, name, description, type, id_container, id_shelf, id_location) VALUES (?, ?, ?, ?, ?, ?, ?)", (article['photo'], article['name'], article['description'], article['type'], article['id_container'], article['id_shelf'], article['id_location']))
        conn.commit()
        conn.close()


# ************** USER *************
def db_conn_user():
    conn_user = sql3.connect('dbs/masutier.db')
    conn_user.row_factory = sql3.Row
    return conn_user


def personalData():
    conn_user = db_conn_user()
    getUserInfo = conn_user.execute("SELECT * FROM usersInfo").fetchone()
    conn_user.commit()
    conn_user.close()
    return getUserInfo
