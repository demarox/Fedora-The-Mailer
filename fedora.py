#Fedora
import wx
import os
wildcard = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
         "All files (*.*)|*.*"
SEND_ATT,OPEN_PROMPT,SAVE_PROMT, CLOSE,DEF_ACC,CUST_ACC = 1,2,3,4,5,6
class DialogGener(wx.Dialog):
	def __init__(self,what_happens):
		super(DialogGener, self).__init__(None)
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


class Fedora(wx.Frame):
	def __init__(self, title= 'Fedora'):
		super(Fedora, self).__init__(None,id= -1, title = title, style = wx.MINIMIZE_BOX  | wx.SYSTEM_MENU | wx.CAPTION |wx.CLOSE_BOX, size= (500,270))
		self.GeneralUI()
		self.Show()
	def GeneralUI(self):
		#menu
		menubar = wx.MenuBar()
		filemenu = wx.Menu()
		send_att = wx.MenuItem(filemenu,SEND_ATT, '&Send Attachment \t Select File')
		open_prompt = wx.MenuItem(filemenu,OPEN_PROMPT, '&Open Prompt \t Open Prompt')
		save_prompt = wx.MenuItem(filemenu, SAVE_PROMT, '&Save Prompt\t save Prompt')
		close_opt = wx.MenuItem(filemenu, CLOSE, '&Close\tClose')
		filemenu.AppendItem(send_att)
		filemenu.AppendItem(save_prompt)
		filemenu.AppendItem(open_prompt)
		filemenu.AppendItem(close_opt)

		viewmenu = wx.Menu()
		def_acc = wx.MenuItem(viewmenu, DEF_ACC, '&Use Default\t Use Default')
		cust_acc = wx.MenuItem(viewmenu, CUST_ACC, '&Use Custom\t Use Custom')
		viewmenu.AppendItem(def_acc)
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
		destiny_camp = wx.TextCtrl(panel)
		destiny_box.Add(destiny_camp, proportion = 1)
		box.Add(destiny_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT| wx.TOP ,border = 8)
		box.Add((-1,10))
		#sub
		sub_box = wx.BoxSizer(wx.HORIZONTAL)
		sub_text = wx.StaticText(panel, label = "Sub :")
#		sub_text.SetFont(font)
		sub_box.Add(sub_text, flag = wx.RIGHT, border = 5)
		sub_camp =  wx.TextCtrl(panel)
		sub_box.Add(sub_camp, proportion = 1)
		box.Add(sub_box, flag = wx.EXPAND | wx.RIGHT | wx.LEFT ,border = 8)      
		 #body
		box.Add((-1,20))
		body = wx.BoxSizer(wx.HORIZONTAL)
		body_camp = wx.TextCtrl(panel,style = wx.TE_MULTILINE)
		body.Add(body_camp, proportion = 1, flag = wx.EXPAND)
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
		self.Bind(wx.EVT_MENU, self.spec_routes_on_attachment, open_prompt)
		self.Bind(wx.EVT_MENU, self.saveFile, save_prompt)
		self.Bind(wx.EVT_MENU, self.handleDialog, send_att)

	#Fedora popups
	def successDialog(self, e):
		wx.MessageBox('Success at sending!','Good!', wx.OK | wx.ICON_INFORMATION)
	def handleDialog(self, e):
		wx.MessageBox('Error at sending', 'OMAIGA!', wx.OK | wx.ICON_ERROR)
	def spec_routes_on_attachment(self,e):
		spec_route_window = DialogGener('send_att')
		spec_route_window.ShowModal()
		spec_route_window.Destroy()
	def saveFile(self,e):
		#no current directory
		dlg = wx.FileDialog(self, message="Save file as ...",defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.SAVE)	
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			print paths
		dlg.Destroy
		
#superabstraction        
if __name__ == '__main__':
	app = wx.App()
	Fedora('Fedora test')
	app.MainLoop()







