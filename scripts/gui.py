"""GUI overlay for the application."""

# import kivy
from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy import Config

Config.set('graphics', 'multisamples', '1')
Window.clearcolor = (1.0, 1.0, 1.0, 1.0)
Window.size = (500, 400)
Window.minimum_width, Window.minimum_height = Window.size


class MyLayout(BoxLayout):
    departure = ObjectProperty(None)
    arrival = ObjectProperty(None)


class CheckDavid(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        Builder.load_file("style.kv")
        return MyLayout()


if __name__ == "__main__":
    CheckDavid().run()
