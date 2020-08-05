import sys
import re
import time
try:
	import paramiko
except:
	import os
	os.system('pip3 install paramiko')
	os.system('python3 -m pip install paramiko')
	import paramiko

try:
	from PySide2 import QtCore, QtGui, QtWidgets
except:
	import os
	os.system('pip3 install PyQt5 PySide2')
	os.system('python3 -m pip install PyQt5 PySide2')
	from PySide2 import QtCore, QtGui, QtWidgets



class SendSignal(QtCore.QObject):
	sig = QtCore.Signal(str)

class SendMSignal(QtCore.QObject):
	sig = QtCore.Signal(str)

class FirstThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class SecondThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class ThirdThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class FourthThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class FifthThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class SixthThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class SeventhThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class EighthThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class NinthThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.parameters = ""
		self.signal = SendMSignal()
		self.command = "ps aux"

	def run(self):
		message = send_command(self.parameters, self.command)
		self.signal.sig.emit(message)

class Ui_Form(object):

	def finished(self, data):
		self.textBrowser.setText(self.textBrowser.toPlainText() + data)

	def setupUi(self, Form):

		self.first_thread = FirstThread()
		self.first_thread.signal.sig.connect(self.finished)

		self.second_thread = SecondThread()
		self.second_thread.signal.sig.connect(self.finished)

		self.third_thread = ThirdThread()
		self.third_thread.signal.sig.connect(self.finished)

		self.fourth_thread = FourthThread()
		self.fourth_thread.signal.sig.connect(self.finished)

		self.fifth_thread = FifthThread()
		self.fifth_thread.signal.sig.connect(self.finished)

		self.sixth_thread = SixthThread()
		self.sixth_thread.signal.sig.connect(self.finished)

		self.seventh_thread = SeventhThread()
		self.seventh_thread.signal.sig.connect(self.finished)

		self.eighth_thread = EighthThread()
		self.eighth_thread.signal.sig.connect(self.finished)

		self.ninth_thread = NinthThread()
		self.ninth_thread.signal.sig.connect(self.finished)

		config = open('config.txt','r').read().replace('\n','')
		serv_num = len(re.split(r'\|',config))+1
		Form.setObjectName("Form")
		Form.setFixedSize(868, 1049)

		self.verticalLayoutWidget = QtWidgets.QWidget(Form)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(720, 50, 131, 800))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

		self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
		self.scrollArea.setGeometry(QtCore.QRect(0, 0, 131, 800))
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
		self.lineEdit = QtWidgets.QLineEdit(Form)
		self.lineEdit.setGeometry(QtCore.QRect(30, 80, 501, 61))
		self.lineEdit.setObjectName("lineEdit")
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
		self.pushButton_start.setGeometry(QtCore.QRect(550, 80, 61, 61))
		self.pushButton_start.setObjectName("pushButton")
		self.pushButton_clean = QtWidgets.QPushButton(Form)
		self.pushButton_clean.setGeometry(QtCore.QRect(630, 80, 61, 61))
		self.pushButton_clean.setObjectName("pushButton_2")
		self.pushButton_select = QtWidgets.QPushButton(Form)
		self.pushButton_select.setGeometry(QtCore.QRect(720, 910, 131, 20))
		self.pushButton_select.setObjectName("pushButton_4")
		self.pushButton_unselect = QtWidgets.QPushButton(Form)
		self.pushButton_unselect.setGeometry(QtCore.QRect(720, 930, 131, 20))
		self.pushButton_unselect.setObjectName("pushButton_unselect")
		self.pushButton_filter = QtWidgets.QPushButton(Form)
		self.pushButton_filter.setGeometry(QtCore.QRect(720, 950, 131, 20))
		self.pushButton_filter.setObjectName("pushButton_filter")
		self.pushButton_check = QtWidgets.QPushButton(Form)
		self.pushButton_check.setGeometry(QtCore.QRect(720, 970, 131, 20))
		self.pushButton_check.setObjectName("pushButton_check")
		self.textBrowser = QtWidgets.QTextBrowser(Form)
		self.textBrowser.setGeometry(QtCore.QRect(30, 200, 671, 831))
		self.textBrowser.setObjectName("textBrowser")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
		self.label.setText(QtWidgets.QApplication.translate("Form", "Servers list:", None, -1))
		self.label_2.setText(QtWidgets.QApplication.translate("Form", "Input command:", None, -1))
		self.label_4.setText(QtWidgets.QApplication.translate("Form", "Output Data:", None, -1))
		self.pushButton_start.setText(QtWidgets.QApplication.translate("Form", "Run", None, -1))
		self.pushButton_clean.setText(QtWidgets.QApplication.translate("Form", "Clean", None, -1))
		self.pushButton_select.setText(QtWidgets.QApplication.translate("Form", "Select All", None, -1))
		self.pushButton_unselect.setText(QtWidgets.QApplication.translate("Form", "Unselect All", None, -1))
		self.pushButton_check.setText(QtWidgets.QApplication.translate("Form", "Check servers", None, -1))
		self.pushButton_filter.setText(QtWidgets.QApplication.translate("Form", "Filter", None, -1))
		self.textBrowser.setHtml(QtWidgets.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>", None, -1))






#Create application
#app = QtGui.QApplication(sys.argv)

#Create form and unit UI
app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

def connect_ssh(ip, user,key_file,port):

	retries=1
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	for x in range(retries):
		try:
			ssh.connect(ip, username=user, password=key_file, port=port)
			return True
		except Exception as e:
			print(e)
	return False



def availabilityCheck():
	config = open('config.txt','r').read().replace('\n','')
	message = "\t\t\tSTATUS:\n"
	checkArray = []
	for server_info in re.split(r'\|',config):
		server_info_array = re.split(r':',server_info)
		ident = server_info_array[0]
		ipaddr = server_info_array[1]
		port = server_info_array[2]
		user = server_info_array[3]
		password = server_info_array[4]
		checkArray.append(connect_ssh(ipaddr,user,password,port))
	return checkArray

def colorChange():
	checkArray = availabilityCheck()
	for i in range(ui.verticalLayout.count()):
		if checkArray[i]:
			ui.verticalLayout.itemAt(i).widget().setStyleSheet("color: green")
		else:
			ui.verticalLayout.itemAt(i).widget().setStyleSheet("color: red")


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


#Hook logic
def send_command(parameters, command):
	server_info_array = re.split(r':',parameters)
	ident = server_info_array[0]
	ipaddr = server_info_array[1]
	port = server_info_array[2]
	user = server_info_array[3]
	password = server_info_array[4]

	message = "Failed"

	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=ipaddr, username=user, password=password, port=port)
		stdin, stdout, stderr = client.exec_command(command)
		data = stdout.read() + stderr.read()
		message = "\nServer " + ident + " Adress " + ipaddr + ":" + port + "\n\t" +bytes.decode(data).replace('\n','\n\t')
		client.close()
	except:
		message = "\nServer " + ident + " Adress " + ipaddr + ":" + port + "\n\t" + "Failed to connect"
	loggingToDict(ident, message)
	return message


