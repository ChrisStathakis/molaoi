from django.db import models

# Create your models here.

import datetime


class YearMeter(models.Model):
    title = models.IntegerField(default=2)

    def __str__(self):
        return str(self.title) + ' χρόνια.'


class YearEsoda(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(default=str(datetime.datetime.today().year), unique=True, max_length=64)
    paidiko_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    topiko_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    boom_income = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    skala_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    fisika_income= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    my_moda_incoome= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    ola_income= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    counter = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)
    comments = models.TextField(blank=True, null=True, verbose_name='Σχόλια')


    def __str__(self):
        return self.title

    def average_topiko(self):
        if self.counter ==0:
            return 0
        else:
            return self.topiko_income/self.counter

    def average_pediko(self):
        if self.counter ==0:
            return 0
        else:
            return self.paidiko_income/self.counter

    def average_skala(self):
        if self.counter ==0:
            return 0
        else:
            return self.skala_income/self.counter

    def average_mymoda(self):
        if self.counter ==0:
            return 0
        else:
            return self.my_moda_incoome/self.counter

    def average_fisika(self):
        if self.counter ==0:
            return 0
        else:
            return self.fisika_income/self.counter

    def average_ola(self):
        if self.counter ==0:
            return 0
        else:
            return self.ola_income/self.counter

    def average_boom(self):
        if self.counter != 0:
            return self.boom_income/self.counter
        return 0









class MonthEsoda(models.Model):
    CHOICES = (('a','Σε εξέλιξη'),('b','Εκλεισε'))
    title = models.CharField(default=str(datetime.datetime.now().strftime("%B")),max_length=64)
    topiko_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    paidiko_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    skala_income = models.DecimalField(default=0, max_digits=15,decimal_places=2)
    fisika_income= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    my_moda_incoome= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    ola_income= models.DecimalField(default=0, max_digits=15,decimal_places=2)
    counter = models.IntegerField(default=0)
    status = models.CharField(max_length=1, default='a',choices=CHOICES)
    year = models.ForeignKey(YearEsoda,null=True)

    def __str__(self):
        return self.title

    def average_topiko(self):
        if self.counter ==0:
            return 0
        else:
            return self.topiko_income/self.counter

    def average_pediko(self):
        if self.counter ==0:
            return 0
        else:
            return self.paidiko_income/self.counter

    def average_skala(self):
        if self.counter ==0:
            return 0
        else:
            return self.skala_income/self.counter

    def average_mymoda(self):
        if self.counter ==0:
            return 0
        else:
            return self.my_moda_incoome/self.counter

    def average_fisika(self):
        if self.counter ==0:
            return 0
        else:
            return self.fisika_income/self.counter

    def average_ola(self):
        if self.counter ==0:
            return 0
        else:
            return self.ola_income/self.counter




class Katastima(models.Model):
    title = models.CharField(max_length=24,verbose_name="Ονομασία Καταστήματος")



class AddEsoda(models.Model):
    title= models.DateField(verbose_name='Ημερομηνία')
    pediko = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Παιδικό')
    topiko_katastima = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Β Υποκατάστημα')
    boom = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Boom')
    skala = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Σκάλα')
    sinolo_fisikon  = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Σύνολο Φυσίκων')
    mymoda = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='MyModa')
    sinolo_olon = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='Όλα τα Έσοδα')
    comments = models.TextField(blank=True, null=True, verbose_name='Σχόλια')

    month = models.ForeignKey(MonthEsoda)
    year = models.ForeignKey(YearEsoda)

    def __str__(self):
        return str(self.title)
