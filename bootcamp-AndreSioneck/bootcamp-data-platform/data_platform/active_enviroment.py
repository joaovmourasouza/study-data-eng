from data_platform.enviroment import EnviromentEnum
import os

active_enviroment = EnviromentEnum(os.environ["DEPLOY_ENVIROMENT"])