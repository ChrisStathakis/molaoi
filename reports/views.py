from django.shortcuts import render
from products.models import *
from inventory_manager.models import *
from PoS.models import *
from django.db.models import Q
from transcations.models import *
from django.db.models import Avg, Max, Min, Sum
from products.utils import *
from esoda_katastimata.models import AddEsoda
from django.template.context_processors import csrf
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from PoS.models import *
from dateutil.relativedelta import relativedelta
import datetime
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
def diff_month(date_start, date_end):
    return (date_end.year - date_start.year)*12 + (date_end.month - date_start.month)
# Create your views here.
def homepage(request):
    return render(request,'')

from django.db.models import Sum

def get_data(date_start, date_end):
    all_checks = CheckOrder.objects.filter(date_expire__range=[date_start, date_end])
    bills = Order_Fixed_Cost.objects.filter(date__range=[date_start, date_end], active='b')
    payroll = CreatePersonSalaryCost.objects.filter(day_expire__range=[date_start, date_end])
    incomes = AddEsoda.objects.filter(title__range=[date_start, date_end])
    return [all_checks, bills, payroll, incomes]

def get_data_per_month(incomes, all_checks, bills, payroll, month):
    data = incomes.filter(title__month=month.month).aggregate(Sum('sinolo_olon'))['sinolo_olon__sum'] if incomes.filter(title__month=month.month).aggregate(Sum('sinolo_olon'))['sinolo_olon__sum'] else 0
    data_checks = all_checks.filter(date_expire__month=month.month).aggregate(Sum('value'))['value__sum']
    bills_checks = bills.filter(date__month=month.month).aggregate(Sum('price'))['price__sum']
    payroll_checks = payroll.filter(day_expire__month = month.month).aggregate(Sum('value'))['value__sum'] if payroll.filter(day_expire__month = month.month).aggregate(Sum('value'))['value__sum'] else 0
    return [data, data_checks, bills_checks, payroll_checks]

def giorgos_reports(request):
    date_now = datetime.datetime.now()
    date_end = datetime.datetime(datetime.datetime.now().year, 12, 31)
    date_start = datetime.datetime(datetime.datetime.now().year, 1, 1)
    all_checks, bills, payroll, incomes = get_data(date_start=date_start, date_end=date_end)

    date_start_last = date_start - relativedelta(years=1)
    date_end_last = date_end - relativedelta(years=1)
    all_checks_last, bills_last, payroll_last, incomes_last = get_data(date_start=date_start_last, date_end=date_end_last)

    incomes_per_month = {}
    outcomes_per_month = {}
    bills_per_month = {}
    payroll_per_month = {}
    incomes_per_month_last = {}
    outcomes_per_month_last = {}
    bills_per_month_last = {}
    payroll_per_month_last = {}
    months = (date_end.month - date_start.month)
    count = 0
    while count < months+1:
        month = date_end - relativedelta(month=count+1)
        print(month.strftime("%B"))
        data, data_checks, bills_checks, payroll_checks = get_data_per_month(incomes=incomes,
                                                                             all_checks=all_checks,
                                                                             bills=bills,
                                                                             payroll=payroll,
                                                                             month=month)
        data_last, data_checks_last, bills_checks_last, payroll_checks_last = get_data_per_month(incomes=incomes_last,
                                                                             all_checks=all_checks_last,
                                                                             bills=bills_last,
                                                                             payroll=payroll_last,
                                                                             month=month)
        print(month.month, data, data_last)
        payroll_per_month[month.strftime("%B")] = payroll_checks
        bills_per_month[month.strftime("%B")] = bills_checks
        incomes_per_month[month.strftime("%B")] = data
        outcomes_per_month[month.strftime("%B")] = data_checks
        payroll_per_month_last[month.strftime("%B")] = payroll_checks_last
        bills_per_month_last[month.strftime("%B")] = bills_checks_last
        incomes_per_month_last[month.strftime("%B")] = data_last
        outcomes_per_month_last[month.strftime("%B")] = data_checks_last
        count +=1
    mo = MONTHS
    incomes_order = []
    incomes_order_last = []
    outcomes_order = []
    bills_order =[]
    payroll_order =[]
    for month in MONTHS:
        try:
            incomes_order.append((month, incomes_per_month[month]))
        except:
            incomes_order.append((month, 0))

        try:
            incomes_order_last.append((month, incomes_per_month_last[month]))
        except:
            incomes_order_last.append((month, 0))
        try:
            if outcomes_per_month[month] == None:
                outcomes_per_month = 0
            outcomes_order.append((month, outcomes_per_month[month]))
        except:
            outcomes_order.append((month, 0))
        try:
            if bills_per_month[month] == None:
                bills_per_month = 0
            bills_order.append((month, bills_per_month[month]))
        except:
            bills_order.append((month, 0))
        try:
            if payroll_per_month[month] == None:
                bills_per_month = 0
            payroll_order.append((month, payroll_per_month[month]))
        except:
            payroll_order.append((month, 0))
    skroutz_data = None
    cat_name = 1
    skroutz_id = None
    if request.GET:
        skroutz_name = request.GET.get('skroutz_name')
        cat_name = request.GET.get('cat_name')
        skroutz_id = request.GET.get('skroutz_id')
    context = locals()
    return render(request, 'katastimata_esoda/giorgos_anal.html', context)


def warehouse(request):
    title = "Αποθήκη"
    products = Product.objects.all()
    categories = Category.objects.all()
    vendors = Supply.objects.all()
    orders  =Order.objects.all()
    avg_cat = show_avg_per_cat()
    avg_vendor = show_avg_per_vendor()
    avg_order = show_avg_per_order()




    context = {
        'title':title,
        'products':products,
        'categories':categories,
        'vendors':vendors,
        'orders':orders,
        'avg_cat':avg_cat,
        'avg_vendor':avg_vendor,
       'avg_order':avg_order,

    }
    return render(request,'reports/warehouse.html', context)




#---Products--------------------------------------------------------------------------------------------------------------




def products(request):
    title= "Προιόντα"
    products = Product.objects.all()
    categories = Category.objects.all()
    vendors = Supply.objects.all()

    #get data from filters
    category = request.POST.getlist('category')
    vendor = request.POST.getlist('vendor')
    site_status = request.POST.get('site_status')
    ware_status = request.POST.get('ware_status')
    btwob = request.POST.get('btwob_status')

    #use the filters to filter the products without color or size

    if category:
        products=products.filter(category__title__in = category)
    if vendor:
        products=products.filter(supplier__title__in = vendor)
    if site_status:
        products = products.filter(status__in=site_status)
    if ware_status:
        products = products.filter(ware_active = ware_status)
    if btwob:
        products = products.filter(carousel =btwob)



    #create size and color for the products
    colors = ColorAttribute.objects.all().filter(product__in =products).order_by('title')
    colors= [ele.title for ele in colors if Color.objects.get(title = ele.title)]
    colors_unique =[]
    for ele in colors:
        if ele in colors_unique:
            pass
        else:
            colors_unique.append(ele)

    color_name = request.POST.getlist('color_name')

    product_with_colors=None

    if color_name:
        colors_picked = Color.objects.all().filter(title__in = color_name)
        product_with_colors = ColorAttribute.objects.all().filter(title__in=colors_picked)

        if category:
            product_with_colors = product_with_colors.filter(product__category__title__in = category)


        if vendor:
            product_with_colors = product_with_colors.filter(product__supplier__title__in = vendor)

        if site_status:
            product_with_colors = product_with_colors.filter(product__status__in=site_status)

        if ware_status:
            product_with_colors = product_with_colors.filter(product__ware_active = ware_status)

        if btwob:
            product_with_colors = product_with_colors.filter(product__carousel =btwob)

    #if we get a color or size request, we change the way we show
    # the products.
    #if only size_picked
    size_name = request.POST.getlist('size_name')
    products_final=None

    size_check = None
    size_products =None
    product_with_sizes =None
    if size_name:
            size_picked =Size.objects.all().filter(title__in = size_name)
            product_with_sizes =SizeAttribute.objects.all().filter(title__in=size_picked)


            if category:
                product_with_sizes = product_with_sizes.filter(color__product__category__title__in = category)
            if vendor:
               product_with_sizes = product_with_sizes.filter(color__product__supplier__title__in = vendor)
            if site_status:
                product_with_sizes = product_with_sizes.filter(color__product__status__in=site_status)
            if ware_status:
                product_with_sizes = product_with_sizes.filter(color__product__ware_active = ware_status)
            if btwob:
                product_with_sizes = product_with_sizes.filter(color__product__carousel =btwob)






    '''
    #if we get a color or size request, we change the way we show
    # the products.
    #if only size_picked
    size_products =None
    if size_name:
        size_products = SizeAttribute.objects.all().filter(title__title__in =size_name,color__product__in=products).order_by('color__title')
    print(size_products)

    #if picked color then return this
    color_products=None
    if color_name:
        color_products = ColorAttribute.objects.all().filter(title__title__in =color_name,product__in=products)
        if size_products:
            color_products_with_size=[]

            for ele in size_products:
                if ele.color.product.ele in color_products:
                    color_products_with_size.append(ele.color)
            print(color_products_with_size)
            color_products=color_products_with_size



    '''


    sizes = SizeAttribute.objects.all().filter(color__product__in = products).distinct().order_by('title')
    sizes= [ele.title for ele in sizes if Size.objects.get(title = ele.title)]
    sizes_unique =[]
    for ele in sizes:
        if ele in sizes_unique:
            pass
        else:
            sizes_unique.append(ele)

    query =request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(title__contains=query)|
            Q(category__title__contains=query)|
            Q(supplier__title__contains=query)|
            Q(description__icontains=query)
        ).distinct()

    paginator = Paginator(products,100)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context ={
        'title':title,
        'products':products,
        'categories':categories,
        'vendors':vendors,
        'colors':colors_unique,
        'sizes':sizes_unique,

        #filters
        'category_name':category,
        'vendor_name':vendor,
        'color_name':color_name,
        'size_name':size_name,



        #if the user pick color or size then the table data
        #gonna use this variables
        'size_products':product_with_sizes,
        'color_products':product_with_colors,
    }


    return render(request, 'reports/products.html', context)

