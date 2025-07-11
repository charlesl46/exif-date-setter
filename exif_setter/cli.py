from exif_setter.args import parse_args
from pathlib import Path
from exif_setter.utils import update_exif_date,find_and_convert_date,HasDataException,load_json,dump_json
from rich.progress import track


supported_extensions = {'.jpg', '.jpeg', '.tiff','.tif','.png', '.heic', '.heif', '.dng', '.webp'}



def cli():
    args = parse_args()
    progress_file = Path("progress.json")
    if progress_file.exists():
        progress = load_json(progress_file)
    else:
        progress = {"done" : []}
    
    path = Path(args.path)
    if not path.exists():
        raise Exception(f"Path {path} does not exist")
    
    def parse_folder(folder : Path):
        if folder.name in progress["done"]:
            print(f"bypassing {folder.name} as already done")
            return
        
        date = find_and_convert_date(folder.name)
        if not date:
            print(f"No date found for {folder.name}")
        else:
            files = [file for file in folder.iterdir() if file.is_file() and file.suffix.lower() in supported_extensions and not file.name.startswith(".")]
            if not files:
                print(f"No supported files found in directory {folder.name}")
                return

            #ok = input(f"date {date} was found for {folder.name}, proceed on {len(files)} files ? (y/n) ") == "y"
            print(f"date {date} was found for {folder.name} ({len(files)} files)")
            #if ok:
            for subobj in track(files,f"Setting metadata in {folder.name}"):
                if args.dry:
                    print(f"would update file {subobj}")
                else:
                    try:
                        update_exif_date(str(subobj),date=date,text=None,verbose=args.verbose)
                    except HasDataException as e:
                        print(e)
        
        progress["done"].append(folder.name)
        dump_json(progress,progress_file)


    if args.single:
        parse_folder(path)
    else:
        if path.is_dir():
            for obj in path.iterdir():
                if obj.is_dir():
                    parse_folder(obj)