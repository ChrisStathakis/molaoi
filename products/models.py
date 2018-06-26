from django.db import models
import os
from django.core.urlresolvers import reverse
from django.utils import timezone
from time import time
import datetime

# Create your models here.

FOCUS = (
    ('a','Active'),
    ('n','Not active')
)
STATUS=(
    ('a','Σε απόθεμα'),
    ('i','Inactive'),
    ('o','Διαθέσιμο με παραγγελία'),
    ('p','Προσωρινά μη διαθέσιμο'),

)

def upload_location(instance, filename):
    return "%s%s" %(instance.id,filename)

def my_awesome_upload_function(instance, filename):
    """ this function has to return the location to upload the file """
    return os.path.join('/media_cdn/%s/' % instance.id, filename)

class Category(models.Model):

    title = models.CharField(unique=True,max_length=70,verbose_name='Τίτλος Κατηγορίας')
    description = models.TextField(null=True,blank=True, verbose_name='Περιγραφή')

    class Meta:
        ordering=['title']
        verbose_name="Κατηγορίες  "


    def __str__(self):
        return self.title


class TaxesCity(models.Model):
    title = models.CharField(max_length=64,unique=True)

    class Meta:
        verbose_name="ΔΟΥ   "

    def __str__(self):
        return self.title


class Supply(models.Model):
    title = models.CharField(unique=True, max_length=70,verbose_name="'Ονομα")
    afm = models.CharField(max_length=9,blank=True,null=True,verbose_name="ΑΦΜ")
    doy = models.ForeignKey(TaxesCity,verbose_name='Εφορία',null=True,blank=True)
    phone =models.CharField(max_length=10,null=True,blank=True,verbose_name="Τηλέφωνο")
    phone1=models.CharField(max_length=10,null=True,blank=True,verbose_name="Τηλέφωνο")
    fax= models.CharField(max_length=10,null=True,blank=True,verbose_name="Fax")
    email =models.EmailField(null=True,blank=True,verbose_name="Email")
    balance = models.DecimalField(default=0,max_digits=10, decimal_places=3,verbose_name="Υπόλοιπο")
    site =models.CharField(max_length=40,blank=True,null=True, verbose_name='Site')
    address = models.CharField(max_length=40,null=True,blank=True,verbose_name='Διεύθυνση')
    description = models.TextField(null=True,blank=True,verbose_name="Περιγραφή")
    date_added = models.DateField(default=timezone.now)

    #managing deposits
    remaining_deposit = models.DecimalField(default=0,decimal_places=2, max_digits=10, verbose_name='Υπόλοιπο προκαταβολών')




    def __str__(self):
        return self.title

    def get_absolute_url_form(self):
        return reverse('edit_vendor_id',kwargs={'dk':self.id})

    class Meta:
        ordering =['title']
        verbose_name="Προμηθευτές   "





class Costumers(models.Model):
    title = models.CharField(unique=True, max_length=70,verbose_name="Ονομα/Επωνυμία")
    date_added = models.DateField(default=timezone.now)
    description = models.TextField(null=True,blank=True,verbose_name="Περιγραφή")
    phone =models.CharField(max_length=10,null=True,blank=True,verbose_name="Τηλέφωνο")
    phone1=models.CharField(max_length=10,null=True,blank=True,verbose_name="Τηλέφωνο")
    fax= models.CharField(max_length=10,null=True,blank=True,verbose_name="Fax")
    email =models.EmailField(null=True,blank=True,verbose_name="Email")
    site =models.CharField(max_length=40,blank=True,null=True, verbose_name='Site')
    address = models.CharField(max_length=40,null=True,blank=True,verbose_name='Διεύθυνση')
    balance = models.DecimalField(default=0,max_digits=10, decimal_places=3,verbose_name="Υπόλοιπο")
    afm = models.CharField(max_length=9,blank=True,null=True,verbose_name="ΑΦΜ")
    DOY = models.ForeignKey(TaxesCity,verbose_name='Εφορία',blank=True,null=True)

    def __str__(self):
        return self.title