def products_category(request, dk):
    category = Category.objects.get(id=dk)
    title = category.title
    products =Product.objects.all().filter(category=category)
    products_avg_price_buy = products.aggregate(Avg('price_buy'))
    products_avg_price_buy = products_avg_price_buy['price_buy__avg']
    products_total = products.count()
    products_qty = products.aggregate(Sum('reserve'))
    products_qty = products_qty['reserve__sum']
    products_total_cost = Decimal(products_qty)* Decimal(products_avg_price_buy)

    vendors =[]
    for ele in products:
        if ele.supplier in vendors:
            pass
        else:
            vendors.append(ele.supplier)
    vendors_sum ={}
    for ele in vendors:
        sum = products.filter(supplier=ele).aggregate(Avg('price_buy'))
        sum = sum['price_buy__avg']
        count = products.filter(supplier=ele).aggregate(Sum('reserve'))
        count = count['reserve__sum']
        total = Decimal(sum)* Decimal(count)
        vendors_sum[ele.title] = (count,total)

    context={
        'title':title,
        'products':products,
        'category_title':category,
        'products_qty':products_qty,
        'products_total_cost':products_total_cost,
        'vendor_sum':vendors_sum,

        'products_avg_price_buy':products_avg_price_buy,
        'product_total':products_total,
    }
    return render(request, 'reports/products.html', context)

def products_vendors(request, dk):
    title= "Προιόντα"
    products = Product.objects.all().filter(supplier__title = Supply.objects.get(id=dk))
    query =request.GET.get('search_pro')
    if query:
        products=products.filter(
            Q(title__contains=query)|
            Q(category__title__contains=query)|
            Q(supplier__title__contains=query)|
            Q(description__icontains=query)
        ).distinct()

    category = Category.objects.all()
    vendors = Supply.objects.all()
    context ={
        'title':title,
        'products':products,
        'category':category,
        'vendors':vendors,
    }
    return render(request, 'reports/products.html', context)

def product_id(request,dk):
    product = Product.objects.get(id=dk)
    order_item = OrderItem.objects.all().filter(product__title = product.title)
    change_qty = ChangeQtyOrderItem.objects.all().filter(title= product)
    title = product.title





    colors_list ={}
    if product.check_color():
        colors = ColorAttribute.objects.all().filter(product = product)
        for ele in colors:
            sizes = SizeAttribute.objects.all().filter(color =ele)
            for size in sizes:
                try:
                    colors_list[ele.title.title] += (size.title.title, size.qty)
                except:
                    colors_list[ele.title.title] = (size.title.title, size.qty)


    retail = LianikiOrderItem.objects.all().filter(title=product)


    context={
        'title':title,
        'product':product,
        'order_item':order_item,
        'color_list':colors_list,
        'change_qty':change_qty,
        'retail':retail,
    }
    return render(request,'reports/products_id.html', context)



#---Vendors--------------------------------------------------------------------------------------------------------------



def vendors(request):
    vendors = Supply.objects.all()
    taxes_city = TaxesCity.objects.all()
    title= "ΠρομηΘευτές"

    query =request.GET.get('search_pro')
    if query:
        vendors=vendors.filter(
            Q(title__icontains=query)|
            Q(afm__icontains=query)|
            Q(phone__icontains=query)|
            Q(fax__icontains=query)|
            Q(email__icontains=query)|
            Q(phone1__icontains=query)
        ).distinct()
    context ={
        'title':title,
        'vendors':vendors,
        'taxes_city':taxes_city,
    }
    return render(request, 'reports/vendors.html', context)

def vendors_per_doy(request, dk):
    doy = TaxesCity.objects.get(id=dk)
    taxes_city = TaxesCity.objects.all()
    vendors =Supply.objects.all().filter(doy=doy)
    title = doy.title
    query =request.GET.get('search_pro')
    if query:
        vendors=vendors.filter(
            Q(title__icontains=query)|
            Q(afm__icontains=query)|
            Q(phone__icontains=query)|
            Q(fax__icontains=query)|
            Q(email__icontains=query)|
            Q(phone1__icontains=query)
        ).distinct()
    context ={
        'title':title,
        'vendors':vendors,
        'taxes_city':taxes_city,
    }
    return render(request, 'reports/vendors.html', context)

def vendors_id(request,dk):
    vendor = Supply.objects.get(id=dk)
    title = vendor.title
    products = vendor.product_set.all().order_by('description')
    order = vendor.order_set.all().order_by('-date')
    context = {
        'title':title,
        "vendor":vendor,
        "products":products,
        "order":order,
    }
    return render(request, 'reports/vendors_id.html',context)



#---------------Orders----------------------------------------------------------------------------------------------------


def orders(request):
    orders_i = Order.objects.all().order_by('-date')
    vendors = Supply.objects.all()
    payment_method = PaymentMethod.objects.all()
    choices = Order.CHOICES

    title= 'Τιμολόγια'
    query =request.GET.get('search_pro')
    if query:
        orders_i = orders_i.filter(
            Q(code__icontains = query)|
            Q(vendor__title__icontains =query)
        ).distinct()

    #filters
    vendor_name = request.POST.getlist('vendor_name')
    if vendor_name:
        orders_i = orders_i.filter(vendor__title__in=vendor_name)

    payment_name = request.POST.getlist('payment_name')
    if payment_name:
        orders_i = orders_i.filter(payment_method__title__in = payment_name)

    status_name = request.POST.getlist('status_name')
    if status_name:
        orders_i =orders_i.filter(status__in=status_name)


    date_pick = request.POST.get('date_pick')
    try:
        date_range = date_pick.split('-')
        date_range[0]=date_range[0].replace(' ','')
        date_range[1]=date_range[1].replace(' ','')

        date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
        date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
        orders_i = orders_i.filter(date__range=[date_start,date_end])

    except:
        pass

    total_orders = orders_i.count()
    sum_orders = orders_i.aggregate(Sum('total_price'))
    sum_orders =sum_orders['total_price__sum']
    average_orders = orders_i.aggregate((Avg('total_price')))
    average_orders =average_orders['total_price__avg']
    taxes = orders_i.aggregate(Sum('total_taxes'))
    taxes = taxes['total_taxes__sum']

    if 'd' in status_name:
        remaining = orders_i.aggregate(Sum('credit_balance'))
        remaining=remaining['credit_balance__sum']
        remaining =sum_orders - remaining
    else:
        remaining =None
    print(status_name)
    context={
        'choices':choices,
        'choice_name':status_name,
        'remaining':remaining,
        'orders':orders_i,
        'title':title,
        'vendors':vendors,
        'payment_method':payment_method,
        'total_orders':total_orders,
        'sum_orders':sum_orders,
        'avg_orders':average_orders,
        'taxes':taxes,
    }
    return render(request, 'reports/orders.html', context)

#needs to deleted check the urls for total  annihilation
def orders_per_category(request, dk):
    vendor = Supply.objects.get(id=dk)
    orders_i = Order.objects.all().filter(vendor=vendor).order_by('-date')
    vendors = Supply.objects.all()
    title= 'Τιμολόγια'
    query =request.GET.get('search_pro')
    if query:
        orders_i = orders_i.filter(
            Q(code__icontains = query)|
            Q(vendor__title__icontains =query)
        ).distinct()

    context={
        'orders':orders_i,
        'title':title,
        'vendors':vendors,
    }
    return render(request, 'reports/orders.html', context)



def order_id(request,dk):
    order = Order.objects.get(id=dk)
    title =order.code
    products = order.orderitem_set.all()
    pay_info = order.payorders_set.all()
    pay_deposit = order.vendordepositorderpay_set.all()
    context={
        'title':title,
        'products':products,
        'pay_info':pay_info,
        'order':order,
        'deposit':pay_deposit,

    }
    return render(request, 'reports/orders_id.html', context)





#-----------------------------------Restaurant---------------------------------------------------------------------------------------------------------------------

