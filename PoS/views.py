from django.shortcuts import render, HttpResponseRedirect
from .models import *
from .forms import *
from recipes.models import *
from django.core.context_processors import csrf
from django.db.models import Q
from django.contrib import messages
from django.db.models import Avg, Sum

#from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
# Create your views here.

def homepage(request):
    table = Table.objects.all().filter(status='a')
    context={
        'table':table,
    }
    return render(request,'PoS/homepage.html',context)


def new_order(request,dk):
    table_id = Table.objects.get(id=dk)
    year= YearlyIncomeGreg.objects.all().filter(status ='a').last()
    month= MonthlyIncomeGreG.objects.all().filter(status ='a').last()
    day= DailyIncomeGreG.objects.all().filter(status ='a').last()

    if request.POST:
        form = NewOrderForm(request.POST,initial={'table':table_id,'year':year,"month":month,'day':day,})
        if form.is_valid():
            form.save()
            table_id.status = 'b'
            table_id.save()
            order_id = RestoOrder.objects.last()

            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s'%(order_id.id))
    else:
        form = NewOrderForm(initial={'table':table_id,'year':year,"month":month,'day':day,})

    context = {
        'form':form,
        'table_id':table_id
    }
    context.update(csrf(request))
    return render(request, 'PoS/new_order.html', context)


def add_products_to_order_main(request, dk):
    recipes = Recipe.objects.all().filter(active='a')
    recipes_category = MainCategory.objects.all().filter(active='a')
    order = RestoOrder.objects.get(id=dk)
    order_items = order.restoorderitem_set.all()


    context = {
        'recipes':recipes,
        'categories':recipes_category,
        'order':order,
        'order_items':order_items,


    }
    return render(request,'PoS/add_products_main.html', context)


def add_products_to_order_category(request, dk,ck):
    recipes_category = MainCategory.objects.get(id=ck)
    recipes = Recipe.objects.all().filter(active='a')
    recipes = recipes.filter(category=recipes_category)
    order = RestoOrder.objects.get(id=dk)
    order_items = order.restoorderitem_set.all()
    context = {
        'recipes':recipes,
        'categories':recipes_category,
        'order':order,
        'order_items':order_items,

    }
    return render(request,'PoS/add_product_category.html', context)




def add_recipe_to_order_from_cat(request,dk,ck,pk):
    order = RestoOrder.objects.get(id=dk)
    recipe= Recipe.objects.get(id=pk)
    order_items = order.restoorderitem_set.all()
    order_category = MainCategory.objects.get(id=ck)
    if request.POST:
        form  = AddRecipeForm(request.POST, initial={'order':order, 'price':recipe.recipe_price, 'title': recipe,'cost':recipe.recipe_cost, })
        if form.is_valid():
            form.save()
            form.add_recipe(dk=dk)
            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/κατηγορία/%s' %(order.id,order_category.id))
    else:
        form= AddRecipeForm(initial={'order':order, 'price':recipe.recipe_price, 'title': recipe, 'cost':recipe.recipe_cost })

    context ={
        'form':form,
        'οrder':order,
        'order_items':order_items,

    }
    return render(request,'PoS/add_product_to_order.html', context)





def add_recipe_to_order(request,dk,pk):

    recipe= Recipe.objects.get(id=pk)
    order = RestoOrder.objects.get(id=dk)

    order_items = order.restoorderitem_set.all()
    if request.POST:
        form  = AddRecipeForm(request.POST, initial={'order':order, 'price':recipe.recipe_price, 'title': recipe,'cost':recipe.recipe_cost, })
        if form.is_valid():
            form.save()
            form.add_recipe(dk=dk)
            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/' %(dk))
    else:
        form= AddRecipeForm(initial={'order':order, 'price':recipe.recipe_price, 'title': recipe,'cost':recipe.recipe_cost,})

    context ={
        'form':form,
        'order_items':order_items,
        'order':order,
        'recipe':recipe,

    }
    return render(request,'PoS/add_product_to_order.html', context)



