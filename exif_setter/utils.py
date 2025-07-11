import re
import datetime
import piexif
from piexif import ExifIFD, ImageIFD
from PIL import Image
import json

class HasDataException(Exception):
    pass

def dump_json(dico : dict,filepath):
    with open(filepath,"w") as file:
        json.dump(dico,file,indent=4)

def load_json(filepath):
    with open(filepath,"r") as file:
        dico = json.load(file)
    return dico

def find_and_convert_date(text : str):
    clean_text = text.replace('_', '-')

    # YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', clean_text)
    if match:
        year, month, day = map(int, match.groups())
        return datetime.datetime(year, month, day)

    # YYYY-MM
    match = re.search(r'(\d{4})-(\d{1,2})', clean_text)
    if match:
        year, month = map(int, match.groups())
        return datetime.datetime(year, month, 1)

    # YYYY
    match = re.search(r'(\d{4})', clean_text)
    if match:
        year = int(match.group(1))
        return datetime.datetime(year, 1, 1)

    return None

def update_exif_date(filepath, date = None, text = None, verbose : bool = False):
    if date is None:
        date = find_and_convert_date(text)
    
    if date is None:
        return

    #print(f"loading {filepath}")
    try:
        exif_dict = piexif.load(filepath)
    except Exception as e:
        print(e)
        return

    if "0th" not in exif_dict:
        exif_dict["0th"] = {}
    if "Exif" not in exif_dict:
        exif_dict["Exif"] = {}

    date_str = date.strftime('%Y:%m:%d %H:%M:%S')
    encoded_date = date_str.encode("ascii")

    #if exif_dict["0th"].get(ImageIFD.DateTime) is not None or exif_dict["Exif"].get(ExifIFD.DateTimeOriginal) is not None:
    #    raise HasDataException(f"{filepath=} has already datetime {exif_dict['0th'].get(ImageIFD.DateTime)} or {exif_dict['Exif'].get(ExifIFD.DateTimeOriginal)}")
    
    if exif_dict["0th"].get(ImageIFD.DateTime) != encoded_date:
        exif_dict["0th"][ImageIFD.DateTime] = encoded_date
    if exif_dict["Exif"].get(ExifIFD.DateTimeOriginal) != encoded_date:
        exif_dict["Exif"][ExifIFD.DateTimeOriginal] = encoded_date
    
    # exif_dict["Exif"][ExifIFD.DateTimeDigitized] = date_str.encode("ascii")  # optionnel

    try:
        exif_bytes = piexif.dump(exif_dict)
        if verbose:
            print(f"setting {date=} for {filepath=}")

        image = Image.open(filepath)
        image.save(filepath, exif=exif_bytes)
    except Exception as e:
        print(f"error {e} on {filepath}")