def restaurant_reports(request):
    title ='Restaurant'
    resto_orders = RestoOrder.objects.all()
    day = DailyIncomeGreG.objects.all()
    month = MonthlyIncomeGreG.objects.all()
    year = YearlyIncomeGreg.objects.all()
    context={
        'title':title,
        'resto_orders':resto_orders,
        'day':day,
        'month':month,
        'year':year,
    }
    return render(request, 'reports/restaurant_homepage.html', context)



def restaurant_order_specific(request,dk):
    resto_order =RestoOrder.objects.get(id=dk)
    title= resto_order.title
    resto_items = resto_order.restoorderitem_set.all()
    context ={
        'title':title,
        'resto_order':resto_order,
        'resto_items':resto_items
    }
    return render(request, 'reports/restaurant_order.html', context)


def restautant_recipes(request):
    recipes = Recipe.objects.all()
    title = "Συνταγές"
    context ={
        'recipes':recipes,
        'title':title,
    }
    return render(request, 'reports/restaurant_recipes.html', context)
#---------------------------------Outcomes--------------------------------------------




#build from the begin FUCK!
def outcome(request):
    day_now = datetime.datetime.now()
    year_start = datetime.datetime(datetime.datetime.now().year,1,1)
    title ="Συνολική Εικόνα Επιχείρησης"


    #overall data for bills
    bills_all = Order_Fixed_Cost.objects.all().filter(date__range=[year_start,day_now]).aggregate(Sum('price'))
    bills_all = bills_all['price__sum']
    bills_paid = Order_Fixed_Cost.objects.all().filter(date__range=[year_start,day_now],active='b' ).aggregate(Sum('price'))
    bills_paid = bills_paid['price__sum']
    bills_pending = Order_Fixed_Cost.objects.all().filter(date__range=[year_start, day_now], active='a').aggregate(Sum('price'))
    bills_pending = bills_pending['price__sum']

    #overall data for expenses
    expenses_all = Pagia_Exoda_Order.objects.all().filter(date__range=[year_start,day_now]).aggregate(Sum('price'))
    expenses_all= expenses_all['price__sum']
    expenses_paid = Pagia_Exoda_Order.objects.all().filter(date__range=[year_start,day_now],active='b' ).aggregate(Sum('price'))
    expenses_paid = expenses_paid['price__sum']
    expenses_pending = Pagia_Exoda_Order.objects.all().filter(date__range=[year_start, day_now], active='a').aggregate(Sum('price'))
    expenses_pending = expenses_pending['price__sum']

    #overall data for people

    person_all = CreatePersonSalaryCost.objects.all().filter(day_added__range=[year_start,day_now]).aggregate(Sum('value'))
    person_all = person_all['value__sum']
    person_paid = CreatePersonSalaryCost.objects.all().filter(day_added__range=[year_start,day_now], status='b').aggregate(Sum('value'))
    person_paid = person_paid['value__sum']
    person_pending = CreatePersonSalaryCost.objects.all().filter(day_added__range=[year_start,day_now], status='a').aggregate(Sum('value'))
    person_pending = person_pending['value__sum']



    #blls analytic
    fixed_costs = Fixed_Costs_item.objects.all()
    orders_data = Order_Fixed_Cost.objects.all().filter(date__range=[year_start,day_now])
    bills_analytics = {}
    for bill in fixed_costs:
        bill_sum = orders_data.filter(category=bill, active='a').aggregate(Sum('price'))
        bill_sum = bill_sum['price__sum']
        bills_analytics[bill.title]=bill_sum

    #expenses analytic
    expenses_data = Pagia_Exoda_Order.objects.all().filter(date__range=[year_start,day_now])
    pagia_exoda = Pagia_Exoda.objects.all()
    expense_analytics ={}
    for expense in pagia_exoda:
        expenses_sum = expenses_data.filter(category=expense, active='a').aggregate(Sum('price'))
        expenses_sum = expenses_sum['price__sum']
        expense_analytics[expense.title] = expenses_sum

    #occupation_analytic
    occupations = Occupation.objects.all()
    person_data = CreatePersonSalaryCost.objects.all().filter(day_added__range=[year_start,day_now])
    occupation_analytics={}

    for occup in occupations:
        occup_sum = person_data.filter(status='b', person__occupation=occup).aggregate(Sum('value'))
        occup_sum =occup_sum['value__sum']
        occupation_analytics[occup.title] = occup_sum

    logar = Fixed_Costs_item.objects.all()


    #what the fuck is that?
    pagia_id=1
    context = {
        'title':title,
        'fixed_costs':fixed_costs,
        'occupations':occupations,
        'log':logar,
        'pagia_id':pagia_id,
        'pagia_exoda':pagia_exoda,

        'bills_all':bills_all,
        'bills_paid':bills_paid,
        'bills_pending':bills_pending,

        'expenses_all':expenses_all,
        'expenses_paid':expenses_paid,
        'expenses_pending':expenses_pending,

        'person_all':person_all,
        'person_paid':person_paid,
        'person_pending':person_pending,

        #analytics
        'bill_analytics':bills_analytics,
        'expenses_analytics':expense_analytics,
        'occupation_analytics':occupation_analytics,
    }
    return render(request,'reports/outcome.html', context)

def checks_reports(request):
    pagia_id=1
    checks = CheckOrder.objects.all().order_by('-date_expire')
    vendors = Supply.objects.all()
    status = CheckOrder.CHOICES


    payment_method = PaymentMethod.objects.all().filter(payment_group__title = 'Bank')
    payment_method_groups = PaymentMethodGroup.objects.all()






    #filters section
    payment_name = None
    vendor_name = None
    status_name = None
    date_pick =None

    if request.POST:
        payment_name = request.POST.getlist('payment_name')
        vendor_name = request.POST.getlist('vendor')
        status_name = request.POST.getlist('status_name')
        date_pick = request.POST.get('date_pick')



        if payment_name:
            checks = checks.filter(place__title__in=payment_name)

        if vendor_name:
            checks = checks.filter(debtor__title__in = vendor_name)

        if status_name:
            checks =checks.filter(status__in =status_name)
        try:
            date_range = date_pick.split('-')
            date_range[0]=date_range[0].replace(' ','')
            date_range[1]=date_range[1].replace(' ','')

            date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

            checks = checks.filter(date_expire__range=[date_start,date_end])


        except:
            date_pick = None


    # get reports after the filters!
    data_per_bank = {}
    if payment_name:
        for payment in payment_name:
            checks_paid = checks.filter(status='b',place__title=payment).aggregate(Sum('value'))
            checks_pending = checks.filter(status='a',place__title = payment).aggregate(Sum('value'))
            data_per_bank[payment.title] = (checks_paid['value__sum'],checks_pending['value__sum'])
    else:
        for payment in payment_method:
            checks_paid = checks.filter(status='b',place=payment).aggregate(Sum('value'))
            checks_pending = checks.filter(status='a',place = payment).aggregate(Sum('value'))
            data_per_bank[payment.title] = (checks_paid['value__sum'],checks_pending['value__sum'])

    checks_paid = checks.filter(status='b').aggregate(Sum('value'))
    checks_paid =checks_paid['value__sum']

    checks_pending = checks.filter(status='a').aggregate(Sum('value'))
    checks_pending = checks_pending['value__sum']





    context = {
        'pagia_id':pagia_id,
        'checks':checks,
        'status':status,
        'vendors':vendors,
        'payment_method':payment_method,
        'payment_method_groups':payment_method_groups,

        'checks_paid':checks_paid,
        'checks_pending':checks_pending,


        #filters
        'payment_name':payment_name,
        'status_name':status_name,
        'date_pick':date_pick,
        'vendor_name':vendor_name,

        #reports
        'data_per_bank':data_per_bank,

    }
    return render(request, 'reports/check_order_reports.html', context)



