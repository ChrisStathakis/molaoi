from django.shortcuts import render

# Create your views here.
from inventory_manager.models import PaymentMethodGroup, Unit

def set_up_database(request):
    #creates needed models for the database!
    bank = PaymentMethodGroup.objects.create(title ='Bank', balance = 0)
    bank.save()

    # Τεμάχ,Κιλά, Κιβώτ
    #kilos = Unit.objects.create(title=Τεμάχ'')

