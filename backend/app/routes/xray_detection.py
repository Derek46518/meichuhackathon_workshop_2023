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
import pandas as pd
import csv
serialNumber = 0
_logger = logging.getLogger("config")

def detection(filepath):
    process = Popen(["python", "detect.py", '--source', filepath], shell=True)   
    process.wait()
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    #image_path = folder_path+'/'+latest_subfolder+'/'+image.filename
    last_slash_index = filepath.rfind('/')
    image_path = folder_path+'/'+latest_subfolder+'/labels'+'/'+filepath[last_slash_index + 1:].replace('jpg','txt')
    try:
        responseString="無違禁品"
        objects = []
        f = open(image_path, 'r')
        for content in f:
            if content.startswith(('0','1','2','3','4')):
                #底下做有違禁品的處理
                #底下做寄信的動作
                responseString = "有違禁品:"
                objects.append(content[0])
        f.close()
        return responseString,objects
        # 檔案不存在的例外處理
    except FileNotFoundError:
        return "無違禁品",objects
  
# 丟image近來 回傳圖片結果的URL
@bp.route('/detectImg',methods=['POST'])
def detectImage():
    if 'image' in request.files:
        image = request.files['image']
        image.save('./image/'+image.filename)
        filepath = './image/'+image.filename
        message,objects = detection(filepath)
        for str in objects:
            if str == '0': message = message+'\n電子產品'
            elif str == '1': message = message+'\n筆電'
            elif str == '2': message = message+'\n剪刀'
            elif str == '3': message = message+'\n刀子'
            elif str == '4': message = message+'\n槍'
        return Response(message,200)
    else: return Response("400",400)
    
@bp.route('/parseCsvAndSendMail',methods=['GET'])
def parseCsv():
    print(__path__)
    file_path = "./csvData/2023MCH_EmpEntry.csv"
    with open(file_path, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 開始產生txt
        f = open("myfile.txt", "w")
        flag = False
        # 以迴圈輸出每一列
        for row in rows:
            employeeID = row[0]
            employeePic = row[7]
            employeePicURL = "" + employeePic +".jpg"
            message, objects = detect(employeePicURL)
            outMsg = employeeID+":"
            if(message=='有違禁品:'):
                flag = True
                for str in objects:
                    if str == '0': message = message+'\n剪刀'
                    elif str == '1': message = message+'\n電子產品'
                    elif str == '2': message = message+'\n刀子'
                    elif str == '3': message = message+'\n槍'
                    elif str == '4': message = message+'\n筆電'
                outMsg = outMsg+message
                f.write(outMsg)
                
        if flag == True:
            sendIllegalEmail()
    return Response('200',200)

gmail_token = base64.b64decode("ZnlhcSBnaWJvIG9ta3IgZHZrZQ==").decode('utf-8')

def sendIllegalEmail(attachments='',recipients: str= '99588albert@gmail.com'):
    message = MIMEMultipart()
    message["subject"] = "[ALARM] Suspicious luggage invading"
    message["from"] = "99588albert01@gmail.com"
    message["to"] = ( ', ' ).join(recipients.split(','))
    message.attach(MIMEText("主管您好<br>下面附上有攜帶違禁物品的人的員工編號<br>員工XXX敬上"))
    with smtplib.SMTP( host = "smtp.gmail.com", port = "587" ) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("99588albert01@gmail.com", gmail_token)
            smtp.send_message(message)

            print("Done!")

        except Exception as tmp:
            print("Error msg: ", tmp )


    return 'OK'