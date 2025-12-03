from django.test import TestCase , Client
from store.models import Product
from django.urls import reverse
from store.models import Product

class StoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name="Test Product", price=100)

    def test_homepage_loads(self):
        response = self.client.get(reverse("store"))
        self.assertEqual(response.status_code, 200)
      
class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product",
            price=100,
            description="Just a test"
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100)






