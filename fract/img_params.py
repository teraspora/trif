import re

def get_image_params(image_name, res):
  """
    Given a string containing a Teraspora image filename, and a string containing the resolution of the image,
    return a dict containing the image parameters.
      Example args:
        image_name = "xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png"
        res = "877x620";
      Output: {'image_id': '4266', 'size': '877x620', 'type': 'M', 'power': '6', 'func': '424', 'alt_func': '359',
        'mode': 'C','pretrans': '110', 'xparams': ['subc', 'sri']} 
  """
  temp = image_name.split(res, 1)
  param_str = temp[0][3:]  # trim off 'xts' from the head and coords, id and suffix from the tail
  image_id = temp[1].split('_', 1)[1][:-4]
  
  p = re.compile(r'(?P<type>[JM])(?P<power>\d+)f(?P<func>\d+)(?P<mode>[A-Z]+)(?P<alt_func>\d+)(?P<pretrans>\-pre\d+)?(?P<xparams>[a-z\-]*)$')
  m = p.search(param_str)
  prex = m.group('pretrans')

  return { 
    'image_id': image_id,
    'size': res, 
    'type': m.group('type'), 
    'power': m.group('power'), 
    'func': m.group('func'), 
    'alt_func': m.group('alt_func'), 
    'mode': m.group('mode'), 
    'pretrans': '' if prex is None else prex[4:] ,
    'xparams': list(filter(None, m.group('xparams').split('-'))), 
  }

if __name__ == "__main__":
  im = "xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png"
  res = "877x620"
  print(f'Example input: {im}, {res}')
  print(f'Example output: {get_image_params(im, res)}')