from enum import Enum
from constructs import Construct
from aws_cdk import (aws_s3 as s3, Duration)

from data_platform.enviroment import EnviromentEnum

class DataLakeBucketEnum(Enum):
    RAW = "raw"
    CLEAN = "clean"
    PROCESSED = "processed"

class DataLakeBase(s3.Bucket):
    def __init__(self, scope: Construct, construct_id: str, enviroment: EnviromentEnum, layer: DataLakeBucketEnum, **kwargs) -> None:
        self.enviroment = enviroment
        self.layer = layer
        self.obj_name = f"s3-bootcamp{self.enviroment.value}-data-lake-{self.layer.value}"
        super().__init__(
            scope,
            construct_id,
            bucket_name=self.obj_name,
            versioned=True,
            block_public_access=self.default_block_public_access,
            encryption=self.default_encryption,
            **kwargs
        )

        self.set_default_lifecycle_rules()

    @property
    def default_block_public_access(self) -> s3.BlockPublicAccess:
        return s3.BlockPublicAccess(
            ignore_public_acls=True,
            restrict_public_buckets=True,
            block_public_acls=True,
            block_public_policy=True
        )

    @property
    def default_encryption(self) -> s3.BucketEncryption:
        return s3.BucketEncryption.S3_MANAGED

    def set_default_lifecycle_rules(self) -> None:
        self.add_lifecycle_rule(
            abort_incomplete_multipart_upload_after=Duration.days(7),
            enabled=True,
        )
        self.add_lifecycle_rule(
            noncurrent_version_transitions=[
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after=Duration.days(30),
                ),
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=Duration.days(365),
                ),
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.DEEP_ARCHIVE,
                    transition_after=Duration.days(3650),
                ),
            ]
        )