# final_python
Final proyect - Embeded Python - DISSE

Para poder utilizar la aplicación en el dispositivo hay que acceder...



Luego a través de la terminal ingresar los siguientes comandos:

Conectarse a servidor SSH:

# ssh -p <número de puerto> <usuario>@<número IP de android>
ssh -p 22222 adri@192.168.0.102

Copiar archivos por medio de SSH:

# scp -P <número de puerto> <ubicación del archivo a copiar> <usuario>@<número IP de
# android>:<ubicación final del archivo en el dispositivo python>
scp -P 22222 Final_Python.py adri@192.168.0.102:/storage/emulated/0/com.hipipal.qpyplus/scripts




Para correr el programa es necesario tener activado el GPS.
