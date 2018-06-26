from django.db import models
from products.models import *
from decimal import Decimal
# Create your models here.


class PaymentMethodGroup(models.Model):
    # grouping of the payment methods , like Bank etc
    title = models.CharField(max_length=64,unique=True)
    balance = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    def __str__(self):
        return self.title


class PaymentMethod(models.Model):
    # create a unique Payment method like Cash, Paypal, a specific bank etc and
    # if you want you can group it with the payment_group
    title = models.CharField(max_length=64,unique=True)
    payment_group = models.ForeignKey(PaymentMethodGroup, null=True, blank=True)
    balance = models.DecimalField(default=0,max_digits=10,decimal_places=2)


    def __str__(self):
        return self.title


class VendorDepositOrder(models.Model):
    title = models.CharField(max_length=64,blank=True)
    payment_method = models.ForeignKey(PaymentMethod)
    vendor = models.ForeignKey(Supply)
    value = models.DecimalField(decimal_places=3,max_digits=10)
    day_added = models.DateField(auto_now=True)



    def __str__(self):
        return self.title





class Order(models.Model):
    CHOICES =(('a','Ολοκληρώθηκε'),('d','Δόσεις'),('p',"Σε αναμονή"),("c","Ακυρώθηκε"))
    code = models.CharField(max_length=40,verbose_name="Αριθμός Παραστατικού", unique=True)
    vendor = models.ForeignKey(Supply,verbose_name="Προμηθευτής")
    date = models.DateField(verbose_name="Ημερομηνία")
    status =models.CharField(max_length=1,choices=CHOICES,verbose_name="Σε εξέλιξη",default='p')
    notes = models.TextField(null=True,blank=True,verbose_name="")

    payment_method = models.ForeignKey(PaymentMethod,null=True, verbose_name='Τρόπος Πληρωμής')
    total_price_no_discount =models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Αξία προ έκπτωσης")
    total_discount = models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Αξία έκπτωσης")
    total_price_after_discount = models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Αξία μετά την έκπτωση")
    total_taxes = models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Φ.Π.Α")
    cost_transfer= models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Κόστος Μεταφοράς/Επιπλέον Κόστος")
    total_price = models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Τελική Αξία")
    credit_balance = models.DecimalField(default=0,max_digits=9,decimal_places=3,verbose_name="Πιστωτικό υπόλοιπο")


    class Meta:
        verbose_name="Τιμολόγια   "


    def __str__(self):
        return self.code

    def ipoloipo_xreostiko(self):
        return self.total_price - self.credit_balance

    def dept_remaining(self):
        return self.total_price - self.credit_balance




class Unit(models.Model):
    # Τεμάχ,Κιλά, Κιβώτ
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        ordering =['name']
        verbose_name="Μονάδα Μέτρησης  "





class OrderItem(models.Model):
    FPA_CHOICES =(("a",'13'),("b","23"),("c","24"),("d","0"))
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product,verbose_name='Προϊόν')
    unit=  models.ForeignKey(Unit,verbose_name='Μονάδα Μέτρησης')
    discount= models.IntegerField(default=0,verbose_name='Εκπτωση')
    taxes = models.CharField(max_length=1,choices=FPA_CHOICES,default="b",verbose_name='ΦΠΑ')
    qty =models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Ποσότητα')
    price =models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Τιμή Μονάδας')
    color = models.ForeignKey(ColorAttribute,verbose_name='Color',null=True, blank=True )
    size = models.ForeignKey(SizeAttribute, verbose_name='Size', null=True, blank=True)



    class Meta:
        ordering =['product']
        verbose_name="Συστατικά Τιμολογίου   "

    def __str__(self):
        return self.product.title

    def price_before_discount(self):
        pass

    def price_after_discount(self):
        pr = (self.price - (self.price*self.discount)/100)*self.qty
        if pr >=10:
            return str(pr)[0:5]
        elif pr<10:
            return str(pr)[0:3]
        else:
            return 0


    def price_after_taxes(self):
        price = Decimal(self.price)
        qty = Decimal(self.qty)
        taxes = self.get_taxes_display()
        taxes =Decimal(taxes)
        discount = self.discount
        discount = (price*discount)/100
        return ((price - discount)*(100+taxes))/100

    def total_value(self):
        return self.qty*self.price_after_taxes()


    def delete_order_item(self,foo):
        order_item = OrderItem.objects.get(id=foo)
        if order_item.taxes =='a':
            fpa = 0.13
        elif order_item.taxes == 'b':
            fpa=0.23
        elif order_item.taxes == 'c':
            fpa= 0.24
        else:
            fpa = 0
        order = Order.objects.get(id=order_item.order.id)
        order.total_price_no_discount -= Decimal(order_item.price*order_item.qty)
        order.total_discount -= (Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100))
        order.total_price_after_discount -= (Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))
        order.total_taxes -= ((Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))*Decimal(fpa))
        order.total_price -= (Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))+ ((Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))*Decimal(fpa))

        my_vendor = Supply.objects.get(title=order.vendor.title)
        my_vendor.balance -= (Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))+ ((Decimal(order_item.price*order_item.qty)-(Decimal(order_item.price*order_item.qty)*Decimal(order_item.discount/100)))*Decimal(fpa))
        my_product = Product.objects.get(title = order_item.product.title)
        my_product.reserve -= order_item.qty
        my_product.save()
        my_vendor.save()
        order.save()




