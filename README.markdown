# Genshin Icon Downloader

## Overview
The **Genshin Icon Downloader** is a Python script with a graphical user interface (GUI) built using `customtkinter`. It enables users to download item card images for characters from *Genshin Impact* by scraping them from the Fandom wiki. The script includes autocomplete suggestions for character names and resizes downloaded images to 170x170 pixels, saving them in an "items" folder.

## Features
- **Autocomplete Suggestions**: Type a character’s name and get up to 5 matching suggestions from the full list of playable characters.
- **Image Download**: Downloads the item card image for the selected character as a PNG file.
- **Folder Access**: Includes an "Open" button to quickly view the "items" folder containing downloaded images.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Requirements
- **Python 3.x**
- Required Python libraries:
  - `customtkinter`
  - `requests`
  - `beautifulsoup4`
  - `Pillow`
  - `urllib` (part of Python’s standard library)

Install the dependencies using pip:
```bash
pip install customtkinter requests beautifulsoup4 Pillow
```

## How to Use
1. **Run the Script**:
   ```bash
   python icondown.py
   ```
2. **Search for a Character**: Type a character’s name in the search bar. Suggestions will appear below as you type.
3. **Select a Character**: Click a suggestion to fill the search bar with the character’s name.
4. **Download the Icon**: Press the "Download" button to fetch and save the item card image.
5. **View Downloads**: Click the "Open" button to open the "items" folder in your file explorer.

## Character List
The script includes a comprehensive list of playable *Genshin Impact* characters as of Version 5.6 (May 2025), covering:
- **Mondstadt**: Albedo, Amber, Barbara, Bennett, Diluc, Diona, Eula, Fischl, Jean, Kaeya, Klee, Lisa, Mika, Mona, Noelle, Razor, Rosaria, Sucrose, Venti
- **Liyue**: Baizhu, Beidou, Chongyun, Gaming, Ganyu, Hu Tao, Keqing, Lan Yan, Ningguang, Qiqi, Shenhe, Xiangling, Xiao, Xingqiu, Xinyan, Yanfei, Yaoyao, Yelan, Yun Jin, Zhongli, Xianyun
- **Inazuma**: Arataki Itto, Chiori, Gorou, Kaedehara Kazuha, Kamisato Ayaka, Kamisato Ayato, Kirara, Kujou Sara, Kuki Shinobu, Raiden Shogun, Sangonomiya Kokomi, Sayu, Shikanoin Heizou, Thoma, Yae Miko, Yoimiya, Yumemizuki Mizuki
- **Sumeru**: Alhaitham, Candace, Collei, Cyno, Dehya, Dori, Faruzan, Kaveh, Layla, Nahida, Nilou, Sethos, Tighnari, Wanderer
- **Fontaine**: Charlotte, Chevreuse, Clorinde, Emilie, Escoffier, Freminet, Furina, Lyney, Lynette, Navia, Neuvillette, Sigewinne, Wriothesley
- **Natlan**: Chasca, Citlali, Iansan, Ifa, Kachina, Kinich, Mavuika, Mualani, Ororon, Varesa, Xilonen
- **Snezhnaya**: Arlecchino, Tartaglia
- **Others**: Aloy, Traveler

## Notes
- The script scrapes images from the character’s gallery page on the *Genshin Impact* Fandom wiki (e.g., `https://genshin-impact.fandom.com/wiki/<character_name>/Gallery`), targeting images with "Item" in the alt text.
- Special character name formatting (e.g., "Raiden Shogun" to "Raiden_Shogun") is handled via a `character_mappings` dictionary in the code.
- Images are resized to 170x170 pixels using the `Pillow` library with the `LANCZOS` resampling filter.

## Troubleshooting
- **No Image Found**: Verify the character name is correct and the wiki page includes an item card image. Some characters may not have item cards available.
- **Network Errors**: Check your internet connection and ensure the Fandom wiki is accessible.
- **Folder Not Found**: The "items" folder is created automatically when downloading an image or clicking "Open."

## License
This project is open-source and available under the MIT License.