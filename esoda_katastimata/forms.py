from django import forms
from .models import *

class MonthEsodaForm(forms.ModelForm):

    class Meta:
        model= MonthEsoda
        fields = ['title','year']


class YearEsodaForm(forms.ModelForm):

    class Meta:
        model= YearEsoda
        fields = ['title']

class EsodaImerasForm(forms.ModelForm):
    title = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2050),))
    class Meta:
        model= AddEsoda
        fields = '__all__'
        exclude = ['sinolo_olon','sinolo_fisikon']
        #['title','topiko_katastima','pediko','skala','mymoda']

    def add(self):
        day = AddEsoda.objects.last()
        day.sinolo_fisikon = day.skala + day.topiko_katastima + day.pediko + day.boom
        day.sinolo_olon = day.sinolo_fisikon + day.mymoda
        day.save()

        day.month.topiko_income += day.topiko_katastima
        day.month.paidiko_income += day.pediko
        day.month.skala_income += day.skala
        day.month.fisika_income += day.sinolo_fisikon
        day.month.my_moda_incoome += day.mymoda
        day.month.ola_income += day.sinolo_olon
        day.month.counter +=1
        day.month.save()

        day.year.topiko_income += day.topiko_katastima
        day.year.paidiko_income += day.pediko
        day.year.skala_income += day.skala
        day.year.fisika_income += day.sinolo_fisikon
        day.year.my_moda_incoome += day.mymoda
        day.year.ola_income += day.sinolo_olon
        day.year.counter +=1
        day.year.save()


    def edit(self,dk):
        topiko = self.cleaned_data.get('topiko_katastima')
        pediko = self.cleaned_data.get('pediko')
        skala = self.cleaned_data.get('skala')
        mymoda = self.cleaned_data.get('mymoda')
        boom = self.cleaned_data.get('boom')
        day = AddEsoda.objects.get(id=dk)

        #remove olds
        

        day.month.topiko_income -= day.topiko_katastima
        day.month.paidiko_income -= day.pediko
        day.month.skala_income -= day.skala
        #day.month.boom -= day.boom
        day.month.fisika_income -= day.sinolo_fisikon
        day.month.my_moda_incoome -= day.mymoda
        day.month.ola_income -= day.sinolo_olon
        day.month.save()

        day.year.topiko_income -= day.topiko_katastima
        day.year.paidiko_income -= day.pediko
        day.year.skala_income -= day.skala
        day.year.fisika_income -= day.sinolo_fisikon
        day.year.my_moda_incoome -= day.mymoda
        day.year.ola_income -= day.sinolo_olon
        day.year.save()

        #add new values
        day.topiko_katastima = topiko
        day.pediko =pediko
        day.skala =skala
        day.mymoda = mymoda
        day.boom  = boom
        day.sinolo_fisikon = topiko + skala + pediko + boom
        day.sinolo_olon = day.sinolo_fisikon + mymoda
        day.save()


        day.month.topiko_income += topiko
        day.month.paidiko_income += pediko
        day.month.skala_income += skala
        day.month.fisika_income += day.sinolo_fisikon
        day.month.my_moda_incoome += mymoda
        day.month.ola_income += day.sinolo_olon
        day.month.save()

        day.year.topiko_income += topiko
        day.year.paidiko_income += pediko
        day.year.skala_income += skala
        day.year.fisika_income += day.sinolo_fisikon
        day.year.my_moda_incoome += mymoda
        day.year.ola_income += day.sinolo_olon
        day.year.save()