def delete_recipe_from_order(request,dk,pk):
    order_item = RestoOrderItem.objects.get(id = pk)
    order_item.delete_from_order(dk=dk)
    order_item.delete()
    return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/' %(dk))


def edit_recipe_from_order(request,dk,pk):
    order_item = RestoOrderItem.objects.get(id = pk)
    order = RestoOrder.objects.get(id= dk)

    if request.POST:
        form  = AddRecipeForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            form.edit_recipe(dk=dk, pk=pk)
            form.save()
            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/' %(dk))
    else:
        form= AddRecipeForm(instance=order_item)

    context ={
        'form':form,
        'order':order,

    }
    return render(request,'PoS/add_product_to_order.html', context)



def order_pay_not_complete(request, dk):
    order = RestoOrder.objects.get(id=dk)
    if request.POST:
        form = PayRestoOrderForm(request.POST,instance=order )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/' %(dk))
    else:
        form = PayRestoOrderForm(instance=order,initial={'paid_value':order.value})

    context ={
        'form':form,
        'order':order,
    }
    context.update(csrf(request))

    return render(request, 'PoS/add_product_to_order.html', context)




def print_order_to_kitchen(request):
	pass
	'''
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

	'''


def order_paid(request,dk):
    order = RestoOrder.objects.get(id= dk)
    order.order_table_closed(dk=dk)
    #order.paid_value = order.value




    table = Table.objects.get(title = order.table.title)
    table.status ='a'
    table.save()
    return HttpResponseRedirect('/PoS/')

def active_orders(request):
    orders = RestoOrder.objects.all().filter(status='a')
    tables=[]
    for ele in orders:
        if ele.table.status == 'b':
            tables.append(ele)
    context ={
        'tables':tables,
    }
    return render(request,'PoS/active_orders/homepage.html', context)

    
    





def total_stats(request):

    day = datetime.datetime.today()
    month = datetime.datetime.today().month

    print(day)
    day_orders = Lianiki_Order.objects.all().filter(day_added = day).order_by('-id')
    print_order_to_kitchen(day_orders)

    day_income = 0
    day_cost = 0
    if day_orders:
        day_income = day_orders.aggregate(Sum('paid_value'))
        day_income = day_income['paid_value__sum']
        day_cost   = day_orders.aggregate(Sum('total_cost'))
        day_cost   = day_cost['total_cost__sum']

    month_orders = Lianiki_Order.objects.all().filter(day_added__month =month)
    month_income = 0
    month_cost = 0
    if month_orders:
        month_income = month_orders.aggregate(Sum('paid_value'))
        month_income = month_income['paid_value__sum']
        month_cost   = month_orders.aggregate(Sum('total_cost'))
        month_cost   = month_cost['total_cost__sum']

    context ={
        'day_income':day_income,
        'day_cost':day_cost,
        'month_income':month_income,
        'month_cost':month_cost,
        'day_orders':day_orders,
    }
    return render(request, 'PoS/total_stats.html', context)



def admin_section(request):
    title= 'admin'
    day = DailyIncomeGreG.objects.last()
    month = MonthlyIncomeGreG.objects.last()
    year = YearlyIncomeGreg.objects.last()
    user_period = UserInputIncomeSeason.objects.last()
    tables = Table.objects.all().order_by('title')
    context ={
        'title':title,
        'day':day,
        'month':month,
        'year':year,
        'user_period':user_period,
        'tables':tables,
    }
    return render(request, 'PoS/admin_section.html',context)






def admin_section_deactive_day(request):
    day = DailyIncomeGreG.objects.last()
    day.status ='b'
    day.save()
    return HttpResponseRedirect('/PoS/admin/')

