from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kinesis as kinesis
from bootcamp_data_platform import active_enviroment, environment
from bootcamp_data_platform.base import DataLakeBase

class  RawKinesisRole(iam.Role):
    def __init__(self, scope: cdk.Construct, deploy_env: enviroment, data_lake_raw: DataLakeBase, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.data_lake_raw = data_lake_raw
        super().__init__(scope, 
        id=f'{self.deploy_env.value}-raw-kinesis-role',
        assumed_by=iam.ServicePrincipal('kinesis.amazonaws.com'),
        description=f'Role for raw kinesis stream in {self.deploy_env.value} environment',
        **kwargs)
        self.add_to_policy(iam.PolicyStatement(
            actions=[
                's3:PutObject',
                's3:GetObject',
                's3:ListBucket'
            ],
            resources=[
                self.data_lake_raw.bucket_arn,
                f'{self.data_lake_raw.bucket_arn}/*'
            ]
        ))