from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Product, Slider, Category, Cart
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Create your views here.
def index(request):
    # Fetch the featured products and the sliders
    products = Product.objects.select_related('author').filter(featured=True)
    slider = Slider.objects.order_by('order')

    # Pass the variables correctly to the template
    return render(request, 'pages/index.html', {
        'products': products,  # Pass products with correct key
        'slider': slider  # Pass slider with correct key
    })


def product(request, pid):
    pro = Product.objects.get(pk=pid)
    return render(request, 'pages/product.html',{'product': pro})


def category(request, cid=None):
    cat = None
    query = request.GET.get('query')
    cid = request.GET.get('category',cid)

    where = {}
    if cid:
        cat = Category.objects.get(pk=cid)
        where['category_id'] = cid
    if query:
        where['name__icontains'] = query

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/category.html',
                  {'page_obj': page_obj, 'category': cat})


def cart(request):
    return render(request, 'pages/cart.html')




def cart_update(request, pid):
    # Ensure there's a session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Retrieve the Session instance from the session key
    session = get_object_or_404(Session, session_key=session_key)

    # Find the cart associated with the session
    cart_model = Cart.objects.filter(session=session).last()

    # If no cart exists, create a new one
    if cart_model is None:
        cart_model = Cart.objects.create(session=session, items={})

    # Check if the product is already in the cart
    if str(pid) in cart_model.items:
        # If it exists, increase the quantity
        cart_model.items[str(pid)] += 1
    else:
        # If it doesn't exist, add it with a quantity of 1
        cart_model.items[str(pid)] = 1

    # Save the cart after modification
    cart_model.save()

    return JsonResponse({
        'message': _('The product has been added to your cart'),
        'items_count': sum(cart_model.items.values())  # Total quantity of items in the cart
    })

def cart_remove(request, pid):
    session_key = request.session.session_key

    # If no session exists, return an empty response
    if not session_key:
        return JsonResponse({})

    # Retrieve the Session instance from the session key
    session = get_object_or_404(Session, session_key=session_key)

    # Find the cart associated with the session
    cart_model = Cart.objects.filter(session=session).last()

    if cart_model is None:
        return JsonResponse({})

    # Remove the product if it's in the cart
    if str(pid) in cart_model.items:
        del cart_model.items[str(pid)]  # Remove the product from the cart
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been removed from your cart'),
        'items_count': len(cart_model.items)
    })


def checkout(request):
    return render(request, 'pages/checkout.html')


def checkout_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()

    return render(request, 'pages/checkout_complete.html')