def admin_section_create_new_day(request):
    title = ''
    month = MonthlyIncomeGreG.objects.all().last()
    year = YearlyIncomeGreg.objects.last()
    if request.POST:
        form = DailyIncomeForm(request.POST, )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('PoS/admin/')
    else:
        form = DailyIncomeForm(initial={'month':month,'year':year,})

    context = {
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'PoS/admin_section_create_day.html', context)



def admin_section_deactive_month(request):
    month = MonthlyIncomeGreG.objects.last()
    month.status ='b'
    month.save()
    return HttpResponseRedirect('/PoS/admin/')

def admin_section_create_new_month(request):
    title = ''
    year = YearlyIncomeGreg.objects.last()
    if request.POST:
        form = MonthlyIncomeForm(request.POST, )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('PoS/admin/')
    else:
        form = MonthlyIncomeForm(initial={'year':year})

    context = {
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'PoS/admin_section_create_day.html', context)


def admin_section_deactive_year(request):
    year = YearlyIncomeGreg.objects.last()
    year.status ='b'
    year.save()
    return HttpResponseRedirect('/PoS/admin/')

def admin_section_create_new_year(request):
    title = ''
    if request.POST:
        form = YearlyIncomeForm(request.POST, )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('PoS/admin/')
    else:
        form =YearlyIncomeForm()

    context = {
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'PoS/admin_section_create_day.html', context)




# -------------------------------Lianiki--------------------------------------------------------------------------------

def lianiki_section(request):
    today = datetime.datetime.now().day
    try:
        today_incomes = Lianiki_Order.objects.all().filter(day_added = today).aggregate(Sum('paid_value'))
        total_incomes = today_incomes['paid_value__sum']
    except:
        total_incomes = 0

    lianiki_orders = Lianiki_Order.objects.all()
    day= DailyIncomeGreG.objects.all().last()
    month = MonthlyIncomeGreG.objects.all().last()
    context = {
        'orders':total_incomes,
        'day':day,
        'month':month
    }
    return render(request,'PoS/lianiki/homepage.html', context)


def create_return_order(request):

    order = RetailReturnOrder.objects.create()
    order.save()
    return HttpResponseRedirect('/PoS/return-products/%s' %(order.id))





def return_products(request,dk):
    title ='Επιστροφές'
    order = RetailReturnOrder.objects.get(id=dk)
    products = None
    order_items = order.retailreturnitem_set.all()
    categories = Category.objects.all()
    search_products = request.GET.get('search_products')
    if search_products:
        products = Product.objects.all().filter(
            Q(title__icontains = search_products)|
            Q(description__icontains= search_products)|
            Q(product_id__icontains =search_products)|
            Q(supplier__title__icontains = search_products)
        ).distinct()


    query = request.GET.get('search_pro')
    if query:
        categories = categories.filter(title__icontains =query)
    context ={
        'categories':categories,
        'order':order,
        'products':products,
        'order_items':order_items,
        'title':title,
    }

    return render(request, 'PoS/lianiki/return_products.html', context)



def return_products_category(request,dk,ck):
    pass

def return_product_product(request, dk, pk):
    order = RetailReturnOrder.objects.get(id=dk)
    product = Product.objects.get(id=pk)
    order_item = RetailReturnItem.objects.create(title=product, order=order, cost=product.price_buy, price=product.price, qty=1)



    '''
    title = models.ForeignKey(Product)
    order = models.ForeignKey(RetailReturnOrder)
    cost =  models.DecimalField(max_digits=6,decimal_places=2,default=0)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Τιμή Μονάδας')
    qty= models.DecimalField(max_digits=3,decimal_places=1,default=1, verbose_name='Ποσότητα')
    '''



