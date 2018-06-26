from django.shortcuts import render,HttpResponseRedirect
from django.core.context_processors import csrf
from django.db.models import Q
from django.db.models import Sum, Avg, Count
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from .models import *
from .forms import *
# Create your views here.

from dateutil.relativedelta import relativedelta
def diff_month(date_start, date_end):
    return (date_end.year -date_start.year)*12 + (date_end.month - date_start.month)


@staff_member_required
def homepage(request):
    date_now = datetime.date.today()
    katastimata = ['Σκάλα','Μολάοι Κεντρικό','Μολάοι Παιδικό','MyModa', 'Boom']
    search_pro = request.POST.get('search_pro', None)
    
    try:
        picked_date = request.session['date_now']
    except:
        picked_date=None
        request.session['date_now'] = None

    #stats per month
    start_year = datetime.datetime(datetime.datetime.now().year, 1,1)
    months_list =[]
    month=1
    months = diff_month(start_year,date_now)
    while month <= months+1:
        months_list.append(datetime.datetime(datetime.datetime.now().year, month,1).month)
        month +=1
    title = 'Try'
    incomes = AddEsoda.objects.all().filter(title__month=date_now.month,title__year=date_now.year).order_by('-title')
    incomes_initial= AddEsoda.objects.all().filter(title__range=[start_year,date_now])
    date_pick = request.POST.get('date_pick')
    if search_pro:
        incomes = AddEsoda.objects.filter(comments__icontains=search_pro)
    try:
        date_range = date_pick.split('-')
        date_range[0]=date_range[0].replace(' ','')
        date_range[1]=date_range[1].replace(' ','')

        date_start =datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
        date_end =datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
        incomes = AddEsoda.objects.all()

        start_next_year =date_start
        end_next_year = date_end

        start_last_year =date_start
        end_last_year = date_end

        start_next_year = start_next_year + relativedelta(year=start_next_year.year+1)
        end_next_year = end_next_year + relativedelta(year=end_next_year.year+1)

        #start_next_year = datetime.datetime.strptime(start_next_year, '%m/%d/%Y')
        #end_next_year = datetime.datetime.strptime(end_last_year,'%m/%d/%Y')
        incomes_next_year =incomes.filter(title__range=[start_next_year,end_next_year]).order_by('-title')

        start_last_year = start_last_year + relativedelta(year=start_last_year.year-1)
        end_last_year = end_last_year + relativedelta(year=end_last_year.year-1)

        incomes_last_year = incomes.filter(title__range=[start_last_year,end_last_year]).order_by('-title')

        incomes = incomes.filter(title__range=[date_start,date_end]).order_by('-title')
        print (date_end,date_start, start_next_year,end_next_year)
    except:
        date_pick = None



    #get next year reports
    try:
        all_retail_next = incomes_next_year.aggregate(Sum('sinolo_fisikon'))
        all_retail_next = all_retail_next['sinolo_fisikon__sum']
        all_retail_avg_next = incomes_next_year.aggregate(Avg('sinolo_fisikon'))
        all_retail_avg_next = all_retail_avg_next['sinolo_fisikon__avg']
    except:
        all_retail_next = 0
        all_retail_avg_next = 0
    try:
        all_incomes_next = incomes_next_year.aggregate(Sum('sinolo_olon'))
        all_incomes_next = all_incomes_next['sinolo_olon__sum']
        all_incomes_avg_next = incomes_next_year.aggregate(Avg('sinolo_olon'))
        all_incomes_avg_next = all_incomes_avg_next['sinolo_olon__avg']
    except:
        all_incomes_next = 0
        all_incomes_avg_next = 0

    try:
        pediko_total_next = incomes_next_year.aggregate(Sum('pediko'))
        pediko_total_next = pediko_total_next['pediko__sum']
        pediko_total_avg_next = incomes_next_year.aggregate(Avg('pediko'))
        pediko_total_avg_next = pediko_total_avg_next['pediko__avg']
    except:
        pediko_total_next = 0
        pediko_total_avg_next = 0

    try:
        topiko_next = incomes_next_year.aggregate(Sum('topiko_katastima'))
        topiko_next = topiko_next['topiko_katastima__sum']
        topiko_avg_next = incomes_next_year.aggregate(Avg('topiko_katastima'))
        topiko_avg_next = topiko_avg_next['topiko_katastima__avg']
    except:
        topiko_next = 0
        topiko_avg_next = 0
    try:
        skala_next = incomes_next_year.aggregate(Sum('skala'))
        skala_next = skala_next['skala__sum']
        skala_avg_next = incomes_next_year.aggregate(Avg('skala'))
        skala_avg_next = skala_avg_next['skala__avg']
    except:
        skala_next = 0
        skala_avg_next = 0
    try:
        my_moda_next = incomes_next_year.aggregate(Sum('mymoda'))
        my_moda_next = my_moda_next['mymoda__sum']
        my_moda_avg_next = incomes_next_year.aggregate(Avg('mymoda'))
        my_moda_avg_next = my_moda_avg_next['mymoda__avg']
    except:
        my_moda_next = 0
        my_moda_avg_next = 0
    #get last year reports
    try:
        all_retail_last = incomes_last_year.aggregate(Sum('sinolo_fisikon'))
        all_retail_last  =all_retail_last['sinolo_fisikon__sum']
        all_retail_avg_last  = incomes_last_year.aggregate(Avg('sinolo_fisikon'))
        all_retail_avg_last  = all_retail_avg_last['sinolo_fisikon__avg']
    except:
        all_retail_last = 0
        all_retail_avg_last = 0

    try:
        all_incomes_last = incomes_last_year.aggregate(Sum('sinolo_olon'))
        all_incomes_last =all_incomes_last['sinolo_olon__sum']
        all_incomes_avg_last = incomes_last_year.aggregate(Avg('sinolo_olon'))
        all_incomes_avg_last = all_incomes_avg_last['sinolo_olon__avg']
    except:
        all_incomes_last = 0
        all_incomes_avg_last = 0

    try:
        pediko_total_last = incomes_last_year.aggregate(Sum('pediko'))
        pediko_total_last = pediko_total_last['pediko__sum']
        pediko_total_avg_last = incomes_last_year.aggregate(Avg('pediko'))
        pediko_total_avg_last = pediko_total_avg_last['pediko__avg']
    except:
        pediko_total_last = 0
        pediko_total_avg_last = 0

    try:
        topiko_last = incomes_last_year.aggregate(Sum('topiko_katastima'))
        topiko_last = topiko_last['topiko_katastima__sum']
        topiko_avg_last = incomes_last_year.aggregate(Avg('topiko_katastima'))
        topiko_avg_last = topiko_avg_last['topiko_katastima__avg']
    except:
        topiko_last = 0
        topiko_avg_last = 0


    try:
        skala_last = incomes_last_year.aggregate(Sum('skala'))
        skala_last = skala_last['skala__sum']
        skala_avg_last = incomes_last_year.aggregate(Avg('skala'))
        skala_avg_last = skala_avg_last['skala__avg']
    except:
        skala_last = 0
        skala_avg_last = 0

    try:
        my_moda_last = incomes_last_year.aggregate(Sum('mymoda'))
        my_moda_last = my_moda_last['mymoda__sum']
        my_moda_avg_last = incomes_last_year.aggregate(Avg('mymoda'))
        my_moda_avg_last = my_moda_avg_last['mymoda__avg']
    except:
        my_moda_last = 0
        my_moda_avg_last = 0


    #get reports
    try:
        all_retail = incomes.aggregate(Sum('sinolo_fisikon'))
        all_retail =all_retail['sinolo_fisikon__sum']
        all_retail_avg = incomes.aggregate(Avg('sinolo_fisikon'))
        all_retail_avg = all_retail_avg['sinolo_fisikon__avg']
    except:
        all_retail = 0
        all_retail_avg = 0


    try:
        all_incomes = incomes.aggregate(Sum('sinolo_olon'))
        all_incomes =all_incomes['sinolo_olon__sum']
        all_incomes_avg = incomes.aggregate(Avg('sinolo_olon'))
        all_incomes_avg = all_incomes_avg['sinolo_olon__avg']

    except:
        all_incomes = 0
        all_incomes_avg = 0

    try:
        pediko_total = incomes.aggregate(Sum('pediko'))
        pediko_total = pediko_total['pediko__sum']
        pediko_total_avg = incomes.aggregate(Avg('pediko'))
        pediko_total_avg = pediko_total_avg['pediko__avg']
    except:
        pediko_total = 0
        pediko_total_avg = 0

    try:
        topiko = incomes.aggregate(Sum('topiko_katastima'))
        topiko = topiko['topiko_katastima__sum']
        topiko_avg = incomes.aggregate(Avg('topiko_katastima'))
        topiko_avg = topiko_avg['topiko_katastima__avg']
    except:
        topiko = 0
        topiko_avg = 0


    try:
        skala = incomes.aggregate(Sum('skala'))
        skala = skala['skala__sum']
        skala_avg = incomes.aggregate(Avg('skala'))
        skala_avg = skala_avg['skala__avg']
    except:
        skala = 0
        skala_avg = 0

    try:
        my_moda = incomes.aggregate(Sum('mymoda'))
        my_moda = my_moda['mymoda__sum']
        my_moda_avg = incomes.aggregate(Avg('mymoda'))
        my_moda_avg = my_moda_avg['mymoda__avg']
    except:
        my_moda = 0
        my_moda_avg = 0

    try:
        boom = incomes.aggregate(Sum('boom'))['boom__sum'] if incomes.aggregate(Sum('boom')) else 0
        boom_avg = incomes.aggregate(Avg('boom'))['boom__avg'] if incomes.aggregate(Avg('boom')) else 0
    except:
        boom = 0
        boom_avg = 0
    try:
        boom_last = incomes_last_year.aggregate(Sum('boom'))['boom__sum'] if incomes_last_year.aggregate(Sum('boom')) != None else 0
        boom_avg_last = incomes_last_year.aggregate(Avg('boom'))['boom__avg'] if incomes_last_year.aggregate(Avg('boom')) else 0
        boom_next = incomes_next_year.aggregate(Sum('boom'))['boom__sum'] if incomes_next_year.aggregate(Sum('boom')) else 0
        boom_avg_next = incomes_next_year.aggregate(Avg('boom'))['boom__avg'] if incomes_next_year.aggregate(Avg('boom')) else 0

    except:
        boom_last = 0
        boom_avg_last =  0
        boom_next = 0
        boom_avg_next =  0


    total_per_month=[]
    for num in months_list:
        month  = datetime.datetime.now() - relativedelta(months=num-1)

        boom_sum = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('boom'))['boom__sum'] if incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('boom'))['boom__sum'] else 0
        try:
            sum_paidiko = incomes_initial.filter(title__month=month.month,title__year=month.year).aggregate(Sum('pediko'))
            sum_paidiko = sum_paidiko['pediko__sum']
        except:
            sum_paidiko=0
        try:
            sum_kenriko = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('topiko_katastima'))
            sum_kenriko = sum_kenriko['topiko_katastima__sum']
        except:
            sum_kenriko = 0
        try:
            sum_skala = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('skala'))
            sum_skala= sum_skala['skala__sum']
        except:
            sum_skala=0

        try:
            sum_my_moda = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('mymoda'))
            sum_my_moda=sum_my_moda['mymoda__sum']
        except:
            sum_my_moda =0
        try:
            sum_fisikon = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('sinolo_fisikon'))
            sum_fisikon = sum_fisikon['sinolo_fisikon__sum']
        except:
            sum_fisikon=0
        try:
            sum_total = incomes_initial.filter(title__month=month.month, title__year=month.year).aggregate(Sum('sinolo_olon'))
            sum_total = sum_total['sinolo_olon__sum']
        except:
            sum_total=0

        total_per_month.append((month,sum_paidiko,sum_kenriko,sum_skala,sum_fisikon,sum_my_moda,sum_total, boom_sum))





    #the section of total sum per katastima
    katastima_name = request.POST.get('vendor_name') or None
    month_analysis =[]

    this_year = date_now
    years =[]
    year_initial =datetime.datetime.now().today().year

    ele=1
    all_months = [('January','1'),
                  ('February','2'),
                  ('March','3'),
                  ('April','4'),
                  ('May','5'),
                  ('June','6'),
                  ('July','7'),
                  ('August','8'),
                  ('September','9'),
                  ('October','10'),
                  ('November','11'),
                  ('December','12'),]

    try:
        jk = YearMeter.objects.get(id=1).title
    except:
        jk=5
    if katastima_name:
        while ele<jk+1:
            years.append(year_initial)
            year_initial -=1
            ele +=1

        if katastima_name == 'Σκάλα':
            incomes_initial = AddEsoda.objects.all()
            for month in all_months:
                year_analysis=[]
                for yeara in years:
                    try:
                        sum_skala = incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('skala'))
                        sum_skala= sum_skala['skala__sum']
                    except:
                        sum_skala=0
                    year_analysis.append(sum_skala)
                month_analysis.append((month[0],year_analysis))
            final_data=[]
            for month in month_analysis:
                final_data.append(month[0])
                try:
                    print(month[1][0]-month[1][1])
                except:
                    print(month[1][0])

            print(final_data)

    if katastima_name == 'Μολάοι Κεντρικό':
            incomes_initial = AddEsoda.objects.all()
            for month in all_months:
                year_analysis=[]
                for yeara in years:
                    try:
                        sum_skala = incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('topiko_katastima'))
                        sum_skala= sum_skala['topiko_katastima__sum']
                    except:
                        sum_skala=0
                    year_analysis.append(sum_skala)
                month_analysis.append((month[0],year_analysis))

    if katastima_name == 'Μολάοι Παιδικό':
            incomes_initial = AddEsoda.objects.all()
            for month in all_months:
                year_analysis=[]
                for yeara in years:
                    try:
                        sum_skala = incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('pediko'))
                        sum_skala= sum_skala['pediko__sum']
                    except:
                        sum_skala=0
                    year_analysis.append(sum_skala)
                month_analysis.append((month[0],year_analysis))
    if katastima_name == 'MyModa':
            incomes_initial = AddEsoda.objects.all()
            for month in all_months:
                year_analysis=[]
                for yeara in years:
                    try:
                        sum_skala = incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('mymoda'))
                        sum_skala= sum_skala['mymoda__sum']
                    except:
                        sum_skala=0
                    year_analysis.append(sum_skala)
                month_analysis.append((month[0],year_analysis))
    if katastima_name == 'Boom':
            incomes_initial = AddEsoda.objects.all()
            for month in all_months:
                year_analysis=[]
                for yeara in years:
                    sum_boom = incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('boom'))['boom__sum'] if incomes_initial.filter(title__month=month[1], title__year=yeara).aggregate(Sum('boom'))['boom__sum'] else 0
                    year_analysis.append(sum_boom)
                month_analysis.append((month[0],year_analysis))

    if pediko_total == None:
        pediko_total = 0
    pediko_total_last = pediko_total_last if pediko_total_last else 0
    topiko_last = topiko_last if topiko_last else 0
    skala_last = skala_last if skala_last else 0
    my_moda_last = my_moda_last if my_moda_last else 0
    all_retail_last = all_retail_last if all_retail_last else 0
    all_incomes_last = all_incomes_last if all_incomes_last else 0
    boom_last = boom_last if boom_last else 0
    if topiko == None:
        topiko = 0
    if skala == None:
        skala = 0
    if my_moda == None:
        my_moda = 0
    if all_retail == None:
        all_retail = 0
    if all_incomes == None:
        all_incomes = 0
    if boom == None:
        boom = 0


    diff_bewetween_years =[pediko_total-pediko_total_last,
                            topiko-topiko_last,
                            skala-skala_last,
                            my_moda-my_moda_last,
                            all_retail -all_retail_last,
                            all_incomes- all_incomes_last,
                            boom-boom_last,
                            ]
    context ={
        'title':title,
        'kat_name':katastima_name,
        'total_per_month':total_per_month,
        'all_esoda':incomes,
        'vendors':katastimata,

        #next year_analysis

        'all_retail_next':all_retail_next,
        'all_retail_avg_next':all_retail_avg_next,

        'all_incomes_next':all_incomes_next,
        'all_incomes_avg_next':all_incomes_avg_next,

        'pediko_total_next':pediko_total_next,
        'pediko_avg_next':pediko_total_avg_next,

        'topiko_next':topiko_next,
        'topiko_avg_next':topiko_avg_next,

        'skala_next':skala_next,
        'skala_avg_next':skala_avg_next,

        'my_moda_next':my_moda_next,
        'my_moda_avg_next':my_moda_avg_next,

        #last year_analysis

        'all_retail_last':all_retail_last,
        'all_retail_avg_last':all_retail_avg_last,

        'all_incomes_last':all_incomes_last,
        'all_incomes_avg_last':all_incomes_avg_last,

        'pediko_total_last':pediko_total_last,
        'pediko_avg_last':pediko_total_avg_last,

        'topiko_last':topiko_last,
        'topiko_avg_last':topiko_avg_last,

        'skala_last':skala_last,
        'skala_avg_last':skala_avg_last,

        'my_moda_last':my_moda_last,
        'my_moda_avg_last':my_moda_avg_last,

        #current target


        'all_retail':all_retail,
        'all_retail_avg':all_retail_avg,

        'all_incomes':all_incomes,
        'all_incomes_avg':all_incomes_avg,

        'pediko_total':pediko_total,
        'pediko_avg':pediko_total_avg,

        'topiko':topiko,
        'topiko_avg':topiko_avg,

        'skala':skala,
        'skala_avg':skala_avg,

        'my_moda':my_moda,
        'my_moda_avg':my_moda_avg,
		'date_pick':date_pick,

        'month_ana':month_analysis,
        'years':years,
        'picked_date':picked_date,
        'year_meter':jk,
        'diff_be':diff_bewetween_years,
        'boom':boom,
        'boom_avg':boom_avg,
        'boom_next':boom_next,
        'boom_last':boom_last,
        'boom_avg_next':boom_avg_next,
        'boom_avg_last':boom_avg_last,

    }
    return render(request,'katastimata_esoda/homepage.html', context)


