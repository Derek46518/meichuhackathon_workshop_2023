import pandas as pd
from datetime import datetime
from . import bp
from common import logging
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
import os

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

# read data from csv
file_path = "./csvData/2023MCH_EmpEntry.csv"
# must check file name !!!!!!!!!!!
df = pd.read_csv(file_path)

def is_late(row):
    emp_shift_time = datetime.strptime(row['EmpShift'], '%H:%M').time()
    actual_time = row['DateTime'].time()
    return actual_time > emp_shift_time

@bp.route('/getLatePeople', methods=['GET'])
def getLatePeople():
# transfer DateTime to datetime (former is string and latter is datetime)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
# diagnose if is late
# use apply to call and recognize the late employees
    df['Late'] = df.apply(is_late, axis=1)
# find the late employees
    late_employees = df[df['Late'] == True].drop(columns=['Late'])
# sort by datetime
    late_employees_sorted = late_employees.sort_values(by='DateTime')
# save into a csv file
    late_employees_sorted.to_csv("./csvData/late_employees_sorted.csv", index=False)
    return Response("Ok",200)
gmail_token = base64.b64decode("ZnlhcSBnaWJvIG9ta3IgZHZrZQ==").decode('utf-8')

@bp.route('/sendIllegalEmail',methods=['POST'])
def sendIllegalEmail(recipients: str= '99588albert@gmail.com'):
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