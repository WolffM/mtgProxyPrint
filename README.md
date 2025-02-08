# Card Sheet Generator for Magic: The Gathering

This Python script uses the [Scryfall API](https://scryfall.com/docs/api) to fetch images for Magic: The Gathering cards and compile them into printable card sheets. It supports both single-sided and multi-faced (double-sided) cards and can generate sheets either from a CSV file input or from a custom folder containing card image assets.

## Features

- **Scryfall API Integration:**  
  Fetches card images using set code, collector number, and/or card name. Implements multiple fallback methods (direct fetch, name-based search, collector-based search) in case some data is missing.

- **Multi-Faced Card Support:**  
  Detects double-sided or multi-faced layouts and fetches both front and back images when available.

- **Card Sheet Creation:**  
  Arranges individual card images into a composite sheet (grid layout) with 3 cards per row and 3 rows per sheet (9 cards per sheet). Automatically calculates margins for centering on a standard 2550x3300 (8.5" x 11" at 300 DPI) canvas.

- **Input Options:**  
  - **CSV Input:** Reads card entries from a CSV file (default: `input.csv`) with each line containing either a direct Scryfall URL or comma-separated values (`card_name, set_code, collector_number`).
  - **Custom Assets:** Generates sheets from pre-downloaded card images placed in a custom directory structure.

- **Output Management:**  
  Saves output sheets into organized folders by date or batch name.

## Requirements

- Python 3.6 or higher
- [Requests](https://pypi.org/project/requests/)
- [Pillow](https://pypi.org/project/Pillow/)

Install the required packages using pip:

```bash
pip install requests pillow
```

## Usage

### 1. Creating Card Sheets from a CSV File

#### Prepare the CSV File

- Create a CSV file (e.g., `input.csv`) in the same directory as the script.
- Each line in the CSV can be in one of the following formats:
  - **Direct URL:**  
    A Scryfall URL (e.g., `https://scryfall.com/card/abc/123/...`).
  - **Comma-Separated Values:**  
    `card_name, set_code, collector_number`  
    Example:  
    ```
    Lightning Bolt, M10, 150
    ```

#### Run the Script

- To use the CSV input (default file name is `input.csv`), run:

```bash
python <script_name>.py input
```

- If no filename is provided, the script defaults to using `input.csv`.

The script will generate card sheets and save them in an output folder. For example, front sheets will be saved under a directory like `Output/<current_date>/card_sheet_1.png`, and if back images are present, they will be saved similarly.

### 2. Creating Card Sheets from Custom Assets

If you have a batch of pre-downloaded card images (PNG files):

1. **Organize Your Files:**

   - Place your PNG files into a folder structured as:  
     `customAssets/<batch_name>/`
   - The script will naturally sort the files so that they appear in order on the sheet.

2. **Run the Script in Custom Mode:**

```bash
python <script_name>.py custom <batch_name>
```

   Replace `<batch_name>` with the name of your custom batch folder.

The generated sheets will be saved in an output directory like `Output/Misc/<batch_name>_<sheet_number>.png`.

## How It Works

1. **Fetching Card Images:**

   - **Direct Fetch:**  
     If a valid `set_code` and `collector_number` are provided, the script constructs a direct URL to fetch the card data.
   
   - **Fallback Methods:**  
     If the direct fetch fails or required image data is missing, the script falls back to a name-based search or a collector number-based search.
   
   - **Multi-Faced Cards:**  
     For cards with layouts like `transform`, `modal_dfc`, `flip`, etc., the script checks for `card_faces` to retrieve front and back images.

2. **Creating Card Sheets:**

   - **Layout Details:**  
     Each sheet is created on a canvas of 2550x3300 pixels (8.5" x 11" at 300 DPI).
   - **Image Resizing:**  
     Card images are resized to 750x1050 pixels.
   - **Grid Arrangement:**  
     Cards are arranged in a grid of 3 columns and 3 rows per sheet.
   - **Back Image Handling:**  
     If cards have back images, the script creates a separate sheet for them, ensuring the backs are mirrored horizontally to align correctly with the front sheet.

3. **Output Files:**

   - **CSV Mode:**  
     Sheets are saved under a date-based directory (e.g., `Output/04-15-2025/`).
   - **Custom Mode:**  
     Sheets are saved under `Output/Misc/` with filenames incorporating the batch name.

## Troubleshooting

- **Card Data Not Found:**  
  Ensure that the card details (name, set code, collector number) are correct and that the Scryfall API is accessible.

- **Input File Issues:**  
  Verify that the CSV file exists in the same directory as the script and is named correctly (e.g., `input.csv`).

- **Custom Directory Not Found:**  
  Confirm that your custom assets are placed in the correct folder: `customAssets/<batch_name>/`.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **Scryfall API:** For providing comprehensive card data.  
- **Pillow:** For powerful image processing capabilities.  
- **Requests:** For simplifying HTTP requests in Python.
