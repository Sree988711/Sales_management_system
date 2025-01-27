from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('enquiry/<int:id>',views.enquiry,name='enquiry'),
    path("categories/",views.manage_categories,name="manage_categories"),
    path("categories/delete/<int:id>/",views.delete_category,name="delete_category"),
    path("products/",views.manage_products,name="manage_products"),
    path("products/delete/<int:id>/",views.delete_product,name="delete_product"),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
]
