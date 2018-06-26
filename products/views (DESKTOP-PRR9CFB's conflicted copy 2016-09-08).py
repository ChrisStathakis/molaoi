from django.shortcuts import render,redirect, HttpResponseRedirect
from inventory_manager.form import *
from .models import Product,Supply, Category
from .forms import*
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q


from django.core.paginator import PageNotAnInteger, Paginator, Page
# Create your views here.





def welcome_page(request):
    title ="Welcome!"
    products = Product.objects.all()
    products_arrive = OrderItem.objects.all()[0:10]
    day = datetime.datetime.now().date()


    context={
        'title':title,
        'products':products,
        'day':day,
        'products_arrive':products_arrive,
    }
    return render(request,'inventory/welcome_page.html', context)

def homepage(request):
    #warehouse main page
    products = Product.objects.all().order_by('-id')[0:5]
    vendors = Supply.objects.all().order_by('-id')[0:5]
    orders = Order.objects.all().order_by('-id')[0:5]
    last_order = Order.objects.last()
    title='Αποθήκη'
    context = {
        'products':products,
        'vendors':vendors,
        'title':title,
        'orders':orders,
        'last_order':last_order,
    }
    return render(request, 'inventory/homepageNew.html', context)

def products(request):
    #product page
    title='Προϊόντα'
    products = Product.objects.all()
    categories = Category.objects.all()
    vendors = Supply.objects.all()





    query =request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(title__contains=query)|
            Q(category__title__contains=query)|
            Q(supplier__title__contains=query)|
            Q(description__icontains=query)
        ).distinct()

    category = request.POST.getlist('category')
    if category:
        products=products.filter(category__title__in = category)
    vendor = request.POST.getlist('vendor')
    if vendor:
        products=products.filter(supplier__title__in = category)

    site_status = request.POST.get('site_status')
    if site_status:
        products = products.filter(status__in=site_status)

    ware_status = request.POST.get('ware_status')
    if ware_status:
        products = products.filter(ware_active = ware_status)

    btwob = request.POST.get('btwob_status')
    if btwob:
        products = products.filter(carousel =btwob)

    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        product = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        product = paginator.page(paginator.num_pages)
    context ={

        #check filters
        'category_name':category,
        'vendor_name':vendor,
        'site_status_name':site_status,
        'ware_status_name':ware_status,
        'btwob_name':btwob,



        'products':product,
        'title':title,
        'categories':categories,
        'vendors':vendors,

    }
    context.update(csrf(request))
    return render(request, 'inventory/products_edit_section_NEW.html',context)


