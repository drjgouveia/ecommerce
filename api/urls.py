from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
import api.views
from ecommerce import views

urlpatterns = [
    path('prods/', api.views.prods, name='prods_api'),
    path('prod/<int:prod_id>', api.views.prod, name='prod_api'),
    path('sells/', api.views.sells, name='sells_api'),
    path('sell/<int:sell_id>', api.views.sell, name='sell_api'),
    path('sells-details/', api.views.sells_details, name='sells_details_api'),
    path('sells-detail/<int:sell_details_id>', api.views.sells_detail, name='sells_detail_api'),
]

