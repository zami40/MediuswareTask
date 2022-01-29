from itertools import product
from tkinter.messagebox import Message
from django.shortcuts import redirect
from django.views import generic

from product.models import Variant, Product, ProductVariant,ProductVariantPrice,ProductImage
from django.views.generic import ListView
import django_filters

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductList(ListView):
    
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2 

#Showing the products
    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Product.objects.filter(**filter_string)

# to get the summary of product
    def get_product_summary(self, **kwargs):
        product_summary = Product.objects.filter.count()
    
        return product_summary

#Creating Filters
class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    product_variant = ProductVariant.objects.filter(product = product)
    price = ProductVariantPrice.objects.RangeFilter(product=product)
    
    
    class Meta:
        model = Product
        fields = ['title', 'product_variant', 'price']

#Create Product
class ProductCreate(CreateProductView):
    
    def create_product(self, request):

        title = Product.objects.create(
                user=request.user)
        product_variants = ProductVariant.objects.create(
                user=request.user)
        product_product_prices = ProductVariantPrice.objects.create(
                user=request.user)
        product_image = ProductImage.objects.create(
                user=request.user)
        
            
        Message.info(request, f"{product.title} has been created.")
        return redirect("create.html")
   
