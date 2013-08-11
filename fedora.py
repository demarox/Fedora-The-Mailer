#Fedora
import shelve
import wx
import wx.combo
import pdb
import os
import smtplib
import re
import string
import random
import urllib2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from xml.dom.minidom import parseString
import wx.lib.scrolledpanel as scroll

c = shelve.open('d_cache.dat')
directory_cache_list = c.values()
c.close()
trimmer='[]'
supported_regex = "\w+([-+.]\w+)*@(yahoo|gmail|hotmail|googlemail)\.com"
hotmail_regex = "\w+([-+.]\w+)*@hotmail.com"
yahoo_regex ="\w+([-+.]\w+)*@yahoo.com"
gmail_regex = "^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$"
regexion = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
attos = []
wildcard = "xml file (*.xml; *.xml)|*.xml;*.xml|" \
         "All files (*.*)|*.*"
SEND_ATT,OPEN_PROMPT,SAVE_PROMT, CLOSE,DEF_ACC,CUST_ACC,RESET_ALL,MY_ACC,MAN_F = 1,2,3,4,5,6,7,8,9
		
class Gauger(wx.Frame):
	def __init__(self,parent,task_range):
		super(Gauger, self).__init__(None)
		self.parent = parent
		self.task_range = task_range
		self.GaugeBox()
		self.Centre()
		self.Show(True)	
	def GaugeBox(self):
		panel = wx.Panel(self)
		bmp2 = wx.Image('img/gauge.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		panel.bitmap2 = wx.StaticBitmap(panel, -1, bmp2, (0, 0))
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		vbox.Add(-1,20)
		self.gauge = wx.Gauge(panel, range=self.task_range, size=(250, 50))
		self.text = wx.StaticText(panel, label='Sending...')
		self.text.SetFont(self.parent.font)
		hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
		vbox.Add(hbox1,flag=wx.ALIGN_CENTRE|wx.TOP, border =5)
		hbox2.Add(self.text)
		vbox.Add((-1,10))
		vbox.Add(hbox2,flag=wx.ALIGN_CENTRE)
		panel.SetSizer(vbox)
		self.SetSize((300, 130))
		self.SetTitle('wx.Gauge')
	def add_to_gauge(self):	
		completed  = self.gauge.GetValue()
		remain = self.task_range - completed
		completed += 1
		self.gauge.SetValue(completed)
		self.text.SetLabel('Tasks Done ('+str(completed)+')')
		if completed == self.task_range :
			self.Destroy()
	def Explode(self):
			self.Destroy()							
class RaiseAuth(wx.Frame):
	def __init__(self,parent,cancel_view = False):
		super(RaiseAuth, self).__init__(None,style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION ,size = (300,250), pos=(920,80))
		self.parent = parent
		self.cancel_view = cancel_view
		self.DialogUI()
		self.SetTitle("Authenticate please...")
		if cancel_view== False:
			self.Centre()
		self.Show()
	def DialogUI(self):
		pan = wx.Panel(self)
		bmp2 = wx.Image('img/dialog.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		pan.bitmap2 = wx.StaticBitmap(pan, -1, bmp2, (0, 0))
		vbox = wx.BoxSizer(wx.VERTICAL)	
		vbox.Add((-1,110))
	
		user_box = wx.BoxSizer(wx.HORIZONTAL)
		user_text = wx.StaticText(pan, label = "User")
		user_text.SetFont(self.parent.font)
		user_box.Add(user_text ,flag = wx.ALIGN_CENTRE)
		self.user_camp = wx.TextCtrl(pan)
		user_box.Add(self.user_camp, flag = wx.ALIGN_CENTRE |wx.EXPAND|wx.ALL,proportion = 1)
		vbox.Add(user_box,flag =  wx.ALIGN_CENTRE |wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
		vbox.Add((-1,10))
		password_box = wx.BoxSizer(wx.HORIZONTAL)
		password_text = wx.StaticText(pan, label = "Password")
		password_text.SetFont(self.parent.font)
		password_box.Add(password_text)
		self.password_camp = wx.TextCtrl(pan,style=wx.TE_PASSWORD)
		password_box.Add(self.password_camp, proportion = 1)
		vbox.Add(password_box,flag =  wx.ALIGN_CENTRE |wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
		vbox.Add((-1,10))
		opt_box = wx.BoxSizer(wx.HORIZONTAL)
		if self.cancel_view:
			opt_cancel = wx.Button(pan, wx.ID_CANCEL  )
			opt_box.Add(opt_cancel)
		opt_ok = wx.Button(pan, wx.ID_OK  )
		opt_box.Add(opt_ok, flag =  wx.LEFT, border = 5)
		vbox.Add(opt_box, flag = wx.ALIGN_CENTRE|wx.BOTTOM, border = 4)
		pan.SetSizer(vbox)

		#Binder
		self.Bind(wx.EVT_BUTTON, self.it_works, opt_ok)
		self.Bind(wx.EVT_BUTTON, self.close, opt_cancel)
	def it_works(self,e):
#Authentication		
		self.get_user = self.user_camp.GetValue()
		self.get_pass = self.password_camp.GetValue()
		match_mail = re.match(supported_regex,self.get_user)
		if match_mail:

			try:
				gmail_serv =re.match(gmail_regex,self.get_user)
				yahoo_serv =re.match(yahoo_regex, self.get_user)
				hotmail_serv =  re.match(hotmail_regex,self.get_user)
				if gmail_serv:
					smtpserver = smtplib.SMTP("smtp.gmail.com",587)			
				elif yahoo_serv:
					smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
				elif hotmail_serv:
					smtpserver = smtplib.SMTP("smtp.live.com",587)
				else:
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
		else:
			wx.MessageBox('Only gmail, hotmail, and yahoo! are used','Introduce a valid mail', wx.OK | wx.ICON_INFORMATION)	
	def close(self,e):
		self.Close()	
class DropTarget(wx.FileDropTarget):
	def __init__(self,parent):
		wx.FileDropTarget.__init__(self)
		self.parent = parent
	def OnDropFiles(self, x, y, filenames):
		self.parent.SetInsertionPointEnd()
		for filepath in filenames:
			self.parent.updateFiles(filepath)

class Man_at_files(wx.Frame):
	def __init__(self,parent):
		super(Man_at_files, self).__init__(None,pos =(10,50), style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION|wx.CLOSE_BOX)
		self.parent = parent
		self.dict_button = {}
		self.in_box = {}
		self.dest_text = {}
		self.FrameUI()
		self.SetTitle('Files added')
		self.SetSize((350,600))
		self.Show()
		
	def FrameUI(self):
		bmp = wx.Bitmap("img/close.png", wx.BITMAP_TYPE_ANY)
		panel = wx.PyScrolledWindow(self,-1,style = wx.VSCROLL)
		panel.SetScrollbars(0, 1, 0, 1)
		panel.SetScrollRate( 1, 1 ) 
		box = wx.BoxSizer(wx.VERTICAL)
		bmp3 = wx.Image('img/file_man.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		panel.bitmap2 = wx.StaticBitmap(panel, -1, bmp3, (0, 0))
		box.Add((-1,130))
		for path in attos:
			asc_id =self.id_generator()
			self.in_box[path] = wx.BoxSizer(wx.HORIZONTAL)
			label = '...'+path[-25:]
			self.dest_text[path] = wx.StaticText(panel,label =label)
			self.dest_text[path].SetFont(self.parent.font)
			self.in_box[path].Add(self.dest_text[path])	
			self.dict_button[path] = wx.BitmapButton(panel, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=bmp,size=(bmp.GetWidth()+5, bmp.GetHeight()+5))
			self.dict_button[path].parameterVal = path
			self.in_box[path].Add(self.dict_button[path],flag = wx.ALIGN_RIGHT,border =5)
			box.Add(self.in_box[path],flag = wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT, border = 20)
			box.Add((-1,10))
			self.Bind(wx.EVT_BUTTON, self.destroy_file_path,self.dict_button[path])
		panel.SetSizer(box)	
	def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))	
	def destroy_file_path(self,e):
		button = e.GetEventObject()
		idi = button.parameterVal
		if idi in attos: 
			self.parent.statbar.SetStatusText(idi+" removed")
			attos.remove(idi)
			self.dest_text[idi].Hide()
			self.dict_button[idi].Hide()
			self.in_box[idi].Remove(True)


			self.parent.clear_and_update()
	def Explode(self):
		self.Destroy()		
		
class Fedora(wx.Frame):
	def __init__(self, title= 'Fedora'):
		super(Fedora, self).__init__(None,id= -1, title = title, style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION |wx.CLOSE_BOX, size= (500,570))
		self.GeneralUI()
		self.Aproveaccount()
		self.Centre()
		self.Show()
	def GeneralUI(self):
		#background
		#menu
		self.font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
		menubar = wx.MenuBar()
		filemenu = wx.Menu()
		send_att = wx.MenuItem(filemenu,SEND_ATT, '&Send Attachment \tCtrl+A')
		open_prompt = wx.MenuItem(filemenu,OPEN_PROMPT, '&Open Draft \tCtrl+O')
		save_prompt = wx.MenuItem(filemenu, SAVE_PROMT, '&Save Draft\tCtrl+S')
		close_opt = wx.MenuItem(filemenu, CLOSE, '&Close\tCtrl+Q')
		filemenu.AppendItem(send_att)
		filemenu.AppendItem(save_prompt)
		filemenu.AppendItem(open_prompt)
		filemenu.AppendItem(close_opt)

		editmenu = wx.Menu()
		cust_acc = wx.MenuItem(editmenu, CUST_ACC, '&Change Account\tAlt+C')
		reset_all = wx.MenuItem(editmenu, RESET_ALL, '&Reset \tAlt+R')
		editmenu.AppendItem(cust_acc)
		editmenu.AppendItem(reset_all)

		viewmenu = wx.Menu()
		my_acc = wx.MenuItem(viewmenu,MY_ACC,'&My Account\tCtrl+M')
		manage_files = wx.MenuItem(viewmenu,MAN_F,'&Manage Files\tCtrl+F')
		viewmenu.AppendItem(my_acc)
		viewmenu.AppendItem(manage_files)

		menubar.Append(filemenu, '&File')
		menubar.Append(editmenu, '&Edit')
		menubar.Append(viewmenu, '&View')
		self.SetMenuBar(menubar)
		
		#layout
		panel = wx.Panel(self)
		box = wx.BoxSizer(wx.VERTICAL)

		bmp1 = wx.Image('img/back.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		panel.bitmap1 = wx.StaticBitmap(panel, -1, bmp1, (0, 0))
		box.Add((-1,110))
		#destiny
		destiny_box = wx.BoxSizer(wx.HORIZONTAL)
		destiny_text  = wx.StaticText(panel, label = "To :")
		destiny_text.SetFont(self.font)
		destiny_box.Add(destiny_text, flag = wx.RIGHT, border = 5)
		self.destiny_camp =  wx.ComboBox(panel, -1, choices = directory_cache_list)
#		cp = ComboPopup()
#		self.destiny_camp.SetPopupControl(cp)
		destiny_box.Add(self.destiny_camp, proportion = 1)
		box.Add(destiny_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT| wx.TOP ,border = 23)
		box.Add((-1,10))
		#sub
		sub_box = wx.BoxSizer(wx.HORIZONTAL)
		sub_text = wx.StaticText(panel, label = "Sub :")
		sub_text.SetFont(self.font)
		sub_box.Add(sub_text, flag = wx.RIGHT, border = 5)
		self.sub_camp =  wx.TextCtrl(panel)
		sub_box.Add(self.sub_camp, proportion = 1)
		box.Add(sub_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT ,border = 23)      
		 #body
		box.Add((-1,20))
		body = wx.BoxSizer(wx.HORIZONTAL)
		self.body_camp = wx.TextCtrl(panel,style = wx.TE_MULTILINE)
		body.Add(self.body_camp, proportion = 1, flag = wx.EXPAND)
		box.Add(body, flag = wx.EXPAND| wx.RIGHT | wx.LEFT, border = 23)
		box.Add((-1,10))

		#file_viewer
		text_drop = wx.BoxSizer(wx.HORIZONTAL)
		lbl = wx.StaticText(panel, label="Drag your files:")
		lbl.SetFont(self.font)
		text_drop.Add(lbl)
		box.Add(text_drop,flag = wx.RIGHT|wx.LEFT,border = 23)

		file_drop = wx.BoxSizer(wx.HORIZONTAL)
		file_drop_target = DropTarget(self)
		self.fileTextCtrl = wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.TE_READONLY)	
		self.fileTextCtrl.SetDropTarget(file_drop_target)
		file_drop.Add(self.fileTextCtrl, proportion = 1, flag = wx.EXPAND)
		box.Add(file_drop, 1, wx.EXPAND|wx.ALL, 23)
		box.Add((-1,10))
		#send
		
		send_box = wx.BoxSizer(wx.HORIZONTAL)
		send_button = wx.Button(panel,label= "Send!", size = (100,40))
		send_box.Add(send_button, flag  = wx.RIGHT | wx.BOTTOM)
		box.Add(send_box, flag = wx.ALIGN_RIGHT |wx.LEFT|wx.RIGHT, border = 23)
		
		panel.SetSizer(box)
		#status declaration
		self.statbar = self.CreateStatusBar()

		#Binder
		self.Bind(wx.EVT_MENU, self.attach_file, send_att)
		self.Bind(wx.EVT_MENU, self.on_open, open_prompt)
		self.Bind(wx.EVT_MENU, self.on_save, save_prompt)
		self.Bind(wx.EVT_MENU, self.on_quit , close_opt)
		self.Bind(wx.EVT_MENU, self.change_account, cust_acc)
		self.Bind(wx.EVT_MENU, self.reseter, reset_all)
		self.Bind(wx.EVT_MENU, self.account_data, my_acc)
		self.Bind(wx.EVT_MENU, self.manageFiles, manage_files)
		self.Bind(wx.EVT_BUTTON, self.send_mail_instant , send_button)
		self.Bind(wx.EVT_TEXT,self.select_mails ,self.destiny_camp)
		#Accelerators
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('A'), send_att.GetId() ),(wx.ACCEL_CTRL,  ord('F'), manage_files.GetId() ),(wx.ACCEL_CTRL,  ord('S'), save_prompt.GetId() ),(wx.ACCEL_CTRL,  ord('O'), open_prompt.GetId() ),(wx.ACCEL_CTRL,  ord('Q'), close_opt.GetId() ),(wx.ACCEL_ALT,  ord('C'), cust_acc.GetId() ),(wx.ACCEL_ALT,  ord('R'), reset_all.GetId() ),(wx.ACCEL_CTRL,  ord('M'), my_acc.GetId() )])
		self.SetAcceleratorTable(accel_tbl)


	#Fedora popups
	def successDialog(self):
		wx.MessageBox('Success at sending!','Good!', wx.OK | wx.ICON_INFORMATION)
	def handleDialog(self):
		wx.MessageBox('Error at sending', 'OMAIGA!', wx.OK | wx.ICON_ERROR)
	def clear_and_update(self):
		self.fileTextCtrl.Clear()
		for path in attos:
			splitter = path.split('/')
			splitter = splitter[-1]
			splitter = splitter if len(path)<=35 else splitter[0:33]+'...'
			self.fileTextCtrl.WriteText(splitter+"\n")
	def attach_file(self,e):
		dlg = wx.FileDialog(self, message="Open a File...",defaultDir=os.getcwd(), defaultFile="",  style=wx.OPEN)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
