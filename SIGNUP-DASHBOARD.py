import re
import array  
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.graphics.texture import Texture 
from kivy.core.window import Window
from kivy.metrics import dp

Window.size = (360, 640)

class ModeCard(ButtonBehavior, BoxLayout):
    def __init__(self, title, bg_color, icon_char, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(5)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(Label(text=icon_char, font_size='40sp', color=(0.1, 0.1, 0.5, 1), bold=True))
        self.add_widget(Label(text=title, font_size='12sp', color=(0.1, 0.1, 0.5, 1), bold=True, halign='center'))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class VotingModeModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.background_color = (1, 1, 1, 1) 
        self.background = "" 
        
        layout = FloatLayout()
        
        layout.add_widget(Label(text="Choose Voting Mode", font_size='26sp', bold=True, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'top': 1.4}))
        layout.add_widget(Label(text="Voting Mode", font_size='15sp', bold=True, color=(0.4, 0.4, 0.9, 1), pos_hint={'center_x': 0.5, 'top': 1.35}))
        
        grid = GridLayout(cols=2, spacing=dp(10), padding=dp(25), size_hint=(1, 0.55), pos_hint={'center_x': 0.5, 'top': 0.78})
        modes = [("Raise Hand", (0.3, 0.3, 1, 1), "H"), ("Scan Ballot", (0.5, 1, 0.8, 1), "SB"), 
                 ("Digital Forms", (0.9, 0.96, 1, 1), "DF"), ("Ranked Choice", (1, 1, 0.7, 1), "RC")]
        
        for t, c, i in modes:
            card = ModeCard(title=t, bg_color=c, icon_char=i)
            card.bind(on_release=self.dismiss)
            grid.add_widget(card)
        
        layout.add_widget(grid)

        close_btn = Button(text="+", font_size='35sp', background_normal='', background_color=(0.95, 0.95, 1, 1), color=(0.3, 0.3, 1, 1), size_hint=(None, None), size=(dp(65), dp(65)), pos_hint={'center_x': 0.5, 'y': 0.05})
        close_btn.bind(on_release=self.dismiss)
        layout.add_widget(close_btn)
        
        self.add_widget(layout)

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.grad_tex = self.get_gradient_texture([0.41, 0.61, 0.94, 1], [0.59, 0.93, 0.86, 1])
        with self.layout.canvas.before:
            self.bg_rect = Rectangle(pos=self.pos, size=Window.size, texture=self.grad_tex)
            Color(1, 1, 1, 1) 
            self.card = RoundedRectangle(pos=(0, 0), size=(Window.width, Window.height * 0.75), radius=[(40, 40), (40, 40), (0, 0), (0, 0)])
            
        self.layout.bind(size=self.update_rects)
        self.signup_label = Label(text="SIGN UP", font_size='30sp', bold=True, color=(1, 1, 1, 1), size_hint=(0.8, None), height=dp(60), pos_hint={'x': 0.08, 'top': 0.93}, halign='left', valign='middle')
        self.signup_label.bind(size=self.update_text_align)
        self.layout.add_widget(self.signup_label)

        self.sub_label = Label(text="Create your Account!", font_size='15sp', bold=True, color=(0.3, 0.3, 0.8, 1), size_hint=(0.8, None), height=dp(30), pos_hint={'x': 0.08, 'top': 0.87}, halign='left', valign='middle')
        self.sub_label.bind(size=self.update_text_align)
        self.layout.add_widget(self.sub_label)

        content = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(0.85, None), height=dp(420), pos_hint={'center_x': 0.5, 'center_y': 0.42})
        content.add_widget(Label(text="VOTELLY", color=(0.25, 0.7, 0.6, 1), font_size='35sp', bold=True, size_hint_y=None, height=dp(60)))
        
        self.email = self.create_input("Email")
        content.add_widget(self.email)

        p1_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(52), spacing=dp(5))
        self.pass1 = self.create_input("Password", password=True)
        self.pass1.size_hint_x = 0.8
        self.btn1 = Button(text="Show", size_hint_x=0.2, background_color=(0.9,0.9,0.9,1), color=(0.2,0.2,0.8,1), background_normal='')
        self.btn1.bind(on_release=lambda x: self.toggle(self.pass1, self.btn1))
        p1_box.add_widget(self.pass1); p1_box.add_widget(self.btn1); content.add_widget(p1_box)

        p2_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(52), spacing=dp(5))
        self.pass2 = self.create_input("Confirm Password", password=True)
        self.pass2.size_hint_x = 0.8
        self.btn2 = Button(text="Show", size_hint_x=0.2, background_color=(0.9,0.9,0.9,1), color=(0.2,0.2,0.8,1), background_normal='')
        self.btn2.bind(on_release=lambda x: self.toggle(self.pass2, self.btn2))
        p2_box.add_widget(self.pass2); p2_box.add_widget(self.btn2); content.add_widget(p2_box)
        
        self.error = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=dp(20), font_size='12sp')
        content.add_widget(self.error)
        
        self.signup_btn = Button(text="Sign Up", size_hint=(1, None), height=dp(55), bold=True, color=(0.25, 0.7, 0.6, 1), background_color=(0,0,0,0))
        with self.signup_btn.canvas.after:
            Color(0.25, 0.7, 0.6, 1)
            self.line = Line(rounded_rectangle=(0,0,0,0, 25), width=1.2)
        self.signup_btn.bind(pos=self.update_line, size=self.update_line, on_release=self.validate)
        
        content.add_widget(self.signup_btn)
        self.layout.add_widget(content); self.add_widget(self.layout)

    def get_gradient_texture(self, color1, color2):
        tex = Texture.create(size=(2, 1), colorfmt='rgba')
        c1 = [int(c * 255) for c in color1]; c2 = [int(c * 255) for c in color2]
        buf = array.array('B', c1 + c2); tex.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return tex

    def update_rects(self, *args):
        self.bg_rect.pos = self.pos; self.bg_rect.size = self.size
        self.card.size = (self.width, self.height * 0.75); self.card.pos = (0, 0)

    def update_text_align(self, label, size): label.text_size = size
    def create_input(self, hint, password=False): return TextInput(hint_text=hint, password=password, multiline=False, size_hint_y=None, height=dp(52), background_color=(0.94, 0.94, 0.94, 1), background_normal='')
    def toggle(self, f, b): f.password = not f.password; b.text = "Hide" if not f.password else "Show"
    def update_line(self, ins, *args): self.line.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 25)

    def validate(self, *args):
        if "@" not in self.email.text: self.error.text = "Error: Invalid Email"
        elif len(self.pass1.text) < 8: self.error.text = "Password is too short"
        elif self.pass1.text != self.pass2.text: self.error.text = "Error: Passwords do not match!"
        else:
            self.manager.transition.direction = 'left'; self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1); self.bg_rect = Rectangle(pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        layout = FloatLayout()
        
        header = BoxLayout(orientation='vertical', size_hint=(0.80, None), height=dp(60), spacing=dp(-7), pos_hint={'center_x': 0.5, 'top': 0.90})
        welcome_label = Label(text="WELCOME!", font_size='34sp', bold=True, color=(0, 0, 0, 1), halign='left', valign='bottom', size_hint_y=None, height=dp(40))
        welcome_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        subtitle_label = Label(text="VOTE, TALLY, WISELY", font_size='12sp', color=(0, 0, 0, 1), halign='left', valign='top', size_hint_y=None, height=dp(20))
        subtitle_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        header.add_widget(welcome_label); header.add_widget(subtitle_label)
        layout.add_widget(header)
        
        jr = Button(text="Join Room", font_size='32sp', bold=True, color=(0.3, 0.3, 0.9, 1), background_color=(0,0,0,0), size_hint=(0.85, 0.15), pos_hint={'center_x': 0.5, 'top': 0.75})
        with jr.canvas.before:
            Color(0.43, 0.89, 0.75, 1); self.jl = Line(rounded_rectangle=(0,0,0,0, 20), width=1.5)
        jr.bind(pos=self.up_jl, size=self.up_jl, on_release=lambda x: self.go_to_gate("Ballot Form"))
        layout.add_widget(jr)
        
        grid = GridLayout(cols=2, spacing=dp(15), size_hint=(0.85, 0.35), pos_hint={'center_x': 0.5, 'top': 0.55})
        m = [("Raise Hand", (0.3, 0.3, 1, 1)), ("Scan Ballot", (0.5, 1, 0.8, 1)), ("Digital Forms", (0.9, 0.96, 1, 1)), ("Ranked Choice", (1, 1, 0.7, 1))]
        for t, c in m:
            btn = Button(text=t, background_normal='', background_color=c, color=(0.1, 0.1, 0.5, 1), bold=True)
            btn.bind(on_release=lambda x, name=t: self.go_to_gate(name))
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        plus_btn = Button(text="+", font_size='35sp', background_normal='', background_color=(0.3, 0.3, 1, 1), size_hint=(None, None), size=(dp(60), dp(60)), pos_hint={'center_x': 0.5, 'y': 0.05})
        plus_btn.bind(on_release=lambda x: VotingModeModal().open())
        layout.add_widget(plus_btn)
        self.add_widget(layout)

    def update_bg(self, *args): self.bg_rect.pos = self.pos; self.bg_rect.size = self.size
    def up_jl(self, ins, *args): self.jl.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 20)
    def go_to_gate(self, mode_name):
        self.manager.get_screen('room_gate').mode_subtitle.text = f"MODE: {mode_name}"
        self.manager.transition.direction = 'left'; self.manager.current = 'room_gate'

class RoomGateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.96, 1, 0.98, 1); self.bg_rect = Rectangle(pos=(0, 0), size=Window.size)
        layout.bind(size=self.update_bg)
        back_btn = Button(text="Back", size_hint=(0.2, 0.05), pos_hint={'x': 0.05, 'top': 0.91}, background_color=(0, 0, 0, 0), color=(0.3, 0.3, 1, 1), bold=True, font_size='14sp')
        with back_btn.canvas.before:
            Color(0.43, 0.89, 0.75, 1); self.back_line = Line(rounded_rectangle=(0, 0, 0, 0, 12), width=1.1)
        back_btn.bind(pos=self.update_back_ui, size=self.update_back_ui, on_release=self.go_back); layout.add_widget(back_btn)
        
        label_container = BoxLayout(orientation='vertical', size_hint=(0.8, None), height=dp(65), pos_hint={'center_x': 0.5, 'top': 0.80})
        title_label = Label(text="Enter Room Code", font_size='26sp', bold=True, color=(0.3, 0.3, 1, 1), size_hint_y=None, height=dp(35))
        self.mode_subtitle = Label(text="MODE: Ballot Form", font_size='18sp', color=(0.1, 0.8, 0.6, 1), size_hint_y=None, height=dp(30))
        label_container.add_widget(title_label); label_container.add_widget(self.mode_subtitle); layout.add_widget(label_container)
        
        self.code_input = TextInput(hint_text="######", multiline=False, halign='center', font_size='32sp', size_hint=(0.8, 0.12), pos_hint={'center_x': 0.5, 'top': 0.68}, background_color=(0.92, 0.92, 0.92, 1), background_normal='', padding_y=[dp(20), 0])
        layout.add_widget(self.code_input)
        
        btn_box = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(0.7, 0.20), pos_hint={'center_x': 0.5, 'top': 0.45})
        btn_box.add_widget(self.create_styled_button("Join"))
        c_btn = self.create_styled_button("Create"); c_btn.bind(on_release=self.go_to_create); btn_box.add_widget(c_btn)
        layout.add_widget(btn_box); self.add_widget(layout)

    def update_bg(self, *args): self.bg_rect.size = Window.size
    def update_back_ui(self, ins, *args): self.back_line.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 12)
    def go_back(self, *args): self.manager.transition.direction = 'right'; self.manager.current = 'dashboard'
    def go_to_create(self, *args): self.manager.transition.direction = 'left'; self.manager.current = 'create_room'

    def create_styled_button(self, txt):
        btn = Button(text=txt, font_size='22sp', bold=True, color=(0.3, 0.3, 1, 1), background_color=(0,0,0,0))
        with btn.canvas.before:
            Color(0.43, 0.89, 0.75, 1); btn.line = Line(rounded_rectangle=(0,0,0,0, 25), width=1.5)
        btn.bind(pos=lambda i, v: setattr(i.line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, 25)), size=lambda i, v: setattr(i.line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, 25)))
        return btn

class CreateRoomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(1, 1, 1, 1); Rectangle(pos=(0, 0), size=Window.size)
        content = BoxLayout(orientation='vertical', spacing=dp(20), size_hint=(0.85, None), height=dp(400), pos_hint={'center_x': 0.5, 'top': 0.85})
        content.add_widget(Label(text="Create New Room", font_size='24sp', bold=True, color=(0, 0, 0, 1)))
        self.room_name = TextInput(hint_text="Room Name", multiline=False, size_hint_y=None, height=dp(50))
        self.room_pass = TextInput(hint_text="Room Password (Optional)", password=True, multiline=False, size_hint_y=None, height=dp(50))
        content.add_widget(self.room_name); content.add_widget(self.room_pass)
        content.add_widget(Button(text="CREATE & START", size_hint_y=None, height=dp(55), bold=True, background_color=(0.43, 0.89, 0.75, 1), background_normal=''))
        
        cancel_btn = Button(text="Cancel", size_hint_y=None, height=dp(45), color=(0.3, 0.3, 0.9, 1), background_color=(0, 0, 0, 0))
        cancel_btn.bind(on_release=self.go_back); content.add_widget(cancel_btn)
        layout.add_widget(content); self.add_widget(layout)

    def go_back(self, *args): self.manager.transition.direction = 'right'; self.manager.current = 'room_gate'

class VotellyApp(App):
    def build(self):
        sm = ScreenManager(transition=CardTransition(direction='left', mode='push', duration=0.3))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(RoomGateScreen(name='room_gate'))
        sm.add_widget(CreateRoomScreen(name='create_room'))
        return sm

if __name__ == '__main__':
    VotellyApp().run()
