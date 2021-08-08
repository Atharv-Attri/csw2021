from PIL import Image
from pyzbar.pyzbar import decode


def decode_barcode(image_path: str) -> str:
    try:
        return decode(Image.open(image_path))[0].data.decode("utf-8")
    except IndexError:
        return "0"  # Return 0 if no barcode is found
