import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import os
from urllib.parse import quote
import subprocess

class GenshinIconDownloader:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Genshin Icon Downloader")
        self.window.geometry("400x60")
        self.window.resizable(False, True)  # Allow vertical resizing only
        
        # Updated List of all character names
        self.character_list = [
            # Mondstadt
            "albedo", "amber", "barbara", "bennett", "diluc", "diona", "eula",
            "fischl", "jean", "klee", "mika", "mona", "noelle", "razor",
            "rosaria", "sucrose", "venti",
            
            # Liyue
            "baizhu", "beidou", "chongyun", "gaming", "ganyu", "hu tao", "keqing",
            "ningguang", "qiqi", "shenhe", "xiangling", "xiao", "xingqiu",
            "xinyan", "yanfei", "yaoyao", "yelan", "yun jin", "zhongli",
            
            # Inazuma
            "arataki itto", "gorou", "kaedehara kazuha", "kamisato ayaka",
            "kamisato ayato", "kujou sara", "kuki shinobu", "raiden shogun",
            "sangonomiya kokomi", "sayu", "shikanoin heizou", "thoma",
            "yae miko", "yoimiya",
            
            # Sumeru
            "alhaitham", "candace", "collei", "cyno", "dehya", "dori",
            "kaveh", "kirara", "nahida", "nilou", "tighnari",
            
            # Fontaine
            "charlotte", "chevreuse", "freminet", "furina", "lyney",
            "lynette", "navia", "neuvillette", "wriothesley",

            # Natlan
            "chasca", "mualani", "xilonen", "kinich", "ororon",
            
            # Others
            "tartaglia", "wanderer", "arlecchino"
        ]
        
        # Create main search frame
        self.search_frame = ctk.CTkFrame(self.window)
        self.search_frame.pack(pady=10, padx=10, fill="x")
        
        # Search entry with suggestions dropdown
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Enter character name..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.update_suggestions)
        
        # Buttons
        self.open_folder_button = ctk.CTkButton(
            self.search_frame,
            text="Open",
            command=self.open_download_folder
        )
        self.open_folder_button.pack(side="right", padx=(0, 8))
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Download",
            command=self.download_icon
        )
        self.search_button.pack(side="right")
        
        # Suggestions dropdown (will appear below search bar)
        self.dropdown_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        self.dropdown_list = ctk.CTkFrame(
            self.dropdown_frame,
            fg_color=("gray90", "gray20")
        )
        self.suggestion_labels = []
        
        # Bind events for better dropdown behavior
        self.search_entry.bind('<FocusOut>', lambda e: self.hide_dropdown_delayed())
        self.window.bind('<Configure>', lambda e: self.update_dropdown_position())

    def hide_dropdown_delayed(self):
        """Hide dropdown with slight delay to allow for clicks"""
        self.window.after(100, self.dropdown_frame.place_forget)

    def update_dropdown_position(self):
        """Update dropdown position relative to search bar"""
        if self.dropdown_frame.winfo_ismapped():
            x = self.search_entry.winfo_rootx() - self.window.winfo_rootx()
            y = self.search_entry.winfo_rooty() - self.window.winfo_rooty() + self.search_entry.winfo_height()
            self.dropdown_frame.place(x=x, y=y, width=self.search_entry.winfo_width())

    def update_suggestions(self, event=None):
        current_input = self.search_entry.get().lower().strip()
        
        # Clear previous suggestions
        for label in self.suggestion_labels:
            label.destroy()
        self.suggestion_labels.clear()
        
        # Reset window size when no input
        if not current_input:
            self.dropdown_frame.place_forget()
            self.window.geometry("400x60")
            return
            
        # Find matching characters
        suggestions = [char for char in self.character_list 
                      if current_input in char.lower()][:5]
        
        if suggestions:
            # Calculate new window height based on number of suggestions
            suggestion_height = 35  # Height per suggestion
            new_window_height = 60 + (len(suggestions) * suggestion_height)
            self.window.geometry(f"400x{new_window_height}")
            
            # Position dropdown
            self.dropdown_list.pack(fill="both", expand=True)
            self.dropdown_frame.place(
                x=10,  # Match padding with search frame
                y=50,  # Position below search bar
                relwidth=0.95  # Slightly smaller than window width
            )
            
            # Create suggestion buttons
            for suggestion in suggestions:
                label = ctk.CTkButton(
                    self.dropdown_list,
                    text=suggestion,
                    anchor="w",
                    fg_color="transparent",
                    hover_color=("gray75", "gray25"),
                    command=lambda s=suggestion: self.use_suggestion(s),
                    height=30
                )
                label.pack(fill="x", padx=2, pady=(0, 2))
                self.suggestion_labels.append(label)
        else:
            self.dropdown_frame.place_forget()
            self.window.geometry("400x60")

    def use_suggestion(self, suggestion):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, suggestion)
        self.dropdown_frame.place_forget()
        self.window.geometry("400x60")  # Reset window size

    def download_icon(self):
        character_name = self.search_entry.get().strip()
        if not character_name:
            return
            
        try:
            # Format the URL - handle special cases
            character_mappings = {
                "raiden shogun": "Raiden_Shogun",
                "hu tao": "Hu_Tao",
                "yae miko": "Yae_Miko",
                "kamisato ayaka": "Kamisato_Ayaka",
                "kamisato ayato": "Kamisato_Ayato",
                "arataki itto": "Arataki_Itto",
                "kujou sara": "Kujou_Sara",
                "kaedehara kazuha": "Kaedehara_Kazuha",
                "sangonomiya kokomi": "Sangonomiya_Kokomi",
                "yun jin": "Yun_Jin",
                "kuki shinobu": "Kuki_Shinobu",
                "shikanoin heizou": "Shikanoin_Heizou",
            }
            
            formatted_name = character_name.lower()
            if formatted_name in character_mappings:
                formatted_name = character_mappings[formatted_name]
            else:
                # Default formatting for other names
                formatted_name = character_name.title().replace(" ", "_")
                
            url = f"https://genshin-impact.fandom.com/wiki/{quote(formatted_name)}/Gallery"
            
            # Get the page content
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the item image (looking for "Item" in alt text instead of "Icon")
            item_img = soup.select_one('img[alt*="Item"]')
            
            if item_img and 'src' in item_img.attrs:
                item_url = item_img['src']
                if item_url.startswith('//'):
                    item_url = 'https:' + item_url
                    
                # Download the image
                img_response = requests.get(item_url)
                img_response.raise_for_status()
                
                # Save the image with resizing
                if not os.path.exists('items'):
                    os.makedirs('items')
                    
                image = Image.open(io.BytesIO(img_response.content))
                # Resize image to 170x170 while maintaining aspect ratio
                image = image.resize((170, 170), Image.Resampling.LANCZOS)
                filename = f"items/{formatted_name}_item.png"
                image.save(filename)
                
                return f"Successfully downloaded item card to {filename}"
            else:
                return "Could not find item card for this character"
                
        except requests.exceptions.RequestException as e:
            return f"Error downloading item card: {str(e)}"

    def open_download_folder(self):
        """Opens the items folder in file explorer"""
        if not os.path.exists('items'):
            os.makedirs('items')
        
        # Open folder based on operating system
        if os.name == 'nt':  # Windows
            os.startfile('items')
        else:  # macOS and Linux
            subprocess.run(['xdg-open', 'items'])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = GenshinIconDownloader()
    app.run()