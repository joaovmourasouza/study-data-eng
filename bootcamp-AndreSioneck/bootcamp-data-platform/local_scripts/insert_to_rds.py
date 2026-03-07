import psycopg2
from datetime import datetime
import os
from random import choice
import time

conn = psycopg2.connect(
    host="rds-orders.cluster-ro-c1f9q7j1p35v.us-east-1.rds.amazonaws.com", # Verificar esse código aqui
    user="postgres",
    password="postgres",
    database="orders",
    port="5432"
)

conn.set_session(autocommit=True)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2), created_at TIMESTAMP)")

products = ["notebook", "mouse", "keyboard", "monitor", "headphone", "webcam", "speaker", "microphone", "printer", "scanner"]

idx = 0

while True:
    cur.execute("INSERT INTO orders (name, price, created_at) VALUES (%s, %s, %s)", (choice(products), idx, datetime.now().isoformat()))
    idx += 1
    time.sleep(1)
