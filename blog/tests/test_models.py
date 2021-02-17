from django.test import TestCase
from ..models import Category
from django.core.exceptions import ValidationError

class CategoryModelTestCase(TestCase):

    def test_category_fullname_depth_one(self):
        category_one = Category.objects.create(name='Top Level')
        self.assertEqual(str(category_one), category_one.full_name())

    def test_category_fullname_depth_two(self):
        category_one = Category.objects.create(name='Top Level')
        category_two = Category.objects.create(name='Middle Level', parent=category_one)
        
        self.assertEqual([category_one.name, category_two.name], category_two.full_name().split('/'))

