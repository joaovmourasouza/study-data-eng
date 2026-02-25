import redis
import json
from datetime import timedelta

# Conexão
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 1. STRING: Cache simples
r.setex("produto:5001:detalhes", 3600, json.dumps({
    "nome": "Notebook Dell",
    "preco": 3500.00,
    "estoque": 15
}))

cached = r.get("produto:5001:detalhes")
print(json.loads(cached))

# 2. HASH: Dados de usuário
r.hset("user:1001", mapping={
    "nome": "Ana Silva",
    "email": "ana@email.com",
    "cidade": "São Paulo"
})
print(r.hgetall("user:1001"))

# 3. LIST: Timeline de eventos
r.lpush("timeline:user:1001", "comprou_produto", "visualizou_pagina", "login")
events = r.lrange("timeline:user:1001", 0, -1)  # últimos 10 eventos

# 4. SET: Tags únicas
r.sadd("user:1001:tags", "premium", "vip", "pioneiro")
r.sadd("user:1001:tags", "premium")  # duplicata ignorada
print(r.smembers("user:1001:tags"))

# 5. SORTED SET: Leaderboard
r.zadd("ranking_vendas", {"Ana": 150, "Carlos": 89, "Beatriz": 203})
print(r.zrevrange("ranking_vendas", 0, 2, withscores=True))  # Top 3

# 6. INCR: Contador
views = r.incr("produto:5001:views")