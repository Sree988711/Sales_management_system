from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Admin,Product,Category,Enquiry
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
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
            return redirect('dashboard')
        except Admin.DoesNotExist:
            messages.error(request,"Incorrect email/password")
        
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('register_email')
        password = request.POST.get('register_password')

        if Admin.objects.filter(email=email).exists():
            messages.error(request, "Duplicate Entry: This email is already registered.")
            return redirect('register')

        new_admin = Admin.objects.create(email=email, password=password)
        new_admin.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

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
            messages.success(request,'Enquiry sent')
            return redirect('enquiry')
        except Exception:
            pass
    
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
    
def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    response=HttpResponse(content_type='application/pdf')
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with the report generation',content_type='text/plain')
    return response

def generate_enquiry_report(request):
    enquiries=Enquiry.objects.all()
    context={'enquiries':enquiries}
    return render_to_pdf('enquiry_report.html',context)

def generate_individual_report(request,id):
    enquiry=Enquiry.objects.get(id=id)
    context={'enquiry':enquiry}
    return render_to_pdf('individual_report.html',context)

def change_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        if not email or not new_password:
            messages.error(request,"Email and password are required!")
            return render(request,'change_password.html')

        try:
            admin=Admin.objects.get(email=email)
            admin.password=new_password
            admin.save()
            messages.success(request,"Password updated successfully!")
        except Admin.DoesNotExist:
            messages.error(request,"Email does not exist in the database!")

    return render(request,'change_password.html')