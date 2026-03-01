# O que é engenharia de dados?
Disciplina tecnica que foca no projeto, contrução e manuteção de sistemas que coletam, processam, armazenam e disponibilza dados. Esses profissionais, sempre pensam em escalar esse sistema, qualidade e segurança dos dados.
# Analogia com engenharia de dados
Asssm como engenheiro civis garantem que a água chegue de forma confiavel na torneira, Data Eng. garatem que dados cheguem aos usuarios quando necessário.Em ambos os casos a fonte é variavel e imprevisível, assim, o sistema deve ser robosto e confiável para o fornecimento, pois o consumidor espera consistência e qualidade na entrega.
# Estrutura de dados
1. Bronze: Dados como eles são extraidos
2. Silver: Dados limpos e padronizados
3. Gold: Agregados e prontos para consumo
## Pipeline muito comum
1. Ingestão usando Python Scritps e utilizando o Airflow para fazer o orquestramento desses Scripts
2. Armazenados em um "Data Lake" (por exemplo, AWS S3) - Aqui é a camada Bronze
3. Processamento usando Spark (Jobs Spark processam grandes volumes de dados, por exemplo, calculo de métricas como ticket médio, LTV, churnrate) - Aqui a camada é Silver
4. Transformação usando o dbt - Aqui a camada é Gold
5. Disponibilização: Data warehouse otimizado para consultas analíticas; Analysts fazem queries para criar dashboards; Data scientists exportam dados para treinar modelos
# As duas etapas da Data Eng.
1. Fundação das operações: Coleta - scripts (Python + Apache airflow) que trazem dados de fontes externas; Armazenamento - bancos de dados, datalake, datawarehouse (S3, Postegress SnowFlake); processamento - Clusters, servidores, containers (Apache Spark cluster em Kubernets); Orquestração - sistemas que agendam e coordenam jobs (Airflow); Segurança - acesso, criptografia e governança (IAM, Criptografia). Uma analogia: Antes de ter carros circulando em uma rodovia é necessário planejar rotas, preparas terreno, asfaltar, instalar sinalizações e construir pontes e tuneis.
2. Construção de pipelines de dados: Dado a infraestrutura escolhida é o momento de colocar a mão na massa executando a construção do pipeline de dados; Um pipeline é uma serie de steps que Extraem, transforma e carregam os dados para um destino.
# Responsabilidades de um Data Eng.
1. Construir e manter a infraestrutura escalável: Garantir o crescimento do sistema de dados sem quebrar e resistente a falhas
2. Garantir qualidade, segurança e governança: Qualidade dos dados devem ser garantidas através de validações, valores dentro de ranges esperados e Unicidade; Segurança é garantida quando cada usuario tem acesso apenas ao que precisa, dados são criptografados e anonimizados, auditoria de logs, quem acesso e quando foi acessado
3. Otimizar custos: Gerenciamento dos custos de infraestrutura de dados. Desligamento de clusteres quando não estiverem sendo usados (auto-sacling), arquivamentos ou compreensão dos dados antigos, minimizar cross-region transfer, otimização de queries, uso de índices no db e materialized views
4. Monitoramento e manutenção de pipelines: verificação se os pipelines estão funcionando corretamento atraves de métricas como Latencia (demora para finalizar um job), Throughput volume de dados processados por hora, taxa de erro atraves de um registro percentual de erro, custo e data freshness verificação desde a última atualização
# Capitulo 3 - Fundamentos de bancos de Dados
## RDBMS - RELATIONAL DATA BASE MODEL SYSTEM
Dados organizados em tabelas (com colunas e linhas) e relações (PK e FK). 
Sendo a linguagem padrão para a manipulação a SQL (STRUCTURED QUERY LANGUAGE).
A estrutura deve ser definada antes de inserir os dados, o que permite ter consistencia garantida, otimização antecipada, porém tem pouca flexibilidade e migrações dificies e custosas.

### Integridade referencial
As relações devem ser explicidamente definidas e enforced (imposto) pelo banco. O quer isso garante? Não permite inserir um pedido com um client_id inexistente e/ou deletar um cliente todos os pedidos são deletado (fomoso CASCADE)

### Normalização
Dados são organizados para minimizar redundâncias:
- 1NF: cada célula é individual, nao tendo ligações com outras (Atomica)
- 2NF: Todos os atributos não-chave dependem da chave primária
- 3NF: Não há dependências transitivas

