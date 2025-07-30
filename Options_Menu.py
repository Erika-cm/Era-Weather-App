import customtkinter as ctk
import pandas as pd
import json
from Logic import AppLogic

class MainWindow(ctk.CTk):
    def __init__(self, title, windowsize):
        super().__init__()

        #window stuff
        self.title(title)
        self.geometry(f'{windowsize[0]}x{windowsize[1]}')

        self.base_font = ("Ariel", 15)
        self.selected_city_var = ctk.StringVar(value="No City Selected")
        self.selected_lat = "default"
        self.selected_long = "default"

        self.app_logic = AppLogic(self)
        self.app_logic.load_city_data() #this function still needs to be called to fill city_list (in main app this will be called when options menu is raised)
        self.options_menu = OptionsMenu(self, self.base_font, self.app_logic, self.app_logic.city_list, self.selected_city_var, self.selected_lat, self.selected_long)
        self.options_menu.pack(expand=True, fill="both")
        self.testing_button = ctk.CTkButton(self, text="Test", command=self.testing_function)
        self.testing_button.pack()
        self.mainloop()
    
    def testing_function(self): #for testing (can be altered to test other stuff)
        print(self.selected_city_var.get())
        print(self.selected_lat)

class OptionsMenu(ctk.CTkFrame):
        def __init__(self, parent, font, app_logic, city_list, selected_city_var, selected_lat, selected_long):
            super().__init__(master=parent)
            self.grid_rowconfigure(0, weight=4, uniform="a")
            self.grid_rowconfigure(1, weight=1, uniform="a") #as options are added this row moves down while new ones are added above
            self.grid_columnconfigure((0,1), weight=1, uniform="a")
            
            #variables
            self.city_list = city_list
            self.dropdown_selection = ctk.StringVar()
            self.parent = parent
            
            #frames
            self.options_frame = ctk.CTkFrame(self)
            self.button_frame = ctk.CTkFrame(self)
            #widgets
            #searchable list ui
            self.dropdown_instuctions = ctk.CTkLabel(self.options_frame, text="Click to Search, and/or Select City from Dropdown", text_color="#1c5d5d")
            self.dropdown_menu = ctk.CTkComboBox(self.options_frame, width=250, values=self.city_list, variable=self.dropdown_selection)
            self.dropdown_menu.set("Search")
            
            self.confirm_button = ctk.CTkButton(self.button_frame, text="Confirm", font=font, command=lambda: self.confirm_city_selection(app_logic))
            self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", font=font, command=lambda: self.destroy()) #this needs to call a method from Logic to raise the other frames instead

            #layout
            self.options_frame.grid(row=0, column=0, columnspan=2, sticky="new")
            self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ews")

            self.dropdown_instuctions.pack(padx=2, pady=2)
            self.dropdown_menu.pack(padx=2, pady=2)
            self.confirm_button.pack(fill="x", side="right")
            self.cancel_button.pack(fill="x", side="left")
            
            self.dropdown_menu.bind("<KeyRelease>", lambda event, dropdown_menu=self.dropdown_menu, city_list=self.city_list: app_logic.city_search(event, dropdown_menu, city_list))
            self.dropdown_menu.bind("<FocusIn>", self.clear_dropdown)

        def confirm_city_selection(self, app_logic):
            app_logic.store_selected_city(self.dropdown_selection)            
            self.destroy()
            
        def clear_dropdown(self, event):
            self.dropdown_menu.set("")
            self.sub_lst = []   

if __name__ == "__main__":               
    main_window = MainWindow("Testing Options Menu", (960, 540))