# Importing the required libraries from Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from libdw import pyrebase

# Set up firebase
url = "https://dw-keyboard-warriors.firebaseio.com/"
apikey = "AIzaSyCho_88MLCkNDOGGEE9tmGvObj54HKFd8Q"
config = {"apiKey": apikey, "databaseURL": url}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# This creates a GridLayout with 6 columns
class floor_layout(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.cols = 6
        
# This creates a label with formatted text
class my_label(Label):
    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        self.halign = 'center'
        self.valign = 'center'
        self.font_size = 30

# This creates a button with formatted text      
class my_button(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.font_size = 30

# This creates the Main Screen
class choose_floor_screen(Screen): 
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        # Set the layout of the screen to be a GridLayout with 1 column
        self.layout = GridLayout(cols = 1)
        # Create 3 buttons for 3 floors
        # Floors 1 and 2 are dummy buttons
        floor1 = my_button(text="Level 1")
        floor2 = my_button(text="Level 2")
        floor3 = my_button(text="Level 3")
        
        # Floor 3, when pressed, brings you to the level 3 screen
        floor3.bind(on_press=self.change_to_floor3)
        
        # Quit button
        quit_button = my_button(text="Quit")
        quit_button.bind(on_press=self.quit_app)
        
        # Add the widgets to the layout widget
        self.layout.add_widget(floor1)
        self.layout.add_widget(floor2)
        self.layout.add_widget(floor3)
        self.layout.add_widget(quit_button)
        
        # Add the layout widget to the screen
        self.add_widget(self.layout)
    
    # This function changes the screen to the level_3_screen
    def change_to_floor3(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'floor3'
    
    # This function exits the application
    def quit_app(self, value):
        App.get_running_app().stop()
        
# Creating a Screen for Level 3
class level_3_screen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.g = floor_layout(height=100)
        
        # Seat 1
        # Retrieve information from firebase as f3l1
        f3l1 = db.child("1D_final").child("floor3").child("led1").get().val()
        self.seat1_status = my_label(text="Seat 1")
        # If Seat 1 is occupied
        if f3l1 == "occupied":
            # Set the background to be red
            self.seat1_status.canvas.before.add(Color(1,0,0,1))
            # And the text to be white
            self.seat1_status.color = (1,1,1,1)
        # If it is unoccupied
        else:
            # Set the background to be green
            self.seat1_status.canvas.before.add(Color(0,1,0,1))
            # And the text to be black
            self.seat1_status.color = (0,0,0,1)
        # Creating the background
        self.seat1_status.canvas.before.add(Rectangle(pos=(3,301), size=(94,97)))
        
        
        ### The same thing applies for the subsequent seats


        # Seat 2
        f3l2 = db.child("1D_final").child("floor3").child("led2").get().val()
        self.seat2_status = my_label(text="Seat 2")
        if f3l2 == "occupied":
            self.seat2_status.canvas.before.add(Color(1,0,0,1))
            self.seat2_status.color = (1,1,1,1)
        else:
            self.seat2_status.canvas.before.add(Color(0,1,0,1))
            self.seat2_status.color = (0,0,0,1)
        self.seat2_status.canvas.before.add(Rectangle(pos=(100,301), size=(97,97)))

        # Seat 3
        f3l3 = db.child("1D_final").child("floor3").child("led3").get().val()
        self.seat3_status = my_label(text="Seat 3")
        if f3l3 == "occupied":
            self.seat3_status.canvas.before.add(Color(1,0,0,1))
            self.seat3_status.color = (1,1,1,1)
        else:
            self.seat3_status.canvas.before.add(Color(0,1,0,1))
            self.seat3_status.color = (0,0,0,1)
        self.seat3_status.canvas.before.add(Rectangle(pos=(200,301), size=(97,97)))
        
        # Seat 4
        f3l4 = db.child("1D_final").child("floor3").child("led4").get().val()
        self.seat4_status = my_label(text="Seat 4")
        if f3l4 == "occupied":
            self.seat4_status.canvas.before.add(Color(1,0,0,1))
            self.seat4_status.color = (1,1,1,1)
        else:
            self.seat4_status.canvas.before.add(Color(0,1,0,1))
            self.seat4_status.color = (0,0,0,1)
        self.seat4_status.canvas.before.add(Rectangle(pos=(300,301), size=(97,97)))
        
        # Seat 5
        f3l5 = db.child("1D_final").child("floor3").child("led5").get().val()
        self.seat5_status = my_label(text="Seat 5")
        if f3l5 == "occupied":
            self.seat5_status.canvas.before.add(Color(1,0,0,1))
            self.seat5_status.color = (1,1,1,1)
        else:
            self.seat5_status.canvas.before.add(Color(0,1,0,1))
            self.seat5_status.color = (0,0,0,1)
        self.seat5_status.canvas.before.add(Rectangle(pos=(400,301), size=(97,97)))
        
        # Seat 6
        f3l6 = db.child("1D_final").child("floor3").child("led6").get().val()
        self.seat6_status = my_label(text="Seat 6")
        if f3l6 == "occupied":
            self.seat6_status.canvas.before.add(Color(1,0,0,1))
            self.seat6_status.color = (1,1,1,1)
        else:
            self.seat6_status.canvas.before.add(Color(0,1,0,1))
            self.seat6_status.color = (0,0,0,1)
        self.seat6_status.canvas.before.add(Rectangle(pos=(500,301), size=(97,97)))
        
        
       ### The code for the seats end here
        
        
        # Add the Seats(which are widgets) to the GridLayout self.g
        self.g.add_widget(self.seat1_status)
        self.g.add_widget(self.seat2_status)
        self.g.add_widget(self.seat3_status)
        self.g.add_widget(self.seat4_status)
        self.g.add_widget(self.seat5_status)
        self.g.add_widget(self.seat6_status)
        
        # Add a Corridor to be of the class FloatLayout with a height of 200
        self.f1 = FloatLayout(height=200)
        
        # Add a Menu Button
        menu_button = my_button(text="Back to Menu", size_hint_x=0.5, size_hint_y=0.73, pos=(0,0))
        
        # When pressed, returns to the Main Menu
        menu_button.bind(on_press=self.change_to_menu)
        
        # Add a Refresh button
        refresh_button = my_button(text="Refresh", size_hint_x=0.5, size_hint_y=0.73, pos=(300,0))
        
        # When pressed, refreshes the page
        refresh_button.bind(on_press=self.refresh)
        
        # Create a FloatLayout
        self.f2 = FloatLayout()
        self.f2.add_widget(menu_button)
        self.f2.add_widget(refresh_button)
        
        # Setting the Background Image for the main layout
        i = Image(source="real_layout.jpg")
        
        # Defining the Main layout as a FloatLayout
        self.main_layout = FloatLayout()
        
        # Creating a BoxLayout with a vertical orientation, and adding
        # the different layouts to this layout
        self.layout2 = BoxLayout(orientation="vertical")
        self.layout2.add_widget(self.g)
        self.layout2.add_widget(self.f1)
        self.layout2.add_widget(self.f2)
        
        # Adding the background image, and the BoxLayout to the main layout
        self.main_layout.add_widget(i)
        self.main_layout.add_widget(self.layout2)
        
        # Adding the main layout to the screen
        self.add_widget(self.main_layout)
    
    # Exits to Main Menu  
    def change_to_menu(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    # Refreshes the status of all the seats
    def refresh(self, value):
        f3l1 = db.child("1D_final").child("floor3").child("led1").get().val()
        f3l2 = db.child("1D_final").child("floor3").child("led2").get().val()
        f3l3 = db.child("1D_final").child("floor3").child("led3").get().val()
        f3l4 = db.child("1D_final").child("floor3").child("led4").get().val()
        f3l5 = db.child("1D_final").child("floor3").child("led5").get().val()
        f3l6 = db.child("1D_final").child("floor3").child("led6").get().val()
        
        # Seat 1
        if f3l1 == "occupied":
            self.seat1_status.canvas.before.add(Color(1,0,0,1))
            self.seat1_status.color = (1,1,1,1)
        else:
            self.seat1_status.canvas.before.add(Color(0,1,0,1))
            self.seat1_status.color = (0,0,0,1)
        self.seat1_status.canvas.before.add(Rectangle(pos=(3,301), size=(94,97)))
        
        # Seat 2
        if f3l2 == "occupied":
            self.seat2_status.canvas.before.add(Color(1,0,0,1))
            self.seat2_status.color = (1,1,1,1)
        else:
            self.seat2_status.canvas.before.add(Color(0,1,0,1))
            self.seat2_status.color = (0,0,0,1)
        self.seat2_status.canvas.before.add(Rectangle(pos=(100,301), size=(97,97)))
        
        # Seat 3
        if f3l3 == "occupied":
            self.seat3_status.canvas.before.add(Color(1,0,0,1))
            self.seat3_status.color = (1,1,1,1)
        else:
            self.seat3_status.canvas.before.add(Color(0,1,0,1))
            self.seat3_status.color = (0,0,0,1)
        self.seat3_status.canvas.before.add(Rectangle(pos=(200,301), size=(97,97)))
        
        # Seat 4
        if f3l4 == "occupied":
            self.seat4_status.canvas.before.add(Color(1,0,0,1))
            self.seat4_status.color = (1,1,1,1)
        else:
            self.seat4_status.canvas.before.add(Color(0,1,0,1))
            self.seat4_status.color = (0,0,0,1)
        self.seat4_status.canvas.before.add(Rectangle(pos=(300,301), size=(97,97)))
        
        # Seat 5
        if f3l5 == "occupied":
            self.seat5_status.canvas.before.add(Color(1,0,0,1))
            self.seat5_status.color = (1,1,1,1)
        else:
            self.seat5_status.canvas.before.add(Color(0,1,0,1))
            self.seat5_status.color = (0,0,0,1)
        self.seat5_status.canvas.before.add(Rectangle(pos=(400,301), size=(97,97)))
        
        # Seat 6
        if f3l6 == "occupied":
            self.seat6_status.canvas.before.add(Color(1,0,0,1))
            self.seat6_status.color = (1,1,1,1)
        else:
            self.seat6_status.canvas.before.add(Color(0,1,0,1))
            self.seat6_status.color = (0,0,0,1)
        self.seat6_status.canvas.before.add(Rectangle(pos=(500,301), size=(97,97)))
        

# Create a Main App
class switch_screen_app(App):
    def build(self):
        Window.size = (600, 400)
        sm = ScreenManager()
        # Add the Main Menu and the level 3 screen
        cfs = choose_floor_screen(name='menu')
        self.l3s = level_3_screen(name='floor3')
        sm.add_widget(cfs)
        sm.add_widget(self.l3s)
        # Startup to Main Menu
        sm.current = 'menu'
        return sm
    

# Run the application
if __name__ == "__main__":
    switch_screen_app().run()