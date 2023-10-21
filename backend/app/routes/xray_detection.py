from . import bp
from common import logging
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from ..metricss import custom_metrics
import detect 
import subprocess
from subprocess import Popen
import os
from werkzeug.utils import secure_filename, send_from_directory
import uvicorn
from fastapi import FastAPI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64
from email.mime.image import MIMEImage
from pathlib import Path
from fastapi import File, UploadFile
import numpy as np
# import model.detection as det
import cv2 as cv
import time

serialNumber = 0
_logger = logging.getLogger("config")

'''
# 底下先宣告在哪個路徑 並且宣告為post method
@bp.route('/upload', methods=['POST'])
# 上傳圖片
def upload_image():
    if 'images' in request.files:
        image = request.files['images']
    _logger.info(image.filename)

    image.save('./aaa.jpg')
    if 'aaa' in image.filename:
        custom_metrics.abnormal_counter.inc()
        return Response("e",200)
    return Response("哈哈哈", 200)
'''
gmail_token = base64.b64decode("ZnlhcSBnaWJvIG9ta3IgZHZrZQ==").decode('utf-8')


# 丟image近來 回傳圖片結果的URL
@bp.route('/detectImg',methods=['POST'])
def detectImage():
    if 'image' in request.files:
        image = request.files['image']
        image.save('./image/'+image.filename)
        filepath = './image/'+image.filename
        process = Popen(["python", "detect.py", '--source', filepath], shell=True)   
        process.wait()
        folder_path = 'runs/detect'
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
        latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
        #image_path = folder_path+'/'+latest_subfolder+'/'+image.filename
        image_path = folder_path+'/'+latest_subfolder+'/labels'+'/'+image.filename.replace('jpg','txt')
        responseString = ''
        try:
            f = open(image_path, 'r')
            for content in f:
                if content.startswith(('1','2','3','4','5')):
                    #底下做有違禁品的處理
                    responseString = responseString+"有違禁品"
                    return Response("有違禁品",200)
                else: 
                    responseString = responseString+"有電子產品"
                    return Response("有電子產品",200)
            f.close()
        # 檔案不存在的例外處理
        except FileNotFoundError:
            return Response("沒有違禁品",200)
        
    else: return Response("400",400)
# 顯示pyplot結果
'''
@app.route('/test')
def chartTest():
  lnprice=np.log(price)
  plt.plot(lnprice)   
  plt.savefig('/static/images/new_plot.png')
  # 下面放html檔
  return render_template('../frontend/untitled1.html', name = 'new_plot', url ='/static/images/new_plot.png')
  
'''