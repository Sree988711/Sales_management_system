from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Admin,Product,Category,Enquiry
from django.contrib import messages
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

def manage_categories(request):
    categories=Category.objects.all()
    if request.method=="POST":
        category_name=request.POST.get("category_name")
        Category.objects.create(category_name=category_name)
        return redirect("manage_categories")
    return render(request,"manage_categories.html",{"categories":categories})

def delete_category(request,id):
    category=get_object_or_404(Category,id=id)
    category.delete()
    return redirect("manage_categories")


def manage_products(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        category_id=request.POST.get("category_id")
        category=get_object_or_404(Category, id=category_id)
        image=request.FILES.get("image")
        Product.objects.create(name=name,price=price,category=category,image=image)
        return redirect("manage_products")
    return render(request,"manage_products.html",{
        "products": products, 
        "categories": categories
    })

def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return redirect("manage_products")

def edit_category(request, id):
    category=get_object_or_404(Category, id=id)

    if request.method=="POST":
        category_name=request.POST.get('category_name')
        
        if category_name:
            category.category_name=category_name
            category.save()
            messages.success(request,"Category updated successfully.")
            return redirect("manage_categories")
        else:
            messages.error(request,"Category name cannot be empty.")

    return render(request,"edit_category.html",{
        "category": category
    })

def edit_product(request,id):
    product=get_object_or_404(Product,id=id)
    categories=Category.objects.all()

    if request.method=="POST":
        name=request.POST.get('name')
        price=request.POST.get('price')
        category_id=request.POST.get('category')
        image=request.FILES.get('image')

        if name and price and category_id:
            product.name=name
            product.price=price
            product.category_id=category_id
            
            if image:
                product.image=image

            product.save()
            messages.success(request,"Product updated successfully.")
            return redirect("manage_products")
        else:
            messages.error(request,"Something wrong")

    return render(request,"edit_product.html",{
        "product": product,
        "categories":categories
    })

def manage_enquiry(request):
    from_date=request.GET.get('from_date')
    to_date=request.GET.get('to_date')

    enquiry=Enquiry.objects.all()

    if from_date and to_date:
        enquiry=enquiry.filter(enquiry_date__range=[from_date,to_date])
    elif from_date:
        enquiry=enquiry.filter(enquiry_date__gte=from_date)
    elif to_date:
        enquiry=enquiry.filter(enquiry_date__lte=to_date)

    return render(request,'manage_enquiry.html',{
        'enquiry':enquiry,
        'from_date':from_date,
        'to_date':to_date
    })

def update_enquiry(request,id):
    if request.method=='POST':
        enquiry=get_object_or_404(Enquiry,id=id)
        status=request.POST.get('status')=='True'
        remark=request.POST.get('remark')

        enquiry.status=status
        enquiry.remark=remark
        enquiry.save()

        messages.success(request, f"Enquiry for {enquiry.contact_person_name} updated successfully.")
        return redirect('manage_enquiry')