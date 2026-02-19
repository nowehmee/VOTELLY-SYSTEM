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
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line, Ellipse
from kivy.graphics.texture import Texture 
from kivy.core.window import Window
from kivy.metrics import dp

Window.size = (360, 640)

# --- SUPPORTING CLASSES ---

class ModeCard(ButtonBehavior, BoxLayout):
    def __init__(self, title, bg_color, icon_char, **kwargs):
        super().__init__(**kwargs)
        self.title = title 
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
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager
        self.size_hint = (1, 1)
        self.background_color = (1, 1, 1, 1) 
        self.background = "" 
        
        layout = FloatLayout()
        layout.add_widget(Label(text="Choose Voting Mode", font_size='26sp', bold=True, color=(0, 0, 0, 1), pos_hint={'center_x': 0.5, 'top': 1.4}))
        layout.add_widget(Label(text="Voting Mode", font_size='15sp', bold=True, color=(0.4, 0.4, 0.9, 1), pos_hint={'center_x': 0.5, 'top': 1.36}))
        
        grid = GridLayout(cols=2, spacing=dp(10), padding=dp(25), size_hint=(1, 0.55), pos_hint={'center_x': 0.5, 'top': 0.78})
        modes = [("Raise Hand", (0.3, 0.3, 1, 1), "H"), ("Scan Ballot", (0.5, 1, 0.8, 1), "SB"), 
                 ("Digital Forms", (0.9, 0.96, 1, 1), "DF"), ("Ranked Choice", (1, 1, 0.7, 1), "RC")]
        
        for t, c, i in modes:
            card = ModeCard(title=t, bg_color=c, icon_char=i)
            card.bind(on_release=self.select_mode)
            grid.add_widget(card)
        
        layout.add_widget(grid)
        close_btn = Button(text="+", font_size='35sp', background_normal='', background_color=(0.95, 0.95, 1, 1), color=(0.3, 0.3, 1, 1), size_hint=(None, None), size=(dp(65), dp(65)), pos_hint={'center_x': 0.5, 'y': 0.05})
        close_btn.bind(on_release=self.dismiss)
        layout.add_widget(close_btn)
        self.add_widget(layout)

    def select_mode(self, instance):
        self.dismiss()
        self.sm.get_screen('dashboard').go_to_gate(instance.title)

