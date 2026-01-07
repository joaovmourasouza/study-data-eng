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
