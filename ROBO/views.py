from django.shortcuts import render
from .models import *
from django.http import JsonResponse, FileResponse
from json import dumps
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from math import ceil


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


def order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            order_instance = Order()
            order_instance.name = request.POST.get("name")
            selectedItemsList = request.POST.get("selectedItems").split(",")
            quantityList = request.POST.get("quantity").split(",")
            mergerdItemsQuantity = {}
            for item in enumerate(selectedItemsList):
                mergerdItemsQuantity.update({item[1]: quantityList[item[0]]})
            order_instance.quantity_items = dumps(mergerdItemsQuantity)
            order_instance.date = date.today()
            if int(request.POST.get("payment_type")) == 3:
                paymentTypeObj = PaymentType.objects.filter(
                    payment_mode='Cash')[0]
                order_instance.payment_type = paymentTypeObj
                order_instance.total = int(
                    request.POST.get("cashPaymentTotal"))
                order_instance.save()
                order_instance2 = Order()
                order_instance2.name = request.POST.get("name")
                order_instance2.quantity_items = dumps(mergerdItemsQuantity)
                order_instance2.date = date.today()
                paymentTypeObj = PaymentType.objects.filter(
                    payment_mode='Online')[0]
                order_instance2.payment_type = paymentTypeObj
                order_instance2.total = int(
                    request.POST.get("onlinePaymentTotal"))
                order_instance2.save()
            else:
                order_instance.total = int(request.POST.get("totalInput"))
                paymentTypeObj = PaymentType.objects.filter(
                    id=request.POST.get("payment_type"))[0]
                order_instance.payment_type = paymentTypeObj
                order_instance.save()
            return render(request, 'order.html')
        else:
            return render(request, 'order.html')
    else:
        return render(request, 'login.html')