def payment_analysis(request):
    title = 'Αναλυση όλων των πληρωμών'
    pagia_id=1


    #filters
    vendors = Supply.objects.all()
    payment_method = PaymentMethod.objects.all()
    payment_method_groups = PaymentMethodGroup.objects.all()
    bills_accounts = Fixed_Costs_item.objects.all()
    occupation_accounts = Occupation.objects.all()
    assets_accounts = Pagia_Exoda.objects.all()


    #collect data for the main table
    deposit_vendor = VendorDepositOrder.objects.all().order_by('-day_added')
    order_pay = Order.objects.all().order_by('-date').exclude(status='p')
    bills = Order_Fixed_Cost.objects.all().filter(active='b').order_by('-date')
    assets = Pagia_Exoda_Order.objects.all().filter(active='b').order_by('-date')
    person = CreatePersonSalaryCost.objects.all().filter(status='b').order_by('-day_expire')

    #create the sum on the total table
    sum_deposit_vendor = deposit_vendor.aggregate(Sum('value'))
    sum_per_payment_method ={}
    for ele in payment_method:
        sum = deposit_vendor.filter(payment_method=ele).aggregate(Sum('value'))
        sum_per_payment_method[ele.title] = sum['value__sum']
    sum_deposit_vendor = sum_deposit_vendor['value__sum']
    total_payed_orders = sum_deposit_vendor



    #filters section
    payment_name = None
    vendor_name = None
    date_pick =None
    bills_name = None
    assets_name = None
    person_name = None
    if request.POST:
        payment_name = request.POST.getlist('payment_name')
        vendor_name = request.POST.getlist('vendor_name')
        date_pick = request.POST.get('date_pick')
        assets_name = request.POST.getlist('asset_name')
        person_name = request.POST.getlist('person_name')
        bills_name = request.POST.getlist('bill_name')


        if payment_name:
            deposit_vendor = deposit_vendor.filter(payment_method__title__in=payment_name)
            order_pay = order_pay.filter(payment_method__title__in=payment_name)
            bills =bills.filter(payment_method__title__in=payment_name)
            assets = assets.filter(payment_method__title__in=payment_name)
            person = person.filter(payment_method__title__in=payment_name)


        date_start = None
        date_end = None
        try:
            date_range = date_pick.split('-')
            date_range[0]=date_range[0].replace(' ','')
            date_range[1]=date_range[1].replace(' ','')

            date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

            deposit_vendor = deposit_vendor.filter(day_added__range=[date_start,date_end])
            order_pay = order_pay.filter(date__range=[date_start,date_end])
            bills = bills.filter(date__range=[date_start,date_end])
            assets = assets.filter(date__range=[date_start,date_end])
            person = person.filter(day_expire__range=[date_start,date_end])
        except:
            date_pick = None


        if vendor_name:
            deposit_vendor = deposit_vendor.filter(vendor__title__in =vendor_name)
            order_pay = order_pay.filter(vendor__title__in= vendor_name)
        else:
            if date_pick or payment_name:
                 deposit_vendor = deposit_vendor.filter(day_added__range=[date_start,date_end])
                 order_pay = order_pay.filter(date__range=[date_start,date_end])

            else:
                deposit_vendor =None
                order_pay = None


        if bills_name:
            bills = bills.filter(category__title__in =bills_name)
        else:
            if date_pick:
                bills = bills.filter(date__range=[date_start,date_end])
            else:
                bills =None

        if assets_name:
            assets = assets.filter(category__title__in = assets_name)
        else:
            if date_pick:
                assets = assets.filter(date__range=[date_start,date_end])
            else:
                assets = None

        if person_name:
            person = person.filter(person__occupation__title__in = person_name)
        else:
            if date_pick:
                person = person.filter(day_expire__range=[date_start,date_end])
            else:
                person = None

    data_per_person=None
    data_per_assets=None
    data_per_bill=None
    data_per_vendor=None
    #get totals on every category
    if deposit_vendor:
        deposit_vendor_sum = deposit_vendor.aggregate(Sum('value'))
        deposit_vendor_sum =deposit_vendor_sum['value__sum']
    else:
        deposit_vendor_sum = 0

    if order_pay:
        order_pay_sum = order_pay.aggregate(Sum('credit_balance'))
        order_pay_sum =order_pay_sum['credit_balance__sum']
    else:
        order_pay_sum = 0

    if bills:
        bills_sum = bills.aggregate(Sum('credit_balance'))
        bills_sum = bills_sum['credit_balance__sum']
    else:
        bills_sum = 0

    if assets:
        assets_sum = assets.aggregate(Sum('credit_balance'))
        assets_sum =assets_sum['credit_balance__sum']
    else:
        assets_sum = 0

    if person:
        person_sum = person.aggregate(Sum('paid_value'))
        person_sum = person_sum['paid_value__sum']
    else:
        person_sum = 0

    #gets total from every category

    list_of_pay_methods = {}

    for payment in payment_method:
        if deposit_vendor:
            deposit_vendor_payment = deposit_vendor.filter(payment_method__title =payment).aggregate(Sum('value'))
            deposit_vendor_payment  = deposit_vendor_payment['value__sum']
            if deposit_vendor_payment == None:
                deposit_vendor_payment = 0
        else:
            deposit_vendor_payment = 0

        if order_pay:
            order_pay_payment = order_pay.filter(payment_method__title =payment).aggregate(Sum('credit_balance'))
            order_pay_payment = order_pay_payment['credit_balance__sum']
            if order_pay_payment == None:
                order_pay_payment =0
        else:
            order_pay_payment = 0

        if bills:
            bills_sum_payment = bills.filter(payment_method__title =payment).aggregate(Sum('credit_balance'))
            bills_sum_payment = bills_sum_payment['credit_balance__sum']
            if bills_sum_payment == None:
                bills_sum_payment=0
        else:
            bills_sum_payment = 0

        if assets:
            assets_sum_payment = assets.filter(payment_method__title =payment).aggregate(Sum('credit_balance'))
            assets_sum_payment = assets_sum_payment['credit_balance__sum']
            if assets_sum_payment == None:
                assets_sum_payment =0
        else:
            assets_sum_payment = 0

        if person:
            person_sum_payment = person.filter(payment_method__title =payment).aggregate(Sum('paid_value'))
            person_sum_payment = person_sum_payment['paid_value__sum']
            if person_sum_payment == None:
                person_sum_payment = 0
        else:
            person_sum_payment = 0

        total_sum = Decimal(deposit_vendor_payment) + Decimal(order_pay_payment) + Decimal(bills_sum_payment) + Decimal(assets_sum_payment) + Decimal(person_sum_payment)
        list_of_pay_methods[payment.title]= total_sum


        #gets total on specific category
        data_per_vendor ={}
        if vendor_name:
            for ele in vendor_name:
                vendor_deposit_sum = deposit_vendor.filter(vendor__title = ele).aggregate(Sum('value'))
                vendor_order_sum = order_pay.filter(vendor__title = ele).aggregate(Sum('total_price'))
                data_per_vendor[ele] = (vendor_deposit_sum['value__sum'],vendor_order_sum['total_price__sum'])

        data_per_bill = {}
        if bills_name:
            for ele in bills_name:
                bills_sum_a = bills.filter(category__title = ele).aggregate(Sum('credit_balance'))
                data_per_bill[ele] = bills_sum_a['credit_balance__sum']

        data_per_assets = {}
        if assets_name:
            for ele in assets_name:
                assets_sum_a = assets.filter(category__title = ele).aggregate(Sum('credit_balance'))
                data_per_assets[ele] = assets_sum_a['credit_balance__sum']

        data_per_person ={}
        if person_name:
            for ele in person_name:
                person_sum_a = person.filter(person__occupation__title = ele).aggregate(Sum('paid_value'))
                data_per_person[ele] = person_sum_a['paid_value__sum']



    context = {

        #filters_update
        'date_pick':date_pick,
        'title':title,
        'pagia_id':pagia_id,
        'vendors':vendors,
        'payment_method':payment_method,
        'payment_method_groups':payment_method_groups,
        'payment_name':payment_name,
        'vendor_name':vendor_name,
        'assets_name':assets_name,
        'person_name':person_name,
        'bill_name':bills_name,
        'bills_account':bills_accounts,
        'assets_accounts':assets_accounts,
        'occupation_account':occupation_accounts,

        #summary data
        'deposit_vendor_sum':deposit_vendor_sum,
        'order_pay_sum':order_pay_sum,
        'bills_sum':bills_sum,
        'assets_sum':assets_sum,
        'person_sum':person_sum,
        'list_of_payment':list_of_pay_methods,

        #summary data after filtering
        'data_per_vendor':data_per_vendor,
        'data_per_bill':data_per_bill,
        'data_per_person':data_per_person,
        'data_per_assets':data_per_assets,


        #table_data
        'bills':bills,
        'person':person,
        'deposit_vendor':deposit_vendor,
        'order_pay':order_pay,
        'assets':assets,

        }

    context.update(csrf(request))
    return render(request, 'reports/payment_analysis.html', context)




def log_all(request):
    pagia_id =1
    log_all = Order_Fixed_Cost.objects.all().filter(category__category__title="Λογαριασμοί").order_by('-date')
    #get all bill ber category
    log_all_cat = Fixed_Costs_item.objects.all().filter(category__title="Λογαριασμοί")
    payment_method = PaymentMethod.objects.all()


    #FILTERS
    bill_name = None
    status_name = None
    date_pick = None
    payment_name = None
    if request.POST:
        bill_name = request.POST.get('bill_name')
        status_name = request.POST.get('status_name')
        date_pick = request.POST.get('date_pick')
        payment_name = request.POST.get('payment_name')
        if bill_name:
            log_all = log_all.filter(category__title=bill_name)
        if status_name:
            log_all = log_all.filter(active=status_name)
        if payment_name:
            log_all =log_all.filter(payment_method__title = payment_name)
        if date_pick:
            try:
                date_range = date_pick.split('-')
                date_range[0]=date_range[0].replace(' ','')
                date_range[1]=date_range[1].replace(' ','')
                print(date_range)

                date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

                log_all = log_all.filter(date__range=[date_start,date_end])
            except:
                date_pick = None

    # i made a dictionary with 2 values, the first is the total order price and the second is the paid value
    # and th third is the pending
    total_orders_per_bill ={}

    for ele in log_all_cat:
        orders = log_all.filter(category__title = ele,).aggregate(Sum('price'))
        pay_orders = log_all.filter(category__title = ele,active ='b').aggregate(Sum('price'))
        pay_order_pending = log_all.filter(category__title = ele,active ='a').aggregate(Sum('price'))
        total_orders_per_bill[ele]=orders['price__sum'],pay_orders['price__sum'],pay_order_pending['price__sum']



    context ={
        'pagia_id':pagia_id,
        #FILTERS
        'bill_name':bill_name,
        'payment_name':payment_name,

        'log_all_cat':log_all_cat,
        'log_all':log_all,

        'status_name':status_name,
        'date_pick':date_pick,
        'payment_method':payment_method,
        'total_orders_per_bill':total_orders_per_bill,
    }
    return render(request, 'reports/log_main_page.html', context)