# --- SCREENS ---

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
        
        prof_btn = Button(text="P", size_hint=(None, None), size=(dp(45), dp(45)), pos_hint={'right': 0.95, 'top': 0.98}, background_color=(0,0,0,0), color=(1,1,1,1), bold=True)
        with prof_btn.canvas.before:
            Color(0.3, 0.3, 1, 1)
            self.p_circ = Ellipse(pos=prof_btn.pos, size=prof_btn.size)
        prof_btn.bind(pos=lambda ins, v: setattr(self.p_circ, 'pos', ins.pos), on_release=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(prof_btn)

        header = BoxLayout(orientation='vertical', size_hint=(0.80, None), height=dp(60), spacing=dp(-7), pos_hint={'center_x': 0.5, 'top': 0.90})
        welcome_label = Label(text="WELCOME!", font_size='34sp', bold=True, color=(0.3, 0.3, 0.9, 1), halign='left', valign='bottom', size_hint_y=None, height=dp(40))
        welcome_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        subtitle_label = Label(text="VOTE, TALLY, WISELY", font_size='12sp', color=(0.3, 0.3, 0.9, 1), halign='left', valign='top', size_hint_y=None, height=dp(20))
        subtitle_label.bind(size=lambda s, w: setattr(s, 'text_size', w))
        header.add_widget(welcome_label); header.add_widget(subtitle_label)
        layout.add_widget(header)
        
        jr = Button(text="Join Room", font_size='32sp', bold=True, color=(0.3, 0.3, 0.9, 1), background_color=(0,0,0,0), size_hint=(0.85, 0.15), pos_hint={'center_x': 0.5, 'top': 0.75})
        with jr.canvas.before:
            Color(0.43, 0.89, 0.75, 1); self.jl = Line(rounded_rectangle=(0,0,0,0, 20), width=1.5)
        jr.bind(pos=self.up_jl, size=self.up_jl, on_release=lambda x: self.go_to_gate("Join Room"))
        layout.add_widget(jr)
        
        grid = GridLayout(cols=2, spacing=dp(15), size_hint=(0.85, 0.35), pos_hint={'center_x': 0.5, 'top': 0.55})
        m = [("Raise Hand", (0.3, 0.3, 1, 1)), ("Scan Ballot", (0.5, 1, 0.8, 1)), ("Digital Forms", (0.9, 0.96, 1, 1)), ("Ranked Choice", (1, 1, 0.7, 1))]
        for t, c in m:
            btn = Button(text=t, background_normal='', background_color=c, color=(0.1, 0.1, 0.5, 1), bold=True)
            btn.bind(on_release=lambda x, name=t: self.go_to_gate(name))
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        plus_btn = Button(text="+", font_size='35sp', background_normal='', background_color=(0.3, 0.3, 1, 1), size_hint=(None, None), size=(dp(60), dp(60)), pos_hint={'center_x': 0.5, 'y': 0.05})
        plus_btn.bind(on_release=lambda x: VotingModeModal(self.manager).open())
        layout.add_widget(plus_btn)
        self.add_widget(layout)

    def update_bg(self, *args): self.bg_rect.pos = self.pos; self.bg_rect.size = self.size
    def up_jl(self, ins, *args): self.jl.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 20)
    
    def go_to_gate(self, mode_name):
        gate = self.manager.get_screen('room_gate')
        if mode_name == "Join Room":
            gate.mode_subtitle.opacity = 0
            gate.create_btn.opacity = 0
            gate.create_btn.disabled = True
        else:
            gate.mode_subtitle.text = f"MODE: {mode_name}"
            gate.mode_subtitle.opacity = 1
            gate.create_btn.opacity = 1
            gate.create_btn.disabled = False
            
        self.manager.transition.direction = 'left'
        self.manager.current = 'room_gate'

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
        self.mode_subtitle = Label(text="", font_size='18sp', color=(0.1, 0.8, 0.6, 1), size_hint_y=None, height=dp(30))
        label_container.add_widget(title_label); label_container.add_widget(self.mode_subtitle); layout.add_widget(label_container)
        
        self.code_input = TextInput(hint_text="######", multiline=False, halign='center', font_size='32sp', size_hint=(0.8, 0.12), pos_hint={'center_x': 0.5, 'top': 0.68}, background_color=(0.92, 0.92, 0.92, 1), background_normal='', padding_y=[dp(20), 0])
        layout.add_widget(self.code_input)
        
        btn_box = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(0.7, 0.20), pos_hint={'center_x': 0.5, 'top': 0.45})
        
        self.join_btn = self.create_styled_button("Join")
        self.create_btn = self.create_styled_button("Create") 
        
        btn_box.add_widget(self.join_btn); btn_box.add_widget(self.create_btn)
        layout.add_widget(btn_box); self.add_widget(layout)

    def update_bg(self, *args): self.bg_rect.size = Window.size
    def update_back_ui(self, ins, *args): self.back_line.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 12)
    def go_back(self, *args): self.manager.transition.direction = 'right'; self.manager.current = 'dashboard'
    
    def create_styled_button(self, txt):
        btn = Button(text=txt, font_size='22sp', bold=True, color=(0.3, 0.3, 1, 1), background_color=(0,0,0,0))
        with btn.canvas.before:
            Color(0.43, 0.89, 0.75, 1); btn.line = Line(rounded_rectangle=(0,0,0,0, 25), width=1.5)
        btn.bind(pos=lambda i, v: setattr(i.line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, 25)), size=lambda i, v: setattr(i.line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, 25)))
        return btn

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        
        # 1. Background (Solid White)
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=Window.size)
        self.layout.bind(size=self.update_bg)

        # 2. Header Buttons (Text Only)
        self.back_btn = Button(
            text="Back", font_size='16sp', size_hint=(None, None), size=(dp(80), dp(50)),
            pos_hint={'x': 0.05, 'top': 0.98}, background_color=(0,0,0,0), color=(0.3, 0.3, 1, 1), bold=True
        )
        self.back_btn.bind(on_release=self.go_back)

        self.settings_btn = Button(
            text="Settings", font_size='16sp', size_hint=(None, None), size=(dp(100), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.98}, background_color=(0,0,0,0), color=(0.3, 0.3, 1, 1), bold=True
        )

        # 3. Profile Icon Shape (Positioned at Top)
        self.avatar_container = FloatLayout(
            size_hint=(None, None), size=(dp(100), dp(180)), pos_hint={'center_x': 0.5, 'top': 7.32}
        )
        
        with self.avatar_container.canvas:
            Color(0.25, 0.85, 0.7, 1) # Teal Ring
            self.avatar_ring = Line(circle=(0, 0, dp(88)), width=dp(2.5))
            Color(1, 1, 1, 1) # White Silhouette
            self.avatar_head = Ellipse(size=(dp(75), dp(75)))
            self.avatar_body = Ellipse(size=(dp(125), dp(60)))
            Color(0.8, 0.8, 0.8, 1) # Subtle border for visibility
            self.head_border = Line(circle=(0, 0, dp(37.5)), width=dp(1))

        self.avatar_container.bind(pos=self.update_avatar_position)

        # 4. Info Card
        self.card = FloatLayout(size_hint=(0.85, 0.28), pos_hint={'center_x': 0.5, 'top': 0.60})
        with self.card.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.card_bg = RoundedRectangle(radius=[dp(25)])
            Color(0.3, 0.3, 1, 1)
            self.card_border = Line(rounded_rectangle=(0, 0, 0, 0, 25), width=dp(1.2))
        self.card.bind(pos=self.update_card, size=self.update_card)

        self.name_label = Label(text="Full Name", font_size='24sp', bold=True, color=(0, 0, 0, 1),
                           pos_hint={'center_x': 0.5, 'center_y': 0.75})
        self.email_label = Label(text="@email_address", font_size='14sp', color=(0.5, 0.5, 0.5, 1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.58})

        # 5. Edit Profile Button
        self.edit_btn = Button(text="Edit Profile", size_hint=(0.7, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.3},
                          background_normal='', background_color=(0,0,0,0), color=(1, 1, 1, 1), bold=True)
        with self.edit_btn.canvas.before:
            Color(0.3, 0.3, 1, 1)
            self.btn_rect = RoundedRectangle(radius=[dp(15)])
        self.edit_btn.bind(pos=self.update_btn_ui, size=self.update_btn_ui)
        self.edit_btn.bind(on_release=self.show_edit_popup)

        self.card.add_widget(self.name_label); self.card.add_widget(self.email_label); self.card.add_widget(self.edit_btn)
        self.layout.add_widget(self.back_btn); self.layout.add_widget(self.settings_btn); self.layout.add_widget(self.avatar_container); self.layout.add_widget(self.card)
        self.add_widget(self.layout)

    def update_bg(self, *args): self.bg_rect.size = self.size; self.bg_rect.pos = self.pos
    def update_avatar_position(self, ins, *args):
        cx, cy = ins.center
        self.avatar_ring.circle = (cx, cy, dp(88))
        self.avatar_head.pos = (cx - dp(37.5), cy - dp(5))
        self.head_border.circle = (cx, cy + dp(32.5), dp(37.5))
        self.avatar_body.pos = (cx - dp(62.5), cy - dp(65))
    def update_card(self, ins, *args): self.card_bg.pos = ins.pos; self.card_bg.size = ins.size; self.card_border.rounded_rectangle = (ins.x, ins.y, ins.width, ins.height, 25)
    def update_btn_ui(self, ins, *args): self.btn_rect.pos = ins.pos; self.btn_rect.size = ins.size
    def go_back(self, *args): self.manager.transition.direction = 'right'; self.manager.current = 'dashboard'

    # --- EDIT POPUP LOGIC ---
    def show_edit_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        popup_content.add_widget(Label(text="Edit Profile", font_size='22sp', bold=True, color=(0.3, 0.3, 1, 1), size_hint_y=None, height=dp(40)))
        
        self.new_name = TextInput(text=self.name_label.text, hint_text="Full Name", multiline=False, size_hint_y=None, height=dp(50), background_color=(0.95, 0.95, 0.95, 1), background_normal='')
        self.new_email = TextInput(text=self.email_label.text, hint_text="Email Address", multiline=False, size_hint_y=None, height=dp(50), background_color=(0.95, 0.95, 0.95, 1), background_normal='')
        popup_content.add_widget(self.new_name); popup_content.add_widget(self.new_email)
        
        save_btn_container = FloatLayout(size_hint_y=None, height=dp(55))
        save_btn = Button(text="SAVE CHANGES", bold=True, color=(1, 1, 1, 1), background_color=(0, 0, 0, 0), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        with save_btn.canvas.before:
            Color(0.25, 0.85, 0.7, 1) # Teal
            self.save_rect = RoundedRectangle(radius=[dp(15)])
        save_btn.bind(pos=lambda i, v: setattr(self.save_rect, 'pos', i.pos), size=lambda i, v: setattr(self.save_rect, 'size', i.size))
        
        save_btn_container.add_widget(save_btn); popup_content.add_widget(save_btn_container)
        self.popup = ModalView(size_hint=(0.85, 0.45), background_color=(1, 1, 1, 1), background="")
        self.popup.add_widget(popup_content)
        save_btn.bind(on_release=self.apply_changes)
        self.popup.open()

    def apply_changes(self, instance):
        if self.new_name.text.strip(): self.name_label.text = self.new_name.text
        if self.new_email.text.strip(): self.email_label.text = self.new_email.text
        self.popup.dismiss()

class VotellyApp(App):
    def build(self):
        sm = ScreenManager(transition=CardTransition(direction='left', mode='push', duration=0.3))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(RoomGateScreen(name='room_gate'))
        sm.add_widget(ProfileScreen(name='profile')) 
        return sm

if __name__ == '__main__':
    VotellyApp().run()
