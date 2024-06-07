import os
from typing import List
import easyocr
import argparse

reader = easyocr.Reader(['en'], gpu=False)

def ocr_scan(image_path: str) -> str:
    """Running ocr over the image"""
    result = reader.readtext(str(image_path))
    recognized_text = "".join(elem[1] for elem in result)
    return recognized_text

def search_images(directory: str, keyword: str) -> List[str]:
    """"Looping over images inside a folder and running the OCR on them"""
    matching_images = []
    image_exts = (".png", ".jpg", ".jpeg")
    for root, dir, files in os.walk(directory):
        for file in files:
            if file.endswith(image_exts):
                image_path = os.path.join(root, file)
                recognized_text = ocr_scan(image_path)
                if keyword.lower() in recognized_text.lower():
                    matching_images.append(image_path)
    return matching_images

def main():
    """" Defines a cli tool that allows for ocr search for a keyword over images in a folder or single image"""
    parser = argparse.ArgumentParser(description=" OCR search for a keyword over images in a folder or single image")
    parser.add_argument('-d', "--directory", type=str, help="Directory of images to scan")
    parser.add_argument('-i',"--image", type=str, help="Path to single image to scan")
    parser.add_argument('-kw', "--keyword", type=str, help="Keyword to search for")
    args = parser.parse_args()

    if args.directory:
        matching_images = search_images(args.directory, args.keyword)
        print("Images that contain the keyword")
        for image_path in matching_images:
            print(image_path)
    elif args.image:
        recognized_text = ocr_scan(args.image)
        if args.keyword.lower() in recognized_text.lower():
            print("Keyword was detected in image")
        else:
            print(f"Keyword was not detected in image!")
            print(f"Detected text: {recognized_text}")
    else:
        print("Please provide a directory or image")

if __name__ == "__main__":
    main()