## No SQL
Bancos que não utiliza o modelo relacional, priorizam flexibilidade de esquema e escalabilidade, sacrificam algumas garantias acid por performace e escala.
Armazenam dados como documentos do tipo Json/Bson

## Diferença entre os tipos de bancos NoSQL
### No SQL para Documento - Documentos seguem a estrutura padrão de Json
- MongoDB
- CouchDB
- Firestore
- Elasticsearch
#### Caracteristicas:
- Schema-flexible: Cada documento pode ter estrutura diferente
- Nested Documents: Suporte natural a estruturas hierárquicas
- Arrays: Listas nativas dentro do documento
- Rich Queries: Consultas por campos aninhados
### No SQL para Chave-Valor - Armazenam pares simples de chave-valor, como um dicionário distribuído gigante.
- Redis (Padrão da industria)
- MemCached
- DynamoDB
- Cassandra
#### Caracteristicas:
- Extrema performance
- Simplicidade: Api minimalista (Get, Set, Delete)
- In-memory: Dados ficam armazenados na RAM
- Data structures: Lista, sets, sorted sets, hashes
#### Cuidado
A maioria desses dados é in-memory, ou seja, se o servidor cair antes de persistir no disco, dados serão perdidos.
#### Exemplo de código de criação
```python
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
```

### No SQL para Grafo (Nodes e Edges) - Projetados especificamente para dados com relações complexas
- Neo4j (padrão do mercado)
- ArangoDB
- AmazonNeptune
#### Casos de uso
- Redes sosicias
- Roteamento (caminhos mais curtos)
```
-- Criar nós
CREATE (ana:Pessoa {nome: "Ana Silva", email: "ana@email.com"})
CREATE (carlos:Pessoa {nome: "Carlos", email: "carlos@email.com"})
CREATE (python:Skill {nome: "Python", categoria: "programacao"})
CREATE (data_eng:Skill {nome: "Data Engineering", categoria: "dados"})

-- Criar relacionamentos
MATCH (ana:Pessoa {nome: "Ana Silva"})
MATCH (carlos:Pessoa {nome: "Carlos"})
CREATE (ana)-[:AMIGO_DE]->(carlos)

MATCH (ana:Pessoa {nome: "Ana Silva"})
MATCH (python:Skill {nome: "Python"})
CREATE (ana)-[:CONHECE {nivel: "avançado"}]->(python)

-- Consultas: Encontrar amigos de amigos
MATCH (eu:Pessoa {nome: "Ana Silva"})-[:AMIGO_DE]-(amigo:Pessoa)-[:AMIGO_DE]-(amigo_de_amigo:Pessoa)
WHERE NOT (eu)-[:AMIGO_DE]-(amigo_de_amigo)
RETURN amigo_de_amigo.nome

-- Consultas: Recomendação de skills baseada em amigos
MATCH (eu:Pessoa {nome: "Ana Silva"})-[:AMIGO_DE]-(amigo:Pessoa)-[:CONHECE]->(skill:Skill)
WHERE NOT (eu)-[:CONHECE]->(skill)
RETURN skill.nome, count(*) as frequencia
ORDER BY frequencia DESC
LIMIT 5
```
## Outros modelos NoSQL
### Banco colunares (wide-column stores)
Projetas para escalar horizontalmente, dados são priorizados pelas colunas é ideal para time-series e dados de alta throughput. Sendo os mais comuns:
- InfluxDb, TimescaleDB: otimizados para dados temporais, normalmente usados em Iot, finacial data
### Bancos multimodelos
Suportam múltiplos modelos em um único banco. Dentro de um mesmo banco pode-se aplicar o Documentos + Grafos + Key-value
- ArangoDb
- CouchBase

## OLTP vs OLAP
OLTP (Online transaction Processing) - Processamento de transações em tempo real, foco em operações CRUD, transações curtas e frequentes. Normalmente usa-se MySQL, Postgress
OLAP (Online analytical Processing) - Processamento para analises em grandes escalas foco em consultar complexas. Normalmente usa o RDS, BigQuery...
Na prática: Dados fluem do OLTP para OLAP atra´ves de pipeline ETL/ELT. O OLTP mantém o estado atual para operações enquanto o OLAP guarda o histórico para a analise

