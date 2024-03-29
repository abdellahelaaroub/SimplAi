from flask import Flask, jsonify, request
#from modules import getDataset

import json
from flask_cors import CORS

from kaggle.api.kaggle_api_extended import KaggleApi
import os

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
import time
#from pprint import pprint


class Dataset:
    def __init__(self):
        os.environ['KAGGLE_USERNAME'] = 'abdellahelaaroub'  #'abdellahelaaroub'
        os.environ['KAGGLE_KEY'] = 'f6a4b8dfccbbef8c72f5bb2f97429eee'  #'f6a4b8dfccbbef8c72f5bb2f97429eee'
        self.api = KaggleApi()
        self.api.authenticate()
    
    def dataset(self, datasetName):
        self.datasets = self.api.dataset_list(search = datasetName, sort_by = 'votes')
        self.all_Datasets = list()
        for dataset in self.datasets:
            self.all_Datasets.append({
                'ref' : vars(dataset)['ref'],
                'url' : vars(dataset)['url'],
                'title' : vars(dataset)['title'],
                'subtitle' : vars(dataset)['subtitle'],
                'size' : vars(dataset)['size'],
                'viewCount' : vars(dataset)['viewCount'],
                'voteCount' : vars(dataset)['voteCount'],
            })
        return self.all_Datasets
    
    def download_Dataset(self, url, datasetName):
        path = "Download/"
        PATH = "C:\Program Files (x86)\chromedriver.exe"
                
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path = PATH, options=options)
        driver.get(url)
        
        time.sleep(5)
        datasetnameFromKaggle = driver.find_element_by_xpath("//div[@role='button']//div//div").text
        
        self.api.dataset_download_file(datasetName, datasetnameFromKaggle)


app = Flask(__name__)
CORS(app)


@app.route("/dataset/dataset_kaggle/<id>", methods = ["Get", "POST"])
def getDatasetBySearch(id):
    if request.method == "POST":
        dataSearch = request.json['searchData']
    a = str(id)
    newdata = Dataset()
    dataAPI = newdata.dataset(a)
    print(dataAPI)
    return jsonify(dataAPI)


@app.route("/dataset/dataset_kaggle", methods = ["Get", "POST"])
def getDataset():
    if request.method == "POST":
        dataSearch = request.json['searchData']
    a = "iris"
    newdata = Dataset()
    return jsonify(newdata.dataset(a))


x = []
x.append(1)
# running code 
if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)