class OrderItemColor(models.Model):
    title = models.ForeignKey(ColorAttribute)
    qty =models.DecimalField(max_digits=8,decimal_places=2,default=0, verbose_name='Ποσότητα')
    order_item = models.ForeignKey(OrderItem)

    def __str__(self):
        return self.title




class PayOrders(models.Model):
    CHOICES =(('a','Μετρητά'),('b','Πιστωτική'),('c','Μέσω Τραπέζης'))
    CHOICES2 =(('a','Εξόφληση συνολικής αξιας'),('b','Δόσεις'))
    date = models.DateField(verbose_name='Ημερομηνία')
    title = models.ForeignKey(Order,verbose_name='Αριθμός Παραστατικου')
    payment_method = models.ForeignKey(PaymentMethod, null=True, verbose_name='Τρόπος Πληρωμής')

    #this get removed on new version
    value_portion =models.CharField(default='b',max_length=1,choices=CHOICES2)
    way_of_pay = models.CharField(max_length=1,choices=CHOICES,default='a',verbose_name='Τρόπος Εξόφλησης')

    receipt = models.CharField(max_length=64,default='---',verbose_name='Απόδειξη')
    value= models.DecimalField(default=0,max_digits=10,decimal_places=3,verbose_name='Ποσό')

    class Meta:
        verbose_name="Εντολές Πληρωμής    "

    def __str__(self):
        return self.title.code




    def delete_pay_order(self,dk=None):
        pay_order = PayOrders.objects.get(id=dk)

        value = pay_order.value
        order = pay_order.title.code
        vendor = pay_order.title.vendor.title
        my_order = Order.objects.get(code=order)

        my_order.credit_balance -= value

        my_vendor = Supply.objects.get(title =vendor)
        my_vendor.balance += value


        if Decimal(value) >= Decimal(my_order.total_price):
            my_order.status = 'p'
        else:
            my_order.status = 'd'

        my_order.save()
        my_vendor.save()





class VendorDepositOrderPay(models.Model):
    # save the payments from deposit option
    title_de = models.CharField(max_length=64, blank=True, verbose_name='Σχόλια')
    payment_method = models.ForeignKey(PaymentMethod, verbose_name='Τρόπος Πληρωμής')
    order = models.ForeignKey(Order)
    value = models.DecimalField(decimal_places=3,max_digits=10, verbose_name='Ποσό πληρωμής')
    day_added = models.DateField(verbose_name='Ημερομηνία Πληρωμής')



    def __str__(self):
        return self.title_de





class CheckOrder(models.Model):
    CHOICES= (('a','Σε εξέλιξη'), ('b','Εισπράκτηκε'), ('c','Ακυρώθηκε'),)
    title = models.CharField(max_length=64,blank=True, null=True, verbose_name='Σχόλια')
    value = models.DecimalField(decimal_places=2,max_digits=255, verbose_name="Ποσό")
    debtor  =models.ForeignKey(Supply, verbose_name='Πιστωτής')
    place = models.ForeignKey(PaymentMethod, verbose_name='Τόπος- Τράπεζα')
    date_expire = models.DateField(verbose_name='Ημερομηνία Λήξης')
    date_added = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=CHOICES, default='a', verbose_name='Κατάσταση')

    class Meta:
        ordering=['-date_expire']
    def __str__(self):
        return self.title
