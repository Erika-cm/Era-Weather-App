import customtkinter as ctk
import pandas as pd
import json
from searchable_list_ui import SearchableDropdownMenu

class MainWindow(ctk.CTk):
    def __init__(self, title, windowsize):
        super().__init__()

        #window stuff
        self.title(title)
        self.geometry(f'{windowsize[0]}x{windowsize[1]}')

        self.options_menu = OptionsMenu(self)

        self.options_menu.pack(expand=True, fill="both")

        self.mainloop()


class OptionsMenu(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(master=parent)

            #variables
            self.city_data = pd.read_csv('worldcities.csv')
            self.city_data['city_ascii'] = self.city_data['city_ascii'].astype(str)
            self.city_data['admin_name'] = self.city_data['admin_name'].astype(str)
            self.city_region_country = pd.DataFrame()
            self.city_region_country['city_region_country'] = self.city_data["city_ascii"].str.cat(self.city_data['admin_name'], sep=' - ')
            self.city_region_country['city_region_country'] = self.city_region_country["city_region_country"].str.cat(self.city_data['country'], sep=' - ')
            self.city_list = self.city_region_country['city_region_country'].tolist()

            #widgets
            self.city_selection_frame = SearchableDropdownMenu(self, self.city_list)
            self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self.print_selected_city)
            self.cancel_button = ctk.CTkButton(self, text="Cancel", command=lambda: self.destroy())

            #layout
            self.city_selection_frame.pack(expand=True, fill="both")
            self.confirm_button.pack(fill="x", side="right")
            self.cancel_button.pack( fill="x", side="left")

        def print_selected_city(self): #this method will be updated to store the selected city info in a json
                print(self.city_selection_frame.dropdown_selection.get())
                if self.city_selection_frame.dropdown_selection.get() != "Search":
                    self.city = self.city_selection_frame.dropdown_selection.get().split(' - ')[0]
                    self.region = self.city_selection_frame.dropdown_selection.get().split(' - ')[1]
                    self.country = self.city_selection_frame.dropdown_selection.get().split(' - ')[2]
                    selected_city_mask = (self.city_data['city_ascii'] == self.city) & (self.city_data['admin_name'] == self.region) & (self.city_data['country'] == self.country)
                    self.selected_lat = self.city_data[selected_city_mask]['lat'].iloc[0]
                    self.selected_long = self.city_data[selected_city_mask]['lng'].iloc[0]
                    del self.city_data #no need to keep dataset in memory
                    self.destroy()
                
main_window = MainWindow("Testing Options Menu", (960, 540))