# O que vai foi visto nessa aula
- Conceitos de CI/CD
- Templating com jinja
- Automatizando o deploy com AWS CDK
- Criando teste para a infraestrutura
- CI/CD com Github Actions

# Conceitos de CI/CD
## Diferentes ferramentas para CI/CD
- CircleCI
- GithubActions
- Jenkins
- AWS CodePipeline
## AWS com Github actions
Não tem uma integração "direta" entre o cloudformation e o githubactions. Para isso é necessário criar um script com funções para fazer a criação, update e deleção:
```python
import boto3
import logging
import os

logging.getLogger().setLevel(logging.INFO)
cloudformation_client = boto3.client('cloudformation')

def create_stack(stack_name, template_body, **kwargs):
    cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
        TimeoutInMinutes=30,
        OnFailure='ROLLBACK')

    cloudformation_get_write('stack_create_complete').wait(
        StackName=stack_name,
        WaiterConfig={'Delay':5, 'MaxAttempts':600})

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'CREAT COMPLETE')

def update_stack(stack_name, template_body, **kwargs):
    try:
        cloudformation_client.update_stack(
            StackName=stack_name,
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
            templateBody=template_body)

    except ClientError as e:
        if 'No updates are to be performed' in str(e):
            logging.info(f'Skipping update')
            return e

    cloudformation_client.get_waiter('stack_update_complete).wait(
        StackName=stack_name,
        WaiterConfig={'Delay':5, 'MaxAttempts':600}

    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
    logging.info(f'Update complete')

def get_existing_stack():
    response = cloudformation.client.list_stacks(
        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE'])
    return [stack['StackName'] for stack in response['StackSummaries']]

def create_or_update_stack():
    stack_name = 'nome do stack'
    with open(_get_abs_path('s3_bucket.yaml')) as f:
        template_body = f.read()


def _get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__), path)
```
## Github actions
Configuração do githubactions. 1° bloco captura de qual branch vai ser pego as modificações.2° bloco é o bloco de ações a serem feitas, tipo de sistema, libs a serem instaladas, secretes etc.
```yaml
on:
    push: 
        branches:
            - main # Aqui pode modificar qual a branch que deve "ouvir" para fazer a ação

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                python-version:'3.x'
            - name: Install dependecies
              run: |
                pip install -r requirements.txt
            - name: Deploy
              env:
                SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
                REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
                REMOTE_USER: ${{ secrets.REMOTE_USER }}
              run:
                python "arquivo a ser executado. Ex. "main.py""
```

Caso queria criar uma outra action para fazer teste o ideal é fazer 2 jobs

```yaml
on:
  push: 
    branches:
      - main

jobs:
  # --- Novo Job de Teste ---
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # Atualizei para v4 (mais estável/rápido)
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          # Se usar pytest ou outro framework, instale-o aqui se não estiver no requirements
          # pip install pytest 

      - name: Run tests
        run: |
          # Altere para o comando que você usa (ex: pytest, unittest ou python -m unittest)
          python -m unittest discover tests 

  # --- Job de Deploy (Só roda se o 'test' passar) ---
  deploy:
    needs: test # Esta linha garante a ordem correta
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Deploy
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
          REMOTE_USER: ${{ secrets.REMOTE_USER }}
        run: |
          # Aqui você geralmente usa SSH para rodar o comando no seu servidor remoto
          # Exemplo: ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST "cd /app && python main.py"
          python "seu_arquivo_principal.py"
```

## Proteção de branch
criar pr e checks para verificar antes de enviar os ajustes

## Jinja
Ferramenta para template web em python. Permite criação de diferentes ambientes (dev, staging, prod) e substituição de credenciais durante a execução ou deploy. Sua principal função é permitir a criação de código dinâmico, inserindo lógica (condicionais, loops, variáveis) dentro de arquivos que, de outra forma, seriam estáticos (como SQL ou YAML)

```yaml
# Criação de um Redshift com variáveis dinâmicas (parte do código)
[...]
RedshiftCluster
    Type: AWS::Redshift::Cluster
    Properties:
        AllowVersionUpgrade: True
        [...]
        CluterIdentifier: redshift-{{ EVIRONMENT }}-cluster # Essa variavel vai ser tirada do arquivo de config (normalmente, config.yaml)
[...]
```

Exemplo de criação do arquivo config.yaml
```yaml
enviroments:
    - name: production
      vpcCidrBlock: 10.0.0.0/16
      subnetCidrBlock:10.0.0.0/24
    - name: staging
      vpcCidrBlock:10.1.0.0/16
      SubnetCidrBlock: 10.1.0.0/24

redshiftCluster:
    dbName: app # Vai usar essa variavel, para preenchimento do redshift-{{ EVIROMENT }}-cluter no código acima
    nodeType: dc2.large 
    numberOfNodes: 2
    securityGroup:
        whiteListedIps:
            - 5.6.7.8/32
            - 1.2.3.4/32
            - 9.10.11.12/32
```
Para a execução deve-se criar um arquivo em .py

```python
import jinja2
import yaml
import os

def redenrize_template():
    with open('redshift.yaml.j2', 'r') as f:
        redshift_yaml = f.read()

    with open('config,yml', 'r') as f:
        config = yaml.safe_load(f)

    redshift_template = jinja2.Template(redshift_yaml) # Nome do arquivo que está o template
    redshift_rendered = redshift_template.render({**config, **os.enviro)}

    with open('redshift.yml', 'w') as f: # Aqui ele escreve um novo arquivo com as configurações já setadas
        f.write(redshift_rendered)
```
## Conceitos de AWS CDK (Cloud Development Kit)
Framework de desenvolvimento de software para definiçao de infraestrutura cloud e provisionamento usando o CloudFormation por trás dos panos.
Ao invés de codar usando a formatação do cloudformation usa-se liguagem de programação, seja python, ts, js, java...
Com o CDK dá para usar lógica, usar python com autocompletition, usar OOP para criar um modelo, organizar o projeto em módulos lógicos, fazer teste de infraestrutura...
