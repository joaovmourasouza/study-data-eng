from aws_cdk import Stack
from constructs import Construct

from data_platform.data_lake.base import DataLakeBase, DataLakeBucketEnum
from data_platform.enviroment import EnviromentEnum

class BootcampDataPlatformStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, enviroment: EnviromentEnum, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Instantiate the Raw bucket
        self.raw_bucket = DataLakeBase(
            self, 
            construct_id="DataLakeRawBucket", 
            enviroment=enviroment, 
            layer=DataLakeBucketEnum.RAW
        )

        # Instantiate the Clean bucket
        self.clean_bucket = DataLakeBase(
            self, 
            construct_id="DataLakeCleanBucket", 
            enviroment=enviroment, 
            layer=DataLakeBucketEnum.CLEAN
        )

        # Instantiate the Processed bucket
        self.processed_bucket = DataLakeBase(
            self, 
            construct_id="DataLakeProcessedBucket", 
            enviroment=enviroment, 
            layer=DataLakeBucketEnum.PROCESSED
        )
