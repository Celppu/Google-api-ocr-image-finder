# 📸 Image Scraper with OCR 📖

An automated tool to scrape images from Google using a custom search, perform OCR to detect text within those images, and filter/save images based on certain keyword criteria.

## Features 🌟

- 🖼️ Scrape images from Google's custom search.
- 📖 Perform OCR to read text from images.
- 🔍 Filter images based on provided keywords (with 70% similarity).
- 📂 Save filtered images without redundancy.
- 🔄 Handles retries and exceptions gracefully.

## Prerequisites 📋

- Python 3.10 or above
- Google API Key and Custom Search Engine ID for accessing Google's custom search.

## Setup & Installation 🛠️

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required libraries:
   ```sh
   pip install requests Pillow easyocr python-dotenv imagehash
   ```

3. Create a `.env` file in the root directory with the following structure:
   ```sh
   API_KEY=your_google_api_key
   CSE_ID=your_custom_search_engine_id
   SEARCH_TERM=your_search_term
   KEYWORD=your_filtering_keyword
   PAGE_NUM=start_page_number
   ```

4. Run the script:
   ```sh
   python <script_name>.py
   ```

## Usage 🚀

- After setting up, when you run the script, it will scrape images based on the `SEARCH_TERM` provided in the `.env` file.
- It will then perform OCR on these images and filter out the ones which contain the `KEYWORD` or similar keywords.
- The filtered images are saved in `./filteredImages/` directory.
- All downloaded images are saved in `./imgs/` directory for reference.

## Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License 📜
todo