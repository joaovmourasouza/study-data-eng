# O que é engenharia de dados?
Disciplina tecnica que foca no projeto, contrução e manuteção de sistemas que coletam, processam, armazenam e disponibilza dados. Esses profissionais, sempre pensam em escalar esse sistema, qualidade e segurança dos dados.
## Analogia com engenharia de dados
Asssm como engenheiro civis garantem que a água chegue de forma confiavel na torneira, Data Eng. garatem que dados cheguem aos usuarios quando necessário.Em ambos os casos a fonte é variavel e imprevisível, assim, o sistema deve ser robosto e confiável para o fornecimento, pois o consumidor espera consistência e qualidade na entrega.
## Estrutura de dados
1. Bronze: Dados como eles são extraidos
2. Silver: Dados limpos e padronizados
3. Gold: Agregados e prontos para consumo
## Pipeline muito comum
1. Ingestão usando Python Scritps e utilizando o Airflow para fazer o orquestramento desses Scripts
2. Armazenados em um "Data Lake" (por exemplo, AWS S3) - Aqui é a camada Bronze
3. Processamento usando Spark (Jobs Spark processam grandes volumes de dados, por exemplo, calculo de métricas como ticket médio, LTV, churnrate) - Aqui a camada é Silver
4. Transformação usando o dbt - Aqui a camada é Gold
5. Disponibilização: Data warehouse otimizado para consultas analíticas; Analysts fazem queries para criar dashboards; Data scientists exportam dados para treinar modelos