def log_all_id(request, dk):
    log_id = Fixed_Costs_item.objects.get(id=dk)
    log_all_cat = Fixed_Costs_item.objects.all().filter(category__title="Λογαριασμοί")
    log_all =Order_Fixed_Cost.objects.all().filter(category__title=log_id.title).order_by('-date')

    context ={
        'log_all_cat':log_all_cat,
        'log_all':log_all,
        'log_id':log_id,
    }
    return render(request, 'reports/log_main_page.html', context)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def payroll_report(request):

    day_now = datetime.datetime.now()
    year_start = datetime.datetime(datetime.datetime.now().year,1,1)
    payment_method = PaymentMethod.objects.all()


    payment_category =CategoryPersonPay.objects.all()
    occupation = Occupation.objects.all()
    persons = Person.objects.all()
    all_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range =[year_start,day_now]).order_by('-day_expire')


    date_pick = None
    if request.POST:
        occup = request.POST.get('occup')
        person = request.POST.get('person')
        payment_name = request.POST.get('payment_name')
        date_pick = request.POST.get('date_pick')
        try:
            date_range = date_pick.split('-')
            date_range[0]=date_range[0].replace(' ','')
            date_range[1]=date_range[1].replace(' ','')

            date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
            all_pay = all_pay.filter(day_expire__range=[date_start,date_end])

        except:
            date_pick=None

        if occup:
            all_pay =all_pay.filter(person__occupation__title=occup)
        if person:
            all_pay = all_pay.filter(person__title = person)
        if payment_name:
            all_pay =all_pay.filter(payment_method__title=payment_name)



    paginator = Paginator(all_pay,20)
    page = request.GET.get('page')
    try:
        pays = paginator.page(page)
    except PageNotAnInteger:
        pays = paginator.page(1)
    except EmptyPage:
        pays  = paginator.page(paginator.num_pages)

    context={
        'occupation':occupation,
        'persons':persons,
        'all_pay':all_pay,
        'pays':pays,
        'payment_method':payment_method,
        'payment_category':payment_category,
        'date_pick':date_pick,

    }
    return render(request, 'reports/misthodosia_main_page.html', context)





















def misthosia_analisi(request):
    all_pay = CreatePersonSalaryCost.objects.all()
    occupation = Occupation.objects.all()
    persons = Person.objects.all()
    context={
        'occupation':occupation,
        'persons':persons,
        'all_pay':all_pay,
    }
    return render(request, 'reports/anal_misthodosias.html', context)



def misthodosia_ipal(request,dk):
    occupation = Occupation.objects.all()
    persons = Person.objects.all()
    person =Person.objects.get(id=dk)
    all_pay = CreatePersonSalaryCost.objects.all().filter(person__title=person.title)


    context={
        'title':person.title,
        'occupation':occupation,
        'persons':persons,
        'all_pay':all_pay,

    }
    return render(request, 'reports/misthodosia_main_page.html', context)

def misthodosia_occup(request,dk):
    occup = Occupation.objects.get(id=dk)
    occupation = Occupation.objects.all()
    persons = Person.objects.all()

    all_pay = CreatePersonSalaryCost.objects.all().filter(person__occupation__title = occup.title)


    context={
        'title':occup.title,
        'occupation':occupation,
        'persons':persons,
        'all_pay':all_pay,
    }
    return render(request, 'reports/misthodosia_main_page.html', context)


#---Pagia-Agores--------------------------------------------------------------------------------------------------------------


def agoresEpiskeuesReport(request,dk):

    payment_method = PaymentMethod.objects.all()
    person = PersonMastoras.objects.all()
    all_cate = Pagia_Exoda.objects.all()
    cat = Pagia_Exoda.objects.get(id=dk)
    title ='Πάγια Εξοδα'
    buy_orders = Pagia_Exoda_Order.objects.all().order_by('-date')
    search_pro = request.GET.get('search_pro')
    if search_pro:
        buy_orders =buy_orders.filter(
            Q(title__icontains=search_pro)|
            Q(category__title__icontains =search_pro)|
            Q(person__title__icontains =search_pro)
        ).distinct()

    #filters
    bill_name = None
    date_pick = None
    payment_name = None
    person_name = None

    if request.POST:
        bill_name = request.POST.get('bill_name')
        person_name = request.POST.get('person_name')
        date_pick = request.POST.get('date_pick')
        payment_name = request.POST.get('payment_name')

        if person_name:
            buy_orders = buy_orders.filter(person__title=person_name)

        if bill_name:
            buy_orders = buy_orders.filter(category__title= bill_name)

        if payment_name:
            buy_orders = buy_orders.filter(payment_method__title=payment_name)

        if date_pick:
            try:
                date_range = date_pick.split('-')
                date_range[0]=date_range[0].replace(' ','')
                date_range[1]=date_range[1].replace(' ','')
                print(date_range)

                date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

                buy_orders = buy_orders.filter(date__range=[date_start,date_end])
            except:
                date_pick = None


    #summary the reports of each category?
    sum_pending_category = {}
    sum_pending_payment_method = {}

    for ele in all_cate:
        orders_pending_sum = buy_orders.filter(category=ele, active='a').aggregate(Sum('price'))

        keep_data=[]
        for pay in payment_method:
            pay_pending = buy_orders.filter(category=ele,payment_method=pay,active='b').aggregate(Sum('price'))
            pay_paid = buy_orders.filter(category=ele,payment_method=pay, active='a').aggregate(Sum('price'))
            keep_data.append([pay.title,pay_pending['price__sum'],pay_paid['price__sum']])
        sum_pending_category[ele] = keep_data

    context ={
        'title':title,
        'buy_orders':buy_orders,
        'cat':cat,
        'all_cate':all_cate,
        'person':person,
        'payment_method':payment_method,

        'sum_pending_category':sum_pending_category,
    }
    return render(request, 'reports/pagia_agores.html',context)



def exoterikoi_sinergates(request):
    all_cate = Pagia_Exoda.objects.all()
    title = 'Εξωτερικοί συνεργάτες'
    persons = PersonMastoras.objects.all()

    search_pro = request.GET.get('search_pro')
    if search_pro:
        persons =persons.filter(
            Q(title__icontains=search_pro)|
            Q(phone__icontains =search_pro)|
            Q(phone1__icontains =search_pro)|
            Q(occupation__icontains = search_pro)
        ).distinct()

    context ={
        'title':title,


        'persons':persons,
        'all_cate':all_cate,
    }
    return render(request, 'reports/exoterikoi_si.html',context)











#---------------------------------------------------------Esoda-------------



def reports_income(request):

    #gets the data from the start of the year
    day_now= datetime.datetime.now()
    start_month = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,1)
    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_month,day_now])

    date_pick = None
    if request.POST:
        date_pick = request.POST.get('date_pick')
        if date_pick:
            if date_pick:
                try:
                    date_range = date_pick.split('-')
                    date_range[0]=date_range[0].replace(' ','')
                    date_range[1]=date_range[1].replace(' ','')


                    start_month =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                    day_now =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

                    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_month,day_now])
                except:
                    date_pick = None

    #total cost
    total_cost_sum = 0
    total_incomes_sum = 0
    orders_count = 0
    profit = 0
    if orders:
        total_cost_sum = orders.aggregate(Sum('total_cost'))
        total_cost_sum = total_cost_sum['total_cost__sum']

        #total incomes
        total_incomes_sum = orders.aggregate(Sum('paid_value'))
        total_incomes_sum = total_incomes_sum['paid_value__sum']
        orders_count =orders.count()
        profit = total_incomes_sum - total_cost_sum

    try:
        profit_in_percent = 100 - (total_incomes_sum/total_cost_sum)
    except:
        profit_in_percent =0

    average_cost = 0
    avg_profit = 0
    avg_income = 0
    if orders:
        average_cost = orders.aggregate(Avg('total_cost'))
        average_cost  = average_cost['total_cost__avg']

        avg_income = orders.aggregate(Avg('paid_value'))
        avg_income = avg_income['paid_value__avg']
        avg_profit = avg_income - average_cost


    title = 'Πωλήσεις'
    context={
        'title':title,
        'orders':orders,

        'total_cost':total_cost_sum,
        'total_income':total_incomes_sum,
        'profit':profit,
        'profit_in_percent':profit_in_percent,
        'orders_count':orders_count,

        'avg_cost':average_cost,
        'avg_income':avg_income,
        'avg_profit':avg_profit,


        'start_month':start_month,
        'day_now':day_now,



    }
    return render(request, 'reports/incomes.html', context)





