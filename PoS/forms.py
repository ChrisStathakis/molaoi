from django import forms
from .models import *


class NewOrderForm(forms.ModelForm):


    class Meta:
        model = RestoOrder
        fields = ['title','notes','table','day','month','year']


class PayRestoOrderForm(forms.ModelForm):

    class Meta:
        model = RestoOrder
        fields =['paid_value']


class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = RestoOrderItem
        fields = '__all__'

    def add_recipe(self,dk):
        order = RestoOrder.objects.get(id= dk)
        price = self.cleaned_data.get('price')
        cost = self.cleaned_data.get('cost')
        qty = self.cleaned_data.get('qty')

        value = Decimal(price*qty)
        cost = Decimal(cost*qty)



        order.value += value
        order.total_cost += cost

        order.save()


    def edit_recipe(self, dk,pk):
        order = RestoOrder.objects.get(id= dk)
        order_item = RestoOrderItem.objects.get(id= pk)
        price = self.cleaned_data.get('price')
        qty = self.cleaned_data.get('qty')
        cost = self.cleaned_data.get('cost')


        order.value -= Decimal(order_item.price*order_item.qty)
        order.value += Decimal(price*qty)
        order.total_cost -=Decimal(order_item.cost*order_item.qty)
        order.total_cost += Decimal(cost*qty)

        order.save()




#  ---------------------- Create a data for day,month, year incomes etc------------------------------------------------------------


class DailyIncomeForm(forms.ModelForm):

    class Meta:
        model = DailyIncomeGreG
        fields =['title','month','year']

class MonthlyIncomeForm(forms.ModelForm):

    class Meta:
        model = MonthlyIncomeGreG
        fields =['title','year']


class YearlyIncomeForm(forms.ModelForm):

    class Meta:
        model = YearlyIncomeGreg
        fields =['title']


class UserIncomeForm(forms.ModelForm):

    class Meta:
        model = UserInputIncomeSeason
        fields ='__all__'






#--------------------------------------Lianiki Section----------------------------------------------

class LianikiForm(forms.ModelForm):

    class Meta:
        model= Lianiki_Order
        fields =['day','month','year','title','notes',]

class LianikiAddItemForm(forms.ModelForm):

    class Meta:
        model = LianikiOrderItem
        fields ="__all__"

    def add_item(self, dk, product ):
        order = Lianiki_Order.objects.get(id= dk)
        price = self.cleaned_data.get('price')
        cost = self.cleaned_data.get('cost')
        qty = self.cleaned_data.get('qty')

        #updates the order
        value = Decimal(price*qty)
        cost = Decimal(cost*qty)
        order.value += value
        order.total_cost += cost
        order.save()

        #updates the warehouse
        if product.qty_kilo != 0:
            product.reserve -= qty/product.qty_kilo
            product.save()
        else:
            product.reserve -= qty
            product.save()




    def edit_item(self,dk, pk):
        order = Lianiki_Order.objects.get(id= dk)
        order_item = LianikiOrderItem.objects.get(id= pk)
        price = self.cleaned_data.get('price')
        qty = self.cleaned_data.get('qty')
        cost = self.cleaned_data.get('cost')

        #update the order
        order.value -= Decimal(order_item.price*order_item.qty)
        order.value += Decimal(price*qty)
        order.total_cost -=Decimal(order_item.cost*order_item.qty)
        order.total_cost += Decimal(cost*qty)
        order.save()

        #update the warehouse
        product = order_item.title
        if product.qty_kilo != 0:
            product.reserve += order_item.qty/product.qty_kilo
            product.reserve -= qty/product.qty_kilo
            product.save()
        else:
            product.reserve += order_item.qty
            product.reserve -= qty
            product.save()



class PayLianikirderForm(forms.ModelForm):

    class Meta:
        model = Lianiki_Order
        fields =['paid_value']