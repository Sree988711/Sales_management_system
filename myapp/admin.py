from django.contrib import admin
from . models import Admin,Category,Product,Enquiry
# Register your models here.
admin.site.register(Admin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','category_name')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','price','category')
    list_filter=('category',)
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display=('id','enquiry_date','product','product_category','amount','contact_person_name','mobile_number','status','remark')
    list_filter=('enquiry_date','product_category')