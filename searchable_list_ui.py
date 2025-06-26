import customtkinter as ctk

class SearchableDropdownMenu(ctk.CTkFrame):
    def __init__(self, parent, full_lst):
        super().__init__(master=parent)

        #variables
        self.full_lst = full_lst
        self.dropdown_selection = ctk.StringVar()
        self.sub_lst = []
        self.list_of_searches = []

        #widgets
        self.dropdown_instuctions = ctk.CTkLabel(self, text="Click to Search, and/or Select City from Dropdown", text_color="#1c5d5d")
        self.dropdown_menu = ctk.CTkComboBox(self, width=250, values=full_lst, variable=self.dropdown_selection)
        self.dropdown_menu.set("Search")

        #layout
        self.dropdown_instuctions.pack()
        self.dropdown_menu.pack()

        self.dropdown_menu.bind("<KeyRelease>", self.city_search)
        self.dropdown_menu.bind("<FocusIn>", self.clear_dropdown)

    def clear_dropdown(self, event):
        self.dropdown_menu.set("")
        self.sub_lst = []

    def city_search(self, event):
        search = event.widget.get()
        if search == "":
            self.dropdown_menu.configure(values= self.full_lst)
            self.sub_lst = []
        elif len(search) == 1:
            self.matching_cities = []
            self.list_of_searches = []
            all_letters_match = False
            for city in  self.full_lst:
                for i, l in enumerate(search):
                    if l.lower() == city[i].lower():
                        all_letters_match = True
                    else:
                        all_letters_match = False
                if all_letters_match == True:        
                    self.matching_cities.append(city)
            self.matching_cities = tuple(self.matching_cities)
            if self.matching_cities != ():
                self.sub_lst.append(tuple(self.matching_cities))
            self.dropdown_menu.configure(values=self.sub_lst[-1])
            self.list_of_searches.append(search)
        else:
            self.matching_cities = []
            all_letters_match = False
            try:
                #detect if current search is smaller than previous
                if len(search) < len(self.list_of_searches[-1]):
                    self.sub_lst.pop()
                    self.list_of_searches.pop()
                most_recent_matches = self.sub_lst[-1]
            except IndexError or AttributeError: #self.sub_list or self.list_of_searches must be empty, search full list
                most_recent_matches =  self.full_lst
                self.list_of_searches = [] #if skipped first letter, initialize list_of_searches here
            for city in most_recent_matches: #loop through previous sub list
                for i, l in enumerate(search):
                    if l.lower() == city[i].lower():
                        all_letters_match = True
                    else:
                        all_letters_match = False
                if all_letters_match == True:        
                    self.matching_cities.append(city)
            self.matching_cities = tuple(self.matching_cities)        
            if self.matching_cities != () and most_recent_matches != self.matching_cities:
                self.sub_lst.append(tuple(self.matching_cities))
                self.dropdown_menu.configure(values=self.sub_lst[-1])
            elif self.matching_cities != () and most_recent_matches == self.matching_cities:
                self.dropdown_menu.configure(values=self.sub_lst[-1])
            elif self.matching_cities == () and len(search) <= len(self.list_of_searches[-1]): #search got shorter, but found no matches, search again moveing back through sub_lst
                self.sub_lst.pop()
                self.list_of_searches.pop()
                self.city_search(event)
            else:
                self.dropdown_menu.configure(values=[]) #no matching cities found (or some kind of error?)
            if search not in self.list_of_searches:
                self.list_of_searches.append(search)