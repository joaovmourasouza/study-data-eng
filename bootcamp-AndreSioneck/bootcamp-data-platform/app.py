#!/usr/bin/env python3
import os
import aws_cdk as cdk
from bootcamp_data_platform.bootcamp_data_platform_stack import BootcampDataPlatformStack
from data_platform.common_stack import CommonStack
from data_platform.enviroment import EnviromentEnum
from data_platform.kinesis import KinesisStack

app = cdk.App()

deploy_env = EnviromentEnum(app.node.try_get_context("deploy_enviroment"))

common_stack = CommonStack(app, "CommonStack", enviroment=deploy_env)
data_platform_stack = BootcampDataPlatformStack(app, "BootcampDataPlatformStack", enviroment=deploy_env)
kinesis = KinesisStack(app,  data_lake_raw=data_platform_stack.data_lake_raw, enviroment=deploy_env)

app.synth()