@staff_member_required
def new_esoda(request):
    all_esoda = AddEsoda.objects.all().order_by('-title')
    years = YearEsoda.objects.all().order_by('-id')

    year = YearEsoda.objects.last()
    month = MonthEsoda.objects.last()
    months = MonthEsoda.objects.all().filter(year=year).order_by('-id')

    last_day = AddEsoda.objects.last()
    new_day = last_day.title + datetime.timedelta(days=1)
    if request.POST:
        form = EsodaImerasForm(request.POST,initial={'year':year,"month":month,})
        if form.is_valid():
            form.save()
            form.add()
            return HttpResponseRedirect('/katastimata/')
    else:
        form = EsodaImerasForm(initial={'title':new_day,'year':year,"month":month,})

    context = {
        'all_esoda':all_esoda,
        'years':years,
        'months':months,
        'year':year,
        'month':month,
        'form':form,

    }
    context.update(csrf(request))
    return render(request, 'katastimata_esoda/new_order.html', context)

@staff_member_required
def esoda_income_choose_year(request,yk):
    years = YearEsoda.objects.all().order_by('-id')
    year = YearEsoda.objects.get(id=yk)
    months = MonthEsoda.objects.all().filter(year=year).order_by('-id')
    all_esoda = AddEsoda.objects.all().filter(year=year).order_by('-title')
    query = request.GET.get('search_pro')
    if query:
        all_esoda =all_esoda.filter(
            Q(title__icontains =query)|
            Q(month__title__icontains=query)
            ).distinct()

    context={
        'all_esoda':all_esoda,
        'years':years,
        'months':months,
        'year':year,

    }
    return render(request,'katastimata_esoda/show_year.html', context)


