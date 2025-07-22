from django.db import models
class Register(models.Model):
    name  = models.CharField(max_length=50,null=False)
    email = models.EmailField(null=False)
    contact = models.IntegerField(null=False)
    password = models.CharField(max_length=40,null=False)

    def __str__(self):
        return self.name


class Billing(models.Model):
    shipping_first_name = models.CharField(max_length=200)
    shipping_last_name   = models.CharField(max_length=200)
    shipping_phone_no = models.CharField(max_length=15)
    shipping_email  = models.EmailField(null=False)
    shipping_zipcode = models.CharField(max_length=10)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_address = models.TextField()
    shipping_country = models.CharField(max_length=100)
    shipping_notes = models.TextField(null=True, blank=True)   

    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)    