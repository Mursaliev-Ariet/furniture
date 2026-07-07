from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm, ContactForm
from .models import CartItem

def contacts_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')  # Перенаправление после успешной отправки
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form})

def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # Очистка корзины после оформления
            cart_items.delete()
            return redirect('order_success')  # Страница "Спасибо за заказ"
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items})
class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        context['total_order_price'] = sum(item.total_price for item in cart_items)
        return context

class FavoritesListView(LoginRequiredMixin, ListView):
    model = LikedFurniture
    template_name = 'favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return LikedFurniture.objects.filter(user=self.request.user)
def furniture_list(request):
    furniture = Furniture.objects.all()

    return render(request, "furniture.html", {
        "furniture": furniture,
    })

def sale(request):
    furniture = Furniture.objects.all()

    return render(request, "sale.html", {
        "furniture": furniture
    })

def add_to_favorite(request, pk):
    furniture = get_object_or_404(Furniture, id=pk)

    LikedFurniture.objects.get_or_create(user=request.user, furniture=furniture)

    return redirect(request.META.get("HTTP_REFERER"))

def add_to_cart(request, pk):
    furniture = get_object_or_404(Furniture, id=pk)

    cart, created = CartItem.objects.get_or_create(user=request.user,furniture=furniture)

    if not created:
        cart.quantity += 1
        cart.save()

    return redirect(request.META.get("HTTP_REFERER"))
# Create your views here.