@staff_member_required
def esoda_income_choose_month(request,mk):
    month = MonthEsoda.objects.get(id=mk)
    years = YearEsoda.objects.all().order_by('-id')
    year = month.year
    months = MonthEsoda.objects.all().filter(year=year).order_by('-id')
    all_esoda = AddEsoda.objects.all().filter(month=month).order_by('-title')
    query = request.GET.get('search_pro')
    if query:
        all_esoda =all_esoda.filter(
            Q(title__icontains =query)|
            Q(month__title__icontains=query)
            ).distinct()

    context={
        'all_esoda':all_esoda,
        'years':years,
        'months':months,
        'year':year,
        'month':month,

    }
    return render(request,'katastimata_esoda/homepage.html', context)


@staff_member_required
def edit_day(request,dk):
    day_esodo = AddEsoda.objects.get(id=dk)
    day= day_esodo
    if request.POST:
        form = EsodaImerasForm(request.POST,instance=day_esodo)
        if form.is_valid():
            form.save(commit=False)
            form.edit(dk=dk)
            form.save()
            day_esodo.comments = form.cleaned_data.get('comments', None)
            day_esodo.save()
            day_esodo.sinolo_fisikon = day.skala + day.topiko_katastima + day.pediko + day.boom
            day_esodo.sinolo_olon = day.sinolo_fisikon + day.mymoda
            day_esodo.save()
            return HttpResponseRedirect('/katastimata/')
    else:
        form = EsodaImerasForm(instance=day_esodo)



    context={
        'form':form,
        'day_esodo':day_esodo,

    }
    return render(request,'katastimata_esoda/new_order.html', context)


@staff_member_required
def deactive_month(request):
    month = MonthEsoda.objects.last()
    month.status ='b'
    month.save()
    return HttpResponseRedirect('/katastimata/')

@staff_member_required
def create_new_month(request):
    title = ''
    year = YearEsoda.objects.last()
    if request.POST:
        form = MonthEsodaForm(request.POST, )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = MonthEsodaForm(initial={'year':year})

    context = {
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'PoS/admin_section_create_day.html', context)

@staff_member_required
def deactive_year(request):
    year = YearEsoda.objects.last()
    year.status ='b'
    year.save()
    return HttpResponseRedirect('/katastimata/')

    
@staff_member_required
def create_new_year(request):
    title = ''
    if request.POST:
        form = YearEsodaForm(request.POST, )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form =YearEsodaForm()

    context = {
        'form':form,
        'title':title,
    }
    context.update(csrf(request))
    return render(request, 'PoS/admin_section_create_day.html', context)
