import os


def add_file(fileitem):
    try:
        filename = os.path.basename(fileitem.filename)
        filename = 'static/photo/'+filename
        open(filename, 'wb').write(fileitem.file.read())
    except:
        filename = "aaaaaaaaaaaaaNULL"
    finally:
        return filename[13:len(filename)]


