from enum import Enum
from aws_cdk import Core
from aws_cdk import (aws_s3 as s3,)

from data_platform.enviroment import EnviromentEnum

class DataLakeBucketEnum(Enum):
    RAW = "raw"
    CLEAN = "clean"
    PROCESSED = "processed"

class DataLakeBase(s3.Bucket):
    def __init__(self, scope: Core, construct_id: str, enviroment: EnviromentEnum, **kwargs) -> None:
        super().__init__(scope, construct_id, versioned=True)