from django import forms
from .models import *



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields ="__all__"







class Supplier_new(forms.ModelForm):


    class Meta:
        model = Supply
        fields = ('title','description','afm','phone','balance')

class CategoryNew(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'



class TaxesForm(forms.ModelForm):

    class Meta:
        model = TaxesCity
        fields = '__all__'




class CreateColor(forms.ModelForm):

    class Meta:
        model = Color
        fields = '__all__'


class CreateSize(forms.ModelForm):

    class Meta:
        model = Size
        fields = '__all__'






class ChangeQtyOrderForm(forms.ModelForm):

    class Meta:
        model = ChangeQtyOrder
        fields = '__all__'


class ChangeQtyOrderItemForm(forms.ModelForm):

    class Meta:
        model = ChangeQtyOrderItem
        fields = '__all__'


    def update_product(self):
        product = self.cleaned_data.get('title')
        qty = self.cleaned_data.get('qty')
        product.reserve += qty
        product.save()



class ChangeQtyOrderItemColorForm(forms.ModelForm):

    class Meta:
        model = ChangeQtyOrderItemColor
        fields = '__all__'


    def update_product(self):
        product_color = self.cleaned_data.get('title')

        qty = self.cleaned_data.get('qty')
        product_color.qty += qty
        product_color.save()

        product = product_color.product
        product.reserve += qty
        product.save()




class ChangeQtyOrderItemSizeForm(forms.ModelForm):

    class Meta:
        model = ChangeQtyOrderItemSize
        fields = '__all__'


    def update_product(self):
        product_size = self.cleaned_data.get('title')
        qty = self.cleaned_data.get('qty')
        product_size.qty += qty
        product_size.save()

        product = product_size.color.product
        product.reserve += qty
        product.save()

        product_color = product_size.color
        product_color.qty += qty
        product_color.save()