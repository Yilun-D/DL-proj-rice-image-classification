import os
import pathlib
import requests
import zipfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

"""
Load the rice image dataset and preprocessing 
"""


def download_dataset(url, filename):
    response = requests.get(url)
    if response == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
            return True
    else:
        return False


def unzip_file(file_name, location):
    with zipfile.ZipFile(file_name, location) as f:
        f.extractall(location)


def check_file_exists(directory_path) -> bool:
    return os.path.exists(directory_path)


def print_number_of_files(data_dir):
    Arborio = list(data_dir.glob("Arborio/*"))
    Basmati = list(data_dir.glob("Basmati/*"))
    Ipsala = list(data_dir.glob("Ipsala/*"))
    Jasmine = list(data_dir.glob("Jasmine/*"))
    Karacadag = list(data_dir.glob("Karacadag/*"))

    print("The length of Arborio: %d" % len(Arborio))
    print("The length of Jasmine: %d" % len(Jasmine))
    print("The length of Basmati: %d" % len(Basmati))
    print("The length of Ipsala: %d" % len(Ipsala))
    print("The length of Karacadag: %d" % len(Karacadag))


def get_image_files(dir_path):
    all_image_dirs = [f.path for f in os.scandir(dir_path) if f.is_dir()]
    for dir in all_image_dirs:
        for img in os.listdir(dir):
            yield os.path.join(dir, img)


def get_image_size(image_path) -> tuple:
    image = Image.open(image_path)
    return image.size


def check_image_size(image_path, actual_width, actual_height) -> bool:
    width, height = get_image_size(image_path)
    if actual_width is width and actual_height is height:
        print("checked")
        return True
    else:
        return False


def resize_image(image_path, target_size=(250, 250)):
    image = Image.open(image_path)
    resized_image = image.resize(target_size)
    resized_image.save(image_path)
    print(f'Resized image "{image_path}" to {target_size}.')


def resize_if_required(data_dir, actual_width, actual_height):
    with ThreadPoolExecutor(max_workers=8) as executor:
        for img in get_image_files(data_dir):
            result = executor.submit(check_image_size, img, actual_width, actual_height)
            if not result:
                resize_image(img)


directory_path = "Rice_Image_Dataset"
if not check_file_exists(directory_path):
    if not download_dataset(link, directory_path):
        print("Download failed")
        exit()

data_dir = pathlib.Path(directory_path).absolute()
print_number_of_files(data_dir)

first_image = next(get_image_files(data_dir))
actual_width, actual_height = get_image_size(first_image)
resize_if_required(data_dir, actual_width, actual_height)
