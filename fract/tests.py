import django.test
from .models import Image

# Expected results
a_expected_params = {'image_id': '84077', 'size': '877x620', 'type': 'M', 'power': '6','func': '424',
    'alt_func': '359', 'mode': 'C', 'pretrans': '110', 'xparams': ['subc', 'sri'], 'full_flavour': 'Mandelbrot'}

b_expected_params = {'image_id': '42', 'size': '438x310', 'type': 'J', 'power': '1',
            'func': '3', 'alt_func': '62', 'mode': 'GM', 'pretrans': '70', 'xparams': [], 'full_flavour': 'Julia'}
              

class TestImageFunctions(django.test.TestCase):

    @classmethod
    def setUpTestData(cls):
        # Test Cases
        cls.img_a = Image.objects.create(
            name='xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png',
            size='877x620')
        
        cls.img_b = Image.objects.create(
            name='xtsJ1f3GM62-pre70-438x310xx0.y0._42.png',
            size='438x310')

    def test_params(self):
        self.assertEqual(self.img_a.params(), a_expected_params)
        self.assertEqual(self.img_b.params(), b_expected_params)        


if __name__ == '__main__':
    django.test.main()

