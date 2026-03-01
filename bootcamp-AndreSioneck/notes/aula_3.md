# O que foi visto nessa aula?
- Conceitos de Data Lake
- Criando Data Lakes com IaC + Ingestão com Firehose
- Aws Glue para catalogar os dados
- Aws Athena para fazer queries sobre demanda

# O que é um Data Lake?
"Repositório" centralizado que permite armazenar dados estruturados e não estruturados em grande escala. É a partir dele que pode-se executar consultas, análises e processamentos.

Normalmente se utiliza 3 buckets para separar os dados:
- Raw: Dado mais bruto possível, sem alterações.
- Clean: Dado limpo e tratado. Utiliza-se Spark, pandas, presto. Os dados são mais otimizados para leitura, utiliza-se parquet ou delta lake.
- Processed: Dado processado e pronto para uso. Dados podem estar no db relacional ou não relacional, ou seja, pular o bucket e já enviar para o db. Ou criar um bucket e replicar os dados para o db (o ideal é nao deixar modelos de ML conectado diretamente no Redshift, pois tem problemas de performance e custo (pois a instancia é compartilhada, ou seja, se o modelo de ML fizer uma query muito pesada, pode derrubar o Redshift), o ideal é usar o S3 direto para o modelo de ML ou criar um db a parte para isso). É aqui que se utiliza o DBT para fazer as transformações.

# Particionamento em um data lake
Ajuda a reduzir os custos de processamento e melhorar a performance das consultas. Sendo muito comum particionar por data (ano, mes, dia, hora). Assim:
- Muitas partições = Baixa Performance
- Poucas partições = Baixa Performance

O recomendado é ter 150mb por partição.