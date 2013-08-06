#Fedora
import shelve
import wx
import os
import smtplib
import re
import urllib2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
regexion = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
attos = []
wildcard = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
         "All files (*.*)|*.*"
SEND_ATT,OPEN_PROMPT,SAVE_PROMT, CLOSE,DEF_ACC,CUST_ACC = 1,2,3,4,5,6
class RaiseAuth(wx.Dialog):
	def __init__(self,cancel_view = False):
		super(RaiseAuth, self).__init__(None)
		self.cancel_view = cancel_view
		self.DialogUI()
		self.SetSize((300, 150))
		self.SetTitle("Authenticate please...")
	def DialogUI(self):
		pan = wx.Panel(self)
		pan1 = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)	
		user_box = wx.BoxSizer(wx.HORIZONTAL)
		user_text = wx.StaticText(pan, label = "User")
#falta definir cuadro de texto
		user_box.Add(user_text,0,wx.ALL,5)
		self.user_camp = wx.TextCtrl(pan)
		user_box.Add(self.user_camp,wx.EXPAND)
		pan.SetSizer(user_box)
		vbox.Add(pan,wx.ALIGN_CENTER|wx.TOP, border = 4)

		password_box = wx.BoxSizer(wx.HORIZONTAL)
		password_text = wx.StaticText(pan1, label = "Password")
#falta definir cuadro de texto
		password_box.Add(password_text,0,wx.ALL,5)
		self.password_camp = wx.TextCtrl(pan1,style=wx.TE_PASSWORD)
		password_box.Add(self.password_camp,wx.EXPAND)
		pan1.SetSizer(password_box)
		vbox.Add(pan1,wx.ALIGN_CENTER, border = 4)

		opt_box = wx.BoxSizer(wx.HORIZONTAL)
		if self.cancel_view:
			opt_cancel = wx.Button(self, wx.ID_CANCEL  )
			opt_box.Add(opt_cancel)
		opt_ok = wx.Button(self, wx.ID_OK  )
		opt_box.Add(opt_ok, flag =  wx.LEFT, border = 5)
		vbox.Add(opt_box, flag = wx.ALIGN_RIGHT|wx.BOTTOM, border = 4)
		self.SetSizer(vbox)

		#Binder
		self.Bind(wx.EVT_BUTTON, self.it_works, opt_ok)
	def it_works(self,e):
#Authentication		
		self.get_user = self.user_camp.GetValue()
		self.get_pass = self.password_camp.GetValue()
		try:
			smtpserver = smtplib.SMTP("smtp.gmail.com",587)
			smtpserver.ehlo()
			smtpserver.starttls()
			smtpserver.ehlo
			smtpserver.login(self.get_user, self.get_pass)
			smtpserver.close()
		except smtplib.SMTPAuthenticationError:
			wx.MessageBox('something went wrong','Introduce your keys again', wx.OK | wx.ICON_INFORMATION)
			self.user_camp.SetValue('')
			self.password_camp.SetValue('')
		else:
			connection = shelve.open('account.dat')
			connection['username'] = self.get_user
			connection['password'] = self.get_pass
			connection.close()
			self.Destroy()
class DialogGener(wx.Dialog):
	def __init__(self):
		super(DialogGener, self).__init__(None)
#		self.Aproveaccount()
		self.DialogUI()
		self.SetSize((300, 100))
		self.SetTitle("Specify Route...")
	def DialogUI(self):
		pan = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)	
		dial_box = wx.BoxSizer(wx.HORIZONTAL)
		dial_text = wx.StaticText(pan, label = "Route :")
#falta definir cuadro de texto
		dial_box.Add(dial_text,0,wx.ALL,5)
		dial_camp = wx.TextCtrl(pan)
		dial_box.Add(dial_camp,wx.EXPAND)
		pan.SetSizer(dial_box)
		vbox.Add(pan,wx.ALIGN_CENTER|wx.TOP, border = 4)
		opt_box = wx.BoxSizer(wx.HORIZONTAL)
		opt_close = wx.Button(self, wx.ID_CANCEL)
		opt_ok = wx.Button(self, wx.ID_OK  )
		opt_box.Add(opt_ok)
		opt_box.Add(opt_close, flag =  wx.LEFT, border = 5)
		vbox.Add(opt_box, flag = wx.ALIGN_RIGHT|wx.BOTTOM, border = 4)
		self.SetSizer(vbox)

