import os
from pyzbar.pyzbar import decode
from PIL import Image

def decode_barcode(image_path: str) -> str:
    return decode(Image.open(image_path))[0].data.decode('utf-8')