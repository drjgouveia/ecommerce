import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from prods.models import Product
from sells.models import Sell, SellDetails


# @login_required(login_url="auth/login")
@csrf_exempt
def prods(request):
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
            prod_price = request.POST.get("price", 0.0)
            prod = Product(name=prod_name, price=prod_price)
            prod.save()

            return JsonResponse({"method": request.method, "prod_id": prod.id, "success": True}, status=200)

    except Product.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=500)

    return HttpResponse(status=500)


# @login_required(login_url="auth/login")
@csrf_exempt
def prod(request, prod_id):
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
            body = json.loads(request.body)
            prod = Product.objects.get(pk=prod_id)

            if "name" in body:
                prod.name = str(body["name"])

            if "price" in body:
                prod.price = float(body["price"])

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
    View responsible for providing all Sells available on the database (when a request is made) or create a new Sell object (when a POST request is performed),
    :param request: request made by the user
    :return: 
    """
    try:
        if request.method == "GET":
            data = []
            for sell in Sell.objects.all():
                details = []
                for detail in sell.sell_details:
                    details.append({
                        "id": detail.id,
                        "total": detail.total,
                        "sells_details": detail,
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
            body = json.loads(request.body)
            sell = Sell()
            sell.total = float(request.POST.get("total", 0.0))

            if "sells_details" in body:
                for sells_details_id in str(request.POST.get("sells_details", "")).split(","):
                    sell.sell_details.add(Sell.objects.get(pk=int(sells_details_id)))

            sell.save()

            return JsonResponse({"method": request.method, "sell_id": sell.id, "success": True}, status=200)

        else:
            return JsonResponse({"method": request.method, "data":[], "success": False}, status=200)

    except Sell.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)


# @login_required(login_url="auth/login")
@csrf_exempt
def sell(request, sell_id):
    """
    View responsible for the proving of the data of a sell (when a GET request is performed), update an object with the data provided (when a PUT request if made) or delete an object (when a DELETE request is made).

    :param request: request made by the user
    :param sell_id: primary key of a sell
    :return:
    """
    try:
        if request.method == "GET":
            data = []
            sell = Sell.objects.get(pk=sell_id)
            details = []
            for detail in sell.sell_details:
                details.append({
                    "id": detail.id,
                    "total": detail.total,
                    "sells_details": detail,
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
            body = json.loads(request.body)
            sell = Sell.objects.get(pk=sell_id)

            if "total" in body:
                prod.total = float(body["total"])

            if "sells_details" in body:
                for sells_details_id in str(body["sells_details"]).split(","):
                    if Sell.objects.get(pk=int(sells_details_id)) not in sell.sell_details.all():
                        sell.sell_details.add(Sell.objects.get(pk=int(sells_details_id)))

            sell.save()
            return JsonResponse({"method": request.method, "success": True}, status=200)

        elif request.method == "DELETE":
            Sell.objects.get(pk=sell_id).delete()
            return JsonResponse({"method": request.method, "prod_id": sell_id, "success": True}, status=200)

        else:
            return HttpResponse(status=500)

    except (Sell.DoesNotExist, SellDetails.DoesNotExist):
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)


# @login_required(login_url="auth/login")
@csrf_exempt
def sells_details(request):
    try:
        if request.method == "GET":
            data = []

            for detail in SellDetails.objects.all():
                data.append({
                    "id": detail.id,
                    "total": detail.total,
                    "sells_details": detail,
                    "prod_id": detail.product.id,
                    "prod_price": detail.product.price,
                    "prod_name": detail.product.name,
                    "qty": detail.quantity,
                })

            return JsonResponse({"method": request.method, "data": data, "success": True}, status=200)

        elif request.method == "POST":
            detail = SellDetails()

            detail.total = float(request.POST.get("total", 0.0))
            try:
                detail.product = Product.objects.get(pk=request.POST.get("prod_id", ""))
            except Product.DoesNotExist:
                return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)

            detail.save()
        else:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)
    except SellDetails.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)


# @login_required(login_url="auth/login")
@csrf_exempt
def sells_detail(request, sell_details_id):
    try:
        if request.method == "GET":
            data = []
            detail = SellDetails.objects.get(pk=sell_details_id)

            data.append({
                "id": detail.id,
                "total": detail.total,
                "sells_details": detail,
                "prod_price": detail.product.price,
                "prod_name": detail.product.name,
                "qty": detail.quantity,
            })

            return JsonResponse({"method": request.method, "sell_id": sell_details_id.id, "data": data, "success": True}, status=200)

        elif request.method == "PUT":
            detail = SellDetails.objects.get(pk=sell_details_id)
            body = json.loads(request.body)

            if "total" in body:
                detail.total = float(body["total"])

            if "qty" in body:
                detail.quantity = float(body["qty"])

            detail.save()
            return JsonResponse({"method": request.method, "sell_details_id": sell_details_id, "success": True}, status=200)

        elif request.method == "DELETE":
            SellDetails.objects.get(pk=sell_details_id).delete()
            return JsonResponse({"method": request.method, "success": True}, status=200)

        else:
            return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)

    except SellDetails.DoesNotExist:
        return JsonResponse({"method": request.method, "data": [], "success": False}, status=200)
