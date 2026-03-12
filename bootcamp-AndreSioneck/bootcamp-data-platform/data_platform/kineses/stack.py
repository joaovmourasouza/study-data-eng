from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kinesis as kinesis

from data_platform.enviroment import EnviromentEnum
from data_platform.data_lake.base import DataLakeBase

class RawKinesisRole(iam.Role):
    def __init__(self, scope: Construct, deploy_env: EnviromentEnum, data_lake_raw: DataLakeBase, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.data_lake_raw = data_lake_raw
        super().__init__(
            scope, 
            id=f'{self.deploy_env.value}-raw-kinesis-role',
            assumed_by=iam.ServicePrincipal('kinesis.amazonaws.com'),
            description=f'Role for raw kinesis stream in {self.deploy_env.value} environment',
            **kwargs
        )
        self.set_policy()

    def set_policy(self) -> None:
        policy = iam.Policy(
            self,
            id=f'{self.deploy_env.value}-raw-kinesis-policy',
            policy_name=f'{self.deploy_env.value}-raw-kinesis-policy',
            statements=[
                iam.PolicyStatement(
                    actions=[
                        's3:PutObject',
                        's3:GetObject',
                        's3:ListBucket',
                        's3:AbortMultipartUpload',
                        's3:DeleteObject'
                    ],
                    resources=[
                        self.data_lake_raw.bucket_arn,
                        f'{self.data_lake_raw.bucket_arn}/*'
                    ]
                )
            ]
        )
        self.attach_inline_policy(policy)

class KinesisStack(cdk.Stack):
    def __init__(self, scope: Construct, deploy_env: EnviromentEnum, data_lake_raw: DataLakeBase, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.data_lake_raw = data_lake_raw
        super().__init__(
            scope,
            id=f'{self.deploy_env.value}-kinesis-stack',
            description=f'Kinesis stack for {self.deploy_env.value} environment',
            **kwargs)

        self.atomic_events = firehose.CfnDeliveryStream(
            self,
            id = f'firehose-{self.deploy_env.value}-raw-delivery-stream',
            delivery_stream_type='DirectPut',
            delivery_stream_name=f'firehose-{self.deploy_env.value}-raw-delivery-stream',
            extended_s3_destination_configuration=self.s3_config
        )

    @property
    def s3_config(self):
        return firehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(
            bucket_arn=self.data_lake_raw.bucket_arn,
            buffering_hints=firehose.CfnDeliveryStream.BufferingHintsProperty(
                interval_in_seconds=60,
                size_in_mbs=1
            ),
            compression_format='GZIP',
            error_output_prefix=f'{self.deploy_env.value}/errors',
            prefix=f'{self.deploy_env.value}/raw/',
            role_arn=self.raw_kinesis_role.role_arn
        )

    @property
    def kinesis_role(self):
        return RawKinesisRole(
            self,
            deploy_env=self.deploy_env,
            data_lake_raw=self.data_lake_raw
        )