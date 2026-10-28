import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import os

# --- APP CONFIGURATION & COLORS ---
APP_TITLE = "Kitchen Mate 🧑‍🍳 - Your Recipe Recommender"
FILE_NAME = "kitchen_mate_recipes.csv"
BG_COLOR = "#FFFDF7"       # Creamy White
PRIMARY_COLOR = "#E25822"  # Flame Orange/Saffron
SEC_COLOR = "#4CAF50"      # Fresh Green
TEXT_COLOR = "#2B2B2B"     # Dark Grey
FONT_TITLE = ("Helvetica", 18, "bold")
FONT_HEADING = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 11)

# --- 50 INDIAN VEG RECIPES (Auto-generated on first run) ---
DEFAULT_RECIPES = [
    ("Aloo Gobi", "Potato, Cauliflower, Red Tomato, Onion, Cumin, Turmeric, Salt", "1. Heat oil in a pan.\n2. Add cumin seeds and chopped onions.\n3. Add chopped red tomatoes and cook until soft.\n4. Add potatoes and cauliflower.\n5. Add spices, cover, and cook until tender.\n6. Garnish with coriander."),
    ("Palak Paneer", "Spinach, Paneer cubes, Onion, Garlic, Green Chili, Garam Masala, Cream", "1. Blanch spinach and puree it.\n2. Sauté onion, garlic, and green chili.\n3. Add spinach puree and spices. Cook for 5 mins.\n4. Add paneer cubes and simmer.\n5. Finish with a swirl of cream."),
    ("Chana Masala", "Chickpeas, Onion, Ripe Tomato, Ginger, Garlic, Chole Masala", "1. Soak and boil chickpeas.\n2. Sauté ginger, garlic, and onions.\n3. Add pureed ripe tomato and chole masala.\n4. Cook until oil separates.\n5. Add chickpeas, simmer for 10 mins."),
    ("Dal Makhani", "Black Urad Dal, Kidney Beans, Butter, Tomato Puree, Cream, Garlic", "1. Soak and boil dal and beans until soft.\n2. In a pan, add butter and garlic paste.\n3. Add tomato puree and cook well.\n4. Mix in the boiled dal and simmer for 30 mins.\n5. Add cream and serve hot."),
    ("Baingan Bharta", "Roasted Eggplant, Onion, Tomato, Green Chili, Mustard Oil, Coriander", "1. Roast eggplant over open flame until charred.\n2. Peel and mash the eggplant.\n3. Heat mustard oil, add onion and green chili.\n4. Add chopped tomatoes and cook.\n5. Mix in mashed eggplant and cook for 5 mins."),
    ("Bhindi Masala", "Okra (Bhindi), Onion, Tomato, Cumin, Coriander Powder, Amchur", "1. Wash, dry, and chop okra.\n2. Fry okra in a little oil until non-sticky, keep aside.\n3. Sauté onions and tomatoes with spices.\n4. Add fried okra back to the pan.\n5. Cook for 5 mins and serve."),
    ("Matar Paneer", "Green Peas, Paneer, Onion, Tomato, Cashew, Garam Masala", "1. Blend onion, tomato, and cashew into a paste.\n2. Cook the paste in oil until fragrant.\n3. Add spices and water to make gravy.\n4. Add green peas and paneer cubes.\n5. Simmer for 8-10 mins."),
    ("Rajma", "Kidney Beans, Onion, Tomato, Ginger, Garlic, Rajma Masala", "1. Boil soaked kidney beans.\n2. Prepare a gravy with onion, ginger, garlic, and tomato.\n3. Add Rajma masala and cook.\n4. Add the beans and simmer until thick.\n5. Serve with steaming rice."),
    ("Aloo Jeera", "Potato, Cumin seeds (Jeera), Green Chili, Turmeric, Coriander leaves", "1. Boil and cube potatoes.\n2. Heat oil, generously add cumin seeds.\n3. Add green chilies and turmeric.\n4. Toss in potatoes and roast slightly.\n5. Garnish with fresh coriander."),
    ("Malai Kofta", "Potato, Paneer, Cashew, Cream, Tomato, Onion, Cardamom", "1. Mash potato and paneer, make balls and deep fry (Koftas).\n2. Make a rich, smooth gravy with onion, tomato, and cashews.\n3. Add cream and cardamom to the gravy.\n4. Pour gravy over koftas just before serving."),
    ("Kadai Paneer", "Paneer, Bell Pepper (Capsicum), Onion, Tomato, Kadai Masala", "1. Dry roast and grind whole spices for Kadai Masala.\n2. Cube bell peppers, onions, and paneer.\n3. Sauté veggies, add tomato paste and the ground masala.\n4. Toss in paneer and cook for 5 mins."),
    ("Mix Veg Curry", "Carrot, Beans, Cauliflower, Peas, Onion, Tomato, Cream", "1. Chop and lightly boil all vegetables.\n2. Make a basic onion-tomato gravy.\n3. Add spices and the boiled vegetables.\n4. Simmer for 5 mins and finish with a dash of cream."),
    ("Dum Aloo", "Baby Potatoes, Yogurt, Fennel Powder, Ginger Powder, Mustard Oil", "1. Boil, peel, and fry baby potatoes.\n2. Whisk yogurt with fennel and ginger powder.\n3. Heat mustard oil, add spices, then slowly stir in the yogurt mixture.\n4. Add potatoes and slow-cook (dum) for 15 mins."),
    ("Paneer Butter Masala", "Paneer, Butter, Tomato, Cashew, Honey, Kasuri Methi", "1. Boil tomatoes and cashews, then puree.\n2. Melt butter, add the puree and cook.\n3. Add spices and a touch of honey.\n4. Add paneer cubes and crushed Kasuri Methi.\n5. Simmer for 2 minutes."),
    ("Dal Tadka", "Yellow Moong Dal, Toor Dal, Garlic, Cumin, Dry Red Chili, Ghee", "1. Boil both dals with turmeric and salt.\n2. Heat ghee in a tadka pan.\n3. Add cumin, crushed garlic, and dry red chilies.\n4. Pour this sizzling tadka over the boiled dal.\n5. Garnish with coriander."),
    ("Vegetable Biryani", "Basmati Rice, Mix Veggies, Biryani Masala, Saffron, Mint, Yogurt", "1. Marinate veggies in yogurt and biryani masala.\n2. Parboil basmati rice with whole spices.\n3. Layer rice over the marinated veggies in a heavy pot.\n4. Top with saffron milk and mint.\n5. Seal and cook on low heat (dum) for 25 mins."),
    ("Lemon Rice", "Cooked Rice, Lemon Juice, Peanuts, Mustard seeds, Curry leaves, Turmeric", "1. Heat oil, temper mustard seeds and curry leaves.\n2. Roast peanuts in the same pan.\n3. Add turmeric and turn off heat.\n4. Mix in cooked rice and fresh lemon juice.\n5. Toss well and serve."),
    ("Curd Rice", "Cooked Rice, Yogurt, Milk, Mustard seeds, Green Chili, Pomegranate", "1. Mash cooked rice slightly.\n2. Mix with yogurt and a little milk.\n3. Temper mustard seeds and green chili in oil and pour over rice.\n4. Garnish with pomegranate seeds."),
    ("Jeera Rice", "Basmati Rice, Cumin Seeds (Jeera), Ghee, Bay leaf", "1. Wash and soak basmati rice for 30 mins.\n2. Heat ghee, add bay leaf and lots of cumin seeds.\n3. Add rice, water, and salt.\n4. Cook until water is absorbed and rice is fluffy."),
    ("Tomato Rice", "Cooked Rice, Ripe Tomato, Onion, Garlic, Curry leaves, Spices", "1. Heat oil, add curry leaves and garlic.\n2. Sauté onions, then add finely chopped ripe tomatoes.\n3. Cook until it becomes a thick, oily paste.\n4. Gently fold in the cooked rice."),
    ("Bisi Bele Bath", "Rice, Toor Dal, Tamarind, Bisi Bele Bath Masala, Mix Vegetables", "1. Pressure cook rice, dal, and vegetables together.\n2. Extract tamarind juice.\n3. Mix tamarind and the special masala into the cooked mix.\n4. Simmer until flavours blend. Top with ghee."),
    ("Ven Pongal", "Raw Rice, Moong Dal, Black Pepper, Cumin, Ghee, Cashews", "1. Dry roast moong dal slightly, then pressure cook with rice.\n2. Coarsely crush black pepper and cumin.\n3. Heat ghee, fry cashews, and add the pepper-cumin mix.\n4. Pour the tempering over the cooked rice-dal mix."),
    ("Upma", "Semolina (Rava), Onion, Green Chili, Mustard seeds, Urad Dal, Curry leaves", "1. Dry roast semolina and keep aside.\n2. Temper mustard seeds, urad dal, and curry leaves.\n3. Sauté onions and green chilies.\n4. Add boiling water, then slowly whisk in the semolina to avoid lumps."),
    ("Poha", "Flattened Rice (Poha), Onion, Potato, Peanuts, Mustard seeds, Turmeric", "1. Wash poha gently in a sieve and let it soften.\n2. Fry peanuts and keep aside.\n3. Temper mustard seeds, cook diced potatoes and onions.\n4. Add turmeric, mix in poha and peanuts. Serve with lemon."),
    ("Idli", "Idli Rice, Urad Dal, Fenugreek seeds", "1. Soak rice and dal separately for 6 hours.\n2. Grind to a smooth batter and ferment overnight.\n3. Grease idli molds, pour batter.\n4. Steam for 10-12 minutes until fluffy."),
    ("Masala Dosa", "Dosa Batter, Potato, Onion, Mustard seeds, Turmeric", "1. Make potato masala by tempering mustard seeds, sautéing onions, and adding boiled potatoes and turmeric.\n2. Spread dosa batter thinly on a hot griddle.\n3. Drizzle oil/ghee and cook until crispy.\n4. Place potato masala in the center and fold."),
    ("Uttapam", "Dosa Batter, Onion, Tomato, Green Chili, Coriander", "1. Pour a thick ladle of dosa batter on a griddle.\n2. Do not spread it too much.\n3. Sprinkle finely chopped onion, tomato, and chilies on top.\n4. Flip and cook both sides until golden."),
    ("Medu Vada", "Urad Dal, Green Chili, Ginger, Curry leaves, Black Pepper", "1. Soak urad dal for 2 hours, grind to a thick, fluffy batter with minimal water.\n2. Mix in chopped chili, ginger, and curry leaves.\n3. Wet hands, shape batter into donuts with a hole in the center.\n4. Deep fry until golden and crispy."),
    ("Sambar", "Toor Dal, Tamarind, Sambar Powder, Drumstick, Carrot, Pumpkin", "1. Boil toor dal until mushy.\n2. Boil vegetables in tamarind water.\n3. Add sambar powder and the cooked dal.\n4. Temper mustard seeds, fenugreek, and curry leaves, and add to the sambar."),
    ("Tomato Rasam", "Tomato, Tamarind, Rasam Powder, Garlic, Coriander", "1. Mash tomatoes in tamarind water.\n2. Boil the mixture with rasam powder and salt.\n3. Crush garlic and temper with mustard seeds and cumin.\n4. Add tempering to rasam and garnish with coriander."),
    ("Coconut Chutney", "Fresh Coconut, Roasted Chana Dal, Green Chili, Ginger, Mustard seeds", "1. Grind coconut, roasted chana dal, chili, and ginger to a paste.\n2. Add water for desired consistency.\n3. Temper mustard seeds and curry leaves in oil.\n4. Pour tempering over the chutney."),
    ("Peanut Chutney", "Peanuts, Dry Red Chili, Garlic, Tamarind, Cumin", "1. Dry roast peanuts and remove skins.\n2. Roast red chilies and garlic slightly.\n3. Grind all ingredients with a small piece of tamarind and salt.\n4. Temper with mustard seeds."),
    ("Aloo Paratha", "Whole Wheat Flour, Potato, Onion, Green Chili, Amchur", "1. Knead a soft dough with wheat flour.\n2. Mash boiled potatoes and mix with chopped onion, chili, and spices.\n3. Stuff the potato mix into small dough balls.\n4. Roll out gently and cook on a tawa with butter/ghee."),
    ("Gobi Paratha", "Whole Wheat Flour, Grated Cauliflower, Ginger, Ajwain, Coriander", "1. Grate cauliflower, squeeze out excess water.\n2. Mix with grated ginger, ajwain (carom seeds), and spices.\n3. Stuff dough balls with the mixture and roll out.\n4. Cook on a hot griddle with oil until golden spots appear."),
    ("Paneer Paratha", "Whole Wheat Flour, Grated Paneer, Green Chili, Garam Masala", "1. Grate paneer and mix with spices and herbs.\n2. Stuff the mixture inside wheat dough balls.\n3. Roll into flatbreads.\n4. Roast on a tawa with ghee on both sides."),
    ("Puri Bhaji", "Whole Wheat Flour, Potato, Tomato, Mustard Seeds, Turmeric", "1. Knead a stiff dough, roll into small circles, and deep fry (Puris).\n2. For Bhaji: Boil and crumble potatoes.\n3. Temper mustard seeds, sauté tomatoes and spices.\n4. Add potatoes and water, simmer into a thick curry."),
    ("Chole Bhature", "Chickpeas, All-purpose Flour (Maida), Yogurt, Tea leaves, Chole Masala", "1. Make dough with maida, yogurt, and a pinch of baking soda. Let it rest.\n2. Boil chickpeas with a tea bag for dark color.\n3. Make spicy chole gravy using onion, tomato, and chole masala.\n4. Roll dough into ovals and deep fry into fluffy Bhatures."),
    ("Pav Bhaji", "Potato, Cauliflower, Peas, Capsicum, Onion, Tomato, Pav Bhaji Masala", "1. Boil and mash potato, cauliflower, and peas.\n2. Sauté onion, capsicum, and tomato in lots of butter.\n3. Add Pav Bhaji masala and the mashed veggies.\n4. Toast Pav (bread) in butter and serve together."),
    ("Misal Pav", "Sprouted Moth Beans (Matki), Onion, Tomato, Misal Masala, Farsan", "1. Make a spicy watery curry (Kat/Sample) with sprouts and Misal masala.\n2. In a bowl, layer the sprouted curry.\n3. Top generously with crunchy Farsan (namkeen), chopped onions, and coriander.\n4. Serve with soft Pav and a wedge of lemon."),
    ("Dhokla", "Gram Flour (Besan), Yogurt, Eno (Fruit Salt), Mustard Seeds, Green Chili", "1. Mix besan, yogurt, turmeric, and water into a smooth batter.\n2. Stir in Eno just before steaming; the batter will froth.\n3. Steam in a greased pan for 15 mins.\n4. Temper mustard seeds, chili, and sugar water, pour over cut dhokla squares."),
    ("Khandvi", "Gram Flour (Besan), Yogurt, Ginger-Green Chili paste, Mustard seeds, Coconut", "1. Whisk besan, yogurt, and water into a thin, lump-free batter.\n2. Cook on low heat, stirring continuously until thick and glossy.\n3. Spread instantly in thin layers on a flat surface.\n4. Once cool, roll up into tight cylinders. Temper and garnish with coconut."),
    ("Thepla", "Whole Wheat Flour, Fenugreek leaves (Methi), Yogurt, Turmeric, Sesame seeds", "1. Chop fresh methi leaves finely.\n2. Knead wheat flour with methi, yogurt, spices, and a little oil.\n3. Roll into thin discs.\n4. Roast on a tawa with oil until cooked. (Great for travel!)."),
    ("Vegetable Handvo", "Rice, Chana Dal, Toor Dal, Bottle Gourd (Lauki), Sesame seeds", "1. Grind soaked rice and dals into a coarse batter and ferment.\n2. Add grated bottle gourd and spices to the batter.\n3. Bake in an oven or slow-cook in a pan with a tempering of sesame seeds and mustard.\n4. Cut into savory cake slices."),
    ("Lauki Kofta", "Bottle Gourd (Lauki), Besan, Onion, Tomato, Garam Masala", "1. Grate lauki, squeeze out water, mix with besan and spices, and fry as koftas.\n2. Prepare a rich onion-tomato gravy.\n3. Gently drop the koftas into the simmering gravy.\n4. Serve immediately so koftas stay soft."),
    ("Navratan Korma", "Mix Veggies, Paneer, Pineapple, Cashew Paste, Cream, Mild Spices", "1. Parboil a mix of 9 vegetables/fruits/nuts.\n2. Make a sweet and savory white gravy using cashew paste and cream.\n3. Fold in the vegetables, paneer, and pineapple chunks.\n4. Simmer gently; this dish is creamy and mildly sweet."),
    ("Methi Matar Malai", "Fenugreek leaves (Methi), Green Peas, Cream, Cashew, Onion", "1. Boil green peas and blanch chopped methi leaves to reduce bitterness.\n2. Sauté onion and cashew paste.\n3. Add the methi and peas, cook for 5 mins.\n4. Stir in heavy cream and a pinch of garam masala. Serve hot."),
    ("Shahi Paneer", "Paneer, Tomato, Onion, Cashew, Yogurt, Cardamom, Saffron", "1. Make a smooth puree of boiled onion, tomato, and cashews.\n2. Heat ghee, add cardamom and the puree.\n3. Whisk in yogurt and cook until oil separates.\n4. Add paneer cubes and saffron strands. Simmer until creamy."),
    ("Kashmiri Dum Aloo", "Baby Potatoes, Yogurt, Kashmiri Red Chili Powder, Fennel, Ginger Powder", "1. Deep fry pricked baby potatoes until golden.\n2. Whisk yogurt with Kashmiri chili powder (for bright red color), fennel, and ginger.\n3. Heat mustard oil, add the yogurt mix and potatoes.\n4. Slow cook (Dum) covered until the gravy coats the potatoes."),
    ("Veg Kolhapuri", "Mixed Vegetables, Dry Red Chilies, Coconut, Sesame Seeds, Kolhapuri Masala", "1. Dry roast coconut, sesame seeds, and whole spices, then grind.\n2. Sauté mixed vegetables in oil.\n3. Add the ground spicy masala paste and water.\n4. Cook until vegetables are tender and gravy is fiery red."),
    ("Mushroom Do Pyaza", "Mushrooms, Onion (Lots of it), Tomato, Cumin, Garam Masala", "1. Slice mushrooms and chop onions in two different ways (diced and petals).\n2. Sauté the onion petals lightly and keep aside.\n3. Make a base gravy with diced onions and tomatoes.\n4. Add mushrooms and the sautéed onion petals. Cook till mushrooms release water and shrink.")
]

