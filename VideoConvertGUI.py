# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class VCFrame
###########################################################################

class VCFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"VideoConverter", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 500,300 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer8 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer8.AddGrowableCol( 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.dir_picker = wx.DirPickerCtrl( self.m_panel1, wx.ID_ANY, u"Folder to Convert...", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		fgSizer8.Add( self.dir_picker, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_start = wx.Button( self.m_panel1, wx.ID_ANY, u"Start!", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.button_start, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer8, 1, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Options" ), wx.VERTICAL )
		
		fgSizer6 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.AddGrowableCol( 2 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.check_recursive = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Recursive?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_recursive.SetValue(True) 
		fgSizer6.Add( self.check_recursive, 0, wx.ALL, 5 )
		
		self.check_reconvert = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Reconvert Videos?", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.check_reconvert, 0, wx.ALL, 5 )
		
		self.check_thumbnails = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Recreate Thumbnails?", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.check_thumbnails, 0, wx.ALL, 5 )
		
		
		sbSizer2.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( sbSizer2, 1, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Current File:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.current_progress_gauge = wx.Gauge( self.m_panel1, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.current_progress_gauge.SetValue( 0 ) 
		fgSizer2.Add( self.current_progress_gauge, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.text_filepercent = wx.StaticText( self.m_panel1, wx.ID_ANY, u"0%", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text_filepercent.Wrap( -1 )
		self.text_filepercent.SetMinSize( wx.Size( 30,-1 ) )
		
		fgSizer2.Add( self.text_filepercent, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"All Files:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.allfiles_progress_gauge = wx.Gauge( self.m_panel1, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.allfiles_progress_gauge.SetValue( 0 ) 
		fgSizer2.Add( self.allfiles_progress_gauge, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.text_allfiles = wx.StaticText( self.m_panel1, wx.ID_ANY, u"0/0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text_allfiles.Wrap( -1 )
		self.text_allfiles.SetMinSize( wx.Size( 30,-1 ) )
		
		fgSizer2.Add( self.text_allfiles, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer7 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer7.AddGrowableCol( 1 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText17 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Status:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer7.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.textctrl_status0 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"Idle", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer7.Add( self.textctrl_status0, 0, wx.ALL|wx.EXPAND, 1 )
		
		self.m_staticText18 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Folder:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer7.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.textctrl_status1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer7.Add( self.textctrl_status1, 0, wx.ALL|wx.EXPAND, 1 )
		
		self.m_staticText19 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"File:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer7.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.textctrl_status2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer7.Add( self.textctrl_status2, 0, wx.ALL|wx.EXPAND, 1 )
		
		
		fgSizer1.Add( fgSizer7, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_start.Bind( wx.EVT_BUTTON, self.event_button_start )
		self.check_recursive.Bind( wx.EVT_CHECKBOX, self.event_recursive )
		self.check_reconvert.Bind( wx.EVT_CHECKBOX, self.event_reconvert )
		self.check_thumbnails.Bind( wx.EVT_CHECKBOX, self.event_thumbnails )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def event_button_start( self, event ):
		event.Skip()
	
	def event_recursive( self, event ):
		event.Skip()
	
	def event_reconvert( self, event ):
		event.Skip()
	
	def event_thumbnails( self, event ):
		event.Skip()
	