def reports_specific_order(request,dk):
    order_lianiki = Lianiki_Order.objects.get(id=dk)
    order_items = order_lianiki.lianikiorderitem_set.all()
    day = DailyIncomeGreG.objects.last()
    year = YearlyIncomeGreg.objects.last()
    month = MonthlyIncomeGreG.objects.last()
    days = DailyIncomeGreG.objects.all().filter(month__title=month).order_by('-id')
    years = YearlyIncomeGreg.objects.all().order_by('-id')
    months = MonthlyIncomeGreG.objects.all().order_by('-id')

    title = 'Έσοδα'
    context={
        'title':title,
        'days':days,
        'month':month,
        'year':year,
        'months':months,
        'years':years,
        'day':day,
        'order':order_lianiki,
        'order_items':order_items,
    }
    return render(request, 'reports/income_specific_order.html', context)


def reports_income_choose_specific_date(request,yk,mk,dk):
    year = YearlyIncomeGreg.objects.get(id=yk)
    month = MonthlyIncomeGreG.objects.get(id=mk)
    day = DailyIncomeGreG.objects.get(id =dk)
    days = DailyIncomeGreG.objects.all().filter(month__title=month).order_by('-id')
    years = YearlyIncomeGreg.objects.all().order_by('-id')
    months = MonthlyIncomeGreG.objects.all().order_by('-id')
    orders = Lianiki_Order.objects.all().filter(day= day).order_by('-id')
    title = str(day.title)+ str(month.title) +str(year)
    context={
        'title':title,
        'days':days,
        'month':month,
        'year':year,
        'months':months,
        'years':years,
        'day':day,
        'orders':orders,
        #'order_items':order_items,
    }
    return render(request, 'reports/incomes.html', context)

def reports_income_choose_month(request,yk,mk):
    year = YearlyIncomeGreg.objects.get(id=yk)
    month = MonthlyIncomeGreG.objects.get(id=mk)
    days = DailyIncomeGreG.objects.all().filter(month__title=month).order_by('-id')
    years = YearlyIncomeGreg.objects.all().order_by('-id')
    months = MonthlyIncomeGreG.objects.all().order_by('-id')
    title =  str(month.title) +str(year)
    context={
        'title':title,
        'days':days,
        'month':month,
        'year':year,
        'months':months,
        'years':years,
        'orders':orders,
        #'order':order_lianiki,
        #'order_items':order_items,


    }
    return render(request, 'reports/incomes.html', context)


#Isologismos



def isologismos(request):

    #gets the data from the start of the year
    day_now= datetime.datetime.now()
    start_year = datetime.datetime(datetime.datetime.now().year, 1,1)

    #outcomes sales
    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_year,day_now])
    orders_b = Order.objects.all().filter(date__range=[start_year,day_now])
    log = Order_Fixed_Cost.objects.all().filter(date__range=[start_year,day_now])
    pagia_exoda =  Pagia_Exoda_Order.objects.all().filter(date__range=[start_year,day_now])
    people_pay = CreatePersonSalaryCost.objects.all().filter(day_expire__range=[start_year,day_now])
    pay_orders = PayOrders.objects.all().filter(date__range=[start_year,day_now])

    pay_log = PayOrderFixedCost.objects.all().filter(date__range=[start_year, day_now])
    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[start_year, day_now],status ='b')
    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[start_year, day_now])

    date_pick = None
    if request.POST:
        date_pick = request.POST.get('date_pick')

        if date_pick:
            if date_pick:
                try:
                    date_range = date_pick.split('-')
                    date_range[0]=date_range[0].replace(' ','')
                    date_range[1]=date_range[1].replace(' ','')


                    start_year =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                    day_now =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

                    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_year,day_now])
                    orders_b = Order.objects.all().filter(date__range=[start_year,day_now])
                    log = Order_Fixed_Cost.objects.all().filter(date__range=[start_year,day_now])
                    pagia_exoda =  Pagia_Exoda_Order.objects.all().filter(date__range=[start_year,day_now])
                    people_pay = CreatePersonSalaryCost.objects.all().filter(day_expire__range=[start_year,day_now])
                    pay_orders = PayOrders.objects.all().filter(date__range=[start_year,day_now])

                    pay_log = PayOrderFixedCost.objects.all().filter(date__range=[start_year, day_now])
                    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[start_year, day_now],status ='b')
                    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[start_year, day_now])

                except:
                    date_pick = None


     #incomes
    #gets the actual paid from costumers
    total_incomes = orders.aggregate(Sum('paid_value'))
    total_incomes = total_incomes['paid_value__sum']

    #gets the total value of the sells
    total_value = orders.aggregate(Sum('value'))
    total_value = total_value['value__sum']

    #gets the income per day
    income_per_day = {}
    for num in range((day_now -start_year).days):
        day  = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date = day).aggregate(Sum('paid_value'))
        income_per_day[day.date()] = sum_day['paid_value__sum']

    sorted(income_per_day)


    #geta the total value per day
    value_per_day = {}

    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date=day).aggregate(Sum('value'))
        value_per_day[day.date()]=sum_day['value__sum']

    sorted(value_per_day)
    #____________________________________________________________________________________________________________________



    #creates a sorted dictionary by date with the value of total disctionary outcoumes
    sum_per_day = {}
    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)

        sum_day = Order.objects.all().filter(date = day_now - datetime.timedelta(days=num) ).aggregate(Sum('total_price'))
        sum_per_day[day.date()]= sum_day['total_price__sum']
    sorted(sum_per_day)

    #total orders outcome for the period
    order_sum = orders_b.aggregate(Sum('total_price'))
    order_sum =order_sum['total_price__sum']

    # gets the others expenses for the period




    ocuppation = Occupation.objects.all()
    total_sum_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = people_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_sum_by_occup[title]=sum

    sorted(total_sum_by_occup)

    #Total outcomes

    pagia_exoda_sum = pagia_exoda.aggregate(Sum('price'))['price__sum']
    log_sum = log.aggregate(Sum('price'))['price__sum']
    people_pay_sum = people_pay.aggregate(Sum('value'))['value__sum']

    if pagia_exoda_sum == None:
        pagia_exoda_sum=0
    if log_sum == None:
        log_sum = 0
    if order_sum == None:
        order_sum = 0
    if people_pay_sum == None:
        people_pay_sum = 0

    total_outcomes = pagia_exoda_sum + +log_sum + order_sum + people_pay_sum

    #Total_paid




    pay_per_day ={}

    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)
        pay_day = pay_orders.filter(date = day_now - datetime.timedelta(days=num)).aggregate(Sum('value'))
        pay_per_day[day.date()]= pay_day['value__sum']

    sorted(pay_per_day)



    pay_orders_sum = pay_orders.aggregate(Sum('value'))['value__sum']
    if pay_orders_sum == None:
        pay_orders_sum = 0


    pay_log_sum = pay_log.aggregate(Sum('price'))['price__sum']
    if pay_log_sum == None:
        pay_log_sum = 0


    person_pay_sum = person_pay.aggregate(Sum('value'))['value__sum']

    if person_pay_sum == None:
        person_pay_sum = 0

    total_pay_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = person_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_pay_by_occup[title]=sum

    sorted(total_pay_by_occup)


    pagia_exoda_pay_sum = pagia_exoda_pay.aggregate(Sum('value'))['value__sum']
    if pagia_exoda_pay_sum == None:
        pagia_exoda_pay_sum = 0

    total_pays = pay_orders_sum + pay_log_sum + person_pay_sum + pagia_exoda_pay_sum






    context = {
        'orders':orders,
        'suma':order_sum,


        'sum_per_day':sum_per_day,
        'pay_per_day':pay_per_day,

        'log':log,
        'log_sum':log_sum,
        'pagia_exoda':pagia_exoda,
        'pagia_exoda_sum':pagia_exoda_sum,
        'people':people_pay,
        'people_sum':people_pay_sum,

        'total_sum_by_occup':total_sum_by_occup,

        'total_outcome':total_outcomes,

        'pay_orders':pay_orders_sum,

        'pay_log':pay_log,
        'pay_log_sum':pay_log_sum,

        'pay_ppl':person_pay,
        'pay_ppl_sum':person_pay_sum,
        'total_pay_by_occup':total_pay_by_occup,

        'pay_pagia':pagia_exoda_pay,
        'pay_pagia_sum':pagia_exoda_pay_sum,

        'total_pay':total_pays,

        'total_income':total_incomes,
        'total_value':total_value,
        'incomes_per_day':income_per_day,

        'date_pick':date_pick,
    }
    context.update(csrf(request))
    return render(request,'reports/isologismos.html',context)




