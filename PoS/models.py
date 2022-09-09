from turtle import onclick
from django.db import models
from recipes.models import *
from django.utils import timezone

# Create your models here.


class YearlyIncomeGreg(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(default=str(datetime.datetime.today().year), unique=True, max_length=64)
    money_income = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    money_outcome = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    order_number = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)

    def __str__(self):
        return self.title

    def show_profit(self):
        if self.money_outcome == 0:
            return 0
        else:
            return self.money_income - self.money_outcome

    def show_profit_percent(self):
        if self.money_outcome == 0:
            return 0
        else:
            return (self.show_profit()/self.money_income)*100

    def show_average_profit_per_order(self):
        if self.order_number ==0:
            return 0
        else:
            return self.show_profit()/self.order_number

    def show_average_order_income(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_income/self.order_number

    def show_average_order_outcome(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_outcome/self.order_number




class UserInputIncomeSeason(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(max_length=64)
    date = models.DateField(default=timezone.now)
    date_done = models.DateField(default=timezone.now)
    money_income = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    money_outcome = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    order_number = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)

    def __str__(self):
        return self.title

    def show_profit(self):
        if self.money_outcome == 0:
            return 0
        else:
            return self.money_income - self.money_outcome

    def show_profit_percent(self):
        if self.money_outcome == 0:
            return 0
        else:
            return (self.show_profit()/self.money_income)*100

    def show_average_order_income(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_income/self.order_number

    def show_average_order_outcome(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_outcome/self.order_number






class MonthlyIncomeGreG(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(default=str(datetime.datetime.now().strftime("%B")),max_length=64)
    money_income = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    money_outcome = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    order_number = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)
    year = models.ForeignKey(YearlyIncomeGreg,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def show_profit(self):
        if self.money_outcome == 0:
            return 0
        else:
            return self.money_income - self.money_outcome

    def show_profit_percent(self):
        if self.money_outcome == 0:
            return 0
        else:
            return (self.show_profit()/self.money_income)*100

    def show_average_profit_per_order(self):
        if self.order_number ==0:
            return 0
        else:
            return self.show_profit()/self.order_number





    def show_average_order_income(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_income/self.order_number

    def show_average_order_outcome(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_outcome/self.order_number




class DailyIncomeGreG(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(default=str(datetime.datetime.today().date()),unique=True, max_length=64)
    date = models.DateField(default=timezone.now)
    money_income = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    money_outcome = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    order_number = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)
    month = models.ForeignKey(MonthlyIncomeGreG,null=True, on_delete=models.CASCADE)
    year = models.ForeignKey(YearlyIncomeGreg,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def show_profit(self):
        if self.money_outcome == 0:
            return 0
        else:
            return self.money_income - self.money_outcome

    def show_profit_percent(self):
        if self.money_outcome == 0:
            return 0
        else:
            return (self.show_profit()/self.money_income)*100

    def show_average_profit_per_order(self):
        if self.order_number ==0:
            return 0
        else:
            return self.show_profit()/self.order_number



    def show_average_order_income(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_income/self.order_number

    def show_average_order_outcome(self):
        if self.order_number ==0:
            return 0
        else:
            return self.money_outcome/self.order_number










class Table(models.Model):
    STATUS_ =(('a','Διαθέσιμο'),('b','Παραγγελία σε εξέλιξη'),('c','Απενεργοποιημένπ'))
    title = models.CharField(max_length=10, unique=True, )
    status = models.CharField(max_length=1, choices=STATUS_, default='a')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name="Τραπέζια"



class RestoOrder(models.Model):
    STATUS_CHOICES =(('a','Σε εξέλιξη'),('b','Αποπληρώθηκε'),('c','Ακύρωση'))
    title = models.CharField(max_length=50,default=timezone.now)
    notes = models.TextField(null=True,blank=True)
    table = models.ForeignKey(Table,verbose_name='Τραπέζι', on_delete=models.CASCADE)
    day_added = models.DateTimeField(default=timezone.now)
    discount = models.IntegerField(default=0, verbose_name='Έκπτωση',)

    value = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Αξία Παραγγελίας')
    total_cost  = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Συνολικό Κόστος Παραγγελίας')
    paid_value = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Αποπληρωμένο Πόσο')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default='a')




    year = models.ForeignKey(YearlyIncomeGreg, null=True, blank=True, on_delete=models.CASCADE)
    month =models.ForeignKey(MonthlyIncomeGreG,null=True, blank=True, on_delete=models.CASCADE)
    day = models.ForeignKey(DailyIncomeGreG,null=True,blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name="Παραγγελία Εστιατορίου"
        
        
        
    def remaining_value(self):
        return str(self.value - self.paid_value)

    def __str__(self):
        return self.title

    def order_table_closed(self,dk):
        # gets the order
        order = RestoOrder.objects.get(id= dk)


        #updates the daily ,monthly,yearly incomes and costs
        order.day.money_income += order.paid_value
        order.day.money_outcome +=order.total_cost
        order.day.save()

        order.month.money_income += order.paid_value
        order.month.money_outcome += order.total_cost
        order.month.order_number +=1
        order.month.save()

        order.year.money_income += order.paid_value
        order.year.money_outcome += order.total_cost
        order.year.order_number +=1
        order.year.save()
        #---------------------------------

        #get the order products
        order_items = order.restoorderitem_set.all()
        for ele in order_items:
            # order quantity per item
            quantity = ele.qty
            # updates the Recipes categories cost and income
            ele.title.category.day_cost += ele.title.recipe_cost*ele.qty
            ele.title.category.month_cost += ele.title.recipe_cost*ele.qty
            ele.title.category.yearly_cost += ele.title.recipe_cost*ele.qty
            #ele.title.category.costum_cost_cost += ele.title.recipe_cost

            ele.title.category.day_income += ele.title.recipe_price*ele.qty
            ele.title.category.month_income += ele.title.recipe_price*ele.qty
            ele.title.category.yearly_income += ele.title.recipe_price*ele.qty
            #ele.title.category.costum_income += ele.title.recipe_price
            ele.title.category.save()

            #gets th products for every recipe
            recipe_item = ele.title.recipeitem_set.all()
            #updates the warehouse stock for very product used on Recipes
            for ele in recipe_item:
                qty_kila = ele.product.qty_kilo
                posotita = ele.qty
                ele.product.reserve -= (quantity*posotita)/qty_kila
                ele.product.save()

        order.status='b'
        order.save()






class RestoOrderItem(models.Model):
    title = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order = models.ForeignKey(RestoOrder, on_delete=models.CASCADE)
    cost =  models.DecimalField(max_digits=6,decimal_places=2,default=0)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    qty= models.DecimalField(max_digits=3,decimal_places=1,default=1, verbose_name='Ποσότητα')

    class Meta:
        verbose_name="Συστατικά Παραγγελίας Εστιατορίου"

    def __str__(self):
        return self.title

    def total_price(self):
        return str(self.qty*self.price)


    def delete_from_order(self,dk):
        order = RestoOrder.objects.get(id = dk)
        price = self.price
        cost =self.cost
        qty = self.qty
        value = price*qty
        cost_value = cost*qty
        order.value -= Decimal(value)
        order.total_cost -= Decimal(cost_value)
        order.save()




#-------------------------Lianiki, epistrofes--------------------------------------------------------------------------------------


class Lianiki_Order(models.Model):
    title = models.CharField(max_length=50,default=datetime.datetime.now())
    notes = models.TextField(null=True,blank=True)
    day_added = models.DateTimeField(default=datetime.datetime.now())
    discount = models.IntegerField(default=0, verbose_name='Έκπτωση',)
    value = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Αξία Παραγγελίας')
    total_cost  = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Συνολικό Κόστος Παραγγελίας')
    paid_value = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Αποπληρωμένο Πόσο')
    year = models.ForeignKey(YearlyIncomeGreg,null=True,blank=True, on_delete=models.CASCADE)
    month =models.ForeignKey(MonthlyIncomeGreG,null=True, blank=True, on_delete=models.CASCADE)
    day = models.ForeignKey(DailyIncomeGreG,null=True,blank=True, on_delete=models.CASCADE)

    def remaining_value(self):
        return str(self.value - self.paid_value)

    def __str__(self):
        return self.title

    def order_table_closed(self,dk):
        # gets the order
        order_lianiki = Lianiki_Order.objects.get(id= dk)
        #---------------------------------

        #get the order products
        order_items = order_lianiki.lianikiorderitem_set.all()
        for ele in order_items:
            # order quantity per item
            quantity = ele.qty
            qty_kila = ele.title.qty_kilo
            #posotita = ele.qty
            ele.title.reserve -= quantity/qty_kila
            ele.title.save()



        order_lianiki.status='b'
        order_lianiki.save()

class LianikiOrderItem(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Lianiki_Order, on_delete=models.CASCADE)
    cost =  models.DecimalField(max_digits=6,decimal_places=2,default=0)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Τιμή Μονάδας')
    qty= models.DecimalField(max_digits=3,decimal_places=1,default=1, verbose_name='Ποσότητα')

    #if needed
    color = models.ForeignKey(ColorAttribute, blank=True, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(SizeAttribute, blank=True ,null=True, on_delete=models.SET_NULL)




    def __str__(self):
        return self.title

    def total_price(self):
       return str(self.qty*self.price)

    def delete_from_order_with_color(self, color_attritube, size_attritube):
        #this used with the next one, its additional code
        # to delete the extra models. If the product have color is checked always
        #from the view
        color_attritube.qty +=1
        color_attritube.save()
        size_attritube.qty += 1
        size_attritube.save()

    def delete_from_order_with_only_color(self, color_attritube):
        #this used with the next one, its additional code
        # to delete the extra models. If the product have color is checked always
        #from the view
        color_attritube.qty +=1
        color_attritube.save()







    def delete_from_order(self, dk, order_item):
        order = Lianiki_Order.objects.get(id = dk)

        #update order
        price = self.price
        cost =self.cost
        qty = self.qty
        value = price*qty
        cost_value = cost*qty
        order.value -= Decimal(value)
        order.total_cost -= Decimal(cost_value)
        order.save()

        #update warehouse
        product = order_item.title

        if product.qty_kilo !=0:
            product.reserve += qty/product.qty_kilo
        else:
            product.reserve += qty
        product.save()




    def update_order_with_color(self, lianiki_order):

        lianiki_order.value += self.price
        lianiki_order.total_cost += self.cost
        lianiki_order.save()

    def update_stock_house_with_color(self, product, color_attritube, size_attritube):

        product.reserve -= 1
        product.save()
        color_attritube.qty -= 1
        color_attritube.save()
        size_attritube.qty -= 1
        size_attritube.save()


    def update_order_with_only_color(self, lianiki_order):
        lianiki_order.value += self.price
        lianiki_order.total_cost += self.cost
        lianiki_order.save()


    def update_stock_house_with_only_color(self, product, color_attritube):
        product.reserve -= 1
        product.save()
        color_attritube.qty -= 1
        color_attritube.save()






class RetailReturnOrder(models.Model):
    title = models.DateField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost  = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    def __str__(self):
        return self.title


class RetailReturnItem(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(RetailReturnOrder, on_delete=models.CASCADE)
    cost  =  models.DecimalField(max_digits=6,decimal_places=2,default=0)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name='Τιμή Μονάδας')
    qty   = models.DecimalField(max_digits=3,decimal_places=1,default=1, verbose_name='Ποσότητα')




    def __str__(self):
        return self.title

    def total_price(self):
       return str(self.qty*self.price)

    def update_order_and_warehouse(self):

        #update_order
        order = self.order


        if self.title.qty_kilo == 1:
            order.cost += self.cost
            order.price += self.price
        else:
            order.cost += self.cost*()



