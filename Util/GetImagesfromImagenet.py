from bs4 import BeautifulSoup
import numpy as np
import requests
import cv2
import PIL.Image
import urllib


def create_url_list(wordnet_id):
  """
  Creates and returns a list of all urls from the chosen wordnet id.

  wordnet_id: ID for the chosen object.

  Return: List object containing the url addresses.
  """
  # Request Url
  page = requests.get("http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=", wordnet_id)
  soup = BeautifulSoup(page.content, 'html.parser')

  # Convert to string with every url in separate line
  str_soup = str(soup)
  tmp = str_soup.split('\r\n')

  url_list = []

  for urls in range(len(tmp)):
    item = str(str_soup.split('\r\n')[urls])
    url_list.append(item)

  return url_list



def request_image(url_string):
  """
  Requests and returns image from input url and converts it to cv2 format.
  Before converting, the urls gets checked for a valid response. If the url
  is invalid, the image is not converted and 'None' is returned as datatype.

  url_string: Url address of the image.

  Return: Requested image converted to cv2 format with cv2.imdecode.
  """
  # Request image URL and return image as cv2 format
  try:
    request = urllib.request.urlopen(url_string)
    image = np.asarray(bytearray(request.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  except:
    print(url_string, ' not valid')
    image = None
  return image


def download_image_batch(url_list, batch_size, target_dir):
  """
  Downloads images via request_image() from the url list and
  saves them to the chosen directory. The amount of images can
  be adjusted with the batch size. Images with datatype 'None'
  will be skipped.

  url_list: List object containing the urls addresses.
  batch_size: Amount of images.
  dir: Directory where the images should be saved.

  """
  # Download images and save them to directory
  # batch_size: Amount of images
  # dir: Directory

  cnt = 1
  for request in range(batch_size):
    #Print progress every 20th image
    if request == 20:
      print('Downloaded ',request,' images')

    image = request_image(url_list[request])
    if image is None:
      continue
    else:
      print('Downloaded image from: ',url_list[request])
      save_path = target_dir + 'img' + str(cnt) + '.jpg'
      cv2.imwrite(save_path,image)
      print('Saved image to: ', save_path)
      cnt = cnt + 1


hazelnut_id = 'n07772788'
walnut_id = 'n07771212'
peanut_id = 'n11748811'

batch_size = 834
target_dir = '/content/gdrive/My Drive/ImageNetImages/'

url_list = create_url_list(hazelnut_id)
download_image_batch(url_list, batch_size, target_dir)
