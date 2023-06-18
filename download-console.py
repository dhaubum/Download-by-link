import requests
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path

def browse_directory():
    directory = input("Введите путь к директории для сохранения файла: ")
    return directory

def download_file(file_url, save_directory):
    parsed_url = urlparse(file_url)
    file_name = parsed_url.path.split("/")[-1]

    save_path = Path(save_directory) / file_name

    response = requests.head(file_url)
    total_size = int(response.headers.get("content-length", 0))

    progress_bar = tqdm(total=total_size, unit="Б", unit_scale=True)

    spin_symbols = ['/', '-', '\\', '|']

    with requests.get(file_url, stream=True) as req:
        req.raise_for_status()
        with open(save_path, "wb") as file:
            for data in req.iter_content(chunk_size=4096):
                file.write(data)
                progress_bar.update(len(data))
                progress_bar.set_postfix_str(spin_symbols[progress_bar.n % len(spin_symbols)])
                progress_bar.refresh()

    progress_bar.close()

save_directory = browse_directory()
if not save_directory:
    sys.exit("Директория не выбрана. Программа завершена.")

file_url = input("URL файла: ")
download_file(file_url, save_directory)