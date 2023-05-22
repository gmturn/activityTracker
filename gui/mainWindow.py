# Import customtkinter module
from PIL import Image
import customtkinter as ctk
from gui.entryManagerFrame import EntryManagerFrame
from gui.homeFrame import HomeFrame

# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("System")

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("green")

# Create App class


class MainWindow(ctk.CTk):
    # Layout of the GUI will be written in the init itself
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sets the title of our window to "App"
        self.title("AccelActivity")
        # Dimensions of the window will be 200x200
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("./images/AccelActivityIcon.ico")

        self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0) # not sure what this does
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Main Menu", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Home Button
        self.sidebar_Home = ctk.CTkButton(
            self.sidebar_frame, text="Home", command=self.home_button_event)
        self.sidebar_Home.grid(row=1, column=0, padx=20, pady=10)

        # Entry Manager Button
        self.sidebar_EntryManager = ctk.CTkButton(
            self.sidebar_frame, text="Entry Manager", command=self.entry_manager_button_event)
        self.sidebar_EntryManager.grid(row=2, column=0, padx=20, pady=10)

        # Button 3
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Appearance Mode Button
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")  # sets default

        # instantiate EntryManagerFrame
        self.HomeFrame = HomeFrame(self)
        self.HomeFrame.grid(row=0, column=1, sticky="nsew")
        self.HomeFrame.grid_remove()  # initially hidden

        # instantiate EntryManagerFrame
        self.entryManagerFrame = EntryManagerFrame(self)
        self.entryManagerFrame.grid(row=0, column=1, sticky="nsew")
        self.entryManagerFrame.grid_remove()  # initially hidden

    def select_frame_by_name(self, name):
        # set button color for selected button
        # self.sidebar_Home.configure(
        #     fg_color=("gray75", "gray25") if name == "home" else "transparent")
        # self.sidebar_EntryManager.configure(
        #     fg_color=("gray75", "gray25") if name == "entry_manager" else "transparent")

        # show selected frame
        if name == "home":
            self.HomeFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.HomeFrame.grid_forget()

        if name == "entry_manager":
            self.entryManagerFrame.grid()
        else:
            self.entryManagerFrame.grid_remove()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def entry_manager_button_event(self):
        self.select_frame_by_name("entry_manager")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
