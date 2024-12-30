import requests
from PIL import Image, ImageDraw
from io import BytesIO
import re
import csv
import os
import sys
from datetime import datetime

def fetch_card_image(card_name, set_code=None, collector_number=None):
    base_url = 'https://api.scryfall.com/cards'
    if set_code and collector_number:
        url = f'{base_url}/{set_code.lower()}/{collector_number}'
    else:
        url = f'{base_url}/named?fuzzy={card_name}'
    
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()

        # Handle double-sided cards or tokens
        if 'layout' in data and data['layout'] in ['transform', 'double_faced_token']:
            print(f"Card is double-sided with layout: {data['layout']}")
            front_image_url = data['card_faces'][0]['image_uris']['large']
            back_image_url = data['card_faces'][1]['image_uris']['large']

            front_image = Image.open(BytesIO(requests.get(front_image_url).content))
            back_image = Image.open(BytesIO(requests.get(back_image_url).content))

            return front_image, back_image

        # Handle single-sided cards
        if 'image_uris' in data:
            image_url = data['image_uris']['large']
            image_response = requests.get(image_url)
            print(f"Image Fetch Status: {image_response.status_code}")
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content)), None

    return None, None

def fetch_card_image_by_url(card_url):
    try:
        parts = card_url.strip().split("/")
        set_code = parts[-3]
        collector_number = parts[-2]
        print(f"Extracted Set Code: {set_code}, Collector Number: {collector_number}")

        # Call the API with correct structure
        front_image, back_image = fetch_card_image(None, set_code, collector_number)

        if not front_image and not back_image:
            print(f"Card not found or has special layout: {card_url}")
        return front_image, back_image
    except IndexError:
        print(f"Malformed URL: {card_url}")
        return None, None

def get_output_file(sheet_num, file_name):
    if file_name == "input":
        today = datetime.now().strftime("%m-%d-%Y")
        output_dir = os.path.join(os.path.dirname(__file__), "Output", today)
        output_file = os.path.join(output_dir, f"card_sheet_{sheet_num}.png")
    else:
        output_dir = os.path.join(os.path.dirname(__file__), "Output", "Misc")
        output_file = os.path.join(output_dir, f"{file_name}_{sheet_num}.png")

    os.makedirs(output_dir, exist_ok=True)
    return output_file, output_dir

def create_card_sheet_from_file(file_name="input"):
    if file_name.endswith(".csv"):
        file_name = file_name[:-4]

    input_file = os.path.join(os.path.dirname(__file__), f"{file_name}.csv")
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, newline='') as csvfile:
        card_list = [row[0].strip() for row in csv.reader(csvfile)]

    cards_per_row = 3
    card_width = 750  # Correct width for 2.5 inches at 300 DPI
    card_height = 1050  # Correct height for 3.5 inches at 300 DPI
    cards_per_sheet = cards_per_row * 3  # 9 cards per sheet

    sheet_num = 1

    for sheet_start in range(0, len(card_list), cards_per_sheet):
        sheet_front = Image.new("RGB", (2550, 3300), "white")
        draw = ImageDraw.Draw(sheet_front)
        current_specs = card_list[sheet_start:sheet_start + cards_per_sheet]
        x_margin = (2550 - card_width * cards_per_row) // 2
        y_margin = (3300 - card_height * 3) // 2

        for idx, card_entry in enumerate(current_specs):
            print(f"Processing: {card_entry}")
            if card_entry.startswith("http"):
                card_image, back_image = fetch_card_image_by_url(card_entry)
            else:
                card_parts = card_entry.split(",")
                card_name = card_parts[0].strip()
                set_code = card_parts[1].strip() if len(card_parts) > 1 else None
                collector_number = card_parts[2].strip() if len(card_parts) > 2 else None
                card_image, back_image = fetch_card_image(card_name, set_code, collector_number)

            if card_image:
                x_offset = x_margin + (idx % cards_per_row) * card_width
                y_offset = y_margin + (idx // cards_per_row) * card_height
                sheet_front.paste(card_image.resize((card_width, card_height)), (x_offset, y_offset))
            else:
                print(f"Failed to fetch: {card_entry}")

        output_file_front = get_output_file(sheet_num, file_name)[0]
        sheet_front.save(output_file_front)
        print(f"Saved card sheet to {output_file_front}")
        sheet_num += 1

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_card_sheet_from_custom(batch_name):
    custom_dir = os.path.join(os.path.dirname(__file__), "customAssets", batch_name)
    if not os.path.exists(custom_dir):
        print(f"Custom directory {custom_dir} not found.")
        return

    # Sort files naturally by filename
    card_files = sorted(
        [os.path.join(custom_dir, f) for f in os.listdir(custom_dir) if f.endswith('.png')],
        key=natural_sort_key
    )
    
    if not card_files:
        print(f"No .png files found in {custom_dir}.")
        return

    cards_per_row = 3
    card_width = 750
    card_height = 1050
    cards_per_sheet = cards_per_row * 3

    sheet_num = 1
    for sheet_start in range(0, len(card_files), cards_per_sheet):
        sheet_front = Image.new("RGB", (2550, 3300), "white")
        x_margin = (2550 - card_width * cards_per_row) // 2
        y_margin = (3300 - card_height * 3) // 2

        current_files = card_files[sheet_start:sheet_start + cards_per_sheet]
        for idx, card_file in enumerate(current_files):
            card_image = Image.open(card_file).resize((card_width, card_height))
            x_offset = x_margin + (idx % cards_per_row) * card_width
            y_offset = y_margin + (idx // cards_per_row) * card_height
            sheet_front.paste(card_image, (x_offset, y_offset))

        output_file, _ = get_output_file(sheet_num, batch_name)
        sheet_front.save(output_file)
        print(f"Custom card sheet saved to {output_file}")
        sheet_num += 1

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "custom":
        batch_name = sys.argv[2]
        create_card_sheet_from_custom(batch_name)
    else:
        file_name = sys.argv[1] if len(sys.argv) > 1 else "input"
        create_card_sheet_from_file(file_name)