def refresh():
	config = open('config.txt','r').read().replace('\n','')

	for server_info in re.split(r'\|',config):
		message = send_command(server_info, ui.lineEdit_refresh.text())
		ui.textBrowser.setText(ui.textBrowser.toPlainText() + message)

def run_button():
	send_threads(ui.lineEdit.text())

def send_threads(command):
	config = open('config.txt','r').read().replace('\n','')
	i = 1
	for server_info in re.split(r'\|',config):
		checkArray = formCheckArray()
		if checkArray[int(re.split(r':',server_info)[0])-1]:
			if i == 1:
				ui.first_thread.wait()
				ui.first_thread.parameters = server_info
				ui.first_thread.command = command
				ui.first_thread.start()
				i += 1
			elif i == 2:
				ui.second_thread.wait()
				ui.second_thread.parameters = server_info
				ui.second_thread.command = command
				ui.second_thread.start()
				i += 1
			elif i == 3:
				ui.third_thread.wait()
				ui.third_thread.parameters = server_info
				ui.third_thread.command = command
				ui.third_thread.start()
				i += 1
			elif i == 4:
				ui.fourth_thread.wait()
				ui.fourth_thread.parameters = server_info
				ui.fourth_thread.command = command
				ui.fourth_thread.start()
				i += 1
			elif i == 5:
				ui.fifth_thread.wait()
				ui.fifth_thread.parameters = server_info
				ui.fifth_thread.command = command
				ui.fifth_thread.start()
				i += 1
			elif i == 6:
				ui.sixth_thread.wait()
				ui.sixth_thread.parameters = server_info
				ui.sixth_thread.command = command
				ui.sixth_thread.start()
				i += 1
			elif i == 7:
				ui.seventh_thread.wait()
				ui.seventh_thread.parameters = server_info
				ui.seventh_thread.command = command
				ui.seventh_thread.start()
				i += 1
			elif i == 8:
				ui.eighth_thread.wait()
				ui.eighth_thread.parameters = server_info
				ui.eighth_thread.command = command
				ui.eighth_thread.start()
				i += 1
			else:
				ui.ninth_thread.wait()
				ui.ninth_thread.parameters = server_info
				ui.ninth_thread.command = command
				ui.ninth_thread.start()
				i = 1

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

def changeTime():
	ui.ref_thread.wait_time = int(ui.spinBox.value())

def changeCommand():
	ui.ref_thread.command = ui.lineEdit_refresh.text()


ui.pushButton_start.clicked.connect(run_button)
ui.pushButton_select.clicked.connect(selectAll)
ui.pushButton_unselect.clicked.connect(unselectAll)
ui.pushButton_clean.clicked.connect(clean)
ui.pushButton_filter.clicked.connect(showingInfo)
ui.pushButton_check.clicked.connect(colorChange)

sys.exit(app.exec_())