#			print path
			self.updateFiles(path)
			self.statbar.SetStatusText("File Correctly Added!")
		dlg.Destroy	
		
	def on_open(self,e):
		dlg = wx.FileDialog(self, message="Open a draft...",defaultDir=os.getcwd(), defaultFile="",  style=wx.OPEN)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
			file_read = open(path,'r')
			d = file_read.read()
			file_read.close()
			parse_d = parseString(d)
			to_tag = parse_d.getElementsByTagName('to')[0].toxml()
			to_data = to_tag.replace('<to>','').replace('</to>','')		
			subject_tag = parse_d.getElementsByTagName('subject')[0].toxml()
			subject_data = subject_tag.replace('<subject>','').replace('</subject>','')			
			body_tag = parse_d.getElementsByTagName('body')[0].toxml()
			body_data = body_tag.replace('<body>','').replace('</body>','')

			self.destiny_camp.SetValue(to_data)
			self.sub_camp.SetValue(subject_data)
			self.body_camp.SetValue(body_data)
		dlg.Destroy	

	def on_save(self,e):
		dlg = wx.FileDialog(self, message="Save Draft as...",defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.SAVE)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
			destiny_get = self.destiny_camp.GetValue()
			subject_get = self.sub_camp.GetValue()
			body_getter = self.body_camp.GetValue()
			file_saver = open(path,'w')
			file_saver.write('<?xml version ="1.0" encoding="utf-8" ?>\n')
			file_saver.write("<mail>")
			file_saver.write("\t<to>"+destiny_get+"</to>\n")
			file_saver.write("\t<subject>"+subject_get+"</subject>\n")
			file_saver.write("\t<body>"+body_getter+"</body>\n")
			file_saver.write("</mail>")
			file_saver.close
			self.statbar.SetStatusText("Draft saved!")
		dlg.Destroy	
	def reseter(self,e):
		self.destiny_camp.SetValue('')
		self.sub_camp.SetValue('')
		self.body_camp.SetValue('')
		self.fileTextCtrl.Clear()
		del attos[:]
		self.statbar.SetStatusText('Clear!')
		print attos
	def change_account(self,e):
		RaiseAuth(self,True)
