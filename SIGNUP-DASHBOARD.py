import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.window import Window
from kivy.metrics import dp

# Fixed Mobile Window Size
Window.size = (360, 640)

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # --- 1. Background Canvas ---
        with self.layout.canvas.before:
            Color(0.43, 0.89, 0.75, 1)  # Your Teal Color
            self.bg_rect = Rectangle(pos=self.layout.pos, size=Window.size)
            Color(1, 1, 1, 1) # White Card Background
            self.card = RoundedRectangle(
                pos=(0, 0), 
                size=(Window.width, Window.height * 0.75),
                radius=[(40, 40), (40, 40), (0, 0), (0, 0)]
            )
        self.layout.bind(size=self.update_rects)

        # --- 2. Header ---
        self.layout.add_widget(Label(
            text="SIGN UP", font_size='40sp', bold=True, 
            pos_hint={'center_x': 0.5, 'top': 0.93}
        ))

        # --- 3. Input Fields Container ---
        content = BoxLayout(
            orientation='vertical', spacing=dp(15), size_hint=(0.85, None), 
            height=dp(420), pos_hint={'center_x': 0.5, 'center_y': 0.45} 
        )
        
        content.add_widget(Label(
            text="VOTELLY", color=(0.25, 0.7, 0.6, 1), 
            font_size='35sp', bold=True, size_hint_y=None, height=dp(60)
        ))
        
        self.email = self.create_input("Email")
        content.add_widget(self.email)

        # Password 1
        p1_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(52), spacing=dp(5))
        self.pass1 = self.create_input("Password", password=True)
        self.pass1.size_hint_x = 0.8
        self.btn1 = Button(text="Show", size_hint_x=0.2, background_color=(0.9,0.9,0.9,1), color=(0.2,0.2,0.8,1), background_normal='')
        self.btn1.bind(on_release=lambda x: self.toggle(self.pass1, self.btn1))
        p1_box.add_widget(self.pass1); p1_box.add_widget(self.btn1)
        content.add_widget(p1_box)

        # Password 2
        p2_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(52), spacing=dp(5))
        self.pass2 = self.create_input("Confirm Password", password=True)
        self.pass2.size_hint_x = 0.8
        self.btn2 = Button(text="Show", size_hint_x=0.2, background_color=(0.9,0.9,0.9,1), color=(0.2,0.2,0.8,1), background_normal='')
        self.btn2.bind(on_release=lambda x: self.toggle(self.pass2, self.btn2))
        p2_box.add_widget(self.pass2); p2_box.add_widget(self.btn2)
        content.add_widget(p2_box)
        
        self.error = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=dp(20), font_size='12sp')
        content.add_widget(self.error)
        
        # Sign Up Button
        self.signup_btn = Button(
            text="Sign Up", size_hint=(1, None), height=dp(55),
            bold=True, color=(0.43, 0.89, 0.75, 1), background_color=(0,0,0,0)
        )
        with self.signup_btn.canvas.after:
            Color(0.43, 0.89, 0.75, 1)
            self.line = Line(rounded_rectangle=(0,0,0,0, 25), width=1.0)
        self.signup_btn.bind(pos=self.update_line, size=self.update_line, on_release=self.validate)
        
        content.add_widget(self.signup_btn)
        self.layout.add_widget(content)
        self.add_widget(self.layout)

    def create_input(self, hint, password=False):
        return TextInput(hint_text=hint, password=password, multiline=False, size_hint_y=None, height=dp(52), background_color=(0.94, 0.94, 0.94, 1), background_normal='')

    def toggle(self, f, b):
        f.password = not f.password
        b.text = "Hide" if not f.password else "Show"

    def update_rects(self, *args):
        self.bg_rect.size = Window.size
        self.card.size = (Window.width, Window.height * 0.75)

    def update_line(self, ins, *args):
        self.line.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 25)

    def validate(self, *args):
        # Email Check: Ensures "@" is in the text
        if "@" not in self.email.text:
            self.error.text = "Error: Invalid Email"
        # Length Check: Added 8 character minimum requirement
        elif len(self.pass1.text) < 8:
            self.error.text = "Password is too short"
        # Match Check: Ensure both passwords are identical
        elif self.pass1.text != self.pass2.text:
            self.error.text = "Error: Check passwords"
        else:
            self.error.text = ""
            self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(1, 1, 1, 1); Rectangle(pos=(0,0), size=Window.size)

        # Header
        header = BoxLayout(orientation='vertical', size_hint=(0.85, 0.1), pos_hint={'center_x': 0.5, 'top': 0.92})
        header.add_widget(Label(text="WELCOME!", font_size='34sp', bold=True, color=(0,0,0,1), halign='left', text_size=(Window.width*0.85, None)))
        header.add_widget(Label(text="VOTE, TALLY, WISELY", font_size='14sp', color=(0.3, 0.3, 0.9, 1), halign='left', text_size=(Window.width*0.85, None)))
        layout.add_widget(header)

        # Join Room
        jr = Button(text="Join Room", font_size='32sp', bold=True, color=(0.3, 0.3, 0.9, 1), background_color=(0,0,0,0), size_hint=(0.85, 0.15), pos_hint={'center_x': 0.5, 'top': 0.75})
        with jr.canvas.before:
            Color(0.43, 0.89, 0.75, 1); self.jl = Line(rounded_rectangle=(0,0,0,0, 20), width=1.5)
        jr.bind(pos=self.up_jl, size=self.up_jl)
        layout.add_widget(jr)

        # Grid
        grid = GridLayout(cols=2, spacing=dp(15), size_hint=(0.85, 0.35), pos_hint={'center_x': 0.5, 'top': 0.50})
        m = [("Raise Hand", (0.3, 0.3, 1, 1)), ("Scan Ballot", (0.5, 1, 0.8, 1)), ("Digital Forms", (0.9, 0.96, 1, 1)), ("Ranked Choice", (1, 1, 0.7, 1))]
        
        for t, c in m:
            btn = Button(text=t, background_normal='', background_color=c, color=(0.1, 0.1, 0.5, 1), bold=True)
            btn.bind(on_release=self.go_to_create_with_mode)
            grid.add_widget(btn)
        layout.add_widget(grid)

        # Bottom FAB (+)
        plus_btn = Button(
            text="+", font_size='35sp', background_normal='', 
            background_color=(0.3, 0.3, 1, 1), size_hint=(None, None), 
            size=(dp(60), dp(60)), pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        plus_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'create_room'))
        layout.add_widget(plus_btn)
        
        self.add_widget(layout)

    def up_jl(self, ins, *args):
        self.jl.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 20)

    def go_to_create_with_mode(self, instance):
        self.manager.get_screen('create_room').mode_label.text = f"Mode: {instance.text}"
        self.manager.current = 'create_room'

class CreateRoomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(1, 1, 1, 1); Rectangle(pos=(0, 0), size=Window.size)

        content = BoxLayout(
            orientation='vertical', spacing=dp(20), size_hint=(0.85, None), 
            height=dp(400), pos_hint={'center_x': 0.5, 'top': 0.85}
        )
        
        self.mode_label = Label(text="Create New Room", font_size='24sp', bold=True, color=(0, 0, 0, 1))
        content.add_widget(self.mode_label)
        
        self.room_name = TextInput(hint_text="Room Name", multiline=False, size_hint_y=None, height=dp(50))
        self.room_pass = TextInput(hint_text="Room Password (Optional)", password=True, multiline=False, size_hint_y=None, height=dp(50))
        
        content.add_widget(self.room_name)
        content.add_widget(self.room_pass)
        
        start_btn = Button(
            text="CREATE & START", size_hint_y=None, height=dp(55), bold=True,
            background_color=(0.43, 0.89, 0.75, 1), background_normal=''
        )
        content.add_widget(start_btn)
        
        back_btn = Button(
            text="Cancel", size_hint_y=None, height=dp(45), color=(0.3, 0.3, 0.9, 1),
            background_color=(0, 0, 0, 0)
        )
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        content.add_widget(back_btn)

        layout.add_widget(content)
        self.add_widget(layout)

class VotellyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(CreateRoomScreen(name='create_room'))
        return sm

if __name__ == '__main__':
    VotellyApp().run()