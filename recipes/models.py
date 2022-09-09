from django.db import models
from inventory_manager.models import*

# Create your models here.



# Setting the categories!
class SecondaryCategory(models.Model):
    title = models.CharField(max_length=64)
    id_focus = models.IntegerField(default=1)

    class Meta:
        ordering =['id_focus','title']

    def __str__(self):
        return self.title

class MainCategory(models.Model):
    STATUS = (('a','Ενεργό'),('i','Μη Ενεργό'))
    title = models.CharField(max_length=64)
    sub_category = models.ForeignKey(SecondaryCategory,blank=True,null=True, on_delete=models.CASCADE)
    id_focus = models.IntegerField(default=1)
    active = models.CharField(max_length=1,choices=STATUS, default='a',verbose_name='Κατάσταση')
    day_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Ημερήσιο Κόστος')
    month_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Μηνιαίο κόστος')
    yearly_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Έτος κόστος')
    costum_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Επιλογή χρήστη κόστος')
    
    
    day_income = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Ημερήσιο Κόστος')
    month_income = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Μηνιαίο κόστος')
    yearly_income = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Έτος κόστος')
    costum_income = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Επιλογή χρήστη κόστος')

    class Meta:
        ordering =['id_focus','title']
        verbose_name="Κεντρική Κατηγορία Menu."

    def __str__(self):
        return self.title

class CategoryCata(models.Model):
    title = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SecondaryCategory, on_delete=models.CASCADE)
    id_focus = models.IntegerField(default=1)
    
    

    class Meta:
        ordering =['title','sub_category']

    def __str__(self):
        return self.title.title+ ' - ' + self.sub_category.title








class Recipe(models.Model):
    STATUS = (('a','Ενεργό'),('i','Μη Ενεργό'))
    title = models.CharField(max_length=62,verbose_name='Όνομα Συνταγής',unique=True)
    category = models.ForeignKey(MainCategory,verbose_name='Κατηγορία', on_delete=models.CASCADE)
    active = models.CharField(max_length=1,choices=STATUS, default='a',verbose_name='Κατάσταση')
    description = models.TextField(blank=True,verbose_name='Πληροφορίες')
    recipe_cost = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Κόστος Παραγωγής')
    recipe_price = models.DecimalField(max_digits=10,decimal_places=2, default=0,verbose_name='Τιμή Πωλησης')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name="Συνταγή    "


class RecipeItem(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Συνταγή', on_delete=models.CASCADE)
    recipe_part =models.CharField(max_length=64, verbose_name='Συστατικό')
    product = models.ForeignKey(Product, verbose_name='Προιόν ', on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=8,decimal_places=3,verbose_name='Ποσότητα σε κιλά')
    price_cost = models.DecimalField(default=0,max_digits=8,decimal_places=3,verbose_name='Κόστος')

    def __str__(self):
        return self.recipe_part
        
        
    class Meta:
        verbose_name="Συστατικά Συνταγής   "

    def delete_recipe_item(self,dk):
        recipe_item = RecipeItem.objects.get(id=dk)
        recipe = Recipe.objects.get(title = recipe_item.recipe.title)
        recipe.recipe_cost -= recipe_item.price_cost
        recipe.save()
        recipe_item.delete()








