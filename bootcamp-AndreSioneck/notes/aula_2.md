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
