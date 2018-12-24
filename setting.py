# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AK = os.environ.get("APP_KEY")
AS = os.environ.get("APP_SECRET")
SK = os.environ.get("SECRET_KEY")