def initialize_csv():
    """Creates the CSV file with 50 recipes if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Recipe_Name", "Ingredients", "Instructions"])
            for recipe in DEFAULT_RECIPES:
                writer.writerow(recipe)

class KitchenMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("800x650")
        self.root.configure(bg=BG_COLOR)
        
        self.recipes = [] # List to hold dictionaries of recipes
        initialize_csv()
        self.load_data()

        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_BODY, padding=[15, 5], background="#E0E0E0")
        style.map("TNotebook.Tab", background=[("selected", PRIMARY_COLOR)], foreground=[("selected", "white")])
        
        style.configure("TButton", font=FONT_BODY, background=SEC_COLOR, foreground="white", padding=6)
        style.map("TButton", background=[("active", "#45a049")])

        # Title Label
        title_lbl = tk.Label(self.root, text=APP_TITLE, font=FONT_TITLE, bg=BG_COLOR, fg=PRIMARY_COLOR, pady=10)
        title_lbl.pack()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Create Tabs
        self.tab_find = tk.Frame(self.notebook, bg=BG_COLOR)
        self.tab_browse = tk.Frame(self.notebook, bg=BG_COLOR)
        self.tab_add = tk.Frame(self.notebook, bg=BG_COLOR)

        self.notebook.add(self.tab_find, text=" 🔍 Smart Chef ")
        self.notebook.add(self.tab_browse, text=" 📖 Recipe Book ")
        self.notebook.add(self.tab_add, text=" ➕ Add Recipe ")

        self.setup_find_tab()
        self.setup_browse_tab()
        self.setup_add_tab()

    def load_data(self):
        """Loads recipes from the CSV file."""
        self.recipes.clear()
        try:
            with open(FILE_NAME, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.recipes.append(row)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load recipes: {e}")

    # ================= TAB 1: SMART CHEF (ALGORITHM) =================
    def setup_find_tab(self):
        lbl = tk.Label(self.tab_find, text="What ingredients do you have? (Comma separated)", font=FONT_HEADING, bg=BG_COLOR, fg=TEXT_COLOR)
        lbl.pack(pady=(15, 5))

        self.inventory_entry = tk.Entry(self.tab_find, font=FONT_BODY, width=50)
        self.inventory_entry.pack(pady=5)
        self.inventory_entry.insert(0, "e.g., tomato, paneer, onion")

        btn = ttk.Button(self.tab_find, text="Find Recipes", command=self.find_recipes)
        btn.pack(pady=10)

        # PanedWindow to show Results List and Recipe Details side-by-side
        pane = ttk.PanedWindow(self.tab_find, orient=tk.HORIZONTAL)
        pane.pack(expand=True, fill="both", padx=10, pady=10)

        # Results Listbox
        list_frame = tk.Frame(pane, bg=BG_COLOR)
        self.result_listbox = tk.Listbox(list_frame, font=FONT_BODY, selectbackground=PRIMARY_COLOR)
        self.result_listbox.pack(expand=True, fill="both", side=tk.LEFT)
        scrollbar1 = ttk.Scrollbar(list_frame, orient="vertical", command=self.result_listbox.yview)
        scrollbar1.pack(side=tk.RIGHT, fill="y")
        self.result_listbox.config(yscrollcommand=scrollbar1.set)
        self.result_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        pane.add(list_frame, weight=1)

        # Details Text Box
        self.result_detail = scrolledtext.ScrolledText(pane, font=FONT_BODY, wrap=tk.WORD, bg="#FFF8F0")
        pane.add(self.result_detail, weight=2)

    def find_recipes(self):
        inventory_input = self.inventory_entry.get().strip()
        if not inventory_input or inventory_input == "e.g., tomato, paneer, onion":
            messagebox.showwarning("Input Error", "Please enter some ingredients.")
            return

        # Clean up inventory input (e.g., "Tomato, potato " -> ["tomato", "potato"])
        inventory = [item.strip().lower() for item in inventory_input.split(",") if item.strip()]

        matches = []
        for recipe in self.recipes:
            # Clean up recipe ingredients
            recipe_ingredients = [ing.strip().lower() for ing in recipe['Ingredients'].split(",")]
            
            # ALGORITHM: Substring check
            # For each required ingredient in the recipe, check if any of the user's inventory items is a substring
            matched_count = 0
            for req_ing in recipe_ingredients:
                for inv_item in inventory:
                    if inv_item in req_ing: # Substring match (e.g., "tomato" in "red tomato")
                        matched_count += 1
                        break # Found a match for this required ingredient, move to next req_ing

            # Calculate a match score
            total_req = len(recipe_ingredients)
            if matched_count > 0:
                score = (matched_count / total_req) * 100
                matches.append({"recipe": recipe, "score": score, "matched": matched_count, "total": total_req})

        # Sort by best match (highest score first)
        matches.sort(key=lambda x: x['score'], reverse=True)

        # Update Listbox
        self.result_listbox.delete(0, tk.END)
        self.current_matched_recipes = [] # Keep a reference list aligned with listbox

        if not matches:
            self.result_listbox.insert(tk.END, "No matching recipes found. :(")
            self.result_detail.delete(1.0, tk.END)
            return

        for match in matches:
            r_name = match['recipe']['Recipe_Name']
            display_text = f"{r_name} ({match['matched']}/{match['total']} match)"
            self.result_listbox.insert(tk.END, display_text)
            self.current_matched_recipes.append(match['recipe'])

    def on_result_select(self, event):
        selection = self.result_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.current_matched_recipes):
                recipe = self.current_matched_recipes[index]
                self.show_recipe_details(recipe, self.result_detail)

    # ================= TAB 2: RECIPE BOOK (BROWSE) =================
    def setup_browse_tab(self):
        pane = ttk.PanedWindow(self.tab_browse, orient=tk.HORIZONTAL)
        pane.pack(expand=True, fill="both", padx=10, pady=10)

        # Browse Listbox
        list_frame = tk.Frame(pane, bg=BG_COLOR)
        self.browse_listbox = tk.Listbox(list_frame, font=FONT_BODY, selectbackground=PRIMARY_COLOR)
        self.browse_listbox.pack(expand=True, fill="both", side=tk.LEFT)
        scrollbar2 = ttk.Scrollbar(list_frame, orient="vertical", command=self.browse_listbox.yview)
        scrollbar2.pack(side=tk.RIGHT, fill="y")
        self.browse_listbox.config(yscrollcommand=scrollbar2.set)
        self.browse_listbox.bind('<<ListboxSelect>>', self.on_browse_select)
        pane.add(list_frame, weight=1)

        # Details Text Box
        self.browse_detail = scrolledtext.ScrolledText(pane, font=FONT_BODY, wrap=tk.WORD, bg="#FFF8F0")
        pane.add(self.browse_detail, weight=2)
        
        self.populate_browse_list()

    def populate_browse_list(self):
        self.browse_listbox.delete(0, tk.END)
        # Sort alphabetically for browsing
        sorted_recipes = sorted(self.recipes, key=lambda x: x['Recipe_Name'])
        self.current_browse_recipes = sorted_recipes
        for recipe in sorted_recipes:
            self.browse_listbox.insert(tk.END, recipe['Recipe_Name'])

    def on_browse_select(self, event):
        selection = self.browse_listbox.curselection()
        if selection:
            index = selection[0]
            recipe = self.current_browse_recipes[index]
            self.show_recipe_details(recipe, self.browse_detail)

    # ================= TAB 3: ADD RECIPE =================
    def setup_add_tab(self):
        form_frame = tk.Frame(self.tab_add, bg=BG_COLOR)
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)

        tk.Label(form_frame, text="Recipe Name:", font=FONT_HEADING, bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=10)
        self.add_name = tk.Entry(form_frame, font=FONT_BODY, width=40)
        self.add_name.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Ingredients:\n(Comma separated)", font=FONT_HEADING, bg=BG_COLOR).grid(row=1, column=0, sticky="nw", pady=10)
        self.add_ingredients = tk.Text(form_frame, font=FONT_BODY, width=40, height=4)
        self.add_ingredients.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Instructions:\n(Step-by-step)", font=FONT_HEADING, bg=BG_COLOR).grid(row=2, column=0, sticky="nw", pady=10)
        self.add_instructions = tk.Text(form_frame, font=FONT_BODY, width=40, height=8)
        self.add_instructions.grid(row=2, column=1, pady=10, padx=10)

        save_btn = ttk.Button(form_frame, text="Save Recipe to CSV", command=self.save_recipe)
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def save_recipe(self):
        name = self.add_name.get().strip()
        ingredients = self.add_ingredients.get("1.0", tk.END).strip()
        instructions = self.add_instructions.get("1.0", tk.END).strip()

        if not name or not ingredients or not instructions:
            messagebox.showwarning("Incomplete", "Please fill out all fields.")
            return

        try:
            with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, ingredients, instructions])
            
            messagebox.showinfo("Success", f"'{name}' has been added!")
            
            # Clear form
            self.add_name.delete(0, tk.END)
            self.add_ingredients.delete("1.0", tk.END)
            self.add_instructions.delete("1.0", tk.END)

            # Reload data globally to update algorithm and browse tab
            self.load_data()
            self.populate_browse_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save recipe: {e}")

    # ================= HELPER FUNCTIONS =================
    def show_recipe_details(self, recipe, text_widget):
        """Formats and displays recipe data inside the given ScrolledText widget."""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        # Display Name
        text_widget.insert(tk.END, f"{recipe['Recipe_Name']}\n", "title")
        text_widget.insert(tk.END, "=" * 40 + "\n\n")
        
        # Display Ingredients
        text_widget.insert(tk.END, "🛒 Ingredients:\n", "heading")
        ingredients_list = recipe['Ingredients'].split(',')
        for ing in ingredients_list:
            text_widget.insert(tk.END, f" • {ing.strip()}\n")
        text_widget.insert(tk.END, "\n")
        
        # Display Instructions
        text_widget.insert(tk.END, "🍳 Instructions:\n", "heading")
        text_widget.insert(tk.END, f"{recipe['Instructions']}\n")
        
        # Apply Tags for colors/fonts
        text_widget.tag_configure("title", font=("Helvetica", 16, "bold"), foreground=PRIMARY_COLOR)
        text_widget.tag_configure("heading", font=("Helvetica", 12, "bold"), foreground=SEC_COLOR)
        
        text_widget.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = KitchenMateApp(root)
    root.mainloop()