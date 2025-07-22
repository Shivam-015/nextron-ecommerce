# products/views.py
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Contact,CartItem,ProductDetails 
from django.core.paginator import Paginator
from django.db.models import Q
from category.models import Category


def home(request):
    products = Product.objects.filter(is_available=True).prefetch_related('details_image')
    categories = Category.objects.all()

    return render(request, 'ecommerce/home.html', {'products': products, 'categories': categories})

  

def all_products(request):

    query = request.GET.get('q' , '' ) 
    products = Product.objects.all() 
    if query:
        products = Product.objects.filter( Q(product_name__icontains = query) | Q(category__category_name__icontains = query) )
    category_id = request.GET.get('category')
    if category_id:
        products= products.filter(category_id=category_id)

        
    
    categories = Category.objects.all()

    category = request.GET.getlist('category')  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('is_available')

    if category:
        products = products.filter(category__id__in = category)

    if min_price:
        try:
            products = products.filter(original_price__gte = int(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(original_price__lte = int(max_price))
        except ValueError:
            pass

    if availability:
        if 'in' in availability and 'out' not in availability:
            products = products.filter(is_available = True)
        elif 'out' in availability and 'in' not in availability:
            products = products.filter(is_available = False)

    products = products.prefetch_related('details_image')
    paginator = Paginator(products , 2)    # 10 products per page
    page_number = request.GET.get('page')   # current page number
    page_object = paginator.get_page(page_number)   # display 10 products on curret page

    context = {
        'page_object': page_object , 
        'categories' : categories ,
        'selected_categories' : category , 
        'selected_min_price' : min_price or 0 ,
        'selected_max_price' : max_price or 10000000 ,
        'selected_availability' : availability,
        }

    return render(request, 'products/all_products.html', context)

def contact(request):
    if request.method == 'POST':
        name_var=request.POST.get('name')
        contact_var = request.POST.get('contact')
        email_var= request.POST.get('email')
        description_var = request.POST.get('description')


        cont = Contact(
            name = name_var,
            email = email_var,
            contact = contact_var,
            description = description_var
        )
        cont.save()
        return redirect ('home')
    return render(request, 'ecommerce/contact.html')  




def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_details.html', {'product': product})


def cart(request):                        

    cart_id = request.session.get('register_id')   #current user login session

    if not cart_id:
        return redirect('login') 
    
    items = CartItem.objects.filter(user_id = cart_id)

    total = 0   # total amnt user has to pay
    discount = 0    # total discount
    total_quantity = 0  

    for item in items:
        item_total = item.total_price()     # price of each product
        item_discount = item.discount_price()

        total += item_total
        discount += item_discount
        total_quantity += item.quantity

    if total>=2000:
        shipping = 0
    else:
        shipping = 199

    grand = total + shipping
    return render(request , 'cart/cart.html' , {
        'items' : items , 
        'total' : total , 
        'discount' : discount ,
        'grand' : grand,
        'total_quantity' : total_quantity,
        'shipping' : shipping
        })

def add_to_cart(request , product_id):
    register_id = request.session.get('register_id')
    product = get_object_or_404(Product, id= product_id)

    # Use register_id, not request.user
    cart, created = CartItem.objects.get_or_create(user_id=register_id, product=product)
    if not created:
        cart.quantity += 1
        cart.save() 

    return redirect('cart')
def delete_from_cart(request , item_id):
    
    proj = get_object_or_404(CartItem, id = item_id,) 
    proj.delete()
    return redirect('cart')  

#quantity increase
def increase(request , item_id):
    product = get_object_or_404(CartItem , id = item_id)
    product.quantity += 1
    product.save()
    return redirect('cart')
#quantity decrease
def decrease(request , item_id):
    item = get_object_or_404(CartItem , id=item_id)
    if item.quantity <= 1 :
        item.delete()
    else:
        item.quantity -= 1
        item.save()
    return redirect('cart')    

#profile
def profile(request):
    return render(request,'accounts/profile.html')




 