from django.db import models

# Create your models here.

class PaymentMethod(models.Model):
	title = models.CharField(unique=True, max_length=100)

	def __str__(self):
		return self.title

class Shipping(models.Model):
	title = models.CharField(unique=True, max_length=100)

	def __str__(self):
		return self.title

class Status(models.Model):
	title = models.CharField(unique=True, max_length=100)

	def __str__(self):
		return self.title

class WebOrder(models.Model):
	web_order = models.CharField(max_length=100)
	date = models.DateField(blank=True, null=True)
	value = models.DecimalField(default=0, decimal_places=2, max_digits=10)
	shipping_cost = models.DecimalField(default=0, decimal_places=0, max_digits=10)
	paid_value = models.DecimalField(default=0, decimal_places=2, max_digits=10)
	address = models.CharField(blank=True, null=True, max_length=200)
	city = models.CharField(blank=True, null=True, max_length=200)
	zip_code = models.CharField(blank=True, null=True, max_length=8)
	phone = models.CharField(blank=True, null=True, max_length=15)
	name = models.CharField(blank=True, null=True, max_length=150)	
	shipping_method = models.ForeignKey(Shipping, blank=True, null=True, on_delete=models.SET_NULL)
	payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.SET_NULL)
	is_paid = models.BooleanField(default=False)
	is_cancel = models.BooleanField(default=False)
	status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.web_order

	class Meta:
		ordering = ['-date']
			



		
		