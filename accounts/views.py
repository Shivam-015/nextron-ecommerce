from django.shortcuts import render,redirect
from .models import Register,Billing
from django.core.mail import send_mail
from django.conf import settings
import string,random
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from products.models import CartItem
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def register(request):                    # register page
    if request.method=="POST":
        name_var = request.POST.get('name')
        contact_var = request.POST.get('contact')
        email_var = request.POST.get('email')
        
        password_var = request.POST.get('password')
        confirm_password_var = request.POST.get('confirm_password')

        if confirm_password_var != password_var:
            messages.error(request, 'Passwords donot match.')
            return redirect('register')

        hashed_password = make_password(password_var)
        data1 = Register(
            name=name_var,                # store in model which we get from user
           contact = contact_var,
           
            email=email_var,
            password=hashed_password
            
        )

        data1.save()
        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'accounts/register.html') #which page to open 


#login page
def login(request):  
    if request.method =='POST':
        email_var = request.POST.get('email_login')  # we store email which is entered by user in email_var
        password_var = request.POST.get('password_login')

        try:
            form_data = Register.objects.filter(email = email_var).first() # in form model give rows which match the user entered email [email is register email]
            if check_password(password_var , form_data.password):
                request.session['register_id'] = form_data.id   #register_id is variable and it stores the id of current user
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.error(request,"Incorrect Password!")
                return render(request , 'accounts/login.html')
        except Register.DoesNotExist:   # if email entered by user does not exist
            messages.error("User does not exist")
            return render (request,'accounts/login.html')

    return render(request , 'accounts/login.html')   


def logout(request):
    request.session.flush()
    messages.success(request,"Logout Successfull")
    return redirect('login')


def send_otp(request):

    charc = string.ascii_letters + string.digits 
    otp = ''.join(random.choice(charc) for _ in range(6))
    print(otp)
    send_mail(
        subject=' your otp',
        message=f'1300 ',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[''],
        fail_silently=False
    )

    return redirect('login')





# def billing(request):
#     if request.method == 'POST':
#         shipping_first_name = request.POST.get('shipping_first_name')
#         shipping_last_name  = request.POST.get('shipping_last_name')
#         shipping_phone_no   = request.POST.get ('shipping_phone_no')
#         shipping_email      = request.POST.get('shipping_email')
#         shipping_address    = request.POST.get('shipping_address')
#         shipping_country    = request.POST.get('shipping_country')
#         shipping_state      = request.POST.get('shipping_state')
#         shipping_city       = request.POST.get('shipping_city')
#         shipping_zipcode    = request.POST.get('shipping_zipcode')
#         shipping_notes      = request.POST.get('shipping_notes')

#         bill = Billing(
#            shipping_first_name = shipping_first_name,
#            shipping_last_name =shipping_last_name,
#            shipping_phone_no = shipping_phone_no,
#            shipping_email=shipping_email,
#            shipping_address = shipping_address,
#            shipping_country =shipping_country,
#            shipping_state = shipping_state,
#            shipping_city = shipping_city,
#            shipping_zipcode = shipping_zipcode,
#            shipping_notes = shipping_notes
            
#         )
#         bill.save()
#         return redirect ('billing')
#     return render( request , 'cart/billing.html')   


def billing(request):
    register_id = request.session.get('register_id')
    if request.method == 'POST':
        # Form data
        shipping_first_name = request.POST.get('shipping_first_name')
        shipping_last_name = request.POST.get('shipping_last_name')
        shipping_phone_no = request.POST.get('shipping_phone_no')
        shipping_email = request.POST.get('shipping_email')
        shipping_address = request.POST.get('shipping_address')
        shipping_country = request.POST.get('shipping_country')
        shipping_state = request.POST.get('shipping_state')
        shipping_city = request.POST.get('shipping_city')
        shipping_zipcode = request.POST.get('shipping_zipcode')
        shipping_notes = request.POST.get('shipping_notes')

        # Save billing info
        Billing.objects.create(
            shipping_first_name=shipping_first_name,
            shipping_last_name=shipping_last_name,
            shipping_phone_no=shipping_phone_no,
            shipping_email=shipping_email,
            shipping_address=shipping_address,
            shipping_country=shipping_country,
            shipping_state=shipping_state,
            shipping_city=shipping_city,
            shipping_zipcode=shipping_zipcode,
            shipping_notes=shipping_notes,
        )
        cart = CartItem.objects.filter(user_id = register_id)
        if not cart.exists():
            return redirect('cart')

        grand_total = 0
        for item in cart:
            grand_total = grand_total + item.total_price()
        if grand_total < 2000:
            grand_total = grand_total+199 

       # Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': 'Order from ' + shipping_first_name,},
                    'unit_amount': int (grand_total *100), 
                },
                'quantity': 1,
            }],
            mode='payment',
             success_url= 'http://127.0.0.1:8000/accounts/payment_success/' , 
            cancel_url= 'http://127.0.0.1:8000/accounts/payment_cancel' ,
            customer_email= shipping_email ,
        )

        return redirect(session.url, code=303)

    return render(request, 'cart/billing.html')


def payment_success(request):

    return render(request, 'cart/success.html')

def payment_cancel(request):
    return render(request, 'cart/cancel.html')    