
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)

from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase


class PostFeeds(ScrollView):
	pass

class CategoryBar(MDBoxLayout, CommonElevationBehavior):
	pass

class CustomToolBar(MDBoxLayout, CommonElevationBehavior):
	pass

class MainWindow(FloatLayout):
	pass


class BoothFreedomWallApp(MDApp):
	
	def build(self):
		
		return Builder.load_file("design.kv")

LabelBase.register(name = "lato_bold" , fn_regular = "fonts/Lato-Bold.ttf")
LabelBase.register(name = "lato_bold_italic" , fn_regular = "fonts/Lato-BoldItalic.ttf")

BoothFreedomWallApp().run()

