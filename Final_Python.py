#!-*- coding:utf-8 -*-

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "IT10"
__date__ = "$25/09/2015 16:23:09$"

#Libreria para android y  comunicacion con sensores
import androidhelper as android
import time

# Librerias para el tratamiento del Email 
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##########################################################################################################    

class sensores(object):
    
    def __init__(self):
        self.droid = android.Android()    
        
    def get_info_wifi(self):
        return  self.droid.wifiGetConnectionInfo()

    def get_info_operador(self):
        return self.droid.getSimOperatorName()
    
    def get_info_gps(self):
        self.droid.startLocating()
        time.sleep(20)
        self.gps = self.droid.readLocation()
        return  self.gps.result               
        
# Fin de clase sensores 

class mailSenderWithImg:
    
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        set_fromAddr(userName)
        self.msg = MIMEMultipart()
        
    def set_fromAddr(self, fromAddr):
        self.fromAddr = fromAddr
        
    def set_toAddr(self, toAddr):
        self.toAddr = toAddr
        
    def get_fromAddr(self):
        return self.fromAdrr
    
    def get_toAddr(self):
        return self.toAdrr
        
    def msgWithText(self, subject, text):
        
        self.msg['subject'] = subject
        self.msg['from'] = self.fromAddr
        self.msg['to'] = self.toAddr
        self.msg.attach(MIMEText(text))
        
    def msgWithImg(self, path):
        
        fp = open(path, 'rb')
        msgImg = MIMEImage(fp.read())
        fp.close()
        self.msg.attach(msgImg)
        
    def sendMail(self):    
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com:465')
            server.login(self.userName,self.password)
            server.sendmail(self.fromAddr, self.toAddr, self.msg.as_string())
            server.quit()
            print "Mensaje enviado correctamente a ", self.toAddr , "\n" 
        except Exception,e:
            print "Error en el envío!\n",e

#fin clase sendMailwithImg        

info_sensores = sensores()

dir_img = "/storage/emulated/0/com.hipipal.qpyplus/scripts/"
from_Addr = 'pruebasdisse@gmail.com'
pass_Addr = 'pruebas123'
contador = 1

to_Addr = raw_input("Ingrese su email (debe utilizar gmail) \n")

while (len(to_Addr) == 0 or to_Addr.count('@') == 0):
    to_Addr = raw_input("email incorrecto, vuelva a ingresar (debe utilizar gmail) \n")

sender = mailSenderWithImg(from_Addr, pass_Addr)
sender.set_toAddr(to_Addr)

while True:    

    print "Mandando Email numero = " + str(contador) + "\n"    
    contador = contador +1

    print "Lectura de sensores en proceso ... \n" 

    wifi = info_sensores.get_info_wifi()
    operador = info_sensores.get_info_operador()
    gps = info_sensores.get_info_gps()
    rnet = gps["network"] 

    print "Lectura de Sensores Exitosa \n"    
   
    text_email = "Latitud gps = " + str(rnet["latitude"]) + "\n" + "Longitud gps = " + str(rnet["longitude"]) + "\n" + "Operador ="+ str(operador[1]) + "\n"+ "Datos WIFI = "+ str(wifi[1])+ "\n"    
    
    sender.msgWithText('DISSE Proyect Msg',text_email)
    sender.msgWithImg( dir_img + "logo.png")
    sender.sendMail()
    
    print "Esperando proxima iteracion \n"    
   
    time.sleep(40) #se predispone un ciclo de 40 segundos debido a que la suma de este tiempo con el refrezco del GPS suma un total de 1 min    

#repeticion cada 60 segundos        
