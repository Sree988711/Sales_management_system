from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Admin,Product,Category,Enquiry
# Create your views here.
def index(request):
    categories_id=request.GET.get('category')
    if categories_id:
        products=Product.objects.filter(category_id=categories_id)
    else:
        products=Product.objects.all()

    categories=Category.objects.all()
    return render(request,'index.html',{
        'products':products,
        'categories':categories,
    })

def login(request):
    if request.method=='POST':
        email=request.POST.get('admin_email')
        password=request.POST.get('admin_password')
        try:
            adminobj=Admin.objects.get(email=email,password=password)
            print(adminobj)
        except Admin.DoesNotExist:
            return HttpResponse('Wrong Credentials')
        
        return redirect('dashboard')
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        email=request.POST.get('register_email')
        password=request.POST.get('register_password')
        adminobj=Admin.objects.all()
        for items in adminobj:
            if items.email==email and items.password==password:
                return HttpResponse('Duplicate Credentials')
            else:
                newobj=Admin.objects.create(email=email,password=password)
                newobj.save()
                return HttpResponse('Credentials added Successfully')

    return render(request,'register.html')

def dashboard(request):
    details=Product.objects.all()
    enquries=Enquiry.objects.all()
    return render(request,'dashboard.html',{
        'details':details,
        'enquries':enquries
    })

def enquiry(request,id):
    try:
        details=Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse('Product not found')
    
    if request.method=='POST':
        contact_person_name=request.POST.get('name')
        address=request.POST.get('address')
        quantity=request.POST.get('quantity')
        amount=request.POST.get('amount')
        mobile_number=request.POST.get('phone')

        try:
            enquiry=Enquiry(
                contact_person_name=contact_person_name,
                address=address,
                quantity=quantity,
                amount=amount,
                mobile_number=mobile_number,
                product=details,
                product_category=details.category,
            )
            enquiry.save()
            return HttpResponse('Data saved Successfully')
        except Exception:
            return HttpResponse('Error saving to database')
    
    return render(request,'enquiry.html',{
        'details':details
    })