from statistics import mode
from django.db import models

# Create your models here.

class NewsLetterEmail(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')
    member_rating = models.IntegerField(default=3)

    class Meta:
        verbose_name_plural = 'Emails'

    def __str__(self):
        return self.email


class NewsLetterUser(models.Model):
    title = models.ForeignKey(NewsLetterEmail, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Contact(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Όνομα')
    last_name = models.CharField(max_length=100, verbose_name='Επίθετο')
    email = models.EmailField()
    subject = models.CharField(max_length=50, verbose_name='Θέμα')
    message = models.TextField(verbose_name='Μήνυμα')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Αποστολής')
    is_readed = models.BooleanField(default=False, verbose_name='Διαβασμένο')

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'Μηνύματα Επικοινωνίας'

    def __str__(self):
        return self.subject
