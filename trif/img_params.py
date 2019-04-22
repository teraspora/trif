import re

def get_image_params(image_name, res):
  """
    Given a string containing a Teraspora image filename, and a string containing the resolution of the image,
    return an dict containing the image parameters.
      Example args:
        image_name = "xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png"
        res = "877x620";
      Output: {'type': 'M', 'power': '6', 'func': '424', 'alt_func': '359',
        'mode': 'C','pretrans': '110', 'params': ['subc', 'sri']} 
  """
  param_str = image_name.split(res, 1)[0][3:]  # trim off unnecessary parts
  p = re.compile(r'(?P<type>[JM])(?P<power>\d+)f(?P<func>\d+)(?P<mode>[A-Z]+)(?P<alt_func>\d+)(?P<pretrans>\-pre\d+)?(?P<params>[a-z\-]*)$')

  m = p.search(param_str)
  prex = m.group('pretrans')

  return {'type': m.group('type'), 
    'power': m.group('power'), 
    'func': m.group('func'), 
    'alt_func': m.group('alt_func'), 
    'mode': m.group('mode'), 
    'pretrans': '' if prex is None else prex[4:] ,
    'params': list(filter(None, m.group('params').split('-'))), 
  }

if __name__ == "__main__":
  im = "xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png"
  res = "877x620"
  print(f'Example input: {im}, {res}')
  print(f'Example output: {get_image_params(im, res)}')