#		changer.Destroy()
	def SetInsertionPointEnd(self):
		self.fileTextCtrl.SetInsertionPointEnd()
	def updateFiles(self,path):	
		if path in attos:
			pass
		else:	
			self.SetInsertionPointEnd()
			attos.append(str(path))
			splitter = path.split('/')
			splitter = splitter[-1]
   			splitter = splitter if len(path)<=35 else splitter[0:33]+'...'
   			self.fileTextCtrl.WriteText(splitter+"\n")
	def account_data(self,e):
		account_dat = shelve.open('account.dat')
		account_info = wx.AboutDialogInfo()
		person_ico = wx.Icon('img/person_icon.png', wx.BITMAP_TYPE_PNG)
		account_info.SetIcon(person_ico)
		account_info.SetName(account_dat['username'])
		account_info.SetDescription('                                                         ')
		account_info.SetWebSite('https://github.com/demarox')
		account_info.AddDeveloper('Demarox')
		wx.AboutBox(account_info)
		account_dat.close()
	def select_mails(self,e):
			self.destiny_camp.Clear()
			self.destiny_camp.SetInsertionPointEnd()
			destiny_get = self.destiny_camp.GetValue()
			for element in directory_cache_list:
				fol = re.match(destiny_get,element)
				if fol :
					self.destiny_camp.Append(element)
	def manageFiles(self,e):

		Man_at_files(self)
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
				a_mail = Mail(s['username'],destiny_get,subject_get,body_get,s['password'],self,*attos)
				s.close()
				a_mail.send_it()
				#Cache for name directory
				c = shelve.open('d_cache.dat')
				
				c[destiny_get] = destiny_get
				c.close()
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
			understand =RaiseAuth(self)
			understand.ShowModal()
			understand.Destroy()
		else:
			pass

	def on_quit(self,e):
		self.Close()			