def balance_sheet_estimate(request):
    #gets the day range you want
    #gets the data from the start of the year
    day_now= datetime.datetime.now()
    start_year = datetime.datetime(datetime.datetime.now().year, 1,1)
    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_year,day_now])

    log = Order_Fixed_Cost.objects.all().filter(date__range=[start_year,day_now])
    pagia_exoda =  Pagia_Exoda_Order.objects.all().filter(date__range=[start_year,day_now])
    people_pay = CreatePersonSalaryCost.objects.all().filter(day_expire__range=[start_year,day_now])
    pay_orders = PayOrders.objects.all().filter(date__range=[start_year,day_now])
    pay_log = PayOrderFixedCost.objects.all().filter(date__range=[start_year, day_now])
    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[start_year, day_now],status ='b')
    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[start_year, day_now])

    date_pick = None
    if request.POST:
        date_pick = request.POST.get('date_pick')

        if date_pick:
            if date_pick:
                try:
                    date_range = date_pick.split('-')
                    date_range[0]=date_range[0].replace(' ','')
                    date_range[1]=date_range[1].replace(' ','')
                    start_year =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
                    day_now =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')

                    orders = Lianiki_Order.objects.all().filter(day_added__range=[start_year,day_now])
                    log = Order_Fixed_Cost.objects.all().filter(date__range=[start_year,day_now])
                    pagia_exoda =  Pagia_Exoda_Order.objects.all().filter(date__range=[start_year,day_now])
                    people_pay = CreatePersonSalaryCost.objects.all().filter(day_expire__range=[start_year,day_now])
                    pay_orders = PayOrders.objects.all().filter(date__range=[start_year,day_now])
                    pay_log = PayOrderFixedCost.objects.all().filter(date__range=[start_year, day_now])
                    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[start_year, day_now],status ='b')
                    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[start_year, day_now])

                except:
                    date_pick = None


    #incomes

    #gets the actual paid from costumers
    total_incomes = orders.aggregate(Sum('paid_value'))
    total_incomes = total_incomes['paid_value__sum']

    #gets the total value of the sells
    total_value = orders.aggregate(Sum('value'))
    total_value = total_value['value__sum']
    print(total_incomes)

    #gets the income per day
    income_per_day = {}
    for num in range((day_now -start_year).days):
        day  = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date = day).aggregate(Sum('paid_value'))
        income_per_day[day.date()] = sum_day['paid_value__sum']

    sorted(income_per_day)

    #geta the total value per day
    value_per_day = {}

    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date=day).aggregate(Sum('value'))
        value_per_day[day.date()]=sum_day['value__sum']

    sorted(value_per_day)




    #outcomes

    #creates a sorted dictionary by date with the value of total disctionary outcoumes
    sum_per_day = {}
    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date = day ).aggregate(Sum('total_cost'))
        sum_per_day[day.date()]= sum_day['total_cost__sum']

    sorted(sum_per_day)


    #total orders outcome for the period
    order_lianiki_sum = orders.aggregate(Sum('total_cost'))
    order_lianiki_sum =order_lianiki_sum['total_cost__sum']

    if order_lianiki_sum == None:
        order_lianiki_sum = 0

    # gets the others expenses for the period




    ocuppation = Occupation.objects.all()
    total_sum_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = people_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_sum_by_occup[title]=sum

    sorted(total_sum_by_occup)

    #Total outcomes

    pagia_exoda_sum = pagia_exoda.aggregate(Sum('price'))['price__sum']
    log_sum = log.aggregate(Sum('price'))['price__sum']
    people_pay_sum = people_pay.aggregate(Sum('value'))['value__sum']

    if pagia_exoda_sum == None:
        pagia_exoda_sum=0
    if log_sum == None:
        log_sum = 0
    if order_lianiki_sum == None:
        order_lianiki = 0
    if people_pay_sum == None:
        people_pay_sum = 0

    total_outcomes = pagia_exoda_sum + +log_sum + order_lianiki_sum + people_pay_sum

    #Total_paid




    pay_per_day ={}

    for num in range((day_now -start_year).days):
        day = day_now - datetime.timedelta(days=num)
        pay_day = pay_orders.filter(date = day_now - datetime.timedelta(days=num)).aggregate(Sum('value'))
        pay_per_day[day.date()]= pay_day['value__sum']

    sorted(pay_per_day)



    pay_orders_sum = pay_orders.aggregate(Sum('value'))['value__sum']
    if pay_orders_sum == None:
        pay_orders_sum = 0


    pay_log_sum = pay_log.aggregate(Sum('price'))['price__sum']
    if pay_log_sum == None:
        pay_log_sum = 0


    person_pay_sum = person_pay.aggregate(Sum('value'))['value__sum']

    if person_pay_sum == None:
        person_pay_sum = 0

    total_pay_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = person_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_pay_by_occup[title]=sum

    sorted(total_pay_by_occup)

    pagia_exoda_pay_sum = pagia_exoda_pay.aggregate(Sum('value'))['value__sum']
    if pagia_exoda_pay_sum == None:
        pagia_exoda_pay_sum = 0

    total_pays = order_lianiki_sum + pay_log_sum + person_pay_sum + pagia_exoda_pay_sum

    if total_incomes is not None:
        profit = 100 - ((total_outcomes/total_incomes)*100)
    else:
        profit = 0

    context = {
        'orders':orders,
        'suma':order_lianiki_sum,

        'profit':profit,


        'sum_per_day':sum_per_day,
        'pay_per_day':pay_per_day,

        'log':log,
        'log_sum':log_sum,
        'pagia_exoda':pagia_exoda,
        'pagia_exoda_sum':pagia_exoda_sum,
        'people':people_pay,
        'people_sum':people_pay_sum,

        'total_sum_by_occup':total_sum_by_occup,

        'total_outcome':total_outcomes,

        'pay_orders':pay_orders_sum,

        'pay_log':pay_log,
        'pay_log_sum':pay_log_sum,

        'pay_ppl':person_pay,
        'pay_ppl_sum':person_pay_sum,
        'total_pay_by_occup':total_pay_by_occup,

        'pay_pagia':pagia_exoda_pay,
        'pay_pagia_sum':pagia_exoda_pay_sum,

        'total_pay':total_pays,

        'total_income':total_incomes,
        'total_value':total_value,
        'incomes_per_day':income_per_day,

        'value_per_day':value_per_day,

        'date_pick':date_pick,


    }
    return render(request,'reports/balance_sheet_estimate.html',context)

