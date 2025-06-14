from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from api.controllers import product_controller
import json


@csrf_exempt
def create_product(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        data = json.loads(request.body)
        product = product_controller.create_product(
            name=data.get('name'),
            specification=data.get('specification'),
            image_url=data.get('image_url'),
            category=data.get('category')
        )

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'specification': product.specification,
            'image_url': product.image_url,
            'category': product.category,
        }, status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')
    except Exception as e:
        return HttpResponseBadRequest(str(e))


def get_product(request, product_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        product = product_controller.get_product_by_id(product_id)

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'specification': product.specification,
            'image_url': product.image_url,
            'category': product.category,
        })

    except product_controller.Product.DoesNotExist:
        return HttpResponseNotFound('Produto não encontrado')


def get_all_products(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    products = product_controller.get_all_products()

    products_data = [{
        'id': p.id,
        'name': p.name,
        'specification': p.specification,
        'image_url': p.image_url,
        'category': p.category,
    } for p in products]

    return JsonResponse(products_data, safe=False)


@csrf_exempt
def update_product(request, product_id):
    if request.method not in ['PUT', 'PATCH']:
        return HttpResponseNotAllowed(['PUT', 'PATCH'])

    try:
        data = json.loads(request.body)

        product = product_controller.update_product(
            product_id,
            name=data.get('name'),
            specification=data.get('specification'),
            image_url=data.get('image_url'),
            category=data.get('category')
        )

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'specification': product.specification,
            'image_url': product.image_url,
            'category': product.category,
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')
    except product_controller.Product.DoesNotExist:
        return HttpResponseNotFound('Produto não encontrado')
    except Exception as e:
        return HttpResponseBadRequest(str(e))


@csrf_exempt
def delete_product(request, product_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    try:
        product_controller.delete_product(product_id)
        return JsonResponse({'status': 'success', 'message': 'Produto deletado com sucesso'})

    except product_controller.Product.DoesNotExist:
        return HttpResponseNotFound('Produto não encontrado')
