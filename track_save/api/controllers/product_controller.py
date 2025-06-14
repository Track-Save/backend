from api.entities.product import Product
from django.core.exceptions import ObjectDoesNotExist


def create_product(name, specification, image_url, category):
    if not all([name, specification, image_url, category]):
        raise ValueError("Todos os campos são obrigatórios.")

    product = Product.objects.create(
        name=name,
        specification=specification,
        image_url=image_url,
        category=category
    )
    return product


def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)


def get_all_products():
    return Product.objects.all()


def update_product(product_id, name=None, specification=None, image_url=None, category=None):
    product = Product.objects.get(id=product_id)

    if name:
        product.name = name
    if specification:
        product.specification = specification
    if image_url:
        product.image_url = image_url
    if category is not None:
        product.category = category

    product.save()
    return product


def delete_product(product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
