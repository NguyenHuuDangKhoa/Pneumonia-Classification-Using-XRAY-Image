# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
from zipfile import ZipFile
import glob
import structlog


load_dotenv()
KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME')
KAGGLE_KEY = os.getenv('KAGGLE_KEY')
from kaggle.api.kaggle_api_extended import KaggleApi

logger = structlog.getLogger(__name__)
KAGGLE_COMPETITION = "rsna-pneumonia-detection-challenge"
RAW_DATA_PATH = "./data/raw/"
ZIP_NAME = "rsna-pneumonia-detection-challenge.zip"

def authenticate_kaggle() -> KaggleApi:
    """
    Authenticate connection to Kaggle API
    using username and key saved in .env file
    or from the kaggle.json file.
    :return: Kaggle API object
    """
    api = KaggleApi()
    api.authenticate()
    return api

def extract_zip(input_path: str, output_path: str) -> None:
    """
    Load a .zip file and extract it to a directory.
    :input_path: a path to the .zip file
    :output_path: a path to extract the .zip file to
    :return: None
    """
    with ZipFile(input_path+ZIP_NAME, 'r') as zObject:
        zObject.extractall(path=output_path)

def delete_zip(path: str) -> None:
    """
    Delete all .zip file in the provided path
    :path: a path to where the .zip files located
    :return: None
    """
    for zippath in glob.iglob(os.path.join(path, "*.zip")):
        os.remove(zippath)

def main():
    api = authenticate_kaggle()
    logger.info('Kaggle Account Authenticated')
    api.competition_download_files(competition=KAGGLE_COMPETITION, path=RAW_DATA_PATH)
    extract_zip(input_path=RAW_DATA_PATH, output_path=RAW_DATA_PATH)
    delete_zip(path=RAW_DATA_PATH)
    logger.info('Dataset Downloaded')

if __name__ == '__main__':
    main()
