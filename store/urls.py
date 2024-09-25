from django.urls import path
from .views import index, product, category, cart, checkout, checkout_complete, cart_update, cart_remove
from django.conf.urls.static import static
from CoverToCover import settings

urlpatterns = [
    path('', index, name='store.home'),
    path('product/<int:pid>', product, name='store.product'),
    path('category/<int:cid>', category, name='store.category'),
    path('category/', category, name='store.categories'),
    path('cart/add/<int:pid>', cart_update, name='store.cart_add'),
    path('cart/remove/<int:pid>', cart_remove, name='store.cart_remove'),
    path('cart/', cart, name='store.cart'),
    path('checkout/', checkout, name='store.checkout'),
    path('checkout/complete/', checkout_complete, name='store.checkout_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)