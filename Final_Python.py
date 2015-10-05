#!-*- coding:utf-8 -*-

__author__ = "IT10"
__date__ = "$25/09/2015 16:23:09$"

##########################################################################################################
import androidhelper as android
import time
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydoc import help

##########################################################################################################    

class sensores(object):
    
    def __init__(self):
        """
        Default sensores's constructor
        Create object sensores to get information of device's sensors.
        """
        self.droid = android.Android()    
        
    def get_info_wifi(self):
        """
        get_info_wifi(self)
        Returns information about the currently active access point.
        """
        return  self.droid.wifiGetConnectionInfo()

    def get_info_operador(self):
        """
        get_info_operador(self) 
        Returns the Service Provider Name (SPN).
        """
        return self.droid.getSimOperatorName()
    
    def get_info_gps(self):
        """
        get_info_gps(self)
        Returns the current location as indicated by all available providers.
        """
        self.droid.startLocating()
        time.sleep(20)
        self.gps = self.droid.readLocation()
        return  self.gps.result               
        
# End sensores 
###############################################################################################
class mailSenderWithImg:
    
    def __init__(self, userName, password):
        """
        Default mailSenderWithImg's constructor
        Set from address info and create message object
        """
        self.userName = userName
        self.password = password
        self.set_fromAddr(userName)
        self.msg = MIMEMultipart()
        

    """
    SETTERS
    """

    def set_fromAddr(self, fromAddr):
        self.fromAddr = fromAddr
        
    def set_toAddr(self, toAddr):
        self.toAddr = toAddr

    """
    GETTERS
    """
        
    def get_fromAddr(self):
        return self.fromAdrr
    
    def get_toAddr(self):
        return self.toAdrr
     


    def msgWithText(self, subject, text):
        """
        Set subject, message's body text and from and to address 
        """
        self.msg['subject'] = subject
        self.msg['from'] = self.fromAddr
        self.msg['to'] = self.toAddr
        self.msg.attach(MIMEText(text))
        
    def msgWithImg(self, path):
        """
        Set message's image from path 
        """
        fp = open(path, 'rb')
        msgImg = MIMEImage(fp.read())
        fp.close()
        self.msg.attach(msgImg)
        
    def sendMail(self):
        """
        Try to connect with server, login and send email
        In case of error print send error
        """    
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com:465')
            server.login(self.userName,self.password)
            server.sendmail(self.fromAddr, self.toAddr, self.msg.as_string())
            server.quit()
            print "Mensaje enviado correctamente a ", self.toAddr , "\n" 
        except Exception,e:
            print "Error enviando mensaje!\n",e

#end sendMailwithImg        
####################################################################################################################
# Begin principal structure

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
    subject_email = "Report_"+time.strftime('%d-%m-%Y %H:%M:%S')
    sender.msgWithText(subject_email,text_email)
    sender.msgWithImg( dir_img + "logo.png")
    sender.sendMail()

    print "Esperando proxima iteracion \n"    
   
    time.sleep(40) #Predisposes one cycle of 40 seconds, because this time with the GPS-location is equal to one minute.

# repeat for each 60 seconds        
