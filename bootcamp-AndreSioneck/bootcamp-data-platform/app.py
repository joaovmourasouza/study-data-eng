#!/usr/bin/env python3
import os
import aws_cdk as cdk
from bootcamp_data_platform.bootcamp_data_platform_stack import BootcampDataPlatformStack
from bootcamp_data_platform.data_platform.common_stack import CommonStack
from data_platform.enviroment import EnviromentEnum
from bootcamp_data_platform.data_platform.dms.stack import DmsStack
from bootcamp_data_platform.data_platform.common.base_stack import BaseDataLakeBucket

app = cdk.App()

deploy_env = EnviromentEnum(app.node.try_get_context("deploy_enviroment"))

common_stack = CommonStack(app, "CommonStack", enviroment=deploy_env)
data_lake_raw_bucket = BaseDataLakeBucket(app, "BaseDataLakeBucket", enviroment=deploy_env)
DmsStack(app, "DmsStack", enviroment=deploy_env, common_stack=common_stack, data_lake_raw_bucket=data_lake_raw_bucket)
BootcampDataPlatformStack(app, "BootcampDataPlatformStack", enviroment=deploy_env)

app.synth()