def getItems(request):
    if request.user.is_authenticated:
        response = {}
        items = Item.objects.all()
        item_id = []
        name = []
        price = []
        category_id = []
        category = []
        item_size_id = []
        item_size = []
        main_category = []
        for item in items:
            item_id.append(item.id)
            name.append(item.name)
            price.append(int(item.price))
            category_id.append(item.category.id)
            category.append(item.category.category)
            item_size_id.append(item.size.id)
            item_size.append(item.size.item_size)
            main_category.append(item.main_category.category)
        response.update({'name': name, 'price': price, 'category_id': category_id, 'category': category,
                        'item_size_id': item_size_id, 'item_size': item_size, 'item_id': item_id, 'maincategory': main_category})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getPayTypes(request):
    if request.user.is_authenticated:
        response = {}
        items = PaymentType.objects.all()
        payment_id = []
        payment_mode = []
        for item in items:
            payment_id.append(item.id)
            payment_mode.append(item.payment_mode)
        response.update({'payment_id': payment_id,
                        'payment_mode': payment_mode})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def maintenance(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            price = int(request.POST.get('price'))
            maintenance_date = request.POST.get('MaintenanceDate')
            user = Maintenance(name=name, price=price, date=maintenance_date)
            user.save()
            return render(request, 'maintenance.html')
        else:
            return render(request, 'maintenance.html')
    else:
        return render(request, 'login.html')


def additem(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            item_obj = Item()
            item_obj.name = request.POST.get('name')
            item_obj.price = int(request.POST.get('price'))
            category_obj = Category.objects.filter(
                id=request.POST.get('category'))[0]
            item_obj.category = category_obj
            size_obj = Size.objects.filter(id=request.POST.get('size'))[0]
            item_obj.size = size_obj
            mainCategoryObj = Maincategory.objects.filter(
                category=request.POST.get('mainCategory'))[0]
            item_obj.main_category = mainCategoryObj
            item_obj.save()
            return render(request, 'additem.html')
        else:
            return render(request, 'additem.html')
    else:
        return render(request, 'login.html')


def getSize(request):
    if request.user.is_authenticated:
        response = {}
        items = Size.objects.all()
        size_id = []
        item_size = []
        for item in items:
            size_id.append(item.id)
            item_size.append(item.item_size)
        response.update({'size_id': size_id, 'item_size': item_size})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getCategory(request):
    if request.user.is_authenticated:
        response = {}
        items = Category.objects.all()
        category_id = []
        category = []
        for item in items:
            category_id.append(item.id)
            category.append(item.category)
        response.update({'category_id': category_id, 'category': category})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def report(request):
    if request.user.is_authenticated:
        return render(request, 'report.html')
    else:
        return render(request, 'login.html')


def getOrders(request, ordersDate):
    if request.user.is_authenticated:
        filterDate = datetime.strptime(ordersDate, "%d%m%Y").date()
        response = {}
        orders = Order.objects.filter(date=filterDate).all()
        allOrders = []
        if orders.exists():
            for order in orders:
                allOrders.append({"name": order.name, "quantity_items": order.quantity_items,
                                 "total": order.total, "payment_type": order.payment_type.payment_mode, "id": order.id})
        response.update({'allOrders': allOrders})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getMaintenances(request, maintenanceDate):
    if request.user.is_authenticated:
        filterDate = datetime.strptime(maintenanceDate, "%d%m%Y").date()
        response = {}
        maintenances = Maintenance.objects.filter(date=filterDate).all()
        allMaintenance = []
        if maintenances.exists():
            for item in maintenances:
                allMaintenance.append({"name": item.name, "price": item.price})
        response.update({'allMaintenance': allMaintenance})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getOrdersMonthly(request, month, year):
    if request.user.is_authenticated:
        response = {}
        orders = Order.objects.filter(
            date__month=int(month), date__year=int(year)).all()
        allOrders = []
        if orders.exists():
            for order in orders:
                allOrders.append({"name": order.name, "quantity_items": order.quantity_items, "total": order.total,
                                 "payment_type": order.payment_type.payment_mode, "date": order.date.strftime("%d-%m-%Y")})
        response.update({'allOrders': allOrders})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getMaintenancesMonthly(request, month, year):
    if request.user.is_authenticated:
        response = {}
        maintenances = Maintenance.objects.filter(
            date__month=int(month), date__year=int(year)).all()
        allMaintenance = []
        if maintenances.exists():
            for item in maintenances:
                allMaintenance.append(
                    {"name": item.name, "price": item.price, "date": item.date.strftime("%d-%m-%Y")})
        response.update({'allMaintenance': allMaintenance})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getOrdersYearly(request, year):
    if request.user.is_authenticated:
        response = {}
        orders = Order.objects.filter(date__year=int(year)).all()
        allOrders = []
        if orders.exists():
            for order in orders:
                allOrders.append({"name": order.name, "quantity_items": order.quantity_items, "total": order.total,
                                 "payment_type": order.payment_type.payment_mode, "date": order.date.strftime("%d-%m-%Y")})
        response.update({'allOrders': allOrders})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getMaintenancesYearly(request, year):
    if request.user.is_authenticated:
        response = {}
        maintenances = Maintenance.objects.filter(date__year=int(year)).all()
        allMaintenance = []
        if maintenances.exists():
            for item in maintenances:
                allMaintenance.append(
                    {"name": item.name, "price": item.price, "date": item.date.strftime("%d-%m-%Y")})
        response.update({'allMaintenance': allMaintenance})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def manageOrder(request):
    if request.user.is_authenticated:
        return render(request, 'manageOrder.html')
    else:
        return render(request, 'login.html')


def deleteOrder(request, orderId):
    if request.user.is_authenticated:
        response = {}
        orderObj = Order.objects.filter(id=int(orderId))[0]
        orderObj.delete()
        response.update({'status': True})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def logIn(request):
    if request.method == "POST":
        userId = request.POST.get("UserId")
        userPassword = request.POST.get("Password")
        user = authenticate(request, username=userId, password=userPassword)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logOut(request):
    logout(request)
    return render(request, 'login.html')


def getMainCategory(request):
    if request.user.is_authenticated:
        response = []
        categoties = Maincategory.objects.all()
        for cat in categoties:
            response.append(cat.category)
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def editOrder(request, orderId):
    if request.user.is_authenticated:
        if request.method == "POST":
            order_instance = Order.objects.filter(id=int(orderId))[0]
            order_instance.name = request.POST.get("name")
            selectedItemsList = request.POST.get("selectedItems").split(",")
            quantityList = request.POST.get("quantity").split(",")
            mergerdItemsQuantity = {}
            for item in enumerate(selectedItemsList):
                mergerdItemsQuantity.update({item[1]: quantityList[item[0]]})
            order_instance.quantity_items = dumps(mergerdItemsQuantity)
            order_instance.date = date.today()
            if int(request.POST.get("payment_type")) == 3:
                paymentTypeObj = PaymentType.objects.filter(
                    payment_mode='Cash')[0]
                order_instance.payment_type = paymentTypeObj
                order_instance.total = int(
                    request.POST.get("cashPaymentTotal"))
                order_instance.save()
                order_instance2 = Order()
                order_instance2.name = request.POST.get("name")
                order_instance2.quantity_items = dumps(mergerdItemsQuantity)
                order_instance2.date = date.today()
                paymentTypeObj = PaymentType.objects.filter(
                    payment_mode='Online')[0]
                order_instance2.payment_type = paymentTypeObj
                order_instance2.total = int(
                    request.POST.get("onlinePaymentTotal"))
                order_instance2.save()
            else:
                order_instance.total = int(request.POST.get("totalInput"))
                paymentTypeObj = PaymentType.objects.filter(
                    id=request.POST.get("payment_type"))[0]
                order_instance.payment_type = paymentTypeObj
                order_instance.save()
            return render(request, 'manageOrder.html')
        else:
            return render(request, 'editOrder.html', {"id": orderId})
    else:
        return render(request, 'login.html')


def getOrdersById(request, orderId):
    if request.user.is_authenticated:
        response = {}
        order = Order.objects.filter(id=orderId)[0]
        response.update({"name": order.name, "quantity_items": order.quantity_items, "total": order.total,
                        "payment_type": order.payment_type.payment_mode, "id": order.id, "payment_type_id": order.payment_type.id})
        responseHeader = JsonResponse(dumps(response), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getDailyReportByPDf(request, ordersDate):
    if request.user.is_authenticated:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
        width, heigth = A4
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        p.setFont('VeraBd', 15)
        title = "DAILY REPORT"
        p.drawCentredString(width/2.0, cm, title)
        p.setFont('Vera', 13)
        filterDate = datetime.strptime(
            ordersDate, "%d%m%Y").date().strftime("%d/%m/%Y")
        p.drawString(cm, 2*cm, f"Date = {filterDate}")
        p.setTitle(f"Report_{filterDate}")
        orders = Order.objects.filter(
            date=datetime.strptime(ordersDate, "%d%m%Y").date()).all()
        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm],
               [3*cm, 4*cm, 4*cm, 4*cm, 4*cm])
        p.drawString(1.5*cm, 3.7*cm, "Sr No")
        p.drawString(6.25*cm, 3.7*cm, "Table No")
        p.drawString(11*cm, 3.7*cm, "Pay Type")
        p.drawString(15.75*cm, 3.7*cm, "Amount")
        currentY = 4*cm
        cash = 0
        online = 0
        total = 0
        if orders.exists():
            srNo = 1
            for order in orders:
                if currentY < 29*cm:
                    p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY,
                           currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(6.25*cm, currentY + 0.7*cm, order.name)
                    p.drawString(11*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(15.75*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
                else:
                    p.showPage()
                    currentY = cm
                    p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY,
                           currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(6.25*cm, currentY + 0.7*cm, order.name)
                    p.drawString(11*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(15.75*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
            if currentY < 29*cm:
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY,
                       currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY,
                       currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
        currentY += 1*cm
        maintenances = Maintenance.objects.filter(
            date=datetime.strptime(ordersDate, "%d%m%Y").date()).all()
        p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY +
               1*cm, currentY + 1*cm, currentY + 1*cm])
        p.drawString(1.5*cm, currentY + 0.7*cm, "Sr No")
        p.drawString(7.83*cm, currentY + 0.7*cm, "Maintenance")
        p.drawString(14.16*cm, currentY + 0.7*cm, "Amount")
        currentY += 1*cm
        maintanenceTotal = 0
        if maintenances.exists():
            srNo = 1
            for item in maintenances:
                itemWidth = stringWidth(
                    item.name, fontName="Vera", fontSize=13)
                if currentY < 29*cm:
                    if itemWidth <= 5.33*cm:
                        p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(7.83*cm, currentY + 0.7*cm, item.name)
                        p.drawString(14.16*cm, currentY +
                                     0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (5.33*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(14.16*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(14.16*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                else:
                    p.showPage()
                    currentY = cm
                    if itemWidth <= 5.33*cm:
                        p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(7.83*cm, currentY + 0.7*cm, item.name)
                        p.drawString(14.16*cm, currentY +
                                     0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (5.33*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(14.16*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(14.16*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        7.83*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                srNo += 1
            if currentY < 29*cm:
                p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(14.16*cm, currentY + 0.7 *
                             cm, str(maintanenceTotal))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 7.33*cm, 13.66*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(14.16*cm, currentY + 0.7 *
                             cm, str(maintanenceTotal))
                currentY += 1*cm
        if currentY < 29*cm:
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm,
                         f"Profit = {total - maintanenceTotal}")
        else:
            p.showPage()
            currentY = cm
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm,
                         f"Profit = {total - maintanenceTotal}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=f'Daily_Report_{ordersDate}.pdf')
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getMonthlyReportByPDf(request, month, year):
    if request.user.is_authenticated:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
        width, heigth = A4
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        p.setFont('VeraBd', 15)
        title = "MONTHLY REPORT"
        p.drawCentredString(width/2.0, cm, title)
        p.setFont('Vera', 13)
        stringToMonth = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June",
                         "7": "July", "8": "August", "9": "Sepember", "10": "October", "11": "November", "12": "December"}
        p.drawString(cm, 2*cm, f"Month = {stringToMonth[month]}/{year}")
        p.setTitle(f"Report_{stringToMonth[month]}/{year}")
        orders = Order.objects.filter(date__month=int(month), date__year=int(year)).all()
        p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm],
               [3*cm, 4*cm, 4*cm, 4*cm, 4*cm, 4*cm])
        p.drawString(1.5*cm, 3.7*cm, "Sr No")
        p.drawString(5.3*cm, 3.7*cm, "Table No")
        p.drawString(9.1*cm, 3.7*cm, "Date")
        p.drawString(12.9*cm, 3.7*cm, "Pay Type")
        p.drawString(16.7*cm, 3.7*cm, "Amount")
        currentY = 4*cm
        cash = 0
        online = 0
        total = 0
        if orders.exists():
            srNo = 1
            for order in orders:
                if currentY < 29*cm:
                    p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                           1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(5.3*cm, currentY + 0.7*cm, order.name)
                    p.drawString(9.1*cm, currentY + 0.7*cm,
                                 order.date.strftime("%d-%m-%Y"))
                    p.drawString(12.9*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(16.7*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
                else:
                    p.showPage()
                    currentY = cm
                    p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                           1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(5.3*cm, currentY + 0.7*cm, order.name)
                    p.drawString(9.1*cm, currentY + 0.7*cm,order.date.strftime("%d-%m-%Y"))
                    p.drawString(12.9*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(16.7*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
            if currentY < 29*cm:
                p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(16.7*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(16.7*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
        currentY += 1*cm
        maintenances = Maintenance.objects.filter(date__month=int(month), date__year=int(year)).all()
        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
        p.drawString(1.5*cm, currentY + 0.7*cm, "Sr No")
        p.drawString(6.25*cm, currentY + 0.7*cm, "Maintenance")
        p.drawString(11*cm, currentY + 0.7*cm, "Date")
        p.drawString(15.75*cm, currentY + 0.7*cm, "Amount")
        currentY += 1*cm
        maintanenceTotal = 0
        if maintenances.exists():
            srNo = 1
            for item in maintenances:
                itemWidth = stringWidth(
                    item.name, fontName="Vera", fontSize=13)
                if currentY < 29*cm:
                    if itemWidth <= 3.75*cm:
                        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(6.25*cm, currentY + 0.7*cm, item.name)
                        p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                        p.drawString(15.75*cm, currentY +0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (3.75*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                else:
                    p.showPage()
                    currentY = cm
                    if itemWidth <= 3.75*cm:
                        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(6.25*cm, currentY + 0.7*cm, item.name)
                        p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                        p.drawString(15.75*cm, currentY + 0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (3.75*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                srNo += 1
            if currentY < 29*cm:
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7 *cm, str(maintanenceTotal))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7 *cm, str(maintanenceTotal))
                currentY += 1*cm
        if currentY < 29*cm:
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm, f"Profit = {total - maintanenceTotal}")
        else:
            p.showPage()
            currentY = cm
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm,
                         f"Profit = {total - maintanenceTotal}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=f'report_{stringToMonth[month]}/{year}.pdf')
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader


def getYearlyReportByPDf(request, year):
    if request.user.is_authenticated:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
        width, heigth = A4
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        p.setFont('VeraBd', 15)
        title = "YEARLY REPORT"
        p.drawCentredString(width/2.0, cm, title)
        p.setFont('Vera', 13)
        p.drawString(cm, 2*cm, f"Year = {year}")
        p.setTitle(f"Report_{year}")
        orders = Order.objects.filter(date__year=int(year)).all()
        p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm],
               [3*cm, 4*cm, 4*cm, 4*cm, 4*cm, 4*cm])
        p.drawString(1.5*cm, 3.7*cm, "Sr No")
        p.drawString(5.3*cm, 3.7*cm, "Table No")
        p.drawString(9.1*cm, 3.7*cm, "Date")
        p.drawString(12.9*cm, 3.7*cm, "Pay Type")
        p.drawString(16.7*cm, 3.7*cm, "Amount")
        currentY = 4*cm
        cash = 0
        online = 0
        total = 0
        if orders.exists():
            srNo = 1
            for order in orders:
                if currentY < 29*cm:
                    p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                           1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(5.3*cm, currentY + 0.7*cm, order.name)
                    p.drawString(9.1*cm, currentY + 0.7*cm,
                                 order.date.strftime("%d-%m-%Y"))
                    p.drawString(12.9*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(16.7*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
                else:
                    p.showPage()
                    currentY = cm
                    p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                           1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                    p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                    p.drawString(5.3*cm, currentY + 0.7*cm, order.name)
                    p.drawString(9.1*cm, currentY + 0.7*cm,order.date.strftime("%d-%m-%Y"))
                    p.drawString(12.9*cm, currentY + 0.7*cm,
                                 order.payment_type.payment_mode)
                    p.drawString(16.7*cm, currentY + 0.7*cm, str(order.total))
                    currentY += 1*cm
                    srNo += 1
                    total += order.total
                    if order.payment_type.payment_mode == "Cash":
                        cash += order.total
                    else:
                        online += order.total
            if currentY < 29*cm:
                p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(16.7*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 4.8*cm, 8.6*cm, 12.4*cm, 16.2*cm, 20*cm], [currentY, currentY +
                       1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(16.7*cm, currentY + 0.7*cm, str(total))
                currentY += 1*cm
        currentY += 1*cm
        maintenances = Maintenance.objects.filter(date__year=int(year)).all()
        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
        p.drawString(1.5*cm, currentY + 0.7*cm, "Sr No")
        p.drawString(6.25*cm, currentY + 0.7*cm, "Maintenance")
        p.drawString(11*cm, currentY + 0.7*cm, "Date")
        p.drawString(15.75*cm, currentY + 0.7*cm, "Amount")
        currentY += 1*cm
        maintanenceTotal = 0
        if maintenances.exists():
            srNo = 1
            for item in maintenances:
                itemWidth = stringWidth(
                    item.name, fontName="Vera", fontSize=13)
                if currentY < 29*cm:
                    if itemWidth <= 3.75*cm:
                        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(6.25*cm, currentY + 0.7*cm, item.name)
                        p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                        p.drawString(15.75*cm, currentY +0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (3.75*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                else:
                    p.showPage()
                    currentY = cm
                    if itemWidth <= 3.75*cm:
                        p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY +
                               1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                        p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                        p.drawString(6.25*cm, currentY + 0.7*cm, item.name)
                        p.drawString(11*cm, currentY + 0.7*cm, item.date.strftime("%d-%m-%Y"))
                        p.drawString(15.75*cm, currentY + 0.7*cm, str(item.price))
                        currentY += 1*cm
                        maintanenceTotal += item.price
                    else:
                        no_of_rows = ceil(itemWidth / (3.75*cm))
                        if currentY + no_of_rows*cm < 29*cm:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + no_of_rows*cm,
                                currentY + no_of_rows*cm, currentY + no_of_rows*cm, currentY + no_of_rows*cm])
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows + 1):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                elif i == no_of_rows:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += no_of_rows*cm
                        else:
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, 29*cm,
                                29*cm, 29*cm, 29*cm])
                            no_of_rows_available = 0
                            remainingRows = 0
                            for i in range(no_of_rows)[::-1]:
                                if (currentY + (i+1)*cm < 29*cm):
                                    no_of_rows_available = i+1
                                    remainingRows = no_of_rows - i+1
                                    break
                            divideAt = ceil(len(item.name) / no_of_rows)
                            incrementBy = divideAt
                            p.drawString(1.5*cm, currentY + 0.7*cm, str(srNo))
                            p.drawString(15.75*cm, currentY +
                                        0.7*cm, str(item.price))
                            currentYModified = currentY
                            for i in range(no_of_rows_available):
                                if i == 0:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[:divideAt])
                                    divideAt += incrementBy
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += cm
                            p.showPage()
                            currentY = cm
                            currentYModified = currentY
                            p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + remainingRows*cm,
                                currentY + remainingRows*cm, currentY + remainingRows*cm, currentY + remainingRows*cm])
                            for i in range(remainingRows):
                                if i == remainingRows - 1:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:])
                                else:
                                    p.drawString(
                                        6.25*cm, currentYModified + 0.7*cm, item.name[divideAt-incrementBy:divideAt])
                                    divideAt += incrementBy
                                currentYModified += 1*cm
                            maintanenceTotal += item.price
                            currentY += (remainingRows*cm)
                srNo += 1
            if currentY < 29*cm:
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7 *cm, str(maintanenceTotal))
                currentY += 1*cm
            else:
                p.showPage()
                currentY = cm
                p.grid([cm, 5.75*cm, 10.5*cm, 15.25*cm, 20*cm], [currentY, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm, currentY + 1*cm])
                p.drawString(1.5*cm, currentY + 0.7*cm, "Total")
                p.drawString(15.75*cm, currentY + 0.7 *cm, str(maintanenceTotal))
                currentY += 1*cm
        if currentY < 29*cm:
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm, f"Profit = {total - maintanenceTotal}")
        else:
            p.showPage()
            currentY = cm
            p.drawString(cm, currentY + 1*cm, f"Cash = {cash}")
            p.drawString(7*cm, currentY + 1*cm, f"Online = {online}")
            p.drawString(14*cm, currentY + 1*cm,
                         f"Profit = {total - maintanenceTotal}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=f'report_{year}.pdf')
    else:
        resp = {}
        resp.update({"status": "Not Authenticated"})
        responseHeader = JsonResponse(dumps(resp), safe=False)
        responseHeader['Access-Control-Allow-Origin'] = "https://robospizzeria.co.in/"
        return responseHeader
