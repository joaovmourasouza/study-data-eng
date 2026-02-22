# O que foi visto na 1° aula?
- Conceitos de AWS e CloudFormation
- Criando buckets no S3
- Criando um banco de dados Redshift
- Criando um stream de dados usando Kinesis
- Gerenciando permissões
- Conectando uma ferramenta de BI ao Redshift

# Por que infraestrutura como código?
- Velocidade, simplicidade e replicidade
- Consistencia na configuração
- Minimização de riscos, controle de versão
- Aumento na eficiência no desenvolvimento de Software
- Economia financeira, facil de ativar e desativar recursos
- Fácil de seguir e monitorar política e boas práticas

# CloudFormation X Terraform
Cloud formation é apenas para aws, enquanto Terraform é para multiplataforma. Além disso, sabendo CF fica muito mais fácil trabalhar com Terraform.

Básicamente é uma linguagem da AWS para provisionamento de infraestrutura na AWS. Criar vários serviço de forma simultanea.

## Conceito básico
Ao usar o CF você trabalha com modelos (templates) e pilhas (stack). Você cria modelos para descrever os recursos da AWS e as propriedades. Sempre que você cria um Stack, o AWS CloudFormation provisiona os recursos descritos no template.

### Template
Um modelo é um arquivo de texto formatado em Json ou Yaml para criação dos recursos da AWS. Por exemplo, em um modelo é possível descrever uma instância da EC2, como o tipo da instancia, o id etc.

### Stack
São os resutados do modelo. A partir dele pode-se criar, atualizar e excluir um conjunto de recursos.

## Criando um bucket usando o CF

Basicamente deve-se copiar as informações da documentação na aws relacionadas ao bucket.
Sendo a maioria dos parametros desncessários é possivel criar um bucket com poucas informações. Como se pode ver no código

```yaml
Description: Cria Bucket

Resources:
    MeuBucketS3:
        Type: AWS::S3::Bucket
        Properties:
            BucketName: meu_bucket_s3 # Nomes são universais, ou seja, apenas uma pessoa pode ter no mundo
```

Se quiser acressentar mais informações como criptografia, permitir para acesso publico é so acressentar. Sempre ir descendo na documentação para buscar o tipo básico, como float, integer, boolean...

```yaml
Description: Cria Bucket

Resources:
    MeuBucketS3:
        Type: AWS::S3::Bucket
        Properties:
            BucketName: meu_bucket_s3 # Nomes são universais, ou seja, apenas uma pessoa pode ter no mundo
            BucketEncryption:
                ServerSideEncryptionConfiguration:
                    ServersideEncryptionByDefault:
                        ServerSideEncryptionByDefault:
                            SSEAlgoritm: AES256
            PublicAccessBlockConfiguration:
                BlockPublicAcls: True
                BlockPublicPolicy: True
                IgnorePublicAcls: True
                RestrictPublicBuckets:True
```

Após a criação do arquivo .yaml basta ir na AWS, CloudFormation, Stacks, "Create stack", "Templeta is ready", Selecionar o arquivo que já está em algum Bucket S3 ou Enviar o arquivo selecionado, dá um nome para a Stack, Next...Next e "Criar a Stack"