## Escolhendo o banco de dados certo
Backend - PostgreSQl
CMS/Blogs - MongoDB
Cache - Redis
Analytics - Bigquery/Snowflake/RDS
Recomendações - Neo4j
IOT - influxDB
Leaderboard gaming - Redis
Catalogo de produtos - ElasticSearch
Logs - Cassandra

De maneira geral o PostreSql resolve 80% dos casos, sendo necessário migrar para um banco de dados NoSQL se tiver um requisito específico que bancos relacionais não atendem

## Transações ACID
### O que são transações acid?
"ou todas as operações acontem, ou nenhuma acontece" - É como um "botão de desfazer mágico" Se algo der errado em "midway" o banco deve voltar ao estado original, como se nada tivesse acontecido.
### Termo "ACID"
ACID é um acrônimo para quatro propriedades que garatem a confiabilidade de transações em bancos de dados
A - Atomicity: Todas as operações acontecem ou nenhuma acontece
C - Consistency: A transação deve levar o banco de um estado válido para outro estado válidoI - Isolation: Transações concorrentes nao devem interferir umas nas outras
D - Durability: Uma vez commitada, a transação é permanente, mesmo em caso de falha
## Gerenciamento de concorrência
Deadlocks occore quando duas transações esperam recursivamnete por recursos que a outra segura. Para evitar esse tipo de problema deve-se:
1. Sempre acessar tabelas na mesma ordem de construção no script. Por exemplo:
```python
# BOM: Ordem consistente
def transferencia(conta_a, conta_b, valor):
    if conta_a > conta_b:
        lock_order = (conta_a, conta_b)
    else:
        lock_order = (conta_b, conta_a)

    for conta in lock_order:
        lock(conta)  # Lock em ordem determinística
```
2. Manter as transações mais curtas possíveis
3. Usar timeouts

# Capitulo 4 - SQL Essencial
Dominar o DML e DDL

# DDL - Data Definition Language
Comandos para criar, modificar e deletar estruturas do banco de dados
- CREATE: Cria tabelas, índices, views, etc.
```sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
```sql
CREATE DATABASE minha_base;
```
- ALTER: Modifica tabelas existentes (adicionar/remover colunas, constraints)
```sql
ALTER TABLE usuarios
ADD COLUMN data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```
- DROP: Deleta tabelas, índices, views, etc.
```sql
DROP TABLE usuarios;
```
ou
```sql
DROP DATABASE minha_base;
```
- TRUNCATE: Remove todos os registros de uma tabela de forma rápida
```sql
TRUNCATE TABLE usuarios;
```
## Tipos de dados
- Serial: Inteiro que incrementa automaticamente
- Varchar: Texto de tamanho variável
- Timestamp: Data e hora
- Boolean: Verdadeiro ou falso
- Decimal: Números com precisão decimal
- Text: Texto longo
- JSON: Dados semi-estruturados
- Array: Lista de valores

## Explicação das constraints
- Primary Key: Identificador único da tabela
- Foreign Key: Chave estrangeira que referencia outra tabela
- Unique: Valor único na coluna
- Not Null: Valor não pode ser nulo
- Check: Valor deve atender a uma condição
- Default: Valor padrão se não for informado

# DML - Data Manipulation Language
Comandos para manipular dados em tabelas
- INSERT: Insere dados em tabelas
```sql
INSERT INTO usuarios (nome, email) VALUES ('Ana Silva', 'ana@email.com');
```
- UPDATE: Atualiza dados em tabelas
```sql
UPDATE usuarios SET email = 'ana.silva@email.com' WHERE nome = 'Ana Silva';
```
- DELETE: Deleta dados de tabelas
```sql
DELETE FROM usuarios WHERE nome = 'Ana Silva';
```
- SELECT: Seleciona dados de tabelas
```sql
SELECT * FROM usuarios;
```

# DELETE vs Drop vs Truncate
## DELETE
- Remove linhas específicas
- Mantém a estrutura da tabela
- Pode ser revertido com ROLLBACK
- Mais lento
```sql
DELETE FROM usuarios WHERE nome = 'Ana Silva';
```
## TRUNCATE
- Remove todas as linhas da tabela
- Reduz o tamanho da tabela
- Não pode ser revertido com ROLLBACK
- Mais rápido
```sql
TRUNCATE TABLE usuarios;
```
## DROP
- Remove a tabela inteira
- Remove a estrutura da tabela
- Não pode ser revertido com ROLLBACK
- Mais rápido
```sql
DROP TABLE usuarios;
```