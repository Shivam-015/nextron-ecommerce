from .models import Wishlist

def wishlist_processor(request):
    wishlist_ids = []
    user_id = request.session.get('register_id')
    if user_id:
        wishlist_ids = list(Wishlist.objects.filter(user_id=user_id).values_list('product_id', flat=True))
    return {'wishlist_ids': wishlist_ids}
