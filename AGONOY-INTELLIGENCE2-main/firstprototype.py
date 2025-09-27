from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivymd.uix.snackbar import Snackbar

Window.size = (360,640)

LabelBase.register(
    name="OpenSans-VariableFont_wdth,wght",
    fn_regular="OpenSans-VariableFont_wdth,wght.ttf",
    fn_bold="OpenSans-Bold.ttf"
)

class LoginScreen(Screen):
    mobile_num = ObjectProperty(None)
    password = ObjectProperty(None)

    def login_inter(self):
        mobile_n = self.mobile_num.text
        passw = self.password.text

        if not mobile_n or not passw:
            Snackbar(text="Please enter both fields.",duration=0.5).open()
        else:
            mobile_n = int(mobile_n)
            passw = int(passw)

            if mobile_n in self.manager.students:
                if passw == self.manager.students[mobile_n]:
                    Snackbar(text=f"Welcome to Homepage!",duration=0.5).open()
                    self.manager.current = "homepage"
                    self.mobile_num.text = ""
                    self.password.text = ""
                else:
                    Snackbar(text="Invalid password, please try again.",duration=0.5).open()
                    self.password.text = ""
            else:
                Snackbar(text="Student not found, please sign up.",duration=0.5).open()
                self.mobile_num.text = ""
                self.password.text = ""


class SignupScreen(Screen):
    create_num = ObjectProperty(None)
    c_pass = ObjectProperty(None)
    v_pass = ObjectProperty(None)

    def signup_inter(self):

        if not self.create_num.text or not self.c_pass.text:
            Snackbar(text="Please enter given fields.",duration=0.5).open()
        else:
            if self.c_pass.text == self.v_pass.text:
                self.manager.students[int(self.create_num.text)] = int(self.c_pass.text)
                Snackbar(text="Successfully created an account",duration=0.5).open()
                self.c_pass.text = ""
                self.v_pass.text = ""
                self.create_num.text = ""
            else:
                Snackbar(text="verify password not similar to new password",duration=0.5).open()
                self.v_pass.text = ""

    def go_back(self):
        self.manager.current = "login"


class HomePage(Screen):
    def logout(self):
        Snackbar(text="Goodbye!",duration=0.5).open()
        self.manager.current = "login"

class MainWindow(ScreenManager):
    students = {}

class DemoApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file("demo.kv")

if __name__ == "__main__":
    DemoApp().run()
