from django.db import models

# Create your models here.
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,null=False)
    age = models.IntegerField()
    adetail = models.OneToOneField(to="AuthorDetail",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday = models.DateField()
    tel = models.BigIntegerField()
    addr = models.CharField(max_length=64)

    def __str__(self):
        return str(self.tel)

class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    pdate = models.DateField()
    price = models.DecimalField(max_digits=5,decimal_places=2)

    authors = models.ManyToManyField(to="Author")

    publish = models.ForeignKey(to="Publish",to_field="nid",on_delete=models.CASCADE)

    def __str__(self):
        return self.title
