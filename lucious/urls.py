"""lucious URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.login, name='login'),
    path('additems/', views.form_tbrg, name='additems'),
    path('adddistributor/', views.form_dist, name='adddistributor'),
    path('addcategory/', views.form_cats, name='addcategory'),
    path('addkaryawan/', views.form_tkry, name='addkaryawan'),
    path('checkout', views.checkout, name='checkout'),
    path('search/', views.search_items, name='search_items'),
    path('stats/', views.stats, name='stats'),
    path('history/', views.history, name='history'),
    path('karyawan/', views.karyawan, name='karyawan'),
    path('process_transaction', views.process_transaction_view, name='process_transaction'),
    path('detailtransaksi/<uuid:transaksi_id>/', views.details, name='detail_transaksi'),
    path('distribtrans/', views.distrib_trans, name='distributor_transaksi'),
    path('test-post/', views.test_post, name='test_post'),
    path('data-barang-by-distrib/<uuid:id>/', views.data_barang_by_distrib, name='data_barang_by_distrib'),
    path('edit-item/<uuid:id_barang>/', views.edit_barang, name='edit_barang'),
    path('api/edit-item/', views.edit_barang_api, name='edit_barang'),
    path('api/hapus-transaksi/', views.hapus_trans_api, name='hapus_transaksi'),
    path('api/hapus-item/', views.hapus_barang_api, name='edit_barang'),
    path('api/hapus-distributor/', views.hapus_distributor_api, name='hapus_distributor'),
    path('api/hapus-cat/', views.hapus_cat_api, name='hapus_cat'),
    path('edit-distributor/<uuid:id_distributor>/', views.edit_distrib, name='edit_distributor'),
    path('edit-category/<uuid:id_category>/', views.edit_category, name='edit_category'),
    path('api/edit-distributor/', views.edit_distributor_api, name='edit_distributor'),
    path('api/edit-category/', views.edit_cat_api, name='adit_cat_api'),
    path('api/add-karyawan/', views.add_karyawan_api, name='add_kry_api'),
    path('api/hapus-karyawan/', views.hapus_karyawan_api, name='del_kry_api'),
]