def balance_sheet_estimate_current_month(request):
    #gets the day range you want
    day_now= datetime.datetime.now()

    orders = Lianiki_Order.objects.all().filter(day_added__month=day_now.month)


    #incomes

    #gets the actual paid from costumers
    total_incomes = orders.aggregate(Sum('paid_value'))
    total_incomes = total_incomes['paid_value__sum']

    #gets the total value of the sells
    total_value = orders.aggregate(Sum('value'))
    total_value = total_value['value__sum']

    #gets the income per day
    income_per_day = {}
    for num in range(day_now.isoweekday()):
        day  = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date = day).aggregate(Sum('paid_value'))
        income_per_day[day.date()] = sum_day['paid_value__sum']

    sorted(income_per_day)

    #geta the total value per day
    value_per_day = {}

    for num in range(day_now.isoweekday()):
        day = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date=day).aggregate(Sum('value'))
        value_per_day[day.date()]=sum_day['value__sum']

    sorted(value_per_day)




    #outcomes

    #creates a sorted dictionary by date with the value of total disctionary outcoumes
    sum_per_day = {}
    for num in range(day_now.isoweekday()):
        day = day_now - datetime.timedelta(days=num)
        sum_day = orders.filter(day_added__date = day ).aggregate(Sum('total_cost'))
        sum_per_day[day.date()]= sum_day['total_cost__sum']

    sorted(sum_per_day)


    #total orders outcome for the period
    order_lianiki_sum = orders.aggregate(Sum('total_cost'))
    order_lianiki_sum =order_lianiki_sum['total_cost__sum']

    if order_lianiki_sum == None:
        order_lianiki_sum = 0

    # gets the others expenses for the period
    log = Order_Fixed_Cost.objects.all().filter(date__month=day_now.month)
    pagia_exoda =  Pagia_Exoda_Order.objects.all().filter(date__month=day_now.month)
    people_pay = CreatePersonSalaryCost.objects.all().filter(day_expire__month=day_now.month)



    ocuppation = Occupation.objects.all()
    total_sum_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = people_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_sum_by_occup[title]=sum

    sorted(total_sum_by_occup)

    #Total outcomes

    pagia_exoda_sum = pagia_exoda.aggregate(Sum('price'))['price__sum']
    log_sum = log.aggregate(Sum('price'))['price__sum']
    people_pay_sum = people_pay.aggregate(Sum('value'))['value__sum']

    if pagia_exoda_sum == None:
        pagia_exoda_sum=0
    if log_sum == None:
        log_sum = 0
    if order_lianiki_sum == None:
        order_lianiki = 0
    if people_pay_sum == None:
        people_pay_sum = 0

    total_outcomes = pagia_exoda_sum + +log_sum + order_lianiki_sum + people_pay_sum

    #Total_paid



    pay_orders = PayOrders.objects.all().filter(date__month= day_now.month)
    pay_per_day ={}

    for num in range(day_now.isoweekday()):
        day = day_now - datetime.timedelta(days=num)
        pay_day = pay_orders.filter(date = day_now - datetime.timedelta(days=num)).aggregate(Sum('value'))
        pay_per_day[day.date()]= pay_day['value__sum']

    sorted(pay_per_day)



    pay_orders_sum = pay_orders.aggregate(Sum('value'))['value__sum']
    if pay_orders_sum == None:
        pay_orders_sum = 0

    pay_log = PayOrderFixedCost.objects.all().filter(date__month=day_now.month)
    pay_log_sum = pay_log.aggregate(Sum('price'))['price__sum']
    if pay_log_sum == None:
        pay_log_sum = 0

    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__month=day_now.month,status ='b')
    person_pay_sum = person_pay.aggregate(Sum('value'))['value__sum']

    if person_pay_sum == None:
        person_pay_sum = 0



    total_pay_by_occup = {}

    for occup in ocuppation:
        title = occup.title
        sum = person_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_pay_by_occup[title]=sum

    sorted(total_pay_by_occup)

    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__month=day_now.month)
    pagia_exoda_pay_sum = pagia_exoda_pay.aggregate(Sum('value'))['value__sum']
    if pagia_exoda_pay_sum == None:
        pagia_exoda_pay_sum = 0

    total_pays = order_lianiki_sum + pay_log_sum + person_pay_sum + pagia_exoda_pay_sum

    if total_incomes is not None:
        profit = 100 - ((total_outcomes/total_incomes)*100)
    else:
        profit = 0

    context = {
        'orders':orders,
        'suma':order_lianiki_sum,

        'profit':profit,


        'sum_per_day':sum_per_day,
        'pay_per_day':pay_per_day,

        'log':log,
        'log_sum':log_sum,
        'pagia_exoda':pagia_exoda,
        'pagia_exoda_sum':pagia_exoda_sum,
        'people':people_pay,
        'people_sum':people_pay_sum,

        'total_sum_by_occup':total_sum_by_occup,

        'total_outcome':total_outcomes,

        'pay_orders':pay_orders_sum,

        'pay_log':pay_log,
        'pay_log_sum':pay_log_sum,

        'pay_ppl':person_pay,
        'pay_ppl_sum':person_pay_sum,
        'total_pay_by_occup':total_pay_by_occup,

        'pay_pagia':pagia_exoda_pay,
        'pay_pagia_sum':pagia_exoda_pay_sum,

        'total_pay':total_pays,

        'total_income':total_incomes,
        'total_value':total_value,
        'incomes_per_day':income_per_day,

        'value_per_day':value_per_day,


    }
    return render(request,'reports/balance_sheet_estimate.html',context)




def balance_sheet_estimate_current_three_months(request):

    day_now = datetime.datetime.now()
    day_start = day_now  + relativedelta(months=-3)

    #incomes
    orders = Lianiki_Order.objects.filter(day_added__range =[day_start, day_now])
    total_income = orders.aggregate(Sum('paid_value'))
    total_incomes =total_income['paid_value__sum']


    incomes_per_day = {}
    for num in range((day_now -day_start).days):
        date = day_now - datetime.timedelta(days=num)
        day_sum = orders.filter(day_added__date = date.date()).aggregate(Sum('paid_value'))
        incomes_per_day[date.date()] = day_sum['paid_value__sum']
    sorted(incomes_per_day)

    total_value = orders.aggregate(Sum('value'))
    total_value = total_value['value__sum']

    value_per_day = {}
    for num in range((day_now-day_start).days):
        day = day_now - datetime.timedelta(days=num)
        day_sum = orders.filter(day_added__date = day.date()).aggregate(Sum('value'))
        value_per_day[day.date()]=day_sum['value__sum']
    sorted(value_per_day)



    #outcomes

    #total cost from the orders
    total_cost_orders = orders.aggregate(Sum('total_cost'))
    total_cost_orders = total_cost_orders['total_cost__sum']
    if total_cost_orders == None:
        total_cost_orders = 0

    #total cost from payroll
    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[day_start,day_now],status ='b')
    person_pay_sum = person_pay.aggregate(Sum('value'))['value__sum']
    if person_pay_sum == None:
        person_pay_sum = 0


    #total_pay per occupation
    ocuppation = Occupation.objects.all()
    total_pay_by_occup = {}
    for occup in ocuppation:
        title = occup.title
        sum = person_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_pay_by_occup[title]=sum
    sorted(total_pay_by_occup)



    #total_cost from fixed assets
    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[day_start,day_now])
    pagia_exoda_pay_sum = pagia_exoda_pay.aggregate(Sum('value'))['value__sum']
    if pagia_exoda_pay_sum == None:
        pagia_exoda_pay_sum = 0


    #total bills!!
    pay_log = PayOrderFixedCost.objects.all().filter(date__month=day_now.month)
    pay_log_sum = pay_log.aggregate(Sum('price'))['price__sum']
    if pay_log_sum == None:
        pay_log_sum = 0

    total_pays = total_cost_orders + person_pay_sum +  + pagia_exoda_pay_sum + pay_log_sum

    title = 'Κοστολόγιο Τριμήνου'
    context = {
        'title':title,
        'total_income':total_incomes,
        'total_value':total_value,
        'incomes_per_day':incomes_per_day,
        'value_per_day':value_per_day,

        'total_cost_orders': total_cost_orders,
        'pay_log_sum':pay_log_sum,
        'pay_ppl_sum':person_pay_sum,
        'total_pay_by_occup':total_pay_by_occup,
        'pay_pagia_sum':pagia_exoda_pay_sum,

        'total_pay':total_pays,
    }
    return render(request, 'reports/balance_sheet_estimate.html',context)

def balance_sheet_estimate_six_months(request):
    day_now = datetime.datetime.now()
    day_start = day_now  + relativedelta(months=-6)

    #incomes
    orders = Lianiki_Order.objects.filter(day_added__range =[day_start, day_now])
    total_income = orders.aggregate(Sum('paid_value'))
    total_incomes =total_income['paid_value__sum']


    incomes_per_day = {}
    for num in range((day_now -day_start).days):
        date = day_now - datetime.timedelta(days=num)
        day_sum = orders.filter(day_added__date = date.date()).aggregate(Sum('paid_value'))
        incomes_per_day[date.date()] = day_sum['paid_value__sum']
    sorted(incomes_per_day)

    total_value = orders.aggregate(Sum('value'))
    total_value = total_value['value__sum']

    value_per_day = {}
    for num in range((day_now-day_start).days):
        day = day_now - datetime.timedelta(days=num)
        day_sum = orders.filter(day_added__date = day.date()).aggregate(Sum('value'))
        value_per_day[day.date()]=day_sum['value__sum']
    sorted(value_per_day)



    #outcomes

    #total cost from the orders
    total_cost_orders = orders.aggregate(Sum('total_cost'))
    total_cost_orders = total_cost_orders['total_cost__sum']
    if total_cost_orders == None:
        total_cost_orders = 0

    #total cost from payroll
    person_pay = CreatePersonSalaryCost.objects.all().filter(day_added__range=[day_start,day_now],status ='b')
    person_pay_sum = person_pay.aggregate(Sum('value'))['value__sum']
    if person_pay_sum == None:
        person_pay_sum = 0


    #total_pay per occupation
    ocuppation = Occupation.objects.all()
    total_pay_by_occup = {}
    for occup in ocuppation:
        title = occup.title
        sum = person_pay.filter(person__occupation__title = title).aggregate(Sum('value'))['value__sum']
        total_pay_by_occup[title]=sum
    sorted(total_pay_by_occup)



    #total_cost from fixed assets
    pagia_exoda_pay = Pagia_Exoda_Pay_Order.objects.all().filter(day_added__range=[day_start,day_now])
    pagia_exoda_pay_sum = pagia_exoda_pay.aggregate(Sum('value'))['value__sum']
    if pagia_exoda_pay_sum == None:
        pagia_exoda_pay_sum = 0


    #total bills!!
    pay_log = PayOrderFixedCost.objects.all().filter(date__month=day_now.month)
    pay_log_sum = pay_log.aggregate(Sum('price'))['price__sum']
    if pay_log_sum == None:
        pay_log_sum = 0

    total_pays = total_cost_orders + person_pay_sum +  + pagia_exoda_pay_sum + pay_log_sum

    title = 'Κοστολόγιο Εξαμήνου'
    context = {
        'title':title,
        'total_income':total_incomes,
        'total_value':total_value,
        'incomes_per_day':incomes_per_day,
        'value_per_day':value_per_day,

        'total_cost_orders': total_cost_orders,
        'pay_log_sum':pay_log_sum,
        'pay_ppl_sum':person_pay_sum,
        'total_pay_by_occup':total_pay_by_occup,
        'pay_pagia_sum':pagia_exoda_pay_sum,

        'total_pay':total_pays,
    }
    return render(request, 'reports/balance_sheet_estimate.html',context)
