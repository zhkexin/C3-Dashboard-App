from django.conf import settings
from django.core.files.storage import FileSystemStorage

def handle_uploaded_files(files):
    file_paths = []
    fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/claim_images')

    for file in files:
        filename = fs.save(file.name, file)
        file_paths.append(fs.url(filename))

    return file_paths

