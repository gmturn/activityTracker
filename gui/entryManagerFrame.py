import customtkinter as ctk


class entryManagerFrame(ctk.frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        homeButton = ctk.CTkButton(self, text="Home")
