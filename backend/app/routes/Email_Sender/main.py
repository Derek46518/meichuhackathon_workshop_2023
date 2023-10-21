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


#app = FastAPI(title= 'Alert sender')
gmail_token = base64.b64decode("ZnlhcSBnaWJvIG9ta3IgZHZrZQ==").decode('utf-8')

#@app.get('/api/v1/alert')
def send_alert_email( recipients: str= '99588albert@gmail.com'):
    message = MIMEMultipart()
    # create a MIMEMultipart object
    message["subject"] = "[ALARM] Suspicious luggage invading"
    message["from"] = "99588albert01@gmail.com"
    message["to"] = ( ', ' ).join(recipients.split(','))
    message.attach(MIMEText(""))
    # setup the subject, sender, reciever, content

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

# @app.post('/api/v2/alert')

    

if __name__ == '__main__':
    send_alert_email()
    #uvicorn.run('main:app', reload=True)