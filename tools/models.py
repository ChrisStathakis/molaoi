from django.db import models

# Create your models here.






class ToolsProduct(models.Model):
    title = models.CharField(max_length=64,unique=True)
    show_number_of_products = models.IntegerField(default=50,max_length=200)

