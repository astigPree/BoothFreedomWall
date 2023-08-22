
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)

from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock 
from kivy.properties import BooleanProperty, StringProperty , ObjectProperty

import typing as tp
from threading import Thread

from app_network import AppNetworkHandler

class ApplicationSettings(ModalView):
	pass

class DownloadingView(ModalView):
	info_text : Label = ObjectProperty()
	hasAnError = BooleanProperty(False)
	
	def hasAnConnectionError(self):
		# display an connection error
		self.info_text.text = "CONNECTION ERROR"
		self.hasAnError = True
	
	def hasAnServerDownError(self):
		# display an server down error
		self.info_text.text = "CAN'T CONNECT TO SERVER"
		self.hasAnError = True
	
	
class CategorySelections(ModalView):
	category : str = StringProperty("LOVE")

class Post(MDBoxLayout , CommonElevationBehavior):
	pass

class PostFeeds(ScrollView):
	pass

class CategoryBar(MDBoxLayout, CommonElevationBehavior):
	pass

class CustomToolBar(MDBoxLayout, CommonElevationBehavior):
	pass


class MainWindow(FloatLayout):
	
	lastPostID : tp.Union[None , int] = None
	selectedCategory : str = StringProperty("love")
	listOfCategories = ('love', 'school', 'life' , 'random')
	
	def __init__(self , **kwargs):
		super(MainWindow , self ).__init__(**kwargs)
		self.category_selections = CategorySelections()
		self.downloading_view = DownloadingView()
		self.app_settings = ApplicationSettings()
		self.network = AppNetworkHandler()
		
		self.category_selections.bind( on_dismiss = self.updateCategory)
		
		
	def on_kv_post(self , *args):
		#Clock.schedule_interval(self.clockActivity , 1/30)
		#Clock.schedule_once(self.app_settings.open , 1)
		#Clock.schedule_once(self.downloading_view.open , 1)
		#Clock.schedule_once(self.category_selections.open , 1)
		pass
	
	def updateCategory(self , *args):
		if self.selectedCategory != self.category_selections.category.lower():
			self.selectedCategory = self.category_selections.category.lower()
			self.lastPostID = None
			
	
	def connectToServer(self , interval : float):
		self.downloading_view.open()
		if not self.network.connectToServer():
			self.downloading_view.hasAnServerDownError()
		else:
			self.downloading_view.dismiss()
	
	def downloadDataFromServer(self , interval : float):
		self.downloading_view.open()
		
		if not self.network.hasSocket:
			if not self.network.connectToServer():
				self.downloading_view.hasAnServerDownError()
				return
		
		data = { self.listOfCategories.index(self.selectedCategory) : self.lastPostID }
		self.network.sendDataToServerForce(data)
		
		self.network.activity()
		
		if self.network.hasConnectionError:
			self.downloading_view.hasAnConnectionError()
			return 
		elif self.network.hasDataInterruption:
			Clock.schedule_once(self.downloadDataFromServer)
			return 
		
		

class BoothFreedomWallApp(MDApp):
	
	#def on_start(self):
#		Clock.schedule_once(self.root.connectToServer)
#		
	def build(self):
		
		return Builder.load_file("design.kv")

LabelBase.register(name = "lato_bold" , fn_regular = "fonts/Lato-Bold.ttf")
LabelBase.register(name = "lato_bold_italic" , fn_regular = "fonts/Lato-BoldItalic.ttf")
LabelBase.register(name = "lato_regular" , fn_regular = "fonts/Lato-Regular.ttf")
LabelBase.register(name = "lato_black_italic" , fn_regular = "fonts/Lato-BlackItalic.ttf")
LabelBase.register(name = "lato_italic" , fn_regular = "fonts/Lato-Italic.ttf")

BoothFreedomWallApp().run()

