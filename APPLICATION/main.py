from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CommonElevationBehavior

from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty

import typing as tp

from app_network import AppNetworkHandler, MOODS


class ApplicationSettings(ModalView) :
    pass


class DownloadingView(ModalView) :
    info_text: Label = ObjectProperty()

    hasAnError = BooleanProperty(False)
    downloadingText = StringProperty("D O W N L O A D I N G")  # length 21

    downloadingFunction : callable = ObjectProperty()

    def on_pre_open(self) :
        if self.hasAnError :
            self.hasAnError = False
        self.info_text.text = self.downloadingText
        Clock.schedule_once(self.animation, 0.5)

    def animation(self, interval: int) :
        if self.hasAnError : return

        if len(self.info_text.text) == 21 :
            self.info_text.text = f". {self.info_text.text} ."  # length 25
        elif len(self.info_text.text) == 25 :
            self.info_text.text = f". {self.info_text.text} ."  # length 29
        elif len(self.info_text.text) == 29 :
            self.info_text.text = f". {self.info_text.text} ."  # length 33
        else :
            self.info_text.text = self.downloadingText

        Clock.schedule_once(self.animation, 0.5)

    def hasAnConnectionError(self) :
        # display an connection error
        self.hasAnError = True
        self.info_text.text = "CONNECTION ERROR"

    def hasAnServerDownError(self) :
        # display an server down error
        self.hasAnError = True
        self.info_text.text = "CAN'T CONNECT TO SERVER"


class CategorySelections(ModalView) :
    category: str = StringProperty("LOVE")


class Post(MDBoxLayout, CommonElevationBehavior) :
    post_id: tp.Union[int, None] = None
    content: str = StringProperty("")
    mood: Image = ObjectProperty()
    post_date: str = StringProperty("")
    post_owner: str = StringProperty("")

    def setData(self, data: list) :
        self.post_id = data[0]
        self.content = data[1]
        self.post_owner = data[2]
        self.post_date = data[3]
        self.mood.source = MOODS[int(data[4])]


class PostFeeds(ScrollView) :
    feed_container: MDGridLayout = ObjectProperty()
    
    def moveToTop(self):
    	self.scroll_to(self.feed_container.children[-1])
	
    def clearFeedContainer(self) :
        self.feed_container.clear_widgets()

    def displayPosts(self, data: list) :
        widget = Post()
        widget.setData(data)
        self.feed_container.add_widget(widget)


class CategoryBar(MDBoxLayout, CommonElevationBehavior) :
    pass


class CustomToolBar(MDBoxLayout, CommonElevationBehavior) :
    pass


class MainWindow(FloatLayout) :
    tool_bar: CustomToolBar = ObjectProperty()
    category_bar: CategoryBar = ObjectProperty()
    post_feeds: PostFeeds = ObjectProperty()

    hasNextData = BooleanProperty(False)
    lastPostID: tp.Union[None, int] = None
    selectedCategory: str = StringProperty("love")
    listOfCategories = ('love', 'school', 'life', 'random')

    def __init__(self, **kwargs) :
        super(MainWindow, self).__init__(**kwargs)
        self.category_selections = CategorySelections()
        self.downloading_view = DownloadingView()
        self.app_settings = ApplicationSettings()
        self.network = AppNetworkHandler()

        self.downloading_view.downloadingFunction = self.downloadingTruModalView
        self.category_selections.bind(on_dismiss=self.updateCategory)
        Window.bind(on_keyboard=self.on_key)

    def on_kv_post(self, *args) :
        # Clock.schedule_interval(self.clockActivity , 1/30)
        # Clock.schedule_once(self.app_settings.open , 1)
        # Clock.schedule_once(self.downloading_view.open , 1)
        # Clock.schedule_once(self.category_selections.open , 1)
        pass

    def updateCategory(self, *args) :
        if self.selectedCategory != self.category_selections.category.lower() :
            self.selectedCategory = self.category_selections.category.lower()
            self.lastPostID = None

    def connectToServer(self, interval: float) :
        self.downloading_view.open()
        if not self.network.connectToServer() :
            self.downloading_view.hasAnServerDownError()
        else :
            self.downloading_view.dismiss()

    def downloadDataFromServer(self, interval: float) :
        self.downloading_view.open()

        # Connecting to server if not connected
        if not self.network.hasSocket :
            if not self.network.connectToServer() :
                self.downloading_view.hasAnServerDownError()
                return

        # Preparing the data to be sent
        data = {self.listOfCategories.index(self.selectedCategory) : self.lastPostID}
        self.network.sendDataToServerForce(data)

        # Do the activity
        self.network.activity()

        # Check if it has any error occur
        if self.network.hasConnectionError :
            self.downloading_view.hasAnConnectionError()
            return
        elif self.network.hasDataInterruption :
            Clock.schedule_once(self.downloadDataFromServer)
            return

        # Display the content received
        self.post_feeds.clearFeedContainer()
        received_data = self.network.getReceivedData()
        for key, values in received_data.items() :
            if key == "9" :
                self.hasNextData = values
            else :
                for value in values :
                    self.post_feeds.displayPosts(value)
                    self.lastPostID = int(value[0])
         
        self.post_feeds.moveToTop()
        self.downloading_view.dismiss()

    def downloadingTruModalView(self , interval : float):
        # Connecting to server if not connected
        if not self.network.hasSocket :
            if not self.network.connectToServer() :
                self.downloading_view.hasAnServerDownError()
                return

        # Preparing the data to be sent
        data = {self.listOfCategories.index(self.selectedCategory) : self.lastPostID}
        self.network.sendDataToServerForce(data)

        # Do the activity
        self.network.activity()

        # Check if it has any error occur
        if self.network.hasConnectionError :
            self.downloading_view.hasAnConnectionError()
            return
        elif self.network.hasDataInterruption :
            Clock.schedule_once(self.downloadDataFromServer)
            return

        # Display the content received
        self.post_feeds.clearFeedContainer()
        received_data = self.network.getReceivedData()
        for key, values in received_data.items() :
            if key == "9" :
                self.hasNextData = values
            else :
                for value in values :
                    self.post_feeds.displayPosts(value)
                    self.lastPostID = int(value[0])
         
        self.post_feeds.moveToTop()
        self.downloading_view.dismiss()

    def on_key(self, window, key, *args) :
        if key == 27 :
            # Create a Design for exiting the app
            pass


class BoothFreedomWallApp(MDApp) :

    def on_start(self):
        Clock.schedule_once(self.root.connectToServer)

    def build(self) :
        return Builder.load_file("design.kv")


LabelBase.register(name="lato_bold", fn_regular="fonts/Lato-Bold.ttf")
LabelBase.register(name="lato_bold_italic", fn_regular="fonts/Lato-BoldItalic.ttf")
LabelBase.register(name="lato_regular", fn_regular="fonts/Lato-Regular.ttf")
LabelBase.register(name="lato_black_italic", fn_regular="fonts/Lato-BlackItalic.ttf")
LabelBase.register(name="lato_italic", fn_regular="fonts/Lato-Italic.ttf")

BoothFreedomWallApp().run()
