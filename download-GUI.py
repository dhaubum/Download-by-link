import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from urllib.parse import urlparse
import requests
from tkinter.ttk import Progressbar

def download_file():
    file_url = url_entry.get()

    if not file_url:
        show_custom_error("Ошибка", "Пожалуйста, введите URL файла.")
        return

    parsed_url = urlparse(file_url)
    file_name = parsed_url.path.split("/")[-1]

    save_directory = save_directory_entry.get()

    if not save_directory:
        show_custom_error("Ошибка", "Пожалуйста, выберите директорию сохранения.")
        return

    save_path = save_directory + "/" + file_name

    try:
        response = requests.get(file_url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        progress_bar["maximum"] = total_size
        progress_bar["value"] = 0
        progress_bar.pack()

        with open(save_path, "wb") as file:
            downloaded = 0
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                file.write(data)
                progress_bar["value"] = downloaded
                root.update()

    except requests.exceptions.RequestException as e:
        show_custom_error("Ошибка", str(e))

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_directory_entry.delete(0, tk.END)
        save_directory_entry.insert(0, directory)

def apply_styles():
    root.configure(bg="#121212")
    style = tk.ttk.Style()
    style.theme_use('default')
    style.configure("custom.Horizontal.TProgressbar", thickness=5, troughcolor='white', background='#00bfa5')
    url_label.configure(bg="#121212", fg="#fff", font=("Arial", 12))
    url_entry.configure(bg="#1e1e1e", fg="#fff", font=("Arial", 12), relief="flat", bd=0, highlightthickness=1,
                        highlightbackground="#808080", highlightcolor="#00bfa5", insertbackground="#fff")
    directory_label.configure(bg="#121212", fg="#fff", font=("Arial", 12))
    directory_frame.configure(bg="#121212")
    save_directory_entry.configure(bg="#1e1e1e", fg="#fff", font=("Arial", 12), relief="flat", bd=0, highlightthickness=1,
                              highlightbackground="#808080", highlightcolor="#00bfa5", insertbackground="#fff")
    browse_button.configure(bg="#00bfa5", fg="#fff", font=("Arial", 12), relief="flat", bd=0,
                            activebackground="#00aba9", activeforeground="#fff")
    download_button.configure(bg="#00bfa5", fg="#fff", font=("Arial", 12), relief="flat", bd=0,
                              activebackground="#00aba9", activeforeground="#fff")
    progress_bar.configure(style="custom.Horizontal.TProgressbar")

def show_custom_error(title, message):
    messagebox.showerror(title, message)

root = tk.Tk()
root.title("Загрузчик файла")

url_label = tk.Label(root, text="URL файла")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

directory_label = tk.Label(root, text="Директория сохранения")
directory_label.pack()

directory_frame = tk.Frame(root)
directory_frame.pack()

save_directory_entry = tk.Entry(directory_frame, width=40)
save_directory_entry.pack(side="left")

browse_button = tk.Button(directory_frame, text="Обзор", command=browse_directory)
browse_button.pack(side="left", padx=5)

download_button = tk.Button(root, text="Скачать", command=download_file)
download_button.pack(pady=10)

progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate", style="custom.Horizontal.TProgressbar")

apply_styles()

root.mainloop()