#		self.Bind(wx.EVT_BUTTON, self.)

class Fedora(wx.Frame):
	def __init__(self, title= 'Fedora'):
		super(Fedora, self).__init__(None,id= -1, title = title, style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION |wx.CLOSE_BOX, size= (500,270))
		self.GeneralUI()
		self.Aproveaccount()
		self.Show()
	def GeneralUI(self):
		#menu
		menubar = wx.MenuBar()
		filemenu = wx.Menu()
		send_att = wx.MenuItem(filemenu,SEND_ATT, '&Send Attachment \t Select File')
		open_prompt = wx.MenuItem(filemenu,OPEN_PROMPT, '&Open Draft \t Open Draft')
		save_prompt = wx.MenuItem(filemenu, SAVE_PROMT, '&Save Draft\t save draft')
		close_opt = wx.MenuItem(filemenu, CLOSE, '&Close\tClose')
		filemenu.AppendItem(send_att)
		filemenu.AppendItem(save_prompt)
		filemenu.AppendItem(open_prompt)
		filemenu.AppendItem(close_opt)

		viewmenu = wx.Menu()
		cust_acc = wx.MenuItem(viewmenu, CUST_ACC, '&Change Account\t Change Account')
		viewmenu.AppendItem(cust_acc)

		menubar.Append(filemenu, '&File')
		menubar.Append(viewmenu, '&Edit')
		self.SetMenuBar(menubar)
		
		#layout
		panel = wx.Panel(self)
#		font = wx.SystemSettings_GetFont(self, wx.SYS_SYSTEM_FONT)

#		font.SetPointSize(9)
		box = wx.BoxSizer(wx.VERTICAL)

		#destiny

		destiny_box = wx.BoxSizer(wx.HORIZONTAL)
		destiny_text  = wx.StaticText(panel, label = "To :")
#		destiny_text.SetFont(font)
		destiny_box.Add(destiny_text, flag = wx.RIGHT, border = 5)
		self.destiny_camp = wx.TextCtrl(panel)
		destiny_box.Add(self.destiny_camp, proportion = 1)
		box.Add(destiny_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT| wx.TOP ,border = 8)
		box.Add((-1,10))
		#sub
		sub_box = wx.BoxSizer(wx.HORIZONTAL)
		sub_text = wx.StaticText(panel, label = "Sub :")
#		sub_text.SetFont(font)
		sub_box.Add(sub_text, flag = wx.RIGHT, border = 5)
		self.sub_camp =  wx.TextCtrl(panel)
		sub_box.Add(self.sub_camp, proportion = 1)
		box.Add(sub_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT ,border = 8)      
		 #body
		box.Add((-1,20))
		body = wx.BoxSizer(wx.HORIZONTAL)
		self.body_camp = wx.TextCtrl(panel,style = wx.TE_MULTILINE)
		body.Add(self.body_camp, proportion = 1, flag = wx.EXPAND)
		box.Add(body, flag = wx.EXPAND| wx.RIGHT | wx.LEFT, border = 4)
		box.Add((-1,10))
		
		#options
		opt_box = wx.BoxSizer(wx.HORIZONTAL)
		check_raw = wx.CheckBox(panel, label = " raw ")
#		check_raw.SetFont(font)
		opt_box.Add(check_raw)
		check_localhost = wx.CheckBox(panel, label = " localhost ")
