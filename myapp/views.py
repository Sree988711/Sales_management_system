from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Admin,Product,Category,Enquiry
# Create your views here.
def index(request):
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

    return render(request,'dashboard.html',{
        'details':details
    })
