import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .models import ProductCategory, Product

@pytest.mark.django_db
class TestProductManagement:
    def setup_method(self):
        self.client = APIClient()
        self.category = ProductCategory.objects.create(name="Chicken Parts")
        self.product_url = '/api/products/'

    def test_list_products(self):
        Product.objects.create(
            category=self.category,
            name="Wings",
            price_per_kg=1500
        )
        response = self.client.get(self.product_url)
        assert response.status_code == status.HTTP_200_OK
        # Check for results key if paginated
        if 'results' in response.data:
            assert len(response.data['results']) == 1
        else:
            assert len(response.data) == 1

    def test_product_category_filter(self):
        Product.objects.create(
            category=self.category,
            name="Wings",
            price_per_kg=1500
        )
        cat2 = ProductCategory.objects.create(name="Whole Chicken")
        Product.objects.create(
            category=cat2,
            name="Large Whole",
            price_per_kg=3000
        )
        response = self.client.get(f"{self.product_url}?category={self.category.id}")
        assert response.status_code == status.HTTP_200_OK
        
        results = response.data['results'] if 'results' in response.data else response.data
        assert len(results) == 1
        assert results[0]['name'] == "Wings"
