# fract/add_images.py - run manually to add the details from a folder of images to the database

# Run in the shell: input the directory of SMALL images you want to add to the database.
# Don't forget to add the actual images, and their LARGE counterparts, to the S3 bucket.
# This process is a candidate for further automation...

# Example:

# 02:25: fractrig $ python3 manage.py shell
# In DEVELOPMENT context
# Python 3.7.1 (default, Oct 22 2018, 11:21:55) 
# [GCC 8.2.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# (InteractiveConsole)
# >>> from fract import add_images
# Enter directory string: fract/test
# Directory: fract/test.   Continue? y/ny
# xtsJ1f353C401-pre60-sri-438x310x-3.036256350301346y-1.4303025782411303_5841.png saved.
# Done.   1 image names saved in the database.

from .models import Image, SMALL, LARGE
import os

PREFIX = 'xts'
SUFFIX = '.png'

directory = input('Enter directory string: ')
if input(f'Directory: {directory}.   Continue? y/n') == 'y':
    i = 0
    for name in os.listdir(directory):
        if name.startswith(PREFIX) and name.endswith(SUFFIX) and SMALL in name:
            img = Image(name=name)
            img.save()
            i += 1
            print(f'{name} saved.')
        else:
            print(f'{name} is not a valid name.  Ignored.')
    print(f'Done.   {i} image names saved in the database.')
else:
    print('Operation cancelled by user.')
