from .models import Image, SMALL, LARGE
import os

PREFIX = 'xts'
SUFFIX = '.png'

directory = input('Enter directory string: ')
if input(f'Directory: {directory}.   Continue? y/n') == 'y':
    i = 0
    for name in os.listdir(directory):
        if name.startswith(PREFIX) and name.endswith(SUFFIX) and SMALL in name:
            img =Image(name=name)
            img.save()
            i += 1
            print(f'{name} saved.')
        else:
            print(f'{name} is not a valid name.  Ignored.')
    print(f'Done.   {i} image names saved in the database.')
else:
    print('Operation cancelled by user.')
