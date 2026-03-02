from constructs import Construct

from data_platform.data_lake.base import DataLakeBase, DataLakeBucketEnum
from data_platform.enviroment import EnviromentEnum
from data_platform.active_enviroment import active_enviroment

class DataLakeStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, enviroment: EnviromentEnum, **kwargs) -> None:
        self.deploy_env = active_enviroment
        super().__init__(scope, id=f'{self.deploy_env.value}-data-lake-stack', **kwargs)

        self.data_lake_raw = DataLakeBase(self, "DataLakeRaw", enviroment, DataLakeBucketEnum.RAW)
        self.data_lake_clean = DataLakeBase(self, "DataLakeClean", enviroment, DataLakeBucketEnum.CLEAN)
        self.data_lake_processed = DataLakeBase(self, "DataLakeProcessed", enviroment, DataLakeBucketEnum.PROCESSED)