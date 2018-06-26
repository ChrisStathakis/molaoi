from django import forms
from .models import *


class CategoryEdit(forms.ModelForm):

    class Meta:
        model = MainCategory
        fields = ['title','active','id_focus']

class CategorySubEdit(forms.ModelForm):

    class Meta:
        model = SecondaryCategory
        fields ='__all__'


class NewRecipeForm(forms.ModelForm):

    class Meta:
        model= Recipe
        fields ='__all__'
        exclude = ['recipe_cost']

class NewRecipeItem(forms.ModelForm):

    class Meta:
        model = RecipeItem
        fields = '__all__'
        exclude = ['price_cost',]

    def price_cost(self):
        product = self.cleaned_data.get('product')
        gr = self.cleaned_data.get('qty')
        item_recipe = RecipeItem.objects.all().last()
        price = product.price_buy
        discount = product.ekptosi
        qty= product.qty_kilo
        item_recipe.price_cost = Decimal(((price - (price*(discount)/100))/qty)*gr)
        item_recipe.save()

        recipe = Recipe.objects.all().last()
        recipe.recipe_cost += Decimal(((price - (price*(discount)/100))/qty)*gr)
        recipe.save()

    def edit_recipe_item(self,dk):
        recipe_item = RecipeItem.objects.get(id=dk)
        old_recipe_cost =recipe_item.price_cost
        gr = self.cleaned_data.get('qty')
        product = self.cleaned_data.get('product')
        recipe_name = self.cleaned_data.get('recipe_part')
        price = product.price_buy
        discount = product.ekptosi
        qty= product.qty_kilo

        recipe_item.recipe_part = recipe_name
        recipe_item.product = product
        recipe_item.qty =gr
        recipe_item.price_cost = Decimal(((price - (price*(discount)/100))/qty)*gr)

        recipe_item.save()

        recipe = Recipe.objects.get(title=recipe_item.recipe.title)
        recipe.recipe_cost -= old_recipe_cost
        recipe.recipe_cost += Decimal(((price - (price*(discount)/100))/qty)*gr)
        recipe.save()














