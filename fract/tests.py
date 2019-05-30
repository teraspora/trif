import django.test
from .models import Image
from django.contrib.auth.models import User

# Expected results
a_expected_params = {'image_id': '84077', 'size': '877x620', 'type': 'M', 'power': '6','func': '424',
    'alt_func': '359', 'mode': 'C', 'pretrans': '110', 'xparams': ['subc', 'sri'], 'full_flavour': 'Mandelbrot'}

b_expected_params = {'image_id': '42', 'size': '438x310', 'type': 'J', 'power': '1',
            'func': '3', 'alt_func': '62', 'mode': 'GM', 'pretrans': '70', 'xparams': [], 'full_flavour': 'Julia'}
b_expected_name_large = 'xtsJ1f3GM62-pre70-877x620x0.y0._42.png'
             

class TestImageFunctions(django.test.TestCase):

    @classmethod
    def setUpTestData(this):
        # Test Cases
        this.img_a = Image.objects.create(
            name='xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png',
            size='877x620')
        
        this.img_b = Image.objects.create(
            name='xtsJ1f3GM62-pre70-438x310x0.y0._42.png',
            size='438x310')

        this.users = [User.objects.create(username=f'user{n}', email=f'user{n}@test.org') for n in range(32)]

    def test_params(self):
        self.assertEqual(self.img_a.params(), a_expected_params)
        self.assertEqual(self.img_b.params(), b_expected_params)        

    def test_name_large(self):
        self.assertEqual(self.img_a.name_large(), self.img_a.name)
        self.assertEqual(self.img_b.name_large(), b_expected_name_large)
        
    def test_num_likes(self):
        
        # New images should have no likes
        self.assertEqual(self.img_a.num_likes(), 0)
        self.assertEqual(self.img_b.num_likes(), 0)
        
        # Let all users like img_a and let just every third one like img_b
        for user in self.users:
            user.profile.liked_images.add(self.img_a)
            if int(user.username[4:]) % 3 == 0:
                user.profile.liked_images.add(self.img_b)
        num_users = len(self.users)

        # Check the totals
        self.assertEqual(self.img_a.num_likes(), num_users)
        self.assertEqual(self.img_b.num_likes(), num_users // 3 + 1)
        
        # If a user 're-likes' an image it should not increase the count
        self.users[13].profile.liked_images.add(self.img_a)
        self.assertEqual(self.img_a.num_likes(), num_users)
        
        # If a user's profile is deleted, and the user has liked an image,
        # the value returned by num_likes() for that image should decrease by one
        self.users[7].profile.delete()
        self.users[8].profile.delete()
        self.users[12].profile.delete()        
        self.assertEqual(self.img_a.num_likes(), num_users - 3)
        

class TestIndexView(TestCase):

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
