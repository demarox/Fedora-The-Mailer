#Yubin

import shelve
import wx
import wx.combo
import pdb
import os
import smtplib
import re
import webbrowser
import string
import random
import time
import threading
import urllib2
from threading import Thread
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from xml.dom.minidom import parseString
import  wx.lib.scrolledpanel as scrolled
trimmer='[]'
supported_regex = "\w+([-+.]\w+)*@(yahoo|gmail|hotmail|googlemail)\.com"
hotmail_regex = "\w+([-+.]\w+)*@hotmail.com"
yahoo_regex ="\w+([-+.]\w+)*@yahoo.com"
gmail_regex = "^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$"
regexion = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
attos = []        
SEND_ATT,OPEN_PROMPT,SAVE_PROMT, CLOSE,DEF_ACC,CUST_ACC,RESET_ALL,MY_ACC,MAN_F,MAN_F_X,OPEN_ALL,ACC_X,CUST_X,HELP,IMPORT,EXPORT,CREATE_CONTACT,CONTACT_LIST,CONTACT_LIST_X,EDIT_CONTACT_LIST = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20

class Man_at_contacts(wx.Frame):
	def __init__(self,parent):
		super(Man_at_contacts,self).__init__(None,style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION |wx.CLOSE_BOX,size = (350,400), pos=(300,300))				
		self.parent = parent
		self.box_mail = {}
		self.text = {}
		self.title = {}
		self.mail_text = {}
		self.control_button = {}
		self.control_box = {}
		self.description_box = {}
		self.general_box = {}
		self.boxer = {}
		self.ContactsUI()
		self.SetTitle('Drag Contact')
		self.Show()
	def ContactsUI(self):
		bmp9 = wx.Bitmap("img/close.png", wx.BITMAP_TYPE_ANY)
		self.panel = wx.PyScrolledWindow(self,-1,style = wx.VSCROLL)
		self.panel.SetScrollbars(0, 1, 0, 1)
		self.panel.SetScrollRate( 1, 1 ) 
		self.box = wx.BoxSizer(wx.VERTICAL)
		bmp3 = wx.Image('img/contacts.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.panel.bitmap2 = wx.StaticBitmap(self.panel, -1, bmp3, (0, 0))
		self.box.Add((-1,140))
		core_list = shelve.open('DDRM3A2.dat')
		core_keys = core_list.keys()
		core_values = core_list.values()
		if core_list:
	
			for key,value in core_list.iteritems():

				pass
 		else:
 			self.box.Add((-1,50))
 			self.boxer = wx.BoxSizer(wx.HORIZONTAL)
			self.title = wx.StaticText(self.panel,label = 'Ctrl+D To Add Contacts' )
			self.title.SetFont(self.parent.font3)
			self.title.SetForegroundColour((117,113,113))
			self.boxer.Add(self.title)
			self.box.Add(self.boxer, flag = wx.ALIGN_CENTRE, border = 25)	
		self.panel.SetSizer(self.box)
		core_list.close()	
	def destroy_contact(self,key):
		self.box_mail[key].Remove()
		self.boxer[key].Remove()
		self.text[key].Hide()
		self.mail_text[key].Hide()
		self.control_button[key].Hide()
		self.control_box[key].Remove()
		self.description_box[key].Remove()

		c = shelve.open('DDRM3A2.dat')
		del c[key]
		c.close()

		self.parent.statbar.SetStatusText(key + ' Removed!')
		
	def on_know(self,e):
		x = e.GetEventObject()
		y = x.parameterVal 

		self.PopupMenu(Control_button_popup_menu(self,self.parent,y), e.GetPosition())
	def Explode(self):
		self.Close()	
	def call(self):
		return 
class Control_button_popup_menu(wx.Menu):
			def __init__(self, parent,grandfather,key):
				super(Control_button_popup_menu, self).__init__()
				self.parent = parent
				self.grandfather = grandfather
				self.key = key

				edit_opt = wx.MenuItem(self, wx.NewId(),'Edit')
				self.AppendItem(edit_opt)
				self.Bind(wx.EVT_MENU, self.on_edit, edit_opt)

				destroy_opt = wx.MenuItem(self, wx.NewId(),'Remove')
				self.AppendItem(destroy_opt)
				self.Bind(wx.EVT_MENU, self.on_destroy , destroy_opt)
			def on_edit(self, e):
#				self.grandfather.launch_editor()
				pass
			def on_destroy(self,e):
				self.parent.destroy_contact(self.key)								
class Trash_Engine(wx.Frame):
	def __init__(self,parent):
		super(Contact_Engineer,self).__init__(None,style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION |wx.CLOSE_BOX,size = (350,400), pos=(300,300))				
		self.parent = parent
		self.EngineUI()
		self.SetTitle('Drag to the Trash!')
		self.Show()
	def EngineUI(self):
			pass	
	def Explode(self):
		self.Close()
	def call(self):
		return 	
class DragTxt(wx.StaticText):
	def __init__(self, parent ,panel_parent,grandfather, key):
			wx.StaticText.__init__(self, panel_parent, label=key)
			self.key = str(key)
			self.parent = parent
			self.grandfather = grandfather
			self.SetFont(self.grandfather.font2)
			self.parameterVal = key
			self.Bind(wx.EVT_LEFT_DOWN, self.drag_act)
			self.Bind(wx.EVT_LEFT_DCLICK, self.append_to_Ctrl)
	def drag_act(self, event):
			ds = wx.DropSource(self.GetParent())
			d = wx.PyTextDataObject(self.key)
			ds.SetData(d)
			ds.DoDragDrop(True)
	def append_to_Ctrl(self,evt):
		self.grandfather.append_to_Ctrl(self.key)
		#self.parent.show_ctrl(self.key)
class Add_Contact_PopUp(wx.Frame):
	def __init__(self,parent):
		super(Add_Contact_PopUp, self).__init__(None,style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX ,size = (300,200))
		self.parent = parent
		self.Simple_UI()
		self.SetTitle("Add Someone!")
		self.Centre()
		self.Show()
	def Simple_UI(self):
		pan = wx.Panel(self)
		bmp7 = wx.Bitmap("img/add.png", wx.BITMAP_TYPE_ANY)
		bmp6 = wx.Image('img/add_contact.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		pan.bitmap6 = wx.StaticBitmap(pan, -1, bmp6, (0, 0))
		vbox = wx.BoxSizer(wx.VERTICAL)	
		vbox.Add((-1,110))
	
		name_box = wx.BoxSizer(wx.HORIZONTAL)
		name_text = wx.StaticText(pan, label = "Name :")
		name_text.SetFont(self.parent.font)
		name_box.Add(name_text ,flag = wx.ALIGN_CENTRE)
		self.name_camp = wx.TextCtrl(pan)
		name_box.Add(self.name_camp, flag = wx.ALIGN_CENTRE |wx.EXPAND|wx.ALL,proportion = 1)
		vbox.Add(name_box,flag =  wx.ALIGN_CENTRE |wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
		vbox.Add((-1,9))
		mail_box = wx.BoxSizer(wx.HORIZONTAL)
		mail_text = wx.StaticText(pan, label = "Mail :")
		mail_text.SetFont(self.parent.font)
		mail_box.Add(mail_text)

		self.button = wx.BitmapButton(pan, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=bmp7,size=(bmp7.GetWidth()+5, bmp7.GetHeight()+5))

		self.mail_camp = wx.TextCtrl(pan)
		mail_box.Add(self.mail_camp, proportion = 1)
		mail_box.Add(self.button, flag = wx.ALIGN_RIGHT,border =5)
		vbox.Add(mail_box,flag =  wx.ALIGN_CENTRE |wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
		pan.SetSizer(vbox)	

		self.Bind(wx.EVT_BUTTON, self.add_act , self.button)
	def add_act(self,evt):
		name=self.name_camp.GetValue() 
		mail=self.mail_camp.GetValue() 
		name = name.strip()
		mail = mail.strip()
		fol = re.match(regexion,mail)
		if fol :	
			self.parent.add_contact_permanency(name, mail)
			self.parent.statbar.SetStatusText(name + ' correctly added!')	
			self.Close()
		else :
			RaisePopup('Set a valid mail','please use a mail format')	
			self.mail_camp.GetValue()
			
class Gauger(wx.Frame):
	def __init__(self,grandfather,task_range):
		super(Gauger, self).__init__(None,style=wx.CAPTION)
		self.grandfather = grandfather
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
		self.gauge = wx.Gauge(panel, range=self.task_range, size=(250, 50))
		self.text = wx.StaticText(panel, label='Sending...')
		self.text.SetFont(self.grandfather.font)
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
		wx.Yield()
		if completed == self.task_range :
			self.Close()
			
	def Explode(self):
			self.Close()

class RaiseAuth(wx.Frame):
	def __init__(self,parent,cancel_view = False):
		super(RaiseAuth, self).__init__(None,style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION ,size = (300,250), pos=(920,80))
		self.parent = parent
		self.cancel_view = cancel_view
		self.DialogUI()
		self.SetTitle("Authentication")
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
		user_text = wx.StaticText(pan, label = "User :")
		user_text.SetFont(self.parent.font)
		user_box.Add(user_text ,flag = wx.ALIGN_CENTRE)
		self.user_camp = wx.TextCtrl(pan)
		user_box.Add(self.user_camp, flag = wx.ALIGN_CENTRE |wx.EXPAND|wx.ALL,proportion = 1)
		vbox.Add(user_box,flag =  wx.ALIGN_CENTRE |wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
		vbox.Add((-1,10))
		password_box = wx.BoxSizer(wx.HORIZONTAL)
		password_text = wx.StaticText(pan, label = "Password :")
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
		if self.cancel_view:

			self.Bind(wx.EVT_BUTTON, self.close, opt_cancel)
	def it_works(self,e):
	#Authentication	
		if on_con():	
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
					RaisePopup('Authentication Error','Introduce your keys again')
					self.user_camp.SetValue('')
					self.password_camp.SetValue('')
				else:
					connection = shelve.open('account.dat')
					connection['username'] = self.get_user
					connection['password'] = self.get_pass
					connection.close()
					self.parent.Show()
					if self.cancel_view== False:
						self.parent.open_all(True)
					else:
						self.parent.set_info_label(self.get_user)
					self.Destroy()
			else:	
				RaisePopup('No @ Support Error','Only gmail,yahoo! and hotmail')
		else:
			self.parent.handleDialog()		
	def call(self):
			return 	
	def close(self,e):
		self.Close()
	def Explode(self):
		self.Close()		
class DropTarget(wx.FileDropTarget):
	def __init__(self,parent):
		wx.FileDropTarget.__init__(self)
		self.parent = parent
	def OnDropFiles(self, x, y, filenames):
		self.parent.SetInsertionPointEnd()
		for filepath in filenames:
			self.parent.updateFiles(filepath)
class MyTextDropTarget(wx.TextDropTarget):
	def __init__(self, parent):
		wx.TextDropTarget.__init__(self)
		self.parent = parent
	def OnDropText(self, x, y, text):
		to_eval = self.parent.destiny_camp.GetValue()
		if to_eval:
			self.parent.destiny_camp.WriteText(", "+text)
		else:
			self.parent.destiny_camp.WriteText(text)				

class RaisePopup(wx.Frame):
	def __init__(self,title,text):
		super(RaisePopup, self).__init__(None,style=wx.CAPTION,size=(300,200))
		self.title = title
		self.text = text
		self.LittleUI()
		self.Centre()
		self.SetTitle(self.title)
		self.Show()
	def LittleUI(self):
		panel = wx.Panel(self)
		bmp6 = wx.Image('img/raise.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		panel.bitmap2 = wx.StaticBitmap(panel, -1, bmp6, (0, 0))
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.text = wx.StaticText(panel, label=self.text)
		self.font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.text.SetFont(self.font)
		hbox1.Add(self.text)
		vbox.Add((-1,100))
		vbox.Add(hbox1,flag=wx.ALIGN_CENTRE)
		vbox.Add((-1,10))
		box = wx.BoxSizer(wx.HORIZONTAL)
		button = wx.Button(panel,label= "Ok", size = (100,40))
		box.Add(button, flag  = wx.RIGHT | wx.BOTTOM)
		vbox.Add(box, flag = wx.ALIGN_CENTRE |wx.LEFT|wx.RIGHT, border = 23)
		self.Bind(wx.EVT_BUTTON,self.quit, button)
		panel.SetSizer(vbox)
	def quit(self,e):
		self.Close()			
class SuccessPopup(wx.Frame):
	def __init__(self):
		super(SuccessPopup, self).__init__(None,style=wx.CAPTION,size=(300,130))
		self.LittleUI()
		self.Centre()
		self.Show()
	def LittleUI(self):
		panel = wx.Panel(self)
		bmp6 = wx.Image('img/success.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		panel.bitmap2 = wx.StaticBitmap(panel, -1, bmp6, (0, 0))
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.text = wx.StaticText(panel, label='Success At Sending!')
		self.font = wx.Font(18, wx.MODERN, wx.NORMAL, wx.BOLD)
		self.text.SetFont(self.font)
		hbox1.Add(self.text)
		vbox.Add((-1,55))
		vbox.Add(hbox1,flag=wx.ALIGN_CENTRE)
		vbox.Add((-1,5))
		box = wx.BoxSizer(wx.HORIZONTAL)
		button = wx.Button(panel,label= "Ok!", size = (80,35))
		box.Add(button, flag  = wx.RIGHT | wx.BOTTOM)
		vbox.Add(box, flag = wx.ALIGN_CENTRE |wx.LEFT|wx.RIGHT, border = 23)
		self.Bind(wx.EVT_BUTTON,self.quit, button)
		panel.SetSizer(vbox)
	def quit(self,e):
		self.Close()			
class Man_at_files(wx.Frame):
	def __init__(self,parent):
		super(Man_at_files, self).__init__(None,pos =(10,50), style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION|wx.CLOSE_BOX)
		self.parent = parent
		self.dict_button = {}
		self.in_box = {}
		self.dest_text = {}
		self.FrameUI()

		self.SetTitle('File Manager')
		self.SetSize((350,400))
		self.Show()
		
	def FrameUI(self):
		self.bmp = wx.Bitmap("img/close.png", wx.BITMAP_TYPE_ANY)
		self.panel = wx.ScrolledWindow(self,-1,style = wx.VSCROLL)
		self.panel.SetScrollbars(0, 1, 0, 1)
		self.panel.SetScrollRate( 1, 1 ) 
		self.box = wx.BoxSizer(wx.VERTICAL)
		bmp3 = wx.Image('img/file_man.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.panel.bitmap2 = wx.StaticBitmap(self.panel, -1, bmp3, (0, 0))
		self.Boot()
	def Boot(self):	
		self.box.Add((-1,130))
		if attos :
			for path in attos:
				self.in_box[path] = wx.BoxSizer(wx.HORIZONTAL)
				label = '...'+path[-27:]
				self.dest_text[path] = wx.StaticText(self.panel,label =label)
				self.dest_text[path].SetFont(self.parent.font)
				self.in_box[path].Add(self.dest_text[path])	

				self.dict_button[path] = wx.BitmapButton(self.panel, id=wx.ID_ANY, style=wx.NO_BORDER, bitmap=self.bmp,size=(self.bmp.GetWidth()+5, self.bmp.GetHeight()+5))
				self.dict_button[path].parameterVal = path
				
				self.in_box[path].Add(self.dict_button[path],flag = wx.ALIGN_RIGHT,border =5)
				self.box.Add(self.in_box[path],flag = wx.RIGHT|wx.LEFT|wx.ALIGN_RIGHT, border = 20)
				self.box.Add((-1,10))
				self.Bind(wx.EVT_BUTTON, self.destroy_file_path,self.dict_button[path])
		else:
			self.box.Add((-1,50))
 			self.boxer = wx.BoxSizer(wx.HORIZONTAL)
			self.title = wx.StaticText(self.panel,label = 'Drag your files or Ctrl+T' )
			self.title.SetFont(self.parent.font3)
			self.title.SetForegroundColour((117,113,113))
			self.boxer.Add(self.title)
			self.box.Add(self.boxer, flag = wx.ALIGN_CENTRE, border = 25)				
		self.panel.SetSizer(self.box)
		self.panel.FitInside()
		
	def destroy_file_path(self,e):
		button = e.GetEventObject()
		idi = button.parameterVal
		if idi in attos: 
			self.parent.statbar.SetStatusText(idi+" removed")
			attos.remove(idi)
			self.dest_text[idi].Hide()
			self.dict_button[idi].Hide()
			self.in_box[idi].Remove(True)
			self.box.Layout()

			self.parent.clear_and_update()
			self.update()
	def update(self):
		self.box.Clear(True)
		self.box.Layout()
		self.Boot()	
		self.box.Layout()
	def call(self):
		return 		
	def Explode(self):
		self.Close()	
class Info(wx.Frame):
		def __init__(self, parent,user):
			super(Info, self).__init__(None,title='About',pos =(950,400), style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION|wx.CLOSE_BOX,size = (300,250))
			self.parent = parent
			self.user = user
			self.InfoUI()
			self.Show()
		def InfoUI(self):
			panel  = wx.Panel(self)
			bmp5 = wx.Image('img/info.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
			panel.bitmap2 = wx.StaticBitmap(panel, -1, bmp5, (0, 0))
			vbox = wx.BoxSizer(wx.VERTICAL)	
			vbox.Add((-1,110))
			box = wx.BoxSizer(wx.HORIZONTAL)	
			logged = wx.StaticText(panel,label = "Logged As")
			logged.SetFont(self.parent.font1)
			box.Add(logged)
			vbox.Add(box,flag = wx.ALIGN_CENTRE,border = 5)
			box1 = wx.BoxSizer(wx.HORIZONTAL)
			vbox.Add((-1,10))

			self.user_text = wx.StaticText(panel,label = self.user)
			self.user_text.SetFont(self.parent.font)
			box1.Add(self.user_text)
			vbox.Add(box1,flag = wx.ALIGN_CENTRE,border = 5)
			vbox.Add((-1,15))

			box3 = wx.BoxSizer(wx.HORIZONTAL)
			developer = wx.StaticText(panel, label = "Developed by Demarox")
			developer.SetFont(self.parent.font1)

			box3.Add(developer)
			vbox.Add(box3,flag = wx.ALIGN_CENTRE,border = 5)
			vbox.Add((-1,10))

			box2 = wx.BoxSizer(wx.HORIZONTAL)
			self.link = wx.HyperlinkCtrl(panel,wx.ID_ANY, label = "Fork the Project!",url='https://github.com/demarox/Fedora-The-Mailer')
			box2.Add(self.link)
			vbox.Add(box2,flag = wx.ALIGN_CENTRE,border = 5)
			panel.SetSizer(vbox)
		def new_id(self,new_user):
			self.user_text.SetLabel(new_user)
		def call(self):
			return 	
		def Explode(self):
			self.Close()	
class Yubin(wx.Frame):
	def __init__(self, title= 'Yubin'):
		super(Yubin, self).__init__(None,id= -1, title = title, style  = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION|wx.CLOSE_BOX, size= (500,570))
		self.count = 0
		self.GeneralUI()
	#		self.Aproveaccount()
		self.Centre()

		self.Aproveaccount()
	def GeneralUI(self):
		#background
		#menu
		self.font = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
		self.font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)
		self.font2 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
		self.font3 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD)
		menubar = wx.MenuBar()
		filemenu = wx.Menu()
		send_att = wx.MenuItem(filemenu,SEND_ATT, '&Send Attachment \tCtrl+T')
		open_prompt = wx.MenuItem(filemenu,OPEN_PROMPT, '&Open Draft \tCtrl+O')
		save_prompt = wx.MenuItem(filemenu, SAVE_PROMT, '&Save Draft\tCtrl+S')
		open_all_opt = wx.MenuItem(filemenu,OPEN_ALL,'&Open All\tCtrl+E')
		close_opt = wx.MenuItem(filemenu, CLOSE, '&Close\tCtrl+Q')
		import_opt = wx.MenuItem(filemenu, IMPORT, '&Import Contacts\tCtrl+J')
		export_opt = wx.MenuItem(filemenu, EXPORT, '&Export Contacts\tCtrl+K')
		filemenu.AppendItem(send_att)
		filemenu.AppendItem(save_prompt)
		filemenu.AppendItem(open_prompt)
		filemenu.AppendSeparator()
		filemenu.AppendItem(import_opt)
		filemenu.AppendItem(export_opt)
		filemenu.AppendItem(open_all_opt)
		filemenu.AppendItem(close_opt)

		editmenu = wx.Menu()
		cust_acc = wx.MenuItem(editmenu, CUST_ACC, '&Change Account\tCtrl+A')
		reset_all = wx.MenuItem(editmenu, RESET_ALL, '&Reset \tCtrl+R')
		change_account_x = wx.MenuItem(editmenu,CUST_X,'&Close Account Change Box\tAlt+A')
		create_contact = wx.MenuItem(editmenu, CREATE_CONTACT, '&New Contact\tCtrl+D')
		edit_contact_list = wx.MenuItem(editmenu,EDIT_CONTACT_LIST,'&Edit Contact List\tCtrl+P')
		editmenu.AppendItem(cust_acc)
		editmenu.AppendItem(reset_all)
		editmenu.AppendItem(change_account_x)
		editmenu.AppendSeparator()
		editmenu.AppendItem(create_contact)
		editmenu.AppendItem(edit_contact_list)

		viewmenu = wx.Menu()
		manage_files = wx.MenuItem(viewmenu,MAN_F,'&Manage Files\tCtrl+F')
		my_acc = wx.MenuItem(viewmenu,MY_ACC,'&My Account\tCtrl+I')
		manage_files_x = wx.MenuItem(viewmenu,MAN_F_X, '&Close the Manager\tAlt+F')
		account_data_x = wx.MenuItem(viewmenu,ACC_X,'&Close The Info Box\tAlt+I')
		contact_list = wx.MenuItem(viewmenu, CONTACT_LIST, '&Contact List\tCtrl+L')
		contact_list_x = wx.MenuItem(viewmenu, CONTACT_LIST_X,'&Hide Contact List\tAlt+L')
		viewmenu.AppendItem(manage_files)
		viewmenu.AppendItem(my_acc)
		viewmenu.AppendItem(contact_list)
		viewmenu.AppendSeparator()
		viewmenu.AppendItem(manage_files_x)
		viewmenu.AppendItem(account_data_x)
		viewmenu.AppendItem(contact_list_x)

		helpmenu = wx.Menu()
		help_opt = wx.MenuItem(helpmenu,HELP,'&Help and Documentation\tCtrl+H')
		helpmenu.AppendItem(help_opt)

		menubar.Append(filemenu, '&File')
		menubar.Append(editmenu, '&Edit')
		menubar.Append(viewmenu, '&View')
		menubar.Append(helpmenu, '&Help')
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
		text_drop_target = MyTextDropTarget(self)
		self.destiny_camp =  wx.TextCtrl(panel)
		self.destiny_camp.SetDropTarget(text_drop_target)

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
		self.Bind(wx.EVT_MENU, self.kill_all , close_opt)
		self.Bind(wx.EVT_MENU, self.change_account, cust_acc)
		self.Bind(wx.EVT_MENU, self.reseter, reset_all)
		self.Bind(wx.EVT_MENU, self.account_data, my_acc)
		self.Bind(wx.EVT_MENU, self.manageFiles, manage_files)
		self.Bind(wx.EVT_MENU, self.change_account_close , change_account_x)
		self.Bind(wx.EVT_MENU, self.account_data_close, account_data_x)
		self.Bind(wx.EVT_MENU, self.manageFiles_close, manage_files_x)
		self.Bind(wx.EVT_MENU, self.open_all , open_all_opt)
		# new options
		self.Bind(wx.EVT_MENU, self.on_import, import_opt)
		self.Bind(wx.EVT_MENU, self.on_export, export_opt)
		self.Bind(wx.EVT_MENU, self.on_create_contact,create_contact)
		self.Bind(wx.EVT_MENU, self.on_edit_contact, edit_contact_list)
		self.Bind(wx.EVT_MENU, self.contact_list_show, contact_list)
		self.Bind(wx.EVT_MENU, self.contact_list_hide,contact_list_x)
		#.......
		self.Bind(wx.EVT_CLOSE,self.kill_all)
		self.Bind(wx.EVT_BUTTON, self.send_mail_instant , send_button)
		self.Bind(wx.EVT_MENU,self.popHelp, help_opt)
		#Accelerators
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT,  ord('A'), change_account_x.GetId() ),(wx.ACCEL_ALT,  ord('I'), account_data_x.GetId() ),(wx.ACCEL_CTRL,  ord('T'), send_att.GetId() ),(wx.ACCEL_CTRL,  ord('E'), open_all_opt.GetId() ),(wx.ACCEL_ALT,  ord('F'), manage_files_x.GetId() ),(wx.ACCEL_CTRL,  ord('F'), manage_files.GetId() ),(wx.ACCEL_CTRL,  ord('S'), save_prompt.GetId() ),(wx.ACCEL_CTRL,  ord('O'), open_prompt.GetId() ),(wx.ACCEL_CTRL,  ord('Q'), close_opt.GetId() ),(wx.ACCEL_CTRL,  ord('A'), cust_acc.GetId() ),(wx.ACCEL_CTRL,  ord('R'), reset_all.GetId() ),(wx.ACCEL_CTRL,  ord('I'), my_acc.GetId() ),(wx.ACCEL_CTRL,  ord('J'), import_opt.GetId() ),(wx.ACCEL_CTRL,  ord('K'), export_opt.GetId() ),(wx.ACCEL_CTRL,  ord('D'), create_contact.GetId() ),(wx.ACCEL_CTRL,  ord('P'), edit_contact_list.GetId() ),(wx.ACCEL_CTRL,  ord('L'), contact_list.GetId() ),(wx.ACCEL_ALT,  ord('L'), contact_list_x.GetId() )])
		self.SetAcceleratorTable(accel_tbl)


######Yubin Core######
	def handleDialog(self):
		RaisePopup('No connection','The connection is unnavailable')
	def clear_and_update(self):
		self.fileTextCtrl.Clear()
		for path in attos:
			splitter = path.split('/')
			splitter = splitter[-1]
			splitter = splitter if len(path)<=35 else splitter[0:33]+'...'
			self.fileTextCtrl.WriteText(splitter+"\n")
	def attach_file(self,e):
		dlg = wx.FileDialog(self, message="Open a File...",defaultDir="", defaultFile="",  style=wx.OPEN)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
			self.updateFiles(path)
			self.statbar.SetStatusText("File Correctly Added!")
		dlg.Destroy	
		
	def on_open(self,e):
		dlg = wx.FileDialog(self, message="Open a draft...",defaultDir="", defaultFile="",wildcard= "XML files (*.xml)|*.xml" , style=wx.OPEN | wx.FD_FILE_MUST_EXIST)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
			file_read = open(path,'r')
			d = file_read.read()
			file_read.close()
			parse_d = parseString(d)
			try:
				to_tag = parse_d.getElementsByTagName('to')[0].toxml()
				to_data = to_tag.replace('<to>','').replace('</to>','')		
				subject_tag = parse_d.getElementsByTagName('subject')[0].toxml()
				subject_data = subject_tag.replace('<subject>','').replace('</subject>','')			
				body_tag = parse_d.getElementsByTagName('body')[0].toxml()
				body_data = body_tag.replace('<body>','').replace('</body>','')
			except IndexError: 
				RaisePopup('Xml Error','The Draft is Bad')
				to_data,subject_data,body_data = '','',''
			self.destiny_camp.SetValue(to_data)
			self.sub_camp.SetValue(subject_data)
			self.body_camp.SetValue(body_data)
		dlg.Destroy	

	def on_save(self,e):
		dlg = wx.FileDialog(self, message="Save Draft as...",defaultDir="", defaultFile="", wildcard="XML files (*.xml)|*.xml", style=wx.SAVE)	
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			path = "".join(c for c in path if c not in trimmer)
			path = path+'.xml'
			destiny_get = self.destiny_camp.GetValue()
			subject_get = self.sub_camp.GetValue()
			body_getter = self.body_camp.GetValue()
			file_saver = open(path,'w')
			file_saver.write('<?xml version ="1.0" encoding="utf-8" ?>\n')
			file_saver.write("<mail>\n")
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
	def change_account(self,e):		
		try:
			self.raiseauth_window.call()
		except AttributeError,e :
			self.raiseauth_window =RaiseAuth(self,True)

	def change_account_close(self,e):
		try:
			self.raiseauth_window.call()
		except AttributeError,e :
			pass
		else:
			self.raiseauth_window.Explode()
			del self.raiseauth_window
	def SetInsertionPointEnd(self):
		self.fileTextCtrl.SetInsertionPointEnd()
	def popHelp(self,e):
		webbrowser.open_new('http://yubinapp.wordpress.com')

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
			try:
				self.man_f_window.call()
			except AttributeError,e:	
				pass
			else:	
				#self.man_f_window.Explode()
				##del self.man_f_window
				#self.manageFiles(True)
				self.man_f_window.update()
	def account_data(self,e):
		
		try:
			self.info_window.call()
		except AttributeError,e :
			try:
				account_dat = shelve.open('account.dat')
				self.info_window= Info(self,account_dat['username'])
				account_dat.close()
			except KeyError:
				RaisePopup('Introduce Your Keys','Introduce Your Keys')	
	def account_data_close(self,e):
		try:
			self.info_window.call()
		except AttributeError,e :
			pass
		else:
			self.info_window.Explode()
			del self.info_window
	def set_info_label(self,new_user):
		try:
			self.info_window.new_id(new_user)
		except AttributeError,e :
			pass		
	def manageFiles(self,e):
		try:
			self.man_f_window.call()
		except AttributeError, e:
			self.man_f_window = Man_at_files(self)

	def manageFiles_close(self,e):
		try:
			self.man_f_window.call()
		except AttributeError,e :
			pass
		else:
			self.man_f_window.Explode()
			del self.man_f_window			
	def send_mail_instant(self, e):
		self.destiny_get = self.destiny_camp.GetValue()
		self.subject_get = self.sub_camp.GetValue()
		self.body_get = self.body_camp.GetValue()
		fol = re.match(regexion,self.destiny_get)
		if not self.destiny_get :
			RaisePopup('Destiny in blank','No Destiny?')	
		elif fol is None :
			RaisePopup('Invalid Destiny Format','Set a valid Destiny')	
		elif not self.subject_get:
			RaisePopup('Subject in blank','No Subject?')
		elif not self.body_get:	
			RaisePopup('Body in blank','No Body?')
		else:

			if on_con() :
	
				s =shelve.open('account.dat')
				a_mail = Mail(s['username'],self.destiny_get,self.subject_get,self.body_get,s['password'],self,*attos)
				s.close()				
				a_mail.create_thread()

				#Cache for name directory
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
			self.raiseauth_window =RaiseAuth(self)
		else:
			self.Show()
			self.open_all(True)
	def on_import(self,e):
		pass
	def on_export(self,e):
		pass
	def on_create_contact(self,e):
		Add_Contact_PopUp(self)
	def on_edit_contact(self,e):
		try:
			self.contact_engineer_window.call()	
		except AttributeError, e:
			self.contact_list_hide(True)
			self.contact_engineer_window = Contact_Engineer(self)

	def contact_list_show(self,e):
		try:
			self.contact_window.call()
		except AttributeError, e:
			try:
				self.contact_engineer_window.call()	
			except AttributeError, e:
				self.contact_window = Man_at_contacts(self)
	def contact_list_hide(self,e):
		try:
			self.contact_window.call()
		except AttributeError,e :
			pass
		else:
			self.contact_window.Explode()
			del self.contact_window	
	def append_to_Ctrl(self,to_append):

		to_eval = self.destiny_camp.GetValue()

		if to_eval:
			self.destiny_camp.WriteText(", "+to_append)
		else:
			self.destiny_camp.WriteText(to_append)
	def add_contact_permanency(self, name, mail):
		c = shelve.open('DDRM3A2.dat')
		try:
			i = c[mail]
		except KeyError,e:	
			c[mail] = {'Tag':name, 'mail' :mail}
			try:
				self.contact_window.call()
			except AttributeError,e :
				c.close()
			else:	
				self.contact_window.Explode()
				del self.contact_window
				c.close()
				self.contact_list_show(True)

	def open_all(self,e):
		try:
			self.info_window.call()
		except AttributeError, e:
			self.account_data(True)
		try:
			self.raiseauth_window.call()
		except AttributeError, e:
			self.change_account(True)	
		try:
			self.man_f_window.call()
		except AttributeError, e:
			self.manageFiles(True)	
		try:
			self.contact_window.call()
		except AttributeError, e:
			self.contact_list_show(True)
	def kill_all(self,e):
		try:
			self.info_window.call()
		except AttributeError, e:
			pass
		else:
			self.info_window.Explode()
		try:
			self.raiseauth_window.call()
		except AttributeError, e:
			pass
		else:
			self.raiseauth_window.Explode()	
		try:
			self.man_f_window.call()
		except AttributeError, e:
			pass	
		else:
			self.man_f_window.Explode()	
		try:
			self.contact_window.call()
		except AttributeError,e :
			pass
		else:
			self.contact_window.Explode()
		try:
			self.contact_engineer_window.call()	
		except AttributeError, e:
			pass
		else:
			self.contact_engineer_window.Explode()								
		self.Destroy()

class Mail(object):
	def __init__(self, account, recieverstr,subject, text,password,parent, *attachments ):
		
		self.account = account
		self.accountpriv = account
		self.recieverstr=recieverstr
		self.body = text
		self.subject = subject
		self.__password = password
		self.file_attachments = attachments
		self.parent = parent
		self.yeah_bool = True
		self.reciever = str()
	def create_thread(self):
		self.recieverstr = self.recieverstr.split(',')
		progress_frame = Gauger(self.parent,(len(self.file_attachments)+3)*len(self.recieverstr))
		start_time = time.time()
		for self.reciever in self.recieverstr:

			assign_MIME_thread =threading.Thread(target=self.assign_MIME)
			assign_MIME_thread.start()	
			assign_MIME_thread.join()
			progress_frame.add_to_gauge()
			if self.file_attachments:
				for file_att in self.file_attachments:
					attach_thread = threading.Thread(target=self.attach,args=(file_att,))
					attach_thread.start()	
					attach_thread.join()
					if self.yeah_bool ==False:
						RaisePopup('Where is the file?','File unavailable')
						self.yeah_bool = True
					else:	
						progress_frame.add_to_gauge()

			smtp_thread = threading.Thread(target=self.smtp_create)
			smtp_thread.start()	
			smtp_thread.join()
			progress_frame.add_to_gauge()

			send_thread = threading.Thread(target=self.send)
			send_thread.start()	
			send_thread.join()
			progress_frame.add_to_gauge()
		print time.time() - start_time, "seconds"	
		if self.yeah_bool:
			SuccessPopup()
		elif self.yeah_bool == False:
			RaisePopup('File Load Too Big','Over Server Capacity')	
	def assign_MIME(self):	
	#		self.recieverstr = self.recieverstr.split(',')
	#		progress_frame = Gauger(self.parent,(len(self.file_attachments)+3)*len(self.recieverstr))
	#		for self.reciever in self.recieverstr:
		self.reciever =self.reciever.strip()
		self.msg = MIMEMultipart('alternative')
		self.msg['To'] = self.reciever
		self.msg['From'] = self.account
		self.msg['Date'] = formatdate(localtime=True)
		self.msg['Subject'] = self.subject
		self.msg.attach(MIMEText(self.body))
	#			self.progress_frame.add_to_gauge()
	def attach(self,file_attachment):
	#		if self.file_attachments:
	#		for file_att in self.file_attachments:
			try:
				file_parser = MIMEBase('application', "octet-stream") 
				file_parser.set_payload( open(file_attachment,"rb").read() )
				Encoders.encode_base64(file_parser)
				file_parser.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_attachment))
				self.msg.attach(file_parser)
	#					self.progress_frame.add_to_gauge()
			except IOError:
				self.yeah_bool= False
	#				RaisePopup('Where is the file?','File unavailable')

	def smtp_create(self):					
		gmail_serv =re.match(gmail_regex,self.account)
		yahoo_serv =re.match(yahoo_regex, self.account)
		hotmail_serv = re.match(hotmail_regex,self.account)
		if gmail_serv:
			self.smtpserver = smtplib.SMTP("smtp.gmail.com",587)			
		elif yahoo_serv:
			self.smtpserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
		elif hotmail_serv:
			self.smtpserver = smtplib.SMTP("smtp.live.com",587)
		else:
			self.smtpserver = smtplib.SMTP("smtp.gmail.com",587)	
		self.smtpserver.ehlo()
		self.smtpserver.starttls()
		self.smtpserver.ehlo()
		self.smtpserver.login(self.accountpriv, self.getpwd())
	#
	#			self.progress_frame.add_to_gauge()
	def send(self):
		try:
			pass
			self.smtpserver.sendmail(self.account,self.reciever, self.msg.as_string())
		except smtplib.SMTPSenderRefused :	
	#				self.progress_frame.Explode()
			self.yeah_bool= False
	#				RaisePopup('File Load Too Big','Over Server Capacity')
			self.parent.statbar.SetStatusText("Mail Error :(" )
		else:
	#				self.progress_frame.add_to_gauge()
	#				self.progress_frame.Explode()
			self.parent.statbar.SetStatusText(str("Success at sending mail to " + self.reciever))

		self.smtpserver.close()
	#			if self.yeah_bool:
	#				self.success = SuccessPopup()
			
	def	getpwd(self):
		return self.__password


def on_con():
	try:
		response=urllib2.urlopen('http://example.com',timeout=5)
		return True
	except urllib2.URLError as err: pass
	return False
def success():
	SuccessPopup()							
#superabstraction        
if __name__ == '__main__':
	app = wx.App()
	Yubin()
	app.MainLoop()