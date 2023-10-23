import requests
from PIL import Image
import easyocr
import io
import urllib.parse
import time

# Use dotenv to read .env vars
from dotenv import dotenv_values

# Constants
config = dotenv_values(".env")

API_KEY = config['API_KEY']
CSE_ID = config['CSE_ID']
SEARCH_TERM = config['SEARCH_TERM']
KEYWORD = config['KEYWORD']
PAGE_NUM = config['PAGE_NUM'] # start result number

Keywordlist = KEYWORD.split()

NUM_IMAGES = 10

# 1. Fetch Image URLs using Google's Custom Search API
def fetch_image_urls(query, num_images=10):
    encoded_query = urllib.parse.quote(query)
    #url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={API_KEY}&cx={CSE_ID}&searchType=image&num={num_images}"
    url = f"https://customsearch.googleapis.com/customsearch/v1?cx={CSE_ID}&q={encoded_query}&searchType=image&key={API_KEY}&start={PAGE_NUM}&num={num_images}"
    response = requests.get(url).json()
    return [item['link'] for item in response['items']]

# 2. Download Images
def download_image(url):

    # loop try catch 3 times plus 0.1 sec sleep.

    for i in range(3):
        try:
            # Check if URL starts with http or https
            if not url.startswith(('http://', 'https://')):
                print(f"Skipping unsupported URL: {url}")
                return None

            # Get the image content
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Convert content to Image object
            image = Image.open(io.BytesIO(response.content))
            return image
        except:
            print("Error downloading image, retrying")
            time.sleep(0.1)
            continue

    return None
    #response = requests.get(url)

    #return Image.open(io.BytesIO(response.content))

# 3. OCR the Image using easyocr
def ocr_image(image):
    result = reader.readtext(image)
    return ' '.join([detection[1] for detection in result])

# Create an EasyOCR reader instance
reader = easyocr.Reader(['en'])

# Main Logic
#image_urls = fetch_image_urls(SEARCH_TERM, NUM_IMAGES)

# Loop PAGE_NUM s 0, 11, 21 etc to get more images. 10 increments in total
image_urls = []
for i in range(10):
    image_urls += fetch_image_urls(SEARCH_TERM, NUM_IMAGES)
    PAGE_NUM = int(PAGE_NUM) + 10
    print(f"PAGE_NUM: {PAGE_NUM}")

filtered_images = []
all_images = []

from difflib import SequenceMatcher

def is_similar(a, b):
    return SequenceMatcher(None, a, b).ratio() >= 0.7


for url in image_urls:
    image = download_image(url)
    if image is None:
        continue
    
    #skip if image is too small. aka 100 pixels
    if image.width < 100 or image.height < 100:
        continue

    text = ""
    # try catch ocr incase image is not readable
    try:
        text = ocr_image(image)
    except:
        print("Error reading image, skipping")
        continue
    #text = ocr_image(image)
    print(text)

    # check keywordlist if text contains any of the keywords.
    # lowercase and split text to words
    text_words = text.split()
    # check if any of the words in text is in keywordlist
    for word in text_words:
        if any(is_similar(word, keyword) for keyword in Keywordlist):
            filtered_images.append(image)
            #print green
            print(f"\033[92m{word} found in keywords\033[0m")
            break
        else:
            print(f"{word} not found in keywords")


    # for some reason this skipped all images.
    #for keyword in Keywordlist:
    #    if keyword in text:
    #        filtered_images.append(image)
    #        print("keyword found")
    #        break
    
    #if KEYWORD in text:
    #    filtered_images.append(image)
    all_images.append(image)

# Now, filtered_images contains all images with the keyword
# You can save them or process them further
import os

# Ensure the directory exists
if not os.path.exists("./imgs/"):
    os.makedirs("./imgs/")
if not os.path.exists("./filteredImages/"):
    os.makedirs("./filteredImages/")


import imagehash

def compute_hash(img):
    """Compute the hash of an image."""
    return imagehash.average_hash(img)

def find_max_index(folder_path):
    """Find the current maximum index from filenames in the folder."""
    max_index = -1
    for filename in os.listdir(folder_path):
        if filename.startswith("filtered_image_"):
            index = int(filename.split('_')[2].split('.')[0])
            max_index = max(max_index, index)
    print(f"Max index found: {max_index}")
    return max_index

def image_exists_in_folder(img, folder_path):
    """Check if a similar image already exists in the folder."""
    new_img_hash = compute_hash(img)
    for filename in os.listdir(folder_path):
        existing_img = Image.open(os.path.join(folder_path, filename))
        existing_img_hash = compute_hash(existing_img)
        if new_img_hash - existing_img_hash < 5:  # You can adjust this threshold
            return True
    return False

# Main part of your code
folder_path = "./filteredImages"

# Find the maximum index in the folder
max_index = find_max_index(folder_path)

for img in filtered_images:
    if not image_exists_in_folder(img, folder_path):
        max_index += 1
        img.save(f"{folder_path}/filtered_image_{max_index}.jpg")

for idx, img in enumerate(all_images):
    img.save(f"./imgs/all_image_{idx}.jpg")
