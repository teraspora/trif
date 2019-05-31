import django.test
from .models import Image
# from .views import NUM_IMAGES_PER_PAGE
from django.contrib.auth.models import User
from django.test import Client

# Expected results
a_expected_params = {'image_id': '84077', 'size': '877x620', 'type': 'M', 'power': '6','func': '424',
    'alt_func': '359', 'mode': 'C', 'pretrans': '110', 'xparams': ['subc', 'sri'], 'full_flavour': 'Mandelbrot'}

b_expected_params = {'image_id': '42', 'size': '438x310', 'type': 'J', 'power': '1',
            'func': '3', 'alt_func': '62', 'mode': 'GM', 'pretrans': '70', 'xparams': [], 'full_flavour': 'Julia'}
b_expected_name_large = 'xtsJ1f3GM62-pre70-877x620x0.y0._42.png'

NUM_IMAGES_PER_PAGE = 18    

class TestImageFunctions(django.test.TestCase):

    @classmethod
    def setUpTestData(cls):
        # Test Cases
        cls.img_a = Image.objects.create(
            name='xtsM6f424C359-pre110-subc-sri-877x620x3.5741464342585774y3.0788630954174376_84077.png',
            size='877x620')
        
        cls.img_b = Image.objects.create(
            name='xtsJ1f3GM62-pre70-438x310x0.y0._42.png',
            size='438x310')

        cls.users = [User.objects.create(username=f'user{n}', email=f'user{n}@test.org') for n in range(32)]

    def test_params(self):
        self.assertEqual(self.img_a.params(), a_expected_params, msg="*** Got wrong params for image a! ***")
        self.assertEqual(self.img_b.params(), b_expected_params, msg="*** Got wrong params for image b! ***")        

    def test_name_large(self):
        self.assertEqual(self.img_a.name_large(), self.img_a.name, msg="*** Got wrong name_large for image a! ***")
        self.assertEqual(self.img_b.name_large(), b_expected_name_large, msg="*** Got wrong name_large for image b! ***")
        
    def test_num_likes(self):
        
        # New images should have no likes
        self.assertEqual(self.img_a.num_likes(), 0, msg="*** Got non-zero num_likes for image a! ***")
        self.assertEqual(self.img_b.num_likes(), 0, msg="*** Got non-zero num_likes for image b! ***")
        
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
        

class TestListViews(django.test.TransactionTestCase):

    def test_index_view(self):
        response = self.client.get('/')
        # Test Http status code is 200 OK
        self.assertEqual(response.status_code, 200, msg="*** Didn't get 200 OK from home page! ***")
        # Test queryset has fract.views.NUM_IMAGES_PER_PAGE items
        self.assertNumQueries(NUM_IMAGES_PER_PAGE, msg="*** Wrong number of images on the page! ***")

    def test_likes_view(self):
        user = User.objects.create_user('uuu', None, 'tested123')
        user.save()
        self.client.login(username='uuu', password='tested123')
        self.assertTrue(user.is_authenticated, f'*** User {user} is not authenticated! ***')
        response = self.client.get('/likes/')
        # Test Http status code is 200 OK
        self.assertEqual(response.status_code, 200, msg="*** Didn't get 200 OK from likes page! ***")
        # Queryset should be empty as uuu currently likes no images
        self.assertQuerysetEqual(response.context['image_list'], [], 
            msg="*** Didn't get empty set when no images liked! ***")
           
        # Define 10 images and make user like all of them
        images = []
        for n in range(10):
            img = Image.objects.create(
                name=f'xtsJ16f32GM{n}-pre70-438x310x-0.1y0.1_420.png',
                size='438x310')
            images.append(img)
            user.profile.liked_images.add(img)
            
        response = self.client.get('/likes/')
        # Test if they show up correctly
        self.assertEqual(list(response.context['image_list']), images, msg="*** Liked images don't match! ***")
