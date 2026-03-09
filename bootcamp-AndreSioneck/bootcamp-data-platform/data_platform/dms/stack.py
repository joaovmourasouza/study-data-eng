import json
import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_dms as dms
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from data_platform.enviroment import EnviromentEnum
from data_platform.data_lake.base import DataLakeBase
from data_platform.common_stack import CommonStack

class RawDMSRole(iam.Role):
    def __init__(
        self,
        scope: Construct,
        deploy_env: EnviromentEnum,
        data_lake_raw_bucket: DataLakeBase,
        **kwargs
    ) -> None:
        self.deploy_env = deploy_env
        self.data_lake_raw_bucket = data_lake_raw_bucket
        super().__init__(
            scope,
            f"{self.deploy_env.value}-raw-dms-role",
            assumed_by=iam.ServicePrincipal("dms.amazonaws.com"),
            **kwargs
        )
        self.add_policy()

    def add_policy(self) -> None:
        policy = iam.Policy(
            self,
            f"{self.deploy_env.value}-raw-dms-role-policy",
            policy_name=f"{self.deploy_env.value}-raw-dms-role-policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                    ],
                    resources=[
                        self.data_lake_raw_bucket.bucket_arn,
                        f"{self.data_lake_raw_bucket.bucket_arn}/*",
                    ],
                )
            ]
        )
        self.attach_inline_policy(policy)
        
        return policy

class OrdersDMS(dms.CfnReplicationTask):
    def __init__(
        self,
        scope: Construct,
        common_stack: CommonStack,
        data_lake_raw_bucket: DataLakeBase,
        **kwargs
    ) -> None:
        self.common_stack = common_stack
        self.data_lake_raw_bucket = data_lake_raw_bucket
        
        self.raw_dms_role = RawDMSRole(
            scope,
            deploy_env=self.common_stack.enviroment,
            data_lake_raw_bucket=self.data_lake_raw_bucket,
        )

        self.rds_endpoint = dms.CfnEndpoint(
            scope,
            f"{self.common_stack.enviroment.value}-orders-rds-endpoint",
            endpoint_identifier=f"{self.common_stack.enviroment.value}-orders-rds-endpoint",
            endpoint_type="source",
            engine_name="postgres",
            username=f"postgres",
            password=f"postgres",
            database_name="orders",
            server_name=self.common_stack.orders_rds_instance.instance_endpoint.hostname,
            port=5432,
            ssl_mode="require",
            extra_connection_attributes="",
            tags=[
                cdk.CfnTag(key="Name", value=f"{self.common_stack.enviroment.value}-orders-rds-endpoint"),
            ],
        )
        
        self.s3_endpoint = dms.CfnEndpoint(
            scope,
            f"{self.common_stack.enviroment.value}-s3-endpoint",
            endpoint_identifier=f"{self.common_stack.enviroment.value}-s3-endpoint",
            extra_connection_attributes=f"DataFormat=parquet,MaxFileSize=512;timestampColumnName=created_at, includeOpForFullLoad=true",
            endpoint_type="target",
            engine_name="s3",
            s3_settings=dms.CfnEndpoint.S3SettingsProperty(
                bucket_name=self.data_lake_raw_bucket.bucket_name,
                bucket_folder=f"orders",
                service_access_role_arn=self.raw_dms_role.role_arn,
                compression_type="GZIP",
                csv_delimiter=",",
                csv_row_delimiter="\\n",
            )
        )

        self.dms_sg = ec2.SecurityGroup(
            scope,
            f"{self.common_stack.enviroment.value}-dms-sg",
            vpc=self.common_stack.vpc,
            security_group_name=f"{self.common_stack.enviroment.value}-dms-sg",
        )

        self.dms_subnet_group = dms.CfnReplicationSubnetGroup(
            scope,
            f"{self.common_stack.enviroment.value}-dms-subnet-group",
            subnet_ids=[subnet.subnet_id for subnet in self.common_stack.vpc.private_subnets],
            tags=[
                cdk.CfnTag(key="Name", value=f"{self.common_stack.enviroment.value}-dms-subnet-group"),
            ],
            replication_subnet_group_identifier=f"{self.common_stack.enviroment.value}-dms-subnet-group",
            replication_subnet_group_description="DMS Subnet Group",
        )
        
        self.instance = dms.CfnReplicationInstance(
            scope,
            f"{self.common_stack.enviroment.value}-dms-instance",
            replication_instance_class="dms.t3.micro",
            replication_subnet_group_identifier=f"{self.common_stack.enviroment.value}-dms-subnet-group",
            allocated_storage=20,
            multi_az=False,
            tags=[
                cdk.CfnTag(key="Name", value=f"{self.common_stack.enviroment.value}-dms-instance"),
            ],
            publicly_accessible=False,
            engine_version="3.5.2",
            vpc_security_group_ids = [self.dms_sg.security_group_id]            
        )

        self.instance.node.add_dependency(self.dms_subnet_group)
        self.instance.node.add_dependency(self.rds_endpoint)
        self.instance.node.add_dependency(self.s3_endpoint)
        self.instance.node.add_dependency(self.dms_sg)

        super().__init__(
            scope,
            f"{self.common_stack.enviroment.value}-dms-stack",
            replication_instance_arn=self.instance.ref,
            replication_task_identifier=f"{self.common_stack.enviroment.value}-dms-task",
            source_endpoint_arn=self.rds_endpoint.ref,
            target_endpoint_arn=self.s3_endpoint.ref,
            migration_type="full-load",
            table_mappings=json.dumps({
                "rules": [
                    {
                        "rule-type": "selection",
                        "rule-id": "1",
                        "rule-name": "1",
                        "object-locator": {
                            "schema-name": "public",
                            "table-name": "%"
                        },
                        "rule-action": "include",
                        "filters": []
                    }
                ]
            }),
            
            **kwargs
        )

class DMSStack(Stack):
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        enviroment: EnviromentEnum,
        common_stack: CommonStack,
        data_lake_raw_bucket: DataLakeBase,
        **kwargs) -> None:
        
        self.deploy_env = enviroment
        self.common_stack = common_stack
        self.data_lake_raw_bucket = data_lake_raw_bucket
        
        super().__init__(scope, construct_id, **kwargs)

        self.dms_replication_task = OrdersDMS(
            self,
            common_stack=common_stack,
            data_lake_raw_bucket=data_lake_raw_bucket,
        )