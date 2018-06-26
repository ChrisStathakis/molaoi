from django.shortcuts import render, HttpResponseRedirect

# Create your views here.

from transcations.models import *
from inventory_manager.models import *


def set_up_database(request):
    #creates the models that the database need to start_working
    #disable that url after the use for no duplicate models.

    payment_method = PaymentMethodGroup.objects.create(title='Bank')
    payment_method.save()

    # Τεμάχ,Κιλά, Κιβώτ
    unit_a = Unit.objects.create(name= 'Τεμάχ')
    unit_a.save()
    unit_b = Unit.objects.create(name ='Κιλά')
    unit_b.save()
    unit_c = Unit.objects.create(name= 'Κιβώτ')
    unit_c.save()

    #Λογαριασμοί, Προσωπικό, Αγορές
    fixed_cost = Fixed_costs.objects.create(title= 'Λογαριασμοί')
    fixed_cost.save()
    fixed_cost = Fixed_costs.objects.create(title= 'Προσωπικό')
    fixed_cost.save()
    fixed_cost = Fixed_costs.objects.create(title= 'Αγορές')
    fixed_cost.save()

    # Μισθός, IKA/TEBE, Extra,
    cate = CategoryPersonPay.objects.create(title ='Μισθός',  )
    cate.save()
    cate = CategoryPersonPay.objects.create(title ='IKA/TEBE')
    cate.save()
    cate = CategoryPersonPay.objects.create(title ='Extra')
    cate.save()

    #Αγορές, Επισκευές, Διάφορα Έξοδα

    fixed_assets = Pagia_Exoda.objects.create(title = 'Αγορές', category = Fixed_costs.objects.get(id=3))
    fixed_assets.save()
    fixed_assets = Pagia_Exoda.objects.create(title = 'Επισκευές',category = Fixed_costs.objects.get(id=3))
    fixed_assets.save()
    fixed_assets = Pagia_Exoda.objects.create(title = 'Διάφορα Έξοδα',category = Fixed_costs.objects.get(id=3))
    fixed_assets.save()
    return HttpResponseRedirect('/')


