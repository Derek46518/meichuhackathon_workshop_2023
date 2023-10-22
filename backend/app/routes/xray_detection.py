from . import bp
from common import logging
from flask import Flask,jsonify, render_template, request, redirect, send_file, url_for, Response
from ..metricss import custom_metrics
import detect 
import subprocess
from subprocess import Popen
import os
from werkzeug.utils import secure_filename, send_from_directory
import uvicorn
from fastapi import FastAPI
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64
from email.mime.image import MIMEImage
from pathlib import Path
from fastapi import File, UploadFile
import numpy as np
import pandasql as ps
# import model.detection as det
import cv2 as cv
import time
import pandas as pd
import csv
import email.mime.application
from datetime import datetime, timedelta

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
    file_path = "./csvData/2023MCH_EmpEntry.csv"
    # 開始產生txt
    outMsg = ""
    flag = False
    with open(file_path, newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 以迴圈輸出每一列
        for row in rows:
            employeeID = row[0]
            employeePic = row[6]
            employeePicURL = "./2023MCH_TestData/" + employeePic +".jpg"
            message, objects = detection(employeePicURL)
            if(message=="有違禁品:"):
                message = employeeID+message
                flag = True
                print("有違禁品")
                for str in objects:
                    if str == '0': message = message+'電子產品、'
                    elif str == '1': message = message+'筆電、'
                    elif str == '2': message = message+'剪刀、'
                    elif str == '3': message = message+'刀子、'
                    elif str == '4': message = message+'槍、'
                outMsg = outMsg+message+'\n'
                #break
    f = open("myfile.txt", "w",encoding="utf-8")
    f.write(outMsg)
    f.close()            
    if flag == True:
        sendIllegalEmail()
            
    return Response('200',200)

gmail_token = base64.b64decode("ZnlhcSBnaWJvIG9ta3IgZHZrZQ==").decode('utf-8')
def sendIllegalEmail(recipients: str= '99588albert@gmail.com'):
    message = MIMEMultipart()
    message["subject"] = "[ALARM] Suspicious luggage invading"
    message["from"] = "99588albert01@gmail.com"
    message["to"] = ( ', ' ).join(recipients.split(','))
    message.attach(MIMEText("主管您好\n下面附上有攜帶違禁物品的人的員工編號\n員工XXX敬上"))
    # PDF attachment
    filename='myfile.txt'
    fp=open(filename,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="txt")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=filename)
    message.attach(att)
    
    fp.close()
    fp=open(filename,'rb')
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
@bp.route('/get-data',methods=['POST'])
def get_data():
    print(request.args)
    date = request.json.get('date')
    DeptID = request.json.get('DeptID')
    Zone = request.json.get('Zone')
    queryString = ""
    if date is not None:
        queryString = queryString +"Date == '"+date + "' "
    if DeptID is not None:
        if len(queryString) != 0 : queryString = queryString + ' and '
        queryString = queryString +"DeptId == '"+DeptID + "'"
    if Zone is not None:
        if len(queryString) != 0 : queryString = queryString + ' and '
        queryString = queryString +"Zone == '"+Zone + "'"
    print(queryString)
    df = pd.read_csv("./csvData/sep_date_time.csv")
    
    result = df.query(queryString)
    #result.to_csv('filtered_data.csv', index=False)
    result['Time'] = df['Time'] = pd.to_timedelta(df['Time'])


    # 计算时间列的平均值
    average_time = result['Time'].mean()

    # 将平均时间值格式化为字符串
    average_time_str = str(average_time)
    data = {'time': average_time_str}
   
    return jsonify(data), 200

@bp.route('/getDaily/<date>',methods=['GET'])
def getDaily(date):
    df = pd.read_csv("./csvData/sep_date_time.csv")
    DEPT_LIST = ['DEPT1','DEPT2','DEPT3','DEPT4']
    BRANCH_LIST = ['HQ','AZ']
    
    toreturn ={}
    for dept in DEPT_LIST:
        temp={}
        for branch in BRANCH_LIST:
            queryString = "Date == '"+ date+"' and DeptId == '"+dept + "' and Zone == '" + branch + "'"
            print(queryString)
            result = df.query(queryString)
            length = len(result)
            temp[branch] = length
        toreturn[dept] = temp
    result.to_csv('filtered_data.csv', index=False)
    
    return jsonify(toreturn),200

@bp.route('/getWeekly/<date>',methods=['GET'])
def getWeekly(date):
    df = pd.read_csv("./csvData/sep_date_time.csv")
    date = datetime.strptime(date, '%Y-%m-%d')
    BRANCH_LIST = ['HQ','AZ']
    DATE_LIST = []
    for i in range(7):
        # 将日期添加到列表中
        DATE_LIST.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)
        
    toreturn ={}
    for date in DATE_LIST:
        temp={}
        for branch in BRANCH_LIST:
            queryString = "Date == '"+ date+"' and Zone == '" + branch + "'"
            result = df.query(queryString)
            length = len(result)
            temp[branch] = length
        toreturn[date] = temp
    
    return jsonify(toreturn),200