class Mail(object):

	def __init__(self, account, reciever,subject, text,password,parent, *attachments ):
		self.account = account
		self.reciever=reciever
		self.body = text
		self.subject = subject
		self.__password = password
		self.file_attachments = attachments
		self.parent = parent
	def send_it(self):	
		length = len(self.file_attachments)
		progress_frame = Gauger(self,length+3)

		msg = MIMEMultipart('alternative')
		msg['To'] = self.reciever
		msg['From'] = self.account
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = self.subject
		msg.attach(MIMEText(self.body))
		progress_frame.add_to_gauge()
		if self.file_attachments:
			for file_att in self.file_attachments:
				try:
					file_parser = MIMEBase('application', "octet-stream") 
					file_parser.set_payload( open(file_att,"rb").read() )
					Encoders.encode_base64(file_parser)
					file_parser.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_att))
					msg.attach(file_parser)
					progress_frame.add_to_gauge()
				except IOError:
					wx.MessageBox('file attachment deleted or removed','Oops!', wx.OK | wx.ICON_INFORMATION)
		gmail_serv =re.match(gmail_regex,self.account)
		yahoo_serv =re.match(yahoo_regex, self.account)
		hotmail_serv = re.match(hotmail_regex,self.account)
		if gmail_serv:
			smtpserver = smtplib.SMTP("smtp.gmail.com",587)			
		elif yahoo_serv:
			smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
		elif hotmail_serv:
			smtpserver = smtplib.SMTP("smtp.live.com",587)
		else:
			smtpserver = smtplib.SMTP("smtp.gmail.com",587)	
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(self.account, self.getpwd())
		progress_frame.add_to_gauge()
		try:
			
			smtpserver.sendmail(self.account,self.reciever, msg.as_string())
		except smtplib.SMTPSenderRefused :	
			progress_frame.Explode()
			wx.MessageBox('Please Use Google Drive or MEGA links','The File Load is Too Big', wx.OK | wx.ICON_INFORMATION)
			self.parent.statbar.SetStatusText("Mail Error :(" )
		else:
			progress_frame.add_to_gauge()
			self.parent.successDialog()
			self.parent.statbar.SetStatusText(str("Success at sending mail to " + self.reciever))
		smtpserver.close()
	def	getpwd(self):
		return self.__password

def on_con():
	try:
		response=urllib2.urlopen('http://example.com',timeout=5)
		return True
	except urllib2.URLError as err: pass
	return False						
#superabstraction        
if __name__ == '__main__':
	app = wx.App()
	Fedora()
	app.MainLoop()






