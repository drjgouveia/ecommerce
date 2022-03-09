import decimal
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from prods.models import Product
from sells.models import Sell, SellDetails


# @login_required(login_url="auth/login")
@csrf_exempt
def prods(request):
    """
    View responsible for providing all Products available on the database (when a request is made) or create a new Product object (when a POST request is performed)

    :param request: request made by the user
    :return: returns JSON with what method of request was made, if it was successful or not, and provide the data (GET request) or the Product object ID (POST request). 
    """
    try:
        if request.method == "GET":
            data = []
            for prod in Product.objects.all():
                data.append({
                    "id": prod.id,
                    "name": prod.name,
                    "price": prod.price,
                })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        elif request.method == "POST":
            prod_name = request.POST.get("name", "")
            prod_price = float(str(request.POST.get("price", 0.0)).replace(",", ".").strip())
            prod = Product(name=prod_name, price=prod_price)
            prod.save()

            return JsonResponse({"method": request.method, "prod_id": prod.id, "success": True}, status=200)

    except Product.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    return HttpResponse(status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def prod(request, prod_id):
    """
    View responsible for the proving of the data of a Product (when a GET request is performed), update an object with the data provided (when a PUT request if made) or delete an object (when a DELETE request is made).

    :param request: request made by the user
    :param prod_id: primary key of a Product
    :return: returns JSON with if the request was successful, method of request, and the data requested (GET request) or the Product object ID. 
    """
    if request.method == "GET":
        try:
            data = []
            if prod_id is None:
                for prod in Product.objects.all():
                    data.append({
                        "id": prod.id,
                        "name": prod.name,
                        "price": prod.price,
                    })
            else:
                prod = Product.objects.get(pk=prod_id)
                data.append({
                    "id": prod.id,
                    "name": prod.name,
                    "price": prod.price,
                })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    elif request.method == "PUT":
        try:
            body = QueryDict(request.body)
            prod = Product.objects.get(pk=prod_id)

            if "name" in body:
                prod.name = str(body.get("name"))

            if "price" in body:
                prod.price = float(body.get("price"))

            prod.save()

            return JsonResponse({"method": request.method, "prod_id": prod.id, "success": True}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    elif request.method == "DELETE":
        try:
            Product.objects.get(pk=prod_id).delete()
            return JsonResponse({"method": request.method, "prod_id": prod_id, "success": True}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    return HttpResponse(status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def sells(request):
    """
    View responsible for providing all Sells available on the database (when a request is made) or create a new Sell object (when a POST request is performed)
    
    :param request: request made by the user
    :return: returns JSON with what method of request was made, if it was successful or not, and provide the data (GET request) or the Sell object ID (POST request). 
    """
    try:
        if request.method == "GET":
            data = []
            for sell in Sell.objects.all():
                details = []
                for detail in sell.sell_details.all():
                    details.append({
                        "id": detail.id,
                        "total": detail.total,
                        "prod_id": detail.product.id,
                        "prod_price": detail.product.price,
                        "prod_name": detail.product.name,
                        "qty": detail.quantity,
                    })

                data.append({
                    "id": sell.id,
                    "total": sell.total,
                    "sells_details": details
                })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        elif request.method == "POST":
            sell = Sell()
            sell.save()
            total = 0.0
            sell.sell_details.clear()
            for sells_details_id in str(request.POST.get("sells_details", "")).split(","):
                if sells_details_id.isdigit():
                    detail = SellDetails.objects.get(pk=int(sells_details_id))
                    total += total + (float(detail.product.price) * float(detail.quantity))
                    sell.sell_details.add(detail)

            sell.total = total
            sell.save()

            return JsonResponse({"method": request.method, "sell_id": sell.id, "success": True}, status=200)

        else:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    except Sell.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def sell(request, sell_id):
    """
    View responsible for the proving of the data of a sell (when a GET request is performed), update an object with the data provided (when a PUT request if made) or delete an object (when a DELETE request is made).

    :param request: request made by the user
    :param sell_id: primary key of a sell
    :return: returns JSON with if the request was successful, method of request, and the data requested (GET request) or the Sell object ID. 
    """
    try:
        if request.method == "GET":
            data = []
            sell = Sell.objects.get(pk=sell_id)
            details = []
            for detail in sell.sell_details.all():
                details.append({
                    "id": detail.id,
                    "total": detail.total,
                    "prod_id": detail.product.id,
                    "prod_price": detail.product.price,
                    "prod_name": detail.product.name,
                    "qty": detail.quantity,
                })

            data.append({
                "id": sell.id,
                "total": sell.total,
                "sells_details": details
            })

            return JsonResponse({"method": request.method, "sell_id": sell.id, "data": data, "success": True}, status=200)

        elif request.method == "PUT":
            body = QueryDict(request.body)
            sell = Sell.objects.get(pk=sell_id)

            total = 0.0
            sell.sell_details.clear()
            for sells_details_id in str(body.get("sells_details", "")).split(","):
                detail = SellDetails.objects.get(pk=int(sells_details_id))
                total = total + (float(detail.product.price) * float(detail.quantity))
                sell.sell_details.add(detail)

            sell.total = total
            sell.save()
            return JsonResponse({"method": request.method, "success": True}, status=200)

        elif request.method == "DELETE":
            Sell.objects.get(pk=sell_id).delete()
            return JsonResponse({"method": request.method, "sell_id": sell_id, "success": True}, status=200)

        else:
            return HttpResponse(status=500)

    except (Sell.DoesNotExist, SellDetails.DoesNotExist):
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def sells_details(request):
    """
    View responsible for providing all Sells DEetails available on the database (when a request is made) or create a new Sell Detail object (when a POST request is performed)

    :param request: request made by the user
    :return: returns JSON with what method of request was made, if it was successful or not, and provide the data (GET request) or the Sell object ID (POST request). 
    """
    try:
        if request.method == "GET":
            data = []

            for detail in SellDetails.objects.all():
                data.append({
                    "id": detail.id,
                    "total": detail.total,
                    "prod_id": detail.product.id,
                    "prod_price": detail.product.price,
                    "prod_name": detail.product.name,
                    "qty": detail.quantity,
                })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        elif request.method == "POST":
            detail = SellDetails()

            detail.quantity = float(str(request.POST.get("qty", 0.0)).replace(",", ".").strip())
            if detail.quantity > 0:
                try:
                    detail.product = Product.objects.get(pk=int(request.POST.get("prod_id", "")))
                    detail.total = float(detail.quantity) * float(detail.product.price)
                except Product.DoesNotExist:
                    return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

                detail.save()
                return JsonResponse({"method": request.method, "sell_detail_id": detail.id, "success": True}, status=200)

            else:
                return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)
        else:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)
    except SellDetails.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def sells_detail(request, sell_details_id):
    """
    View responsible for the proving of the data of a sell detail (when a GET request is performed), update an object with the data provided (when a PUT request if made) or delete an object (when a DELETE request is made).

    :param request: request made by the user
    :param sell_details_id: primary key of a sell detail
    :return: returns JSON with if the request was successful, method of request, and the data requested (GET request) or the Sell Detail object ID. 
    """
    try:
        if request.method == "GET":
            data = []
            detail = SellDetails.objects.get(pk=sell_details_id)

            data.append({
                "id": detail.id,
                "total": detail.total,
                "prod_price": detail.product.price,
                "prod_name": detail.product.name,
                "qty": detail.quantity,
            })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        elif request.method == "PUT":
            detail = SellDetails.objects.get(pk=sell_details_id)
            body = QueryDict(request.body)

            if "total" in body:
                detail.total = float(body.get("total"))

            if "qty" in body:
                detail.quantity = float(body.get("qty"))

            detail.save()
            return JsonResponse({"method": request.method, "sell_details_id": sell_details_id, "success": True}, status=200)

        elif request.method == "DELETE":
            SellDetails.objects.get(pk=sell_details_id).delete()
            return JsonResponse({"method": request.method, "success": True}, status=200)

        else:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    except SellDetails.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)
