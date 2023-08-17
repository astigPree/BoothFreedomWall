
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)

from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock

class ApplicationSettings(ModalView):
	pass

class DownloadingView(ModalView):
	pass

class CategorySelections(ModalView):
	pass

class Post(MDBoxLayout , CommonElevationBehavior):
	pass

class PostFeeds(ScrollView):
	pass

class CategoryBar(MDBoxLayout, CommonElevationBehavior):
	pass

class CustomToolBar(MDBoxLayout, CommonElevationBehavior):
	pass


class MainWindow(FloatLayout):
	
	def __init__(self , **kwargs):
		super(MainWindow , self ).__init__(**kwargs)
		self.category_selections = CategorySelections()
		self.downloading_view = DownloadingView()
	
	def on_kv_post(self , *args):
		Clock.schedule_once(self.downloading_view.open , 1)
		#Clock.schedule_once(self.category_selections.open , 1)


class BoothFreedomWallApp(MDApp):
	
	def build(self):
		
		return Builder.load_file("design.kv")

LabelBase.register(name = "lato_bold" , fn_regular = "fonts/Lato-Bold.ttf")
LabelBase.register(name = "lato_bold_italic" , fn_regular = "fonts/Lato-BoldItalic.ttf")
LabelBase.register(name = "lato_regular" , fn_regular = "fonts/Lato-Regular.ttf")
LabelBase.register(name = "lato_black_italic" , fn_regular = "fonts/Lato-BlackItalic.ttf")

BoothFreedomWallApp().run()