def new_lianiki_order(request):
    day= DailyIncomeGreG.objects.all().last()
    month = MonthlyIncomeGreG.objects.all().last()
    year  = YearlyIncomeGreg.objects.all().last()
    if request.POST:
        form = LianikiForm(request.POST, initial={'day':day,'month':month, 'year':year})
        if form.is_valid():
            form.save()
            last_order = Lianiki_Order.objects.all().last()
            return HttpResponseRedirect('/PoS/lianiki/order/%s' %(last_order.id))

    else:
        form = LianikiForm( initial={'day':day,'month':month, 'year':year})

    context ={
        'form':form
    }
    context.update(csrf(request))
    return render(request, 'PoS/lianiki/new_lianiki_order.html', context)


def lianiki_show_categories(request,dk):
    products = None
    get_product_with_attritube = None
    lianiki_order =Lianiki_Order.objects.get(id=dk)
    order_items = lianiki_order.lianikiorderitem_set.all()
    categories = Category.objects.all()
    search_products = request.GET.get('search_products')
    if search_products:
        products = Product.objects.all().filter(ware_active = 'a')
        products = products.filter(
            Q(title__icontains = search_products)|
            Q(description__icontains= search_products)|
            Q(product_id__icontains =search_products)|
            Q(supplier__title__icontains = search_products)
        ).distinct()

        get_product_with_attritube = products.filter(color='a')


    query = request.GET.get('search_pro')
    if query:
        categories = categories.filter(title__icontains =query)
    context ={
        'categories':categories,
        'order':lianiki_order,
        'products':products,
        'order_items':order_items,
        'products_with_att':get_product_with_attritube,
    }
    return render(request, 'PoS/lianiki/show_categories_lianiki.html', context)

def lianiki_choose_category(request,dk,pk):
    lianiki_order =Lianiki_Order.objects.get(id=dk)
    order_items = lianiki_order.lianikiorderitem_set.all()
    category = Category.objects.get(id=pk)
    products = Product.objects.all().filter(category__title=category.title, ware_active ='a')
    search_products = request.GET.get('search_products')
    if search_products:
        products = products.filter(
            Q(title__icontains = search_products)|
            Q(description__icontains= search_products)|
            Q(product_id__icontains =search_products)|
            Q(supplier__title__icontains = search_products)
        ).distinct()
    context={
        'categories':category,
        'order':lianiki_order,
        'products':products,
        'order_items':order_items,
    }
    return render(request,'PoS/lianiki/lianiki_category.html', context)

def lianiki_add_product(request,dk,pk):
    product= Product.objects.get(id=pk)
    order =Lianiki_Order.objects.get(id=dk)
    order_items = order.lianikiorderitem_set.all()
    product_colors = None
    product_size = None
    if product.size == 'a':
        product_size = SizeAttribute.objects.all().filter(color__product =product).order_by('color')
        form = 'hello'
    elif product.color == 'a':
        product_colors = ColorAttribute.objects.all().filter(product = product)
        form = 'hello'
    else:
        if request.POST:
            form  = LianikiAddItemForm(request.POST, initial={'order':order, 'price':product.price, 'title': product,'cost':product.price_with_discount, })
            if form.is_valid():
                form.save()
                form.add_item(dk=dk, product=product)
                return HttpResponseRedirect('/PoS/lianiki/order/%s/' %(dk))
        else:
            form= LianikiAddItemForm(initial={'order':order, 'price':product.price, 'title': product,'cost':product.price_with_discount, })

    context ={
        'form':form,
        'order_items':order_items,
        'order':order,
        'product':product,

        'product_size':product_size,
        'products_colors':product_colors,

    }
    return render(request,'PoS/lianiki/lianiki_add_product.html', context)



