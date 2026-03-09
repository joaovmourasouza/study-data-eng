from aws_cdk import Stack
import aws_cdk as cdk
from aws_cdk import aws_rds as rds, aws_ec2 as ec2
from constructs import Construct
from data_platform.enviroment import EnviromentEnum

class CommonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, enviroment: EnviromentEnum, **kwargs) -> None:
        self.enviroment = enviroment
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "VPC", max_azs=3)

        self.orders_rds_sg = ec2.SecurityGroup(
            self, 
            f"orders-rds-sg-{self.enviroment.value}",
            vpc=self.vpc,
            security_group_name=f"orders-{self.enviroment.value}-sg",
            allow_all_outbound=True,
            )
        
        self.orders_rds_sg.add_ingress_rule(peer=ec2.Peer.ipv4("0.0.0.0/0"), connection=ec2.Port.tcp(5432))

        for subnet in self.vpc.private_subnets:
            self.orders_rds_sg.add_ingress_rule(peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block), connection=ec2.Port.tcp(5432))

        self.orders_rds_parameter_group = rds.ParameterGroup(
            self,
            f"orders-rds-parameter-group-{self.enviroment.value}",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16),
            parameters={
                "max_connections": "100",
                "shared_buffers": "{DBInstanceClassMemory/32768}",
                "work_mem": "65536",
                "maintenance_work_mem": "262144",
                "effective_cache_size": "{DBInstanceClassMemory/10922}",
                # "rds.logical_replication": "1", 'wal_sender_timeout': '0'
            },
        )

        self.orders_rds_instance = rds.DatabaseInstance(
            self,
            f"orders-rds-instance-{self.enviroment.value}-rds",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16),
            database_name="orders",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            vpc=self.vpc,
            instance_identifier=f"orders-{self.enviroment.value}-rds",
            port=5432,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            subnet_group = rds.SubnetGroup(
                self,
                f"orders-rds-subnet-group-{self.enviroment.value}",
                vpc=self.vpc,
                description="Orders RDS Subnet Group",
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            ),

            security_groups=[self.orders_rds_sg],
            parameter_group=self.orders_rds_parameter_group,
            allocated_storage=20,
            storage_encrypted=True,
            multi_az=False,
            deletion_protection=False,
            backup_retention=cdk.Duration.days(0),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            **kwargs
        )