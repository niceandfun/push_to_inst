import requests
import pathlib
import urllib3
from PIL import Image


def download_image(image_url, folder_path):
    image = folder_path
    response = requests.get(image_url, verify=False)
    with open(image, 'wb') as file:
        file.write(response.content)


def fetch_all_hubble_images():
    hubble_collection_api_url = "http://hubblesite.org/api/v3/images/wallpaper"
    response = requests.get(hubble_collection_api_url)
    hubble_image_id_fetched = [hubble_image['id'] for hubble_image in response.json()]
    for image_id in hubble_image_id_fetched:
        hubble_image_api_url = "http://hubblesite.org/api/v3/image/{}".format(image_id)
        response = requests.get(hubble_image_api_url)
        hubble_image_url_fetched = response.json()['image_files']
        hubble_url = 'http:' + hubble_image_url_fetched[-1]['file_url']
        image_type = hubble_url.split('.')[-1]
        hubble_image_name = '{}.{}'.format(image_id, image_type)
        folder_path = images_directory + hubble_image_name
        download_image(hubble_url, folder_path)
        crop_image(folder_path)


def crop_image(folder_path):
    image = Image.open('{}'.format(folder_path))
    image_width = image.width
    image_height = image.height
    if image_width > image_height:
        image_width = image_height
    else:
        image_height = image_width
    coordinates = (0, 0, image_width, image_height)
    cropped = image.crop(coordinates)
    cropped.save(folder_path)


if __name__ == '__main__':
    images_directory = './images/'
    pathlib.Path(images_directory).mkdir(parents=True, exist_ok=True)
    urllib3.disable_warnings()
    fetch_all_hubble_images()
