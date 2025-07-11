# exif-date-setter

A litle Python tool to set EXIF metadata date on image files based on date found in the folder title.

Works typically well with this type of folder architecture : 

- myfolder/2022-photos-family/*.jpg (will set metadata as 2022-01-01 in this case)
- myfolder/christmas-2025-12/*.jpg (will set metadata as 2025-12-01 in this case)
- myfolder/day_at_the_park_1978-05-08/*.jpg (will set metadata as 1978-05-08 in this case)

## Usage

```sh
exif-setter myfolder
```

You can also parse only one folder : 

```sh
exif-setter day_at_the_park_1978-05-08
```

And this will only set metadata in this folder. 