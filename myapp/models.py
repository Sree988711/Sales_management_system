from django.db import models
from django.utils.timezone import now
# Create your models here.
class Admin(models.Model):
    email=models.EmailField(null=False,blank=False)
    password=models.CharField(max_length=50,null=False,blank=False)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Admins"

class Category(models.Model):
    category_name=models.CharField(max_length=100,blank=False,null=False)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name_plural="Categories"

class Product(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
    image=models.ImageField(upload_to="product_images/",null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Products"

class Enquiry(models.Model):
    enquiry_date=models.DateField(default=now)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="enquiries")
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="enquiries")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    contact_person_name=models.CharField(max_length=100,null=False,blank=False)
    address=models.TextField(null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    mobile_number=models.CharField(max_length=15,null=False,blank=False)
    def __str__(self):
        return f"Enquiry by {self.contact_person_name} on {self.enquiry_date}"
    class Meta:
        verbose_name_plural="Enquiries"