import pytest
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from model_bakery import baker

from products.models import Product, Category


@pytest.mark.django_db
class TestProductViewSet:
    @pytest.fixture
    def multiple_products(self):
        products = []
        for _ in range(20):
            product = baker.make(Product)
            products.append(product)
        return products

    def test_list(self, api_client, multiple_products):
        response = api_client.get(reverse("products:product-list"))

        assert response.status_code == 200
        assert len(response.data) == 20

        for product in response.data:
            assert not "id" in product
            assert "name" in product
            assert "price" in product
            assert "uploaded_by" in product
            assert "bought_by" in product

    def test_cacheing_in_list(self, api_client, multiple_products):
        cache_key = "products_list"
        cache.delete(cache_key)

        response = api_client.get(reverse("products:product-list"))

        assert response.status_code == 200

        cached_response = cache.get(cache_key)

        assert cached_response is not None
        assert len(cached_response) == 20

    def test_retrieve(self, api_client, multiple_products):
        response = api_client.get(reverse("products:product-detail", kwargs={"pk": 5}))

        assert response.status_code == 200

        product = Product.objects.get(pk=5)

        assert response.data["name"] == product.name
        assert response.data["uploaded_by"] == product.uploaded_by.id
        assert response.data["category"] == product.category.id

    def test_create_unauthorized_user(self, api_client, test_user, test_category):
        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": "10.00",
                "category": test_category,
            },
        )

        assert response.status_code == 401

    def test_create_success(self, api_client, test_user, test_category):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )

        assert response.status_code == 201
        assert response.data["uploaded_by"] == test_user.id

    def test_delete_product_with_no_owner(
        self, api_client, test_user, test_category, another_test_user
    ):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )

        assert response.status_code == 201
        assert response.data["uploaded_by"] == test_user.id

        api_client.force_authenticate(another_test_user)

        delete_response = api_client.delete(
            reverse("products:product-detail", kwargs={"pk": 1})
        )

        assert delete_response.status_code == 403
        assert len(Product.objects.all()) == 1

    def test_delete_success(self, api_client, test_user, test_category):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )

        assert response.status_code == 201
        assert response.data["uploaded_by"] == test_user.id

        delete_response = api_client.delete(
            reverse("products:product-detail", kwargs={"pk": 1})
        )

        assert delete_response.status_code == 204

    @override_settings(
        REST_FRAMEWORK={
            "DEFAULT_THROTTLE_RATES": {
                "uploads": "5/minute",
                "receives": "5/minute",
            }
        }
    )
    def test_throttle(self, api_client, test_user, test_category):
        # TODO (why) when i run this test alone it passed but if a run all tests it will fail
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        for _ in range(5):
            response = api_client.post(
                reverse("products:product-list"),
                data={
                    "name": f"test product {_}",
                    "price": 10.00,
                    "category": test_category.id,
                },
            )
            assert response.status_code == 201

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )
        assert response.status_code == 429

        for _ in range(5):
            response = api_client.get(
                reverse("products:product-detail", kwargs={"pk": 1})
            )
            assert response.status_code == 200

        response = api_client.get(reverse("products:product-detail", kwargs={"pk": 1}))

        assert response.status_code == 429


@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list(self, api_client):
        response = api_client.get(reverse("products:category-list"))

        assert response.status_code == 200
        assert isinstance(response.data, list)
        for category in response.data:
            assert "id" in category
            assert "name" in category
            assert "description" in category

    def test_cacheing_in_list(self, api_client):
        cache_key = "categories_list"
        cache.delete(cache_key)

        response = api_client.get(reverse("products:category-list"))

        assert response.status_code == 200

        cached_response = cache.get(cache_key)

        assert cached_response is not None
        assert isinstance(response.data, list)
        for category in response.data:
            assert "id" in category
            assert "name" in category
            assert "description" in category

    def test_create_admin_user(self, api_client, test_user):
        test_user.is_active = True
        test_user.is_staff = True

        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:category-list"), data={"name": "test_category name"}
        )

        assert response.status_code == 201
        assert "id" in response.data
        assert response.data["name"] == "test_category name"
        assert response.data["description"] is None

        category_id = response.data["id"]
        assert Category.objects.filter(id=category_id).exists()

    def test_create_normal_user(self, api_client, test_user):
        test_user.is_active = True
        test_user.is_staff = False
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:category-list"), data={"name": "test_category name"}
        )

        assert response.status_code == 403

    def test_delete_admin_user(self, api_client, test_user, test_category):
        test_user.is_active = True
        test_user.is_staff = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.delete(
            reverse("products:category-detail", kwargs={"pk": test_category.id})
        )

        assert response.status_code == 204

    def test_delete_normal_user(self, api_client, test_user, test_category):
        test_user.is_active = True
        test_user.is_staff = False
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.delete(
            reverse("products:category-detail", kwargs={"pk": test_category.id})
        )

        assert response.status_code == 403