def create_product(request):

    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            color = form.cleaned_data['color']
            if color == 'a':
                title  = form.cleaned_data.get('title')
                my_id = Product.objects.get(title=title).id
                return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s'%(my_id))
            else:
                messages.success(request, 'Δημιουργήθηκε το Προϊόν...  %s' %(title))
                return HttpResponseRedirect('/αποθήκη/προιόντα/')
        form_category = CategoryForm(request.POST)
        if form_category.is_valid():
            form_category.save()
            messages.success(request,'')
            return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/')
        form_vendor = VendorForm(request.POST)
        if form_vendor.is_valid():
            form_vendor.save()
            messages.success(request, '')
            return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/')
    else:
        form = ProductForm()
        form_category=CategoryForm()
        form_vendor =VendorForm()




    context = {
        'title': 'Δημιουργία Προϊόντος',
        'form':form,
        'form_category':form_category,
        'form_vendor':form_vendor,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_product.html', context)

def create_vendor_from_product(request):
    form_vendor = VendorForm(request.POST)
    if form_vendor.is_valid():
        form_vendor.save()
        messages.success(request, 'Ο Προμηθευτής προστέθηκε.')
        return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/')
    else:
        form_vendor =VendorForm()
    context = {
        'vendoras': 'Δημιουργία Προϊόντος',

        'form_vendor':form_vendor,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_product.html', context)

def edit_product(request, dk):
    product = Product.objects.get(id=dk)
    if request.POST:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            color = form.cleaned_data.get('color')
            if color == 'a':
                return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s'%(dk))
            else:
                messages.success(request, 'Το προϊόν %s επεξεργάστηκε.'%(product.title))
                return HttpResponseRedirect('/αποθήκη/προιόντα/')
    else:
        form = ProductForm(instance=product)
    title = product.title
    context={
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_product.html', context)

def add_color_and_size(request,dk):
    product  = Product.objects.get(id=dk)
    colors = Color.objects.all()
    color_att = product.colorattribute_set.all()
    colors_selected = []
    for ele in color_att:
        colors_selected.append(ele.title.title)

    sizes = Size.objects.all()
    if request.POST:
        color_name = request.POST.getlist('color_name')
        for ele in color_name:
            new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
            new_color.save()
        return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s' %(dk))




    context = {
            'product':product,
            'colors':colors,
            'sizes':sizes,
            'colors_selected':colors_selected,
            'color_att':color_att,
    }
    return render(request, 'inventory/create_color_and_size.html', context)

def add_size_to_color(request,dk,pk):
    product  = Product.objects.get(id=dk)
    colors = Color.objects.all()
    color_att = product.colorattribute_set.all()
    colors_selected = []
    for ele in color_att:
        colors_selected.append(ele.title.title)

    product_color = ColorAttribute.objects.get(id=pk)
    if request.POST:
        color_name = request.POST.getlist('color_name')
        for ele in color_name:
            new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
            new_color.save()


        size_name = request.POST.getlist('size_name')
        for ele in size_name:
            new_size = SizeAttribute(title=Size.objects.get(title= ele), qty=0, color =product_color )
            new_size.save()
        if size_name:
            return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s/%s' %(dk,pk))
        if color_name:
            return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s' %(dk))


    sizes = Size.objects.all()

    size_att = product_color.sizeattribute_set.all()
    size_selected =[]
    for ele in size_att:
        size_selected.append(ele.title.title)



    context = {
            'product':product,
            'colors':colors,
            'sizes':sizes,
            'colors_selected':colors_selected,
            'color_att':color_att,
            'product_color':product_color,
            'size_att':size_att,
            'size_selected':size_selected,
    }
    return render(request, 'inventory/create_color_and_size.html', context)

def delete_size(request,dk,pk):
    size = SizeAttribute.objects.get(id=pk)
    size.delete()

    return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s/'%(dk))

def activate_deactivate_product(request,dk):
    product = Product.objects.get(id =dk)
    if product.ware_active == 'a':
        product.ware_active = 'b'
        product.save()
        messages.success(request, 'Το προϊόν %s απενεργοποιήθηκε'%(product.title) )
        return HttpResponseRedirect('/αποθήκη/προιόντα/')
    else:
        product.ware_active = 'a'
        product.save()
        messages.success(request, 'Το προϊόν %s ενεργοποιήθηκε'%(product.title) )
        return HttpResponseRedirect('/αποθήκη/προιόντα/')

def vendors(request):
    #vendors page
    title='Προμηθευτές'
    vendor = Supply.objects.all()
    query =request.GET.get('search_pro')
    if query:
        vendor=vendor.filter(
            Q(title__contains=query)|
            Q(email__contains=query)|
            Q(phone__contains=query)|
            Q(phone1__contains=query)|
            Q(fax__contains=query)
        ).distinct()
    context ={
        'vendors':vendor,
        'title':title,
    }
    return render(request, 'inventory/vendors_edit_section_NEW.html',context)

def create_vendor(request):
    title = 'Δημιουργία Προμηθευτή'
    if request.POST:
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('title')
            messages.success(request,'O Προμηθευτής %s δημιουργήθηκε.' %(name))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/')
        form_Doy = TaxesForm(request.POST)
        if form_Doy.is_valid():
            form_Doy.save()
            name = form_Doy.cleaned_data.get('title')
            messages.success(request,'O Προμηθευτής %s δημιουργήθηκε.' %(name))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/δημιουργία/')

    else:
        form = VendorForm()
        form_Doy = TaxesForm()

    context = {
        'title':title,
        'form':form,
        'form_taxes':form_Doy,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_vendor.html' ,context)

def edit_vendor(request,dk):
    vendor = Supply.objects.get(id= dk)
    title = 'Επεξεργασία %s'%(vendor.title)
    if request.POST:
        form = VendorForm(request.POST,instance=vendor)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('title')
            messages.success(request,'O Προμηθευτής %s επεξεργάστηκε.' %(name))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/')
        form_Doy = TaxesForm(request.POST)
        if form_Doy.is_valid():
            form_Doy.save()
            name = form_Doy.cleaned_data.get('title')
            messages.success(request,'H ΔοΥ %s δημιουργήθηκε.' %(name))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/επεξεργασία/%s/'%(dk))

    else:
        form = VendorForm(instance=vendor)
        form_Doy = TaxesForm()

    context = {
        'title':title,
        'form':form,
        'form_taxes':form_Doy,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_vendor.html' ,context)



def vendor_check_order(request, dk):
    # adds a new check payment to vendor with date expire
    title = 'Προσθήκη Επιταγής'
    vendor = Supply.objects.get(id=dk)
    vendors = Supply.objects.all()
    if request.POST:
        form = CheckOrderForm(request.POST,initial={'debtor':vendor})
        if form.is_valid():
            form.save()
            form.create_vendor_deposit_order()
            value = form.cleaned_data.get('value')
            messages.success(request, 'Προστέθηκαν %s  ευρώ στον Προμηθευτή %s ' %(value,vendor.title))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/')
    else:
        form = CheckOrderForm(initial={'debtor':vendor,'date_expire':timezone.now()})

    context ={
        'title':title,
        'vendors':vendors,
        'form':form,
        'vendor':vendor,
    }
    context.update(csrf(request))
    return render(request, 'inventory/vendor_add_deposit.html', context)







def vendor_deposit_order(request,dk):
    #adds a new deposit to the vendor
    title = 'Προσθήκη Προκαταβολής'
    vendor = Supply.objects.get(id=dk)
    vendors = Supply.objects.all()
    if request.POST:
        form = DepositVendorForm(request.POST,initial={'vendor':vendor})
        if form.is_valid():
            form.save()
            form.refresh(dk=dk)
            value = form.cleaned_data.get('value')
            messages.success(request, 'Προστέθηκαν %s  ευρώ στον Προμηθευτή %s ' %(value,vendor.title))
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/')
    else:
        form = DepositVendorForm(initial={'vendor':vendor})

    context ={
        'title':title,
        'vendors':vendors,
        'form':form,
        'vendor':vendor,
    }
    context.update(csrf(request))
    return render(request, 'inventory/vendor_add_deposit.html', context)




def check_orders_management(request):
    checks = CheckOrder.objects.all().order_by('-date_expire').filter(status ='a')
    checks_done = CheckOrder.objects.all().order_by('-date_expire').exclude(status ='a')
    title = 'Διαχείρηση επιταγών'
    context = {
        'checks':checks,
        'checks_done':checks_done,
        'title':title,
    }
    return render(request, 'inventory/check_orders_managment.html', context)

def payment_check(request,dk):
    check_order = CheckOrder.objects.get(id = dk)
    check_order.status = 'b'
    check_order.save()
    return HttpResponseRedirect('/αποθήκη/προμηθευτές/διαχείρηση-επιταγών/')



def edit_check_order(request,dk):
    check = CheckOrder.objects.get(id=dk)
    check_value = check.value
    check_debtor =  check.debtor
    check_place = check.place
    checks = CheckOrder.objects.all().order_by('-date_expire').filter(status ='a')
    checks_done = CheckOrder.objects.all().order_by('-date_expire').exclude(status ='a')
    title = 'Διαχείρηση %s, %s ' %(check.debtor.title, check.place.title)
    if request.POST:
        form = CheckOrderForm(request.POST, instance=check)
        if form.is_valid():
            check_debtor.remaining_deposit -= check_value
            check_debtor.save()
            check_place.balance -= check_value
            check_place.save()
            check_debtor.remaining_deposit += form.cleaned_data.get('value')
            check_debtor.save()
            new_place = form.cleaned_data.get('place')
            new_place.balance += form.cleaned_data.get('value')
            new_place.save()
            form.save()
            return HttpResponseRedirect('/αποθήκη/προμηθευτές/διαχείρηση-επιταγών/')
    else:
        form = CheckOrderForm(instance=check)

    context = {
        'title':title,
        'checks':checks,
        'form':form,
        'checks_done':checks_done,

    }
    context.update(csrf(request))

    return render(request, 'inventory/edit_check_orders.html', context)









def orders(request):
    #ordermain page
    last_order = Order.objects.last()
    title= 'Τιμολόγια'
    order = Order.objects.all().filter(status='p').order_by('-date')
    query =request.GET.get('search_pro')
    if query:
        order=order.filter(
            Q(date__icontains=query)|
            Q(code__icontains=query)|
            Q(vendor__title__contains=query)

        ).distinct()
    context = {
        'last_order':last_order,
        'orders':order,
        'title':title,
    }
    return render(request, 'inventory/orders_edit_section_NEW.html',context)

def create_order(request):
    #creates a new order
    title = 'Δημιουργία τιμολογίου'
    last_order = Order.objects.all().filter(status='p').last()

    if request.POST:
        form = OrderForm(request.POST,)
        if form.is_valid():

            form.save()
            updated_order = Order.objects.all().last()
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/επεξεργασία/%s' %(updated_order.id))

    else:
        form = OrderForm(initial={'date':timezone.now})


    context = {
        'title':title,
        'form':form,
        'last_order':last_order,
    }
    context.update(csrf(request))
    return render(request,'inventory/new_all_NEW.html',context)

def create_vendor_from_order(request):
    last_order = Order.objects.all().last()
    title = 'Νέος Προμηθευτής'
    if request.POST:
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/νέο/')
    else:
        form = VendorForm()

    context = {
        'form':form,
        'title':title,
        'last_order':last_order,
    }

    context.update(csrf(request))
    return render(request,'inventory/new_all_NEW.html',context)

def create_taxes_city(request):
    title = ''
    last_order = Order.objects.all().last()
    if request.POST:
        form = TaxesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/προμηθευτής/')
    else:
        form = TaxesForm()

    context = {
        'form':form,
        'title':title,
        'last_order':last_order,
    }

    context.update(csrf(request))
    return render(request,'inventory/new_all_NEW.html',context)





def order_edit_id(request, dk):
    #the main page which you add or remove products in order

    title ='Προσθήκη Προϊόντος στο Τιμολόγιο'
    order = Order.objects.get(id=dk)
    order_items = OrderItem.objects.all().filter(order__code = order.code)
    products = Product.objects.all().filter(supplier = order.vendor)
    query = request.GET.get('search_pro')
    if query:
        products = products.filter(
            Q(description__icontains=query)|
            Q(title__icontains=query)
        ).distinct()
    context={
        'title':title,
        'order':order,
        'order_items':order_items,
        'products':products,
    }
    return render(request,'inventory/add_product_to_order_NEW.html',context)





def add_product_to_order(request,dk,pk):
    # on this page you add info to OrderItem
    # if product have color returns a new view to pick the color else returns a form to add a OrderItem
    #to product

    product = Product.objects.get(id=pk)
    order = Order.objects.get(id=dk)
    if product.check_color():
        #returns a view with color attritube atc
        colors = Color.objects.all()
        color_att = product.colorattribute_set.all()
        colors_selected = []
        for ele in color_att:
            colors_selected.append(ele.title.title)

        sizes = Size.objects.all()
        if request.POST:
            color_name = request.POST.getlist('color_name')
            for ele in color_name:
                new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
                new_color.save()
                messages.success(request,'Το Χρώμα %s Προστέθηκε'%(ele.title))
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/check/%s/%s' %(dk,pk))
        title = str(order.code) + ' , '+str(product.title)
        context = {
                'product':product,
                'colors':colors,
                'sizes':sizes,
                'colors_selected':colors_selected,
                'color_att':color_att,
                'order':order,
                'title':title,
        }
        return render(request, 'inventory/add_color_and_size_to_order.html', context)
    else:

        unit =Unit.objects.get(name='Τεμάχ')

        order_date = order.date
        date_object = datetime.datetime.strptime('01062016', "%d%m%Y").date()
        if order_date >= date_object:
            fpa = 'c'
        else:
            fpa = 'b'

        products = Product.objects.all().filter(supplier = order.vendor)
        order_items = OrderItem.objects.all().filter(order__code = order.code)
        title=product.title
        query = request.GET.get('search_pro')
        if query:
            products = products.filter(
                Q(description__icontains=query)|
                Q(title__icontains=query)
            ).distinct()

        if product.check_color():
            pass
        else:
            if request.POST:
                form = OrderItemForm(request.POST,initial={'order':order,'product':product})
                if form.is_valid():
                    all_order_item = OrderItem.objects.all().filter(order__id=dk)
                    if all_order_item.filter(product__title=form.cleaned_data['product']).exists():
                        return HttpResponseRedirect("/αποθήκη/τιμολόγια/επεξεργασία/%s/" %(dk))


                    form.save()
                    form.add_to_order()
                    form.add_to_product()
                    item_order = form.cleaned_data['product']
                    messages.success(request,' Το προϊον %s καταχωρήθηκε.'% item_order,extra_tags='item_order')
                    order_item = OrderItem.objects.get(product__title=item_order,order__id=dk)
                    if order_item.product.check_color():
                        return HttpResponseRedirect('/αποθήκη/τιμολόγια/προσθήκη-προιόντος/%s/color/%s/' %(dk,product.id))
                    else:
                        return HttpResponseRedirect("/αποθήκη/τιμολόγια/επεξεργασία/%s/" %(dk))
            else:
                form =OrderItemForm(initial={'order':order,'product':product,'price':product.price_buy,'discount':product.ekptosi,'unit':unit,'taxes':fpa})
        context ={
                'title':title,
                'order_items':order_items,
                'form':form,
                'order':order,
                'product':product,
                'products':products,
            }

        context.update(csrf(request))
        return render(request,'inventory/choose_product_for_order.html', context)

def create_size_to_color_from_order(request,dk,pk,ck):
    order = Order.objects.get(id=dk)
    product=Product.objects.get(id=pk)
    color = ColorAttribute.objects.get(id=ck)
    colors = Color.objects.all()
    color_att = product.colorattribute_set.all()
    colors_selected = []
    for ele in color_att:
        colors_selected.append(ele.title.title)

    product_color = ColorAttribute.objects.get(id=ck)
    if request.POST:
        color_name = request.POST.getlist('color_name')
        for ele in color_name:
            new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
            new_color.save()


        size_name = request.POST.getlist('size_name')
        for ele in size_name:
            new_size = SizeAttribute(title=Size.objects.get(title= ele), qty=0, color =product_color )
            messages.success(request,"Το Μέγεθος %s δημιουργήθηκε" %(ele))
            new_size.save()

        return HttpResponseRedirect('/αποθήκη/τιμολόγια/check/%s/%s' %(dk,pk))




    sizes = Size.objects.all()

    size_att = product_color.sizeattribute_set.all()
    size_selected =[]
    for ele in size_att:
        size_selected.append(ele.title.title)


    title = str(order.code) + ' , '+str(product.title)+' , '+str(color.title)
    context = {
            'product':product,
            'colors':colors,
            'sizes':sizes,
            'colors_selected':colors_selected,
            'color_att':color_att,
            'product_color':product_color,
            'size_att':size_att,
            'size_selected':size_selected,
            'order':order,
            'color':color,
            'title':title,
    }
    return render(request, 'inventory/add_color_and_size_to_order.html', context)

def add_size_to_order_item(request,dk,pk,ck):
    #returns a list of sizes and you pick one

    product = Product.objects.get(id=pk)
    order = Order.objects.get(id=dk)
    product_color = ColorAttribute.objects.get(id=ck)
    color_sizes = product_color.sizeattribute_set.all()
    colors = Color.objects.all()
    color_att = product.colorattribute_set.all()
    colors_selected = []
    for ele in color_att:
        colors_selected.append(ele.title.title)
    sizes = Size.objects.all()
    if request.POST:
        color_name = request.POST.getlist('color_name')
        for ele in color_name:
            new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
            new_color.save()
            return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s' %(dk))

    title = str(order.code) + ' , ' + str(product.title)+' , ' + str(product_color.title) + ' , '+ str()
    context = {
                'product':product,
                'colors':colors,
                'sizes':sizes,
                'colors_selected':colors_selected,
                'color_att':color_att,
                'order':order,
                'product_color':product_color,
                'color_sizes':color_sizes,
                'title':title,
        }
    return render(request, 'inventory/add_color_and_size_to_order.html', context)

def add_color_and_size_to_order_item(request,dk,pk,ck,sk):
    # on this page you add info to OrderItem
    unit =Unit.objects.get(name='Τεμάχ')
    order = Order.objects.get(id = dk)
    product_color = ColorAttribute.objects.get(id=ck)
    product_size = SizeAttribute.objects.get(id=sk)
    order_date = order.date
    date_object = datetime.datetime.strptime('01062016', "%d%m%Y").date()
    if order_date >= date_object:
        fpa = 'c'
    else:
        fpa = 'b'

    product = Product.objects.get(id=pk)
    colors = Color.objects.all()
    color_att = product.colorattribute_set.all()
    colors_selected = []
    for ele in color_att:
        colors_selected.append(ele.title.title)

    sizes = Size.objects.all()
    if request.POST:
        form_item_order = OrderItemForm(request.POST,initial={
            'order':order,
            'product':product,
            'price':product.price_buy,
            'discount':product.ekptosi,
            'unit':unit,
            'taxes':fpa,
            'color':product_color,
            'size':product_size,
        })
        if form_item_order.is_valid():
            form_item_order.save(commit=False)
            form_item_order.add_to_product_with_color_and_size(order=order, product =product, color_attritube=product_color, size_attritube=product_size)
            form_item_order.save()
            messages.success(request,'Προστέθηκε το προϊόν %s στο τιμολόγιο.' %(product.title))
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/επεξεργασία/%s' %(dk))
        else:
            color_name = request.POST.getlist('color_name')
            for ele in color_name:
                new_color = ColorAttribute.objects.create(title = Color.objects.get(title =ele), qty=0,product=product)
                new_color.save()
                return HttpResponseRedirect('/αποθήκη/προιόντα/δημιουργία/add_color/%s' %(dk))
    else:
        form_item_order = OrderItemForm(initial={
            'order':order,
            'product':product,
            'price':product.price_buy,
            'discount':product.ekptosi,
            'unit':unit,
            'taxes':fpa,
            'color':product_color,
            'size':product_size,
        })
    title = str(order.code) + ' , ' + str(product.title)+' , ' + str(product_color.title) + ' , '+ str(product_size.title)
    context = {
            'product':product,
            'colors':colors,
            'sizes':sizes,
            'colors_selected':colors_selected,
            'color_att':color_att,
            'form_item_order':form_item_order,
            'product_color':product_color,
            'product_size':product_size,
            'title':title
        }
    context.update(csrf(request))
    return render(request, 'inventory/add_color_and_size_to_order_item.html', context)

def edit_product_from_order(request,dk,pk):
    order_item= OrderItem.objects.get(id=pk)
    order = Order.objects.get(id=dk)
    product = Product.objects.get(id=pk)
    products = Product.objects.all().filter(supplier = order.vendor)
    order_items = OrderItem.objects.all().filter(order__code = order.code)
    title=order_item.product.title
    query = request.GET.get('search_pro')
    if query:
        products = products.filter(
            Q(description__icontains=query)|
            Q(title__icontains=query)
        ).distinct()



    if request.POST:
        form =OrderItemForm(request.POST,instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            if product.check_color() == False:
                form.update_order(mod=pk)
                form.update_stock_and_vendor(pk=pk)
                form.save()
                messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
                return HttpResponseRedirect('/αποθήκη/τιμολόγια/επεξεργασία/%s/' %dk)
            else:
                form.update_product_with_color_and_size(order=order, order_item=order_item)
                form.update_order_with_color_and_size(order=order, order_item=order_item)
                form.save()
                messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
                return HttpResponseRedirect('/αποθήκη/τιμολόγια/επεξεργασία/%s/' %dk)

    else:
        form =OrderItemForm(instance=order_item)

    context={
        'title':title,
        'order_items':order_items,
        'form':form,
        'order':order,
        'product':product,
        'products':products,
        'order_item':order_item,

    }
    context.update(csrf(request))
    return render(request, 'inventory/edit_order_id_New.html',context)

def create_product_from_order_page(request,dk):
    order = Order.objects.get(id=dk)

    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['title']
            form.save()
            pro = Product.objects.get(title=name)

            if pro.check_color() == True:
                return HttpResponseRedirect('/αποθήκη/τιμολόγια/προσθήκη-προιόντος/%s/color/%s/' %(dk,pro.id))
            else:
                messages.success(request,'To Προϊόν %s δημιουργήθηκε.'%(name))
                return HttpResponseRedirect("/αποθήκη/τιμολόγια/check/%s/%s/" %(dk,pro.id))
    else:
        form = ProductForm(initial={'supplier':order.vendor,})
    context={
        'form':form,
        'order':order,
    }
    context.update(csrf(request))
    return render(request, 'inventory/create_product.html', context)

def choose_color_to_product_from_order(request,ok,pk):
    product = Product.objects.get(id=pk)
    order = Order.objects.get(id=ok)
    product_colors = product.colorattribute_set.all()
    color = Color.objects.all()

    context = {
        'order':order,
        'product':product,
        'color':color,
        'product_color':product_colors,

    }
    return render(request, 'inventory/choose_color_to_product.html', context)

def create_color_to_product_from_order(request,ok,pk,ck):
    order = Product.objects.get(id=ok)
    product = Product.objects.get(id=pk)
    color = Color.objects.get(id=ck)
    for ele in product.colorattribute_set.all():
        if color.title == ele.title.title:
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/προσθήκη-προιόντος/%s/color/%s/' %(order.id,product.id))
    new_attritube = ColorAttribute.objects.create(product=product,title=color)
    new_attritube.save()
    return HttpResponseRedirect('/αποθήκη/τιμολόγια/προσθήκη-προιόντος/%s/color/%s/' %(order.id,product.id))

def add_color_to_product_from_order(request,ok,pk,ck):
    order = Product.objects.get(id=ok)
    product = Product.objects.get(id=pk)
    color_attritube = ColorAttribute.objects.get(id=ck)
    #if OrderItemColor.title == color_attritube:

    if product.check_size():
        pass
        #new_color_order_item = OrderItemColor.objects.create(title=ColorAttribute, qty=0, order_item=)



    context={
        'order':order,
        'color_attritube':color_attritube,
        'product':product,

    }
    return render(request,'inventory/add_color_to_product_from_order.html',context)

def create_category_from_order(request,dk):
    title = ''
    last_order = Order.objects.get(id=dk)

    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/προσθήκη-προιόντος/%s/' %(last_order.id))
    else:
        form = CategoryForm()
    context ={
        'title':title,
        'form':form,
        'last_order':last_order,
    }
    context.update(csrf(request))

    return render(request, 'inventory/done_order_add_product_New.html', context)

def done_order_delete_id(request,dk):
    order_item = OrderItem.objects.get(id=dk)
    order = Order.objects.get(id=order_item.order.id)
    order_item.delete_order_item(foo=dk)
    order_item.delete()
    messages.info(request,'Its deleteded!')
    context={
        'order':order,
        'order_item':order_item

    }
    return render(request,'inventory/add_product_to_order_NEW.html',context)

def order_edit(request,dk):
    order = Order.objects.get(id=dk)
    products = order.orderitem_set.all()
    if request.POST:
        form_o =OrderEditForm(request.POST,instance=order)
        if form_o.is_valid():
            form_o.save(commit=False)
            form_o.update_vendor(pk=order.id)
            form_o.save()
            messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
            return HttpResponseRedirect('/αποθήκη/τιμολόγια/επεξεργασία/%s'%(dk))
    else:
        form_o = OrderEditForm(instance=order)
    context={
        'form':form_o,
        'products':products,
        'order_id':order,
    }
    context.update(csrf(request))
    return render(request,'inventory/done_order_edit_id.html',context)

def delete_order_item(request,dk):
    #delete the order_item from the order and transcates the order!
    order_item = OrderItem.objects.get(id=dk)
    order = Order.objects.get(id=order_item.order.id)
    order_item.delete_order_item(foo=dk)
    order_item.delete()
    return HttpResponseRedirect("/αποθήκη/τιμολόγια/επεξεργασία/%s/" %(order.id))




def tools(request):
    color = Color.objects.all().order_by('title')
    size = Size.objects.all().order_by('-title')
    payment_method= PaymentMethod.objects.all()
    payment_group = PaymentMethodGroup.objects.all()

    if request.POST:
        color_form = CreateColor(request.POST)
        size_form = CreateSize(request.POST)
        payment_group_form = PaymentGroupForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if color_form.is_valid():
            color_form.save()
            title = color_form.cleaned_data['title']
            messages.success(request, 'Το χρώμα %s προστέθηκε'%(title))
            return HttpResponseRedirect('/αποθήκη/εργαλεία/')
        elif size_form.is_valid():
                size_form.save()
                title = size_form.cleaned_data['title']
                messages.success(request, 'Το χρώμα %s προστέθηκε'%(title))
                return HttpResponseRedirect('/αποθήκη/εργαλεία/')
        elif payment_form.is_valid():
                payment_form.save()
                title = payment_form.cleaned_data['title']
                messages.success(request,'Ο τρόπος πληρωμής  %s προστέθηκε.'%(title))
                return HttpResponseRedirect('/αποθήκη/εργαλεία/')
        else:
            if payment_group_form.is_valid():
                payment_group_form.save()
                title = payment_group_form.cleaned_data['title']
                messages.success(request,'Ο τρόπος πληρωμής  %s προστέθηκε.'%(title))
                return HttpResponseRedirect('/αποθήκη/εργαλεία/')
    else:
        color_form = CreateColor()
        size_form = CreateSize()
        payment_form =PaymentForm()
        payment_group_form = PaymentGroupForm()

    context = {
        'color':color,
        'size':size,
        'color_form':color_form,
        'size_form':size_form,
        'payment_form':payment_form,
        'payment_group_form':payment_group_form,
        'payment_method':payment_method,
        'payment_group':payment_group,
    }
    context.update(csrf(request))
    return render(request,'inventory/tools.html',context)

def activate_or_deactive_color(request, dk):

    color = Color.objects.get(id=dk)
    if color.status == 'a':
        color.status = 'b'
        messages.warning(request,'To %s απενεργοποιήθηκε'%(color.title))
    else:
        messages.success(request,'To %s ενεργοποιήθηκε'%(color.title))
        color.status = 'a'
    color.save()
    return HttpResponseRedirect('/αποθήκη/εργαλεία/')



def tools_edit_color(request,dk):
    color = Color.objects.get(id=dk)

    if request.POST:
        form = CreateColor(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/εργαλεία/')
    else:
        form = CreateColor(instance=color)

    context = {
        'form':form,
    }

    return render(request, 'inventory/tools_edit_color.html', context)

def tools_edit_size(request,dk):
    size = Size.objects.get(id=dk)

    if request.POST:
        form = CreateSize(request.POST, instance=size)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/εργαλεία/')
    else:
        form = CreateSize(instance=size)

    context = {
        'form':form,
    }

    return render(request, 'inventory/tools_edit_color.html', context)


def edit_payment_group(request, dk):
    payment_group =PaymentMethodGroup.objects.get(id=dk)
    if request.POST:
        form = PaymentGroupForm(request.POST, instance=payment_group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/εργαλεία/')
    else:
        form = PaymentGroupForm(instance=payment_group)

    context ={
        'form':form,
    }
    context.update(csrf(request))
    return render(request, 'inventory/tools_edit_color.html', context)

def edit_payment(request, dk):
    payment=PaymentMethod.objects.get(id=dk)
    if request.POST:
        form = PaymentGroupForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/αποθήκη/εργαλεία/')
    else:
        form = PaymentForm(instance=payment)

    context ={
        'form':form,
    }
    context.update(csrf(request))
    return render(request, 'inventory/tools_edit_color.html', context)



def activate_deactivate_size(request,dk):

    size = Size.objects.get(id=dk)
    if size.status == 'a':
        size.status = 'b'
    else:
        size.status = 'a'
    size.save()
    return HttpResponseRedirect('/αποθήκη/εργαλεία/')




def tools_change_order(request):
    title ='Αλλαγή Ποσότητας'
    if request.POST:
        form = ChangeQtyOrderForm(request.POST)
        if form.is_valid():
            form.save()
            new_order = ChangeQtyOrder.objects.last().id
            return HttpResponseRedirect('/αποθήκη/εργαλεία/αλλαγή-ποσότητας/%s' %(new_order))
    else:
        form  = ChangeQtyOrderForm()

    context ={
        'title':title,
        'form':form,
    }
    context.update(csrf(request))
    return render(request,'inventory/tools_order.html', context)



def tools_change_qty(request,dk):
    order = ChangeQtyOrder.objects.get(id=dk)
    order_items = ChangeQtyOrderItem.objects.all().filter(order=order)
    vendors = Supply.objects.all()
    categories = Category.objects.all()
    products = None
    title = order.title
    vendor_name = None
    category_name = None
    if request.POST:
        vendor_name = request.POST.getlist('vendor')
        category_name = request.POST.getlist('category')
        products = Product.objects.all()
        if vendor_name:
            products = products.filter(supplier__title__in=vendor_name)
        if category_name:
            products = products.filter(category__title__in =category_name)
    context ={
        'title':title,
        'products':products,
        'vendors':vendors,
        'vendor_name':vendor_name,
        'categories':categories,
        'category_name':category_name,
        'order_item':order_items,
        'order':order,

    }
    return render(request,'inventory/tools_change_qty.html',context)


def tools_grab_qty(request,dk,pk):
    order = ChangeQtyOrder.objects.get(id=dk)
    order_items = ChangeQtyOrderItem.objects.all().filter(order=order)
    product = Product.objects.get(id=pk)
    if request.POST:
        form = ChangeQtyOrderItemForm(request.POST, initial={'title':product, 'order':order,})
        if form.is_valid():
            form.save()
            form.update_product()
            messages.success(request,'Επιτυχής αλλαγή ποσότητας')
            return HttpResponseRedirect('/αποθήκη/εργαλεία/αλλαγή-ποσότητας/%s'%(order.id))
    else:
        form = ChangeQtyOrderItemForm(initial={'title':product, 'order':order,})

    context = {
        'form':form,
        #'title':title,
        'order_item':order_items,
        'order':order,
    }
    context.update(csrf(request))
    return render(request, 'inventory/tools_grab_qty.html',context)

'''
def add_product_to_order(request,dk):
    order = Order.objects.get(id=dk)


    if request.POST:
        form_i= OrderItemForm(request.POST,initial={'order':order})
        if form_i.is_valid():
            form_i.save()
            form_i.add_to_order()
            form_i.add_to_product()
            item_order = form_i.cleaned_data['product']
            messages.success(request,' Το προϊον %s καταχωρήθηκε.'% item_order,extra_tags='item_order')
            return redirect(reverse('last_one'))
    else:
        form_i = OrderItemForm(initial={'order':order})

    context ={
        'form_i':form_i,
        'order':order,
        }

    context.update(csrf(request))
    return render(request, 'inventory/choose_product_for_order.html',context)

'''







#---------------------------------------------------------------------------------------------


'''
def new_category(request):
    if request.POST:
        form_o =OrderForm(request.POST)
        form_c =CategoryNew(request.POST)
        form_v =VendorForm(request.POST)
        if form_o.is_valid():
            form_o.save()
            return redirect('last_order/')
        elif form_c.is_valid():
            form_c.save()
            product_name = form_c.cleaned_data['title']
            messages.success(request,' H Κατηγορία  %s καταχωρήθηκε.'% product_name,extra_tags='product')
            return redirect(reverse(new_all))

        elif form_v.is_valid():
            vendor_name =form_v.cleaned_data['title']
            form_v.save()
            messages.success(request,' Ο Προμηθευτής %s καταχωρήθηκε.'% vendor_name,extra_tags='vendor')
            return redirect(reverse(new_all))
    else:
        form_o =OrderForm()
        form_c =CategoryNew()
        form_v =VendorForm()
    context ={
        'form_c':form_c,
        'form_o':form_o,
        'form_v':form_v,

        }
    context.update(csrf(request))
    return render(request,'inventory/new_category.html',context)
'''




def order_done(request,dk):
    order = Order.objects.get(id=dk)
    products = OrderItem.objects.all().filter(order__code = order.code)
    context ={
        'order':order,
        'products':products,
    }
    return render(request,'inventory/order_done.html',context)


def done_order_edit_id(request,dk):
    order = Order.objects.get(id=dk)
    products = order.orderitem_set.all()
    if request.POST:
        form_o =OrderEditForm(request.POST,instance=order)
        if form_o.is_valid():
            form_o.save(commit=False)
            form_o.update_vendor(pk=order.id)
            form_o.save()
            messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
            return HttpResponseRedirect('/homepage/new_all/last_order/')
    else:
        form_o = OrderEditForm(instance=order)
    context={
        'form_i':form_o,
        'products':products,
        'order_id':order,
    }
    context.update(csrf(request))
    return render(request,'inventory/done_order_edit_id.html',context)

def done_order_product_id(request,dk):
    order_item= OrderItem.objects.get(id=dk)
    if request.POST:
        form =OrderItemForm(request.POST,instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            form.update_order(mod=dk)
            form.update_stock_and_vendor(pk=dk)
            form.save()
            messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
            return HttpResponseRedirect('/homepage/new_all/last_order/edit/%s' %order_item.order.id)

    else:
        form =OrderItemForm(instance=order_item)

    context={

        'form_i':form,
        'order_item':order_item

    }
    context.update(csrf(request))
    return render(request,'inventory/done_order_edit_product_id.html',context)


def done_order_add_product(request,dk):
    order = Order.objects.get(id=dk)

    if request.POST:
        form = OrderItemForm(request.POST,initial={'order':order})
        if form.is_valid():
            form.add_new_order_item()
            form.save()
            return HttpResponseRedirect('/homepage/new_all/last_order/edit/%s' %order.id)
    else:
        form = OrderItemForm(initial={'order':order})

    context = {
        'form_order':form,
        'order':order,
    }
    context.update(csrf(request))
    return render(request,'inventory/edit_order_add.html',context)











def edit_all(request):
    return render(request,'inventory/edit_all.html')


def edit_orders_section(request):
    orders = Order.objects.all()
    vendors = Supply.objects.all()
    query= request.GET.get('vendor_search')
    query_first = request.GET.get('date_start')
    query_last = request.GET.get('date_end')

    if query:
        orders = orders.filter(vendor__title__icontains=query)
    if query_first and query_last:
        orders = orders.filter(date__range=[query_first,query_last])
    context={
        'orders':orders,
        'vendors':vendors,
    }

    return render(request, 'inventory/orders_edit_section_NEW.html',context)



def products_edit_section(request):
    products =Product.objects.all()
    vendors =Supply.objects.all()
    query =request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(title__contains=query)|
            Q(category__title__contains=query)|
            Q(description__icontains=query)
        ).distinct()
    context={
        'products':products,
        'vendors':vendors,
    }
    return render(request, 'inventory/products_edit_section_NEW.html',context)



def edit_product_id(request,dk):
    product = Product.objects.get(id=dk)
    if request.POST:
        form  = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            form_name = form.cleaned_data
            messages.success(request,'Το %s αποθηκεύτηκε' %form_name )
            return HttpResponseRedirect('/homepage/edit_all/products/')
    else:
        form = ProductForm(instance=product)

    context= {
        'form':form,
        'product': product,
    }
    context.update(csrf(request))
    return render(request, 'inventory/edit_product_id.html',context)


def edit_product_vendor_id(request,dk):
    vendors = Supply.objects.all()
    vendor = Supply.objects.get(id=dk)
    products = Product.objects.all().filter(supplier_id =dk)
    query =request.GET.get('search_pro')
    if query:
        products=products.filter(title__contains=query)
    context={
        'products':products,
        'vendors':vendors,
        'vendor':vendor
    }
    return render(request,'inventory/products_edit_choose_vendor.html',context)





def edit_order(request, dk):
    order = Order.objects.get(id=dk)
    products = order.orderitem_set.all()
    if request.POST:
        form_o =OrderEditForm(request.POST,instance=order)
        if form_o.is_valid():
            form_o.save(commit=False)
            form_o.update_vendor(pk=order.id)
            form_o.save()
            messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
            return redirect('/')
    else:
        form_o = OrderEditForm(instance=order)
    context={
        'form':form_o,
        'products':products,
        'order_id':order,
    }
    context.update(csrf(request))
    return render(request,'inventory/edit_order.html',context)

def edit_order_id(request,dk):
    order_item= OrderItem.objects.get(id=dk)
    if request.POST:
        form =OrderItemForm(request.POST,instance=order_item)
        if form.is_valid():
            form.save(commit=False)
            form.update_order(mod=dk)
            form.update_stock_and_vendor(pk=dk)
            form.save()
            messages.success(request,"Οι αλλαγές αποθηκεύτηκαν")
            return HttpResponseRedirect('/homepage/edit_all/order/%s' %order_item.order.id)

    else:
        form =OrderItemForm(instance=order_item)

    context={

        'form_i':form,
        'order_item':order_item

    }
    context.update(csrf(request))
    return render(request, 'inventory/edit_order_id_New.html',context)



def delete_order_id(request,dk):
    order_item = OrderItem.objects.get(id=dk)
    order = Order.objects.get(id=order_item.order.id)
    order_item.delete_order_item(foo=dk)
    order_item.delete()
    context={
        'order':order,
        'order_item':order_item

    }
    return render(request,'inventory/delete_order_id.html',context)


def add_order_id(request,dk):
    order = Order.objects.get(id=dk)

    if request.POST:
        form = OrderItemForm(request.POST,initial={'order':order})
        if form.is_valid():
            form.add_new_order_item()
            form.save()
            return redirect('/homepage/edit_all/')
    else:
        form = OrderItemForm(initial={'order':order})

    context = {
        'form_order':form,
        'order':order,
    }
    context.update(csrf(request))
    return render(request,'inventory/edit_order_add.html',context)




def edit_vendor_section(request):
    vendors = Supply.objects.all()
    data =request.GET.get('vendor_search')
    if data:
        query = Supply.objects.all().filter(title__icontains=data)
    else:
        query=None


    context ={
        'query':query,
        'vendors':vendors
    }
    return render(request, 'inventory/vendors_edit_section_NEW.html',context)

def edit_vendor_id(request, dk):
    data =request.GET.get('vendor_search')
    if data:
        query = Supply.objects.all().filter(title__icontains=data)
    else:
        query=None
    vendors = Supply.objects.all()
    vendor =Supply.objects.get(id=dk)
    if request.POST:
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            vendor_name = form.cleaned_data['title']
            messages.success(request,'Οι αλλαγές στον Προμηθευτή %s ολοκληρώθηκαν.' % vendor_name)
            return HttpResponseRedirect('/homepage/edit_all/vendors/')
    else:
        form = VendorForm(instance=vendor)
    context={
        'query':query,
        'form':form,
        'vendors':vendors
    }
    context.update(csrf(request))
    return render(request,'inventory/vendor_edit_id.html',context)




def informations_inventory(request):
    return render(request, 'inventory/inve_informations/inventory_informations.html')


def inventory_info_calendar(request):
    items = OrderItem.objects.all().order_by('-order__date')
    query = request.GET.get('search_pro')
    if query:
        items = items.filter(
            Q(product__title__icontains =query)|
            Q(order__vendor__title__icontains =query)|
            Q(order__code__icontains =query)).distinct()


    context = {
        'items':items
    }

    return render(request, 'inventory/inve_informations/inventory_info_calendar.html',context)

def info_order(request):
    orders = Order.objects.all().order_by('-date')
    query = request.GET.get('search_pro')
    if query:
        orders = orders.filter(
            Q(code__icontains=query)|
            Q(vendor__title__icontains =query)
        ).distinct()
    context={
        'orders':orders
    }
    return render(request,'inventory/inve_informations/order_informations.html',context)




def info_calendar_payments(request):
    payments = PayOrders.objects.all()
    query = request.GET.get('search_pro')
    if query:
        payments = payments.filter(
            Q(date__icontains=query)|
            Q(title__vendor__title__icontains =query)|
            Q(receipt__icontains =query)
        ).distinct()
    context = {
        'payments':payments,
    }
    return render(request, 'inventory/inve_informations/info_calendar_pay.html',context)




def info_products(request):
    products = Product.objects.all()
    query = request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(description__icontains = query)|
            Q(title__icontains =query)|
            Q(category__title__icontains =query)|
            Q(supplier__title__icontains=query)).distinct()

    context = {
        'products': products
    }
    return render(request,'inventory/inve_informations/info_products.html',context)

def info_products_id(request,dk):
    product = Product.objects.get(id=dk)
    order_items = product.orderitem_set.all().order_by('-order__date')
    context ={
        'product': product,
        'products': order_items
    }
    return render(request,'inventory/inve_informations/info_products_id.html', context)

def info_products_category(request):
    products = Product.objects.all().order_by('category')
    query = request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(description__icontains = query)|
            Q(title__icontains =query)|
            Q(category__title__icontains =query)|
            Q(supplier__title__icontains=query)).distinct()

    context = {
        'products': products
    }
    return render(request,'inventory/inve_informations/info_products_category.html',context)


def info_products_vendors(request):
    products = Product.objects.all().order_by('supplier')
    query = request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(description__icontains = query)|
            Q(title__icontains =query)|
            Q(category__title__icontains =query)|
            Q(supplier__title__icontains=query)).distinct()

    context = {
        'products': products
    }
    return render(request,'inventory/inve_informations/info_products_vendor.html',context)



def info_products_xondriki(request):
    products = Product.objects.all().filter(carousel="a")
    query = request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(description__icontains = query)|
            Q(title__icontains =query)|
            Q(category__title__icontains =query)|
            Q(supplier__title__icontains=query)).distinct()

    context = {
        'products': products
    }
    return render(request,'inventory/inve_informations/info_products_xondriki.html',context)




def info_vendors_section(request):
    return render(request,'inventory/inve_vendor_informations/info_vendor_section.html')


def info_vendor_ipoloipo(request):
    vendors = Supply.objects.all()
    query = request.GET.get('search_pro')
    if query:
        vendors=vendors.filter(title__icontains=query)
    context ={
        'vendors':vendors
    }
    return render(request,'inventory/inve_vendor_informations/info_vendor_ipoloipo.html',context)


def info_vendor_ipoloipo_id(request,dk):
    vendors = Supply.objects.all()
    query = request.GET.get('search_pro')
    if query:
        vendors=vendors.filter(title__icontains=query)
    vendor = Supply.objects.get(id=dk)
    orders = vendor.order_set.all().order_by('-date')
    order_pay = PayOrders.objects.all().filter(title__vendor__title__icontains=vendor).order_by('-date')
    context ={
        'orders':orders,
        'orders_pay':order_pay,
        'vendors':vendors
    }
    return render(request,'inventory/inve_vendor_informations/info_vendor_ipoloipo_id.html',context)

def info_vendor_order(request):
    orders =Order.objects.all().order_by('vendor__title')
    query = request.GET.get('search_pro')
    if query:
        orders=orders.filter(vendor__title__icontains=query).order_by('vendor__title')
    context ={
        'orders':orders
    }
    return render(request,'inventory/inve_vendor_informations/info_order_vendor.html',context)

def info_vendor_order_id(request,dk):
    orders =Order.objects.all().order_by('vendor__title')
    query = request.GET.get('search_pro')
    if query:
        orders=orders.filter(vendor__title__icontains=query).order_by('vendor__title')
    order = Order.objects.get(id=dk)
    order_items =order.orderitem_set.all()
    context={
        'orders':orders,
        'order_item':order_items
    }
    return render(request,'inventory/inve_vendor_informations/info_order_vendor_id.html',context)




def info_vendor_personal_stuff(request):
    vendors = Supply.objects.all()
    query = request.GET.get('search_pro')
    if query:
        vendors=vendors.filter(vendor__title__icontains=query)
    context ={
        'vendors':vendors
    }
    return render(request,'inventory/inve_vendor_informations/info_vendors_all_personal_data.html',context)





def pay_homepage(request):
    return render(request,'inventory/pay_section/pay_homepage.html')

def pay_orders(request):
    orders = Order.objects.all().filter(status="p").order_by('-date')
    context ={
        'orders':orders
    }
    return render(request,'inventory/pay_section/pay_orders.html',context)



def pay_orders_repayment(request,dk):
    orders = Order.objects.all().filter(status="p").order_by('-date')
    order = Order.objects.get(id=dk)
    title =order.code
    value =order.total_price - order.credit_balance
    if request.POST:
        form = PayOrderFrom(request.POST,initial={'title':Order.objects.get(id=dk),'value':value,})
        if form.is_valid():
            form.save()
            form.update_order_and_vendor()

            messages.info(request,'Η αποπληρωμή του τιμολογίου %s ενημερώθηκε.'% title)
            return HttpResponseRedirect('/πληρωμές/αποπληρωμές-τιμολογίων/')
    else:
        form = PayOrderFrom(initial={'title':Order.objects.get(id=dk),'value':value,})
    context={
        'order':order,
        'form':form,
        'orders':orders,
    }
    context.update(csrf(request))
    return render(request,'inventory/pay_section/pay_orders_repayment.html',context)

def pay_orders_doseis(request):
    orders = Order.objects.all().filter(status="d").order_by('-date')
    context ={
        'orders':orders
    }
    return render(request,'inventory/pay_section/pay_orders_doseis.html',context)

def pay_order_doseis_id(request,dk):
    orders = Order.objects.all().filter(status="d").order_by('-date')
    order = Order.objects.get(id=dk)
    pay_orders = PayOrders.objects.all().filter(title__code=order.code)
    title =order.code
    value =order.total_price - order.credit_balance
    if request.POST:
        form = PayOrderFrom(request.POST,initial={'title':Order.objects.get(id=dk),'value':value,})
        if form.is_valid():
            form.save()
            form.update_order_and_vendor()

            messages.info(request,'Η αποπληρωμή του τιμολογίου %s ενημερώθηκε.'% title)
            return HttpResponseRedirect('/πληρωμές/αποπληρωμές-τιμολογίων/')
    else:
        form = PayOrderFrom(initial={'title':Order.objects.get(id=dk),'value':value,})
    context={
        'order':order,
        'form':form,
        'orders':orders,
        'pay_orders':pay_orders,
    }
    context.update(csrf(request))
    return render(request,'inventory/pay_section/pay_orders_doseis_id.html',context)



def pay_orders_fullpayment(request):
    orders = Order.objects.all().filter(status="a").order_by('-date')
    context ={
        'orders':orders
    }
    return render(request,'inventory/pay_section/pay_orders_fullpayment.html',context)

def pay_orders_fullpayment_id(request, dk):
    orders = Order.objects.all().filter(status="a").order_by('-date')
    order = Order.objects.get(id=dk)
    pay_orders = PayOrders.objects.all().filter(title__code=order.code)
    context={
        'order':order,
        'orders':orders,
        'pay_orders':pay_orders,
    }

    return render(request,'inventory/pay_section/pay_order_fullpayment_id.html',context)


def pay_order_delete_id(request,dk):
    pay_order =PayOrders.objects.get(id=dk)
    pay_order.delete_pay_order(dk=dk)
    context ={
        'pay_order':pay_order
    }
    return render(request,'inventory/pay_section/pay_order_delete_id.html',context)

