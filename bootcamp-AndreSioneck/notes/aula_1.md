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

# Criando um bucket usando o CF

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

# Redshift
É um banco de dados Postegress que a aws provisiona uma maquina "automaticamente"

```yaml
Resources:
    MeuRedshift:
        Type: AWS::Redshift::Cluster
        Properties:
            AllowVersionUpgrade: True
            AutomatedSnapshotRetentionPeriod: 5 # Tempo em dias que será feito uma cópia
            AvailabilityZone: us-east-1a
            ClusterIdentifier: my-redshift-cluster
            ClusterParameterGroupName: !Ref RedshiftParameterGroup
            ClusterSubnetGroupName: !Ref RedshiftSubnetGroup
            VpcSecurityGroupIds:
                - !Ref RedshiftEC2SecurityGroup
            ClusterType: multi-node
            DBName: production
            Encrypted: True
            MasterUsername: admin # Não deve ficar aqui, pois esse arquivo vai subir para o Github
            MasterUserPassword: Admin1234
            NodeType: dc2.large
            NumberOfNodes: 2 # Quantidade de máquina que será usada
            PubliclyAccessible: true # Acesso público, pois o prof queria que a gente acessase também
            IamRoles:
                - !GetAtt RedshiftRole.Arn

    RedshiftRole:
        Type: AWS::IAM::Role
        Properties:
            AssumeRolePolicyDocument:
                Version: "2012-10-17"
                Statement:
                    - Effect: Allow
                      Principal:
                          Service:
                              - redshift.amazonaws.com
                      Action:
                          - sts:AssumeRole
            ManagedPolicyArns:
                - arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

    RedshiftParametersGroup: # Para criar um RDS é necessário criar um ParameterGroup e referencia-lo
        Type: AWS::Redshift::ClusterParameterGroup
        Properties:
            Description: Parameter group for redshift cluster
            ParameterGroupFamily: redshift-1.0 # Parametro padrão para o RDS
            Parameters: # De que forma quer que o banco de dados escale?
                - ParameterName: max_concurrency_scaling_cluster
                  ParameterValue: 1

    RedshiftSubnetGroup: # Da mesma forma é necessário criar um group para o subnetgroup
        Type: AWS::Redshift::ClusterSubnetGroup
        Properties:
            Description: Redshift Subnet Group
            SubnetIds:
                - !Ref RedshiftSubnet

    # Deve-se criar tbm o Subnet
    RedshiftSubnet:
        Type: AWS::EC2::Subnet
        Properties:
            AvailabilityZone: us-east-1a
            CidrBlock: 10.0.0.0/24 # Define o tamanho da subnet, ou seja, a quantidade de ips possíveis de serem acessados
            VpcId: !Ref RedshiftVPC

    RedshiftVPC:
        Type: AWS::EC2::VPC
        Properties:
            CidrBlock: 10.0.0.0/16

    RedshiftEC2SecurityGroup:
        Type: AWS::EC2::SecurityGroup
        Properties:
            GroupDescription: Security group for Redshift. Public acess
            GroupName: redshift-security-group
            SecurityGroupEgress:
                - CidrIp: 0.0.0.0/0 # Deixar dessa forma, qualquer pessoa do mundo pode acessar esse redshift
                  FromPort: 5439
                  IpProtocol: tcp
                  ToPort: 5439
            SecurityGroupIngress:
                - CidrIp: 0.0.0.0/0
                  FromPort: 5439
                  IpProtocol: tcp
                  ToPort: 5439
            VpcId: !Ref RedshiftVPC

    RedshiftVPCAttachGateway: # Conectar o RDS a internet
        Type: AWS::EC2::VPCGatewayAttachment
        Properties:
            VpcId: !Ref RedshiftVPC
            InternetGatewayId: !Ref RedshiftVPCInternetGateway

    RedshiftVPCInternetGateway:
        Type: AWS::EC2::InternetGateway

    RedshiftRouterTable:
        Type: AWS::EC2::RouteTable
        Properties:
            VpcId: !Ref RedshiftVPC

    RedshiftVPCRouter:
        Type: AWS::EC2::Route
        Properties:
            DestinationCidrBlock: 0.0.0.0/0
            GatewayId: !Ref RedshiftVPCInternetGateway
            RouteTableId: !Ref RedshiftRouterTable

    RedshiftSubnetRouterTableAssociation:
        Type: AWS::EC2::SubnetRouteTableAssociation
        Properties:
            RouteTableId: !Ref RedshiftRouterTable
            SubnetId: !Ref RedshiftSubnet
```

# Permissões
Configurações das permissões do usuarios

```yaml
Description: Cria grupo, funcao e politicas para engenheiro de dados

Resouces: 
    IamRoleDataEngineer:
        Type: AWS::IAM::Role
        Properties:
            AssumeRolePolicyDocument:
                Version: 2012-10-17
                Statement:
                    - Effect: Allow
                      Principal:
                        AWS: !Sub "arn:aws:iam::${aws::AccountId}:root" # A função "!Sub" substitui uma varivavel dentro de uma string
                      Action:
                        - sts:AssumeRole
            Description: Funcao para ser assumida por data eng
            ManagedPolicyArns:
                - !Ref IamPolicyDataEngineer
            RoleName: role-production-data-engineer

    IamPolicyDataEngineer:
        Type: AWS::IAM::ManagedPolicy
        Properties:
            Descripition: politicas par data eng
            PolicyDocument:
                Version: 2012-10-17
                Action:
                 - s3:GetBucketLocation
                 - s3:LisAllMyBuckets
                 - s3:ListBucket
                 - s3:GetObject
                Resource:
                 - arm:aws:s3:::* # Aqui está para todos os buckets, mas se quiser apenas para um bucket basta digitar o nome do bucket

    IamGroupDataEngineer:
        Type: Aws::IAM:GROUP
        Properties:
            GroupName: iam-group-data-engineer
            ManagedPolicyArns:
                - arn:aws:iam::aws:policy/ReadOnlyAcess
                - !Ref IamPolicyGroupDataEngineer

    IamPolicyGroupDataEngineer:
        Type: AWS::IAM::ManagedPolicy
        Properties:
            Description: Politicas do grupo de data eng
            PolicyDocument:
                Version: 2012-10-17
                Statement
                    - Effet: Allow
                      Action:
                        - sts:AssumeRole
                      Resource
                        - !GetAtt IamRoleDataEngineer.Arn # ARN = Amazon Resouces Name - É uma referencia interna da aws ao "id" do usuario
```
# Amazon Kiness
Produto que facilita a coleta, o processamento e analise de dados de stream. ele permite analisar dados assim que são recebigos e responder instantanemento, em vez de aguar a conclusão da coleta de dados para poder iniciar o processamento (Professor pulou essa etapa de código)