#		check_localhost.SetFont(font)
		opt_box.Add(check_localhost)
		box.Add(opt_box, flag =  wx.LEFT  , border = 10 )
		box.Add((-1,10))

		#send
		
		send_box = wx.BoxSizer(wx.HORIZONTAL)
		send_button = wx.Button(panel,label= "Send!", size = (100,40))
		send_box.Add(send_button, flag  = wx.RIGHT | wx.BOTTOM, border = 5)
		box.Add(send_box, flag = wx.ALIGN_RIGHT |wx.LEFT, border = 10)
		
		panel.SetSizer(box)

		#status declaration
		self.statbar = self.CreateStatusBar()
		self.statbar.Hide()
		#Binder
		self.Bind(wx.EVT_MENU, self.attach_file, send_att)
		self.Bind(wx.EVT_MENU, self.on_open, open_prompt)
		self.Bind(wx.EVT_MENU, self.on_save, save_prompt)
		self.Bind(wx.EVT_MENU, self.on_quit , close_opt)
		self.Bind(wx.EVT_MENU, self.change_account, cust_acc)
		self.Bind(wx.EVT_BUTTON, self.send_mail_instant , send_button)


	#Fedora popups
	def successDialog(self):
		wx.MessageBox('Success at sending!','Good!', wx.OK | wx.ICON_INFORMATION)
	def handleDialog(self):
		wx.MessageBox('Error at sending', 'OMAIGA!', wx.OK | wx.ICON_ERROR)
	def attach_file(self,e):
		dlg = wx.FileDialog(self, message="Open a draft ...",defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.OPEN)	
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			print paths
		dlg.Destroy	
	def on_open(self,e):
		dlg = wx.FileDialog(self, message="Open a draft ...",defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.OPEN)	
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			print paths
		dlg.Destroy	
	def on_save(self,e):
		dlg = wx.FileDialog(self, message="Save file as ...",defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.SAVE)	
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			print paths
		dlg.Destroy	
	def change_account(self,e):
		changer =RaiseAuth(True)
		changer.ShowModal()
		changer.Destroy()
	def send_mail_instant(self, e):
		destiny_get = self.destiny_camp.GetValue()
		subject_get = self.sub_camp.GetValue()
		body_get = self.body_camp.GetValue()
		fol = re.match(regexion,destiny_get)
		if fol is None :
			wx.MessageBox('No Destiny?','Please insert a valid destiny', wx.OK | wx.ICON_INFORMATION)
		elif not destiny_get :
			wx.MessageBox('No Destiny?','Please insert a valid destiny', wx.OK | wx.ICON_INFORMATION)	
		elif not subject_get:
			wx.MessageBox('No subject?','Please insert a subject', wx.OK | wx.ICON_INFORMATION)
		elif not body_get:	
			wx.MessageBox('No body?','Please insert something?', wx.OK | wx.ICON_INFORMATION)
		else:
			if on_con() :
				s =shelve.open('account.dat')
				a_mail = Mail(s['username'],destiny_get,subject_get,body_get,s['password'],*attos)
				a_mail.send_it()
				s.close()
				self.successDialog()
				self.statbar.SetStatusText(str("Success at sending mail to",destiny_get))
			else:
				self.handleDialog()	
				self.statbar.SetStatusText("Error at sending mail")	
	def Aproveaccount(self):
		account_dat = shelve.open('account.dat')
		try:
			username = account_dat['username']
			password_key = account_dat['password']
			account_dat.close()	
		except KeyError:
			understand =RaiseAuth()
			understand.ShowModal()
			understand.Destroy()
		else:
			pass
	def on_quit(self,e):
		self.Close()			
class Mail(object):

	def __init__(self, account, reciever,subject, text,password, *attachments ):
		self.account = account
		self.reciever=reciever
		self.body = text
		self.subject = subject
		self.__password = password
		self.file_attachments = attachments
	def send_it(self):	
		#From Stack Exchange
		html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
		html +='"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
		html +='<body style="font-size:12px;font-family:Verdana"><p>...</p>'
		html += "</body></html>"
		msg = MIMEMultipart('alternative')
		msg['To'] = self.reciever
		msg['From'] = self.account
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = self.subject
		msg.attach(MIMEText(self.body))
		if self.file_attachments:
			for file_att in self.file_attachments:
				file_parser = MIMEBase('application', "octet-stream") 
				file_parser.set_payload( open(file_att,"rb").read() )
				Encoders.encode_base64(file_parser)
				file_parser.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_att))
				msg.attach(file_parser)
		smtpserver = smtplib.SMTP("smtp.gmail.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(self.account, self.getpwd())
		smtpserver.sendmail(self.account,self.reciever, msg.as_string())
		print "Yeah!"
		smtpserver.close()
	def	getpwd(self):
		return self.__password
def on_con():
    try:
        response=urllib2.urlopen('http://example.com',timeout=4)
        return True
    except urllib2.URLError as err: pass
    return False						
#superabstraction        
if __name__ == '__main__':
	app = wx.App()
	Fedora('Fedora test')
	app.MainLoop()







