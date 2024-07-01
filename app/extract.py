import json
import requests
import os
from PIL import Image
from app.auth import get_service
import logging

def download_image(url, filename):
    logging.debug(f"Downloading image from {url} to {filename}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        logging.debug(f"Downloaded image {filename}")
    else:
        logging.error(f"Failed to download image from {url}")

def add_black_bars(image_path, output_folder, aspect_ratio):
    logging.debug(f"Adding black bars to image {image_path} to aspect ratio {aspect_ratio}")
    img = Image.open(image_path)
    width, height = img.size
    
    if aspect_ratio == '4:3':
        target_width = max(width, int(height * 4 / 3))
        target_height = max(height, int(width * 3 / 4))
    elif aspect_ratio == '16:9':
        target_width = max(width, int(height * 16 / 9))
        target_height = max(height, int(width * 9 / 16))
    else:
        raise ValueError("Unsupported aspect ratio")

    new_img = Image.new('RGB', (target_width, target_height), (0, 0, 0))
    offset = ((target_width - width) // 2, (target_height - height) // 2)
    new_img.paste(img, offset)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    new_img.save(output_path)
    logging.debug(f"Saved image with black bars {output_path}")
    return output_path

def save_slides_as_images(presentation_id, slides, service, output_folder='Slides'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    image_filenames = []
    for i, slide in enumerate(slides):
        slide_id = slide.get('objectId')
        logging.debug(f"Processing slide {slide_id}")
        thumbnail = service.presentations().pages().getThumbnail(
            presentationId=presentation_id,
            pageObjectId=slide_id
        ).execute()
        image_url = thumbnail.get('contentUrl')
        filename = os.path.join(output_folder, f"slide_{i + 1}.png")
        download_image(image_url, filename)
        image_filenames.append(filename)
    return image_filenames

def extract_speaker_notes(slides):
    notes = {}
    for i, slide in enumerate(slides):
        slide_notes = slide.get('slideProperties', {}).get('notesPage', {}).get('pageElements', [])
        note_text = ''
        for element in slide_notes:
            if 'shape' in element and 'text' in element['shape']:
                text_elements = element['shape']['text']['textElements']
                note_text += ''.join([te['textRun']['content'] for te in text_elements if 'textRun' in te])
        notes[f"slide_{i + 1}"] = note_text
    return notes

def process_presentation(presentation_id):
    try:
        logging.debug(f"Starting process for presentation ID: {presentation_id}")
        service, drive_service = get_service()
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides')
        logging.debug(f"Retrieved presentation with {len(slides)} slides")

        base_output_folder = os.path.join(os.getcwd(), 'Slides')
        if not os.path.exists(base_output_folder):
            os.makedirs(base_output_folder)

        image_filenames = save_slides_as_images(presentation_id, slides, service, output_folder=base_output_folder)

        speaker_notes = extract_speaker_notes(slides)

        # Create separate folders for 4:3 and 16:9 images
        output_folder_4_3 = os.path.join(base_output_folder, '4_3')
        output_folder_16_9 = os.path.join(base_output_folder, '16_9')
        if not os.path.exists(output_folder_4_3):
            os.makedirs(output_folder_4_3)
        if not os.path.exists(output_folder_16_9):
            os.makedirs(output_folder_16_9)

        slide_data = {}
        for i, filename in enumerate(image_filenames):
            slide_number = f"slide_{i + 1}"
            slide_data[slide_number] = {
                "original": filename,
                "notes": speaker_notes.get(slide_number, ""),
                "4:3": add_black_bars(filename, output_folder_4_3, '4:3'),
                "16:9": add_black_bars(filename, output_folder_16_9, '16:9')
            }

        json_file = os.path.join(base_output_folder, 'slides_data.json')
        with open(json_file, 'w') as f:
            json.dump(slide_data, f, indent=4)
        logging.debug(f"Saved JSON data to {json_file}")

        return base_output_folder, json_file

    except Exception as e:
        logging.exception("An error occurred in process_presentation")
        raise Exception(f"An error occurred: {e}")