class Product(models.Model):

    CHOICES=(('a','Ενεργοποιημένο'),('b','Απενεργοποιημένο'))
    title = models.CharField(unique=True,max_length=70,verbose_name="'Ονομα προιόντος")
    description = models.CharField(null=True,blank=True,max_length=100, verbose_name="Κωδικός Τιμολογίου")

    price_buy = models.DecimalField(decimal_places=2,max_digits=6,default=0,verbose_name="Τιμή Αγοράς") # the price which you buy the product
    image =models.FileField(null=True,blank=True,)

    category = models.ForeignKey(Category)
    supplier = models.ForeignKey(Supply,verbose_name="Προμηθευτής")
    costumer =models.ForeignKey(Costumers,null=True,blank=True,verbose_name="Πελάτης")

    carousel = models.CharField(max_length=1,choices=FOCUS, default='n',verbose_name="Υπερχονδρική")
    reserve =models.DecimalField(default=0,verbose_name="Απόθεμα",max_digits=10, decimal_places=2)
    product_id = models.CharField(max_length=6,null=True,blank=True, verbose_name='Κωδικός/Barcode')
    ekptosi = models.IntegerField( null=True,blank=True, default=0,verbose_name="'Εκπτωση Τιμολογίου σε %")
    day_added = models.DateField( default=timezone.now,verbose_name='Ημερομηνία Δημιουργίας')
    qty_kilo = models.DecimalField(max_digits=5, decimal_places=3, default=1,verbose_name='Βάρος/Τεμάχια ανά Συσκευασία ')
    notes =models.TextField(null=True,blank=True,verbose_name='Περιγραφή')

    safe_stock = models.DecimalField(max_digits=5,decimal_places=2,default=0)


    #site attritubes
    ware_active = models.CharField(max_length=1,default='a',choices=CHOICES, null=True, verbose_name='Κατάσταση' )
    status = models.CharField(max_length=1,choices=STATUS,verbose_name="Κατάσταση",default='a')

    # price sell and discount sells
    price =models.DecimalField(decimal_places=2,max_digits=6,default=0, verbose_name="Τιμή λιανικής") #the price product have in the store
    price_internet= models.DecimalField(decimal_places=2,max_digits=6,default=0,verbose_name="Τιμή Internet")
    price_b2b= models.DecimalField(decimal_places=2,max_digits=6,default=0,verbose_name="Τιμή Χονδρικής") #the price product have in the website, if its 0 then website gets the price from store
    price_discount = models.DecimalField(max_digits=10,decimal_places=2,default=0,)


    #size and color
    CHOICES2 = (('a','True'),('b','False'))
    size  = models.CharField(max_length=1, choices=CHOICES2, default='b', verbose_name='Μεγεθολόγιο Μεγεθών')
    color = models.CharField(max_length=1, choices=CHOICES2, default='b', verbose_name='Μεγεθολόγιο Χρωμάτων')


    class Meta:
        ordering =['title']
        verbose_name_plural ="Προϊόντα"

    def show_warehouse_remain(self):
        return self.reserve * self.qty_kilo


    def check_safe_stock(self):
        current_stock = self.reserve*self.qty_kilo
        if self.safe_stock == 0:
            return 'a'
        elif self.safe_stock >= current_stock:
            return 'b'
        else:
            return 'a'

    def __str__(self):
        return self.title

    def price_with_discount(self):
        price =  (float(self.price_buy)- float(self.price_buy*self.ekptosi)/100)
        if price<10:
            return str(price)[0:4]
        elif price>=10:
            return str(price)[0:5]
        else:
            return 0

    #check if have size and color
    def check_color(self):
        if self.color == 'b':
            return False
        else:
            return True

    def check_size(self):
        if self.size =='b':
            return False
        else:
            return True


    #check if discount exists
    def check_discount_on_sales(self):
        if self.price_discount == 0:
            return False
        else:
            return True


    def get_queryset(self):
        pass



class Color(models.Model):
    STATUS = (('a','Ενεργό'),('b','Μη Ενεργό'))
    title = models.CharField(max_length=64, unique=True, verbose_name='Ονομασία Χρώματος')
    status = models.CharField(max_length=1, default='a',choices=STATUS, verbose_name='Κατάσταση')

    def __str__(self):
        return self.title



class Size(models.Model):
    STATUS = (('a','Ενεργό'),('b','Μη Ενεργό'))
    title = models.CharField(max_length=64, unique=True, verbose_name='Ονομασία Μεγέθους')
    status = models.CharField(max_length=1, default='a',choices=STATUS, verbose_name='Κατάσταση')

    class Meta:
        ordering =['title']

    def __str__(self):
        return self.title



class ColorAttribute(models.Model):
    title = models.ForeignKey(Color,)
    qty = models.IntegerField(default=0)
    product = models.ForeignKey(Product,null=True, blank= True)
    order_discount = models.IntegerField(null=True,blank=True, default=0,verbose_name="'Εκπτωση Τιμολογίου σε %")
    price_buy = models.DecimalField(decimal_places=2,max_digits=6,default=0,verbose_name="Τιμή Αγοράς") # the price which you buy the product

    class Meta:
        ordering =['title']
        unique_together = ('title', 'product')

    def __str__(self):
        return self.product.title + '. Χρώμα : ' + self.title.title

    def check_product_in_order(self):
        return str(self.product.title + '. Χρώμα : ' + self.title.title)


class SizeAttribute(models.Model):
    title = models.ForeignKey(Size)
    qty = models.IntegerField(default=0)
    color = models.ForeignKey(ColorAttribute, null=True, blank=True)
    order_discount = models.IntegerField(null=True,blank=True, default=0,verbose_name="'Εκπτωση Τιμολογίου σε %")
    price_buy = models.DecimalField(decimal_places=2,max_digits=6,default=0,verbose_name="Τιμή Αγοράς") # the price which you buy the product

    def __str__(self):
        return self.color.product.title + '. Χρώμα : ' + self.color.title.title + ', Μέγεθος : ' +self.title.title

    def check_product_in_order(self):
        return str(self.color.product.title + '. Χρώμα : ' + self.color.title.title + ', Μέγεθος : ' +self.title.title)








class ChangeQtyOrder(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Σχολιασμός')
    day_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class ChangeQtyOrderItem(models.Model):
    title = models.ForeignKey(Product)
    order = models.ForeignKey(ChangeQtyOrder)
    qty = models.DecimalField(default=0, max_digits=6, decimal_places=2)



class ChangeQtyOrderItemColor(models.Model):
    title = models.ForeignKey(ColorAttribute)
    order = models.ForeignKey(ChangeQtyOrder)
    qty = models.DecimalField(default=0, max_digits=6, decimal_places=2)

class ChangeQtyOrderItemSize(models.Model):
    title = models.ForeignKey(SizeAttribute)
    order = models.ForeignKey(ChangeQtyOrder)
    qty = models.DecimalField(default=0, max_digits=6, decimal_places=2)
