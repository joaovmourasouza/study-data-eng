#!/usr/bin/env python3
import os
import aws_cdk as cdk
from bootcamp_data_platform.bootcamp_data_platform_stack import BootcampDataPlatformStack
from bootcamp_data_platform.data_platform.common_stack import CommonStack
from data_platform.enviroment import EnviromentEnum

app = cdk.App()

deploy_env = EnviromentEnum(app.node.try_get_context("deploy_enviroment"))

CommonStack(app, "CommonStack", enviroment=deploy_env)
BootcampDataPlatformStack(app, "BootcampDataPlatformStack", enviroment=deploy_env)

app.synth()