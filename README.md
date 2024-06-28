# retrieveGoogleSlideContents
This project is a Flask-based web service that processes Google Slides presentations. It downloads slides as images, extracts speaker notes, resizes images to different aspect ratios, and packages everything into a ZIP file.

## Features
- Downloads slides as images
- Extracts speaker notes
- Resizes images to 4:3 and 16:9 aspect ratios
- Packages results into a ZIP file

## Requirements
- Docker
- Python 3.10
- Google Slides and Drive API

## Installation

### Option 1: Running Locally

1. **Clone the repository:**

2. **Set up Python environment:**
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up Google API credentials:**
    - Follow [Google's instructions](https://developers.google.com/slides/quickstart/python) to enable the Slides and Drive APIs.
    - Download your `credentials.json` file and place it in the `app` directory.

4. **Run the application:**
    ```bash
    python run.py
    ```

### Option 2: Running with Docker

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/PresentationGenerator.git
    cd PresentationGenerator
    ```

2. **Set up Google API credentials:**
    - Follow [Google's instructions](https://developers.google.com/slides/quickstart/python) to enable the Slides and Drive APIs.
    - Download your `credentials.json` file and place it in the `app` directory.

3. **Build the Docker image:**
    ```bash
    docker build -t flask-slides-app .
    ```

4. **Run the Docker container:**
    ```bash
    docker run -d -p 5000:5000 -e FLASK_ENV=development --name flask-slides-app flask-slides-app
    ```

## Usage

### Endpoint

`POST /process`

### Request Body

- `presentation_id`: The ID of the Google Slides presentation.

**Example:**

```bash
curl -X POST http://localhost:5000/process -H "Content-Type: application/json" -d "{\"presentation_id\": \"your_presentation_id_here\"}" --output slides_data.zip
