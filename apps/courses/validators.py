
from django.core.exceptions import ValidationError
import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


def validate_is_audio(file):

    try:
        audio = MP3(file)

        if not audio :
            raise TypeError()

        first_file_check=True
        
    except Exception as e:
        first_file_check=False
    
    if not first_file_check:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp3']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')



def validate_is_video(file):

    try:
        audio = MP4(file)

        if not audio :
            raise TypeError()

        first_file_check=True
        
    except Exception as e:
        first_file_check=False
    
    if not first_file_check:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.mp4']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')