def lianiki_add_product_with_color(request,dk,pk,sk):
    order = Lianiki_Order.objects.get(id =dk)
    product = Product.objects.get(id =pk)
    size = SizeAttribute.objects.get(id =sk)
    if product.qty_kilo == 0:
        cost = product.price_buy
    else:
        cost = product.price_buy/product.qty_kilo

    order_item = LianikiOrderItem.objects.create(title= product, order =order, cost = cost, size = size, color = size.color, price = product.price , qty =1)
    order_item.save()
    order_item.update_order_with_color(lianiki_order=order)
    order_item.update_stock_house_with_color(size_attritube=size, color_attritube=size.color, product=product)
    messages.success(request,'Προστέθηκε το προϊόν %s  στο χρώμα %s και μέγεθος %s' %(product.title, size.title.title, size.color.title.title))

    return HttpResponseRedirect('/PoS/lianiki/order/%s/%s/add/' %(order.id, product.id))



def lianiki_add_product_with_only_color(request, dk, pk, sk):
    order = Lianiki_Order.objects.get(id=dk)
    product = Product.objects.get(id=pk)
    color = ColorAttribute.objects.get(id=sk)
    if product.qty_kilo == 0:
        cost = product.price_buy
    else:
        cost = product.price_buy/product.qty_kilo

    order_item = LianikiOrderItem.objects.create(title= product, order =order, cost = cost,color = color, price = product.price , qty =1)
    order_item.save()
    order_item.update_order_with_only_color(lianiki_order=order)
    order_item.update_stock_house_with_only_color(color_attritube=color, product=product)
    messages.success(request,'Προστέθηκε το προϊόν %s  στο χρώμα %s .' %(product.title, color.title.title))
    return HttpResponseRedirect('/PoS/lianiki/order/%s/%s/add/' %(order.id, product.id))








def lianiki_edit_product(request, dk, pk):
    order_item = RestoOrderItem.objects.get(id = pk)
    order = RestoOrder.objects.get(id= dk)

    if request.POST:
        form  = AddRecipeForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            form.edit_recipe(dk=dk, pk=pk)
            form.save()
            return HttpResponseRedirect('/PoS/επέλεξε-συνταγή/%s/' %(dk))
    else:
        form= AddRecipeForm(instance=order_item)

    context ={
        'form':form,
        'order':order,

    }
    return render(request,'PoS/add_product_to_order.html', context)






def lianiki_edit_order_item(request, dk, pk):
    order_item = LianikiOrderItem.objects.get(id=pk)
    order = Lianiki_Order.objects.get(id=dk)

    if request.POST:
        form = LianikiAddItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            form.edit_item(dk=dk, pk=pk)
            form.save()
            return HttpResponseRedirect('/PoS/lianiki/order/%s'% (dk))
    else:
        form = LianikiAddItemForm(instance=order_item)

    context = {
        'form':form,
        'order':order,
        'order_item':order_item,
    }
    context.update(csrf(request))
    return render(request, 'PoS/lianiki/lianiki_add_product.html' , context)



def lianiki_delete_order_item(request,dk,pk,):
    order_item = LianikiOrderItem.objects.get(id=pk)
    order_item.delete_from_order(dk=dk, order_item=order_item)

    if order_item.size:
        order_item.delete_from_order_with_color(size_attritube=order_item.size, color_attritube=order_item.color)
    elif order_item.color:
        order_item.delete_from_order_with_only_color(color_attritube=order_item.color)
    else:
        pass
    order_item.delete()

    return HttpResponseRedirect('PoS/lianiki/order/%s/' %(dk))








def lianiki_order_pay_not_complete(request, dk):
    order = Lianiki_Order.objects.get(id=dk)
    if request.POST:
        form = PayLianikirderForm(request.POST,instance=order )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/PoS/lianiki/order/%s/' %(dk))
    else:
        form =PayLianikirderForm(instance=order,initial={'paid_value':order.value})

    context ={
        'form':form,
        'order':order,
    }
    context.update(csrf(request))

    return render(request, 'PoS/lianiki/lianiki_add_product.html', context)




def lianiki_print_order_to_warehouse(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




def lianiki_order_closed(request,dk):
    order = Lianiki_Order.objects.get(id= dk)
    order.order_table_closed(dk=dk)
    return HttpResponseRedirect('PoS/lianiki/new-order/')








