
from django.shortcuts import render, redirect
import fun.connection as conns
import fun.auth as auth
import fun.fetcher as fetchr
import fun.creator as creator
import fun.filters as filts
import fun.cryptr as crypts
import fun.transaction as transc
import ast
import json
from decimal import Decimal
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


con = conns.connect()

def home(request):
    data = fetchr.fetch_display()
    data_cat = fetchr.fetch_category()
    headers = ['Nama Barang','Harga Barang','Stok','Kategori','Distributor','Aksi']
    context = {
        'rows': data,
        'headers':headers,
        'show_buttons': True,
        'show_buttons2': False,
        'show_shopping_cart': True,
        'show_promo': True,
        'show_contact': True,
        'show_inventory': False,
        'show_organization': False,
        'show_transaction_history': False,
        'show_logout': False,
        'show_login': True,
        'data_cat':data_cat,
        'show_distrans':False,
    }
    return render(request, 'dashboard.html', context)

def search_items(request):
    headers = ['Nama Barang','Harga Barang','Stok','Kategori','Distributor','Aksi']
    name_filt = request.GET.get('search')
    cat_filt = request.GET.get('cat')
    data = filts.search_bar(name_filt,cat_filt)
    data_cat = fetchr.fetch_category()
    context = {
        'rows': data,
        'headers':headers,
        'show_buttons': True,
        'show_buttons2': False,
        'show_shopping_cart': True,
        'show_promo': True,
        'show_contact': True,
        'show_inventory': False,
        'show_organization': False,
        'show_transaction_history': False,
        'show_logout': False,
        'show_login': True,
        'data_cat':data_cat,
        'show_distrans':False,
    }
    return render(request, 'dashboard.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        log = auth.authen(username, password)
        if log != False:
            response = redirect('inventory')
            response.set_cookie('id_karyawan', log)
            return response
        else:
            return render(request, 'login.html', {'error': 'Username atau password salah'})
    return render(request, 'login.html')

def inventory(request):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    data = fetchr.fetch_barang()
    data_d = fetchr.fetch_distributor()
    cats = fetchr.fetch_category()
    headers1 = ['ID Barang','Nama Barang','Harga Barang','Stok','Kategori','Distributor','Aksi']
    context = {
        'cats': cats,
        'rows': data,
        'headers':headers1,
        'show_buttons': True,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'data_d':data_d,
        'show_distrans':auth.showTrans(auth.degreeAuth(id_karyawan)),
        'show_Nama':nama_karyawan,
    }
    return render(request, 'inventory.html', context)

def form_tbrg(request):
    if request.method == 'POST':
        nama_barang = request.POST.get('nama')
        harga_barang = request.POST.get('harga')
        id_kategori = request.POST.get('kategori')
        id_distributor = request.POST.get('distributor')
        cats = creator.getIdCat(con,id_kategori)
        dists = creator.getIdDis(con,id_distributor)
        creator.tambah_barang(con,nama_barang,harga_barang,0,cats,dists)
        return redirect('inventory')
    data_d = fetchr.fetch_distributor()
    data_c = fetchr.fetch_category()
    return render(request, 'add-item.html', {'data_distrib':data_d, 'data_cats':data_c})

def form_tkry(request):
    return render(request, 'add-karyawan.html')


def form_dist(request):
    if request.method == 'POST':
        dist = request.POST.get('nama')
        alamat = request.POST.get('alamat')
        contact = request.POST.get('contact')
        creator.tambah_distributor(con,dist,contact,alamat)
        return redirect('inventory')
    return render(request, 'add-distributor.html')

def form_cats(request):
    if request.method == 'POST':
        cats = request.POST.get('nama')
        creator.tambah_kategory(con,cats)
        return redirect('inventory')
    return render(request, 'add-kategori.html')

def checkout(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data', '[]')
        print("print",cart_data)

        
        try:
            cart_items = json.loads(cart_data)
        except json.JSONDecodeError:
            cart_items = []
        total_biaya = 0
        data_all = []
        for item in cart_items:
            barang_id = item['id']
            jumlah = int(item['jumlah'])

            data_barang = fetchr.fetch_barang_by_name(barang_id)
            # print("===",data_barang) 
            for cell in data_barang:
                harga_total = cell[1] * jumlah
                temp = cell + (jumlah, harga_total,)
                data_all.append(temp)
                total_biaya = total_biaya + harga_total
            data_barang = data_all
        
        # for item in cart_items:
        print(data_barang,"awdawd")

        headers = ['Nama Barang','Harga Barang','Jumlah','Harga Total']
        context = {
            'rows': data_barang,
            'headers': headers,
            'show_shopping_cart': True,
            'show_promo': True,
            'show_contact': True,
            'show_inventory': False,
            'show_organization': False,
            'show_transaction_history': False,
            'show_logout': False,
            'show_login': True,
            'harga_total' : total_biaya,
            'show_distrans':False,
            }
        return render(request, 'checkout.html', context)

    return render(request, 'checkout.html')

def stats(request):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    jumlah_karyawan = fetchr.count_rows(con,"karyawan3")
    totas = fetchr.count_rows(con,"header_trans2")
    total_distributor = fetchr.count_rows(con,"distributor2") - 1
    total_barang = fetchr.count_rows(con,"barang2")
    data_transaksi = fetchr.fetch_header_transaksi()
    datab = fetchr.fetch_display()
    total_stock = 0
    total_asset = 0
    penjualan = 0
    listOfTanggal = []
    listOfKeuntungan = []
    for data in datab:
        total_stock = total_stock + int(data[2])
        asset_barang = int(data[2]) * int(data[1])
        total_asset = asset_barang
    for total_trans in data_transaksi:
        listOfTanggal.append(total_trans[1])
        if str(total_trans[4]) == '12e4d28c-d0d1-46ca-8997-b53de5605dfd':
            keuntungan = int(total_trans[2])
            listOfKeuntungan.append(keuntungan)
        else:
            keuntungan = int(total_trans[2]) * -1
            listOfKeuntungan.append(keuntungan)
        penjualan = penjualan + keuntungan
    context = {
        'jumlah_karyawan':jumlah_karyawan,
        'penjualan':penjualan,
        'total_barang':total_barang,
        'total_distributor':total_distributor,
        'total_stock': total_stock,
        'total_asset':total_asset,
        'listOfTanggal':listOfTanggal,
        'listOfKeuntungan':listOfKeuntungan,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans': auth.showTrans(auth.degreeAuth(id_karyawan)),
        'totas':totas,
        'show_Nama':nama_karyawan,
    }
    return render(request, 'stats.html', context)

def history(request):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    data_trans = fetchr.fetch_header_transaksi()
    headers = ['ID Transaksi','Tanggal','Harga Transaksi','Karyawan','Status','Distributor', 'Details']
    redefinition = []
    for data in data_trans:
        karyawan = creator.getKryId(con,data[3])
        distributor = data[6]
        jenis = "Pelanggan"
        temp = data + (karyawan, distributor, jenis,)
        redefinition.append(temp)
    context = {
        'rows': redefinition,
        'headers': headers,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans': auth.showTrans(auth.degreeAuth(id_karyawan)),
        'show_Nama':nama_karyawan,
    }
    return render(request, 'riwayat.html', context)

def karyawan(request):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    data_karyawan = fetchr.fetch_karyawan()
    headers = ['No','ID Karyawan','Nama Karyawan','Jabatan','Level','Aksi']

    context = {
        'rows': data_karyawan,
        'headers': headers,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_login': False,
        'show_distrans': auth.showTrans(auth.degreeAuth(id_karyawan)),
        'show_Nama':nama_karyawan,
    }
    return render(request, 'karyawan.html', context)

def process_transaction_view(request):
    if request.method == 'POST':
        cart_data = request.POST.get('rows')
        print("1",cart_data)
        cart_data_list = eval(cart_data) 
        harga_total = request.POST.get('harga_total')
        id_karyawan = 'a249101e-8db2-48fa-a02b-3351b3574ea4'
        listoftuplebarang = []
        for item in cart_data_list:
            print("4",item[1])
            nm_brg = item[0]
            harga_brg = item[1]
            barang_id = creator.getIdBrg(con,item[0])
            jumlah = item[2]
            total_harga = item[3]
            listoftuplebarang.append((barang_id, nm_brg, harga_brg, jumlah, total_harga))
        print("yrdy")
        transc.buat_transaksi( listoftuplebarang, id_karyawan, harga_total, '12e4d28c-d0d1-46ca-8997-b53de5605dfd')

        return redirect('home')

    return redirect('checkout')

def details(request, transaksi_id):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    headers = ['No','Nama Barang','Jumlah','Harga Satuan (Default)','Harga Total']
    data = fetchr.fetch_detail_transaksi(transaksi_id)
    data_header = fetchr.fetch_detail_transaksi_header(transaksi_id)
    distrib_data = creator.cek_id_transaksi(transaksi_id)
    hargaP = []
    for dat in data:
        hrgP = dat[5]*dat[2]
        hargaP.append(hrgP)
    if data_header[4] == False:
        transc.acc_transaction(transaksi_id, id_karyawan)
    context = {
        'headers': headers,
        'rows': data,
        'hrgp': hargaP,
        'trans_header': data_header,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans': auth.showTrans(auth.degreeAuth(id_karyawan)),
        'transaksi': transaksi_id,
        'distrib': distrib_data,
        'show_Nama':nama_karyawan,
    }
    return render(request, 'detail_transaksi.html',context)

def edit_barang(request, id_barang):
    data = fetchr.fetch_barang_by_id(id_barang)
    data_distrib = fetchr.fetch_distributor()
    data_cat = fetchr.fetch_category()
    context = {
        'data_barang': data,
        'distrib':data_distrib,
        'cats':data_cat,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans':True,
        'id_barang': id_barang,
        'transaksi': id_barang,
    }
    return render(request, 'edit-item.html',context)


def distrib_trans(request):
    id_karyawan = request.COOKIES.get('id_karyawan')
    if id_karyawan == None:
        return redirect('login')
    nama_karyawan = fetchr.fetch_nama_karyawan(id_karyawan)
    if request.method == 'POST':
        distrib = request.POST.get('distrib')
        barang = request.POST.getlist('pil_bar')
        stock = request.POST.getlist('stock')
        hargaC = request.POST.getlist('harga')
        id_list = []
        null_list = []
        list_harga = []
        total = 0
        for brg, stk, hrg in zip(barang, stock, hargaC):
            id_brg = creator.getIdBrg(con, brg)
            if hrg == "" or hrg is None:
                harga = creator.getIdBrgHrg(con, id_brg)
            else:
                harga = hrg
            harga_total = int(harga) * int(stk)
            list_harga.append(harga)
            id_list.append(id_brg)
            null_list.append("")
            total = total + harga_total
        IoTB = list(zip(id_list, null_list, barang, stock, list_harga))
        transc.buat_transaksi(IoTB, id_karyawan, total, distrib )
    data_distrib = fetchr.fetch_distributor()
    data_barang = fetchr.fetch_barang()
    context = {
        'distributor': data_distrib,
        'data_barang': data_barang,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': auth.showKaryawan(auth.degreeAuth(id_karyawan)),
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans': auth.showTrans(auth.degreeAuth(id_karyawan)),
        'show_Nama':nama_karyawan,
    }
    return render(request, 'distrib_trans.html', context)

def test_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Memproses data JSON dari body request
            print(data)
            return JsonResponse({"status": "success", "data": data})  # Mengembalikan respon JSON
        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)

def data_barang_by_distrib(request, id):
    if request.method == 'GET':
        data_barang = fetchr.fetch_barang_distrib(id)
        try:# Memproses data JSON dari body request
            # print(data)
            return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "failed", "message": "Invalid request method"}, status=405)

from rest_framework.decorators import api_view

@api_view(["POST"])
def edit_barang_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # print(body.get("nama"))
        fetchr.fetch_edit_barang(body.get("id"),body.get("nama"), body.get("harga"), body.get("kategori"),body.get("distributor"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)

        return JsonResponse(body, safe=False)
    
@api_view(["DELETE"])
def hapus_barang_api(request):
    if request.method == 'DELETE':
        body = json.loads(request.body)
        # print("1", body.get("id") )
        # print(body.get("nama"))
        fetchr.fetch_hapus_barang(body.get("id"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        if body.get("id") :
            return JsonResponse(f"Success", safe=False)
        else:
            return JsonResponse(f"Failed", safe=False)

@api_view(["DELETE"])
def hapus_distributor_api(request):
    if request.method == 'DELETE':
        body = json.loads(request.body)
        print("13333" )
        # print(body.get("nama"))
        fetchr.fetch_hapus_distributor(body.get("id"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        if body.get("id") :
            return JsonResponse(f"Success", safe=False)
        else:
            return JsonResponse(f"Failed", safe=False)

@api_view(["DELETE"])
def hapus_cat_api(request):
    if request.method == 'DELETE':
        body = json.loads(request.body)
        print("13333" )
        # print(body.get("nama"))
        fetchr.fetch_hapus_kategori(body.get("id"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        if body.get("id") :
            return JsonResponse(f"Success", safe=False)
        else:
            return JsonResponse(f"Failed", safe=False)
        
@api_view(["DELETE"])
def hapus_trans_api(request):
    if request.method == 'DELETE':
        body = json.loads(request.body)
        print("13333" )
        # print(body.get("nama"))
        fetchr.fetch_hapus_theader(body.get("id"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        if body.get("id") :
            return JsonResponse(f"Success", safe=False)
        else:
            return JsonResponse(f"Failed", safe=False)

def edit_distrib(request, id_distributor):
    data = fetchr.fetch_distrib_barang(id_distributor)
    context = {
        'data_distributor': data,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans':True,
        'id_distributor': id_distributor,
    }
    return render(request, 'edit-distributor.html',context)

@api_view(["POST"])
def edit_distributor_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # print(body.get("nama"))
        #id, distributor, contact, alamat
        print(body)
        fetchr.edit_distributor(body.get("id"),body.get("nama"), body.get("contact"), body.get("alamat"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)

        return JsonResponse(body, safe=False)

def edit_category(request, id_category):
    data = fetchr.fetch_category_one(id_category)
    context = {
        'data_category': data,
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_logout': True,
        'show_login': False,
        'show_distrans':True,
        'id_category': id_category,
    }
    return render(request, 'edit-category.html',context)

@api_view(["POST"])
def edit_cat_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # print(body.get("nama"))
        #id, distributor, contact, alamat
        print(body)
        fetchr.edit_category(body.get("id"),body.get("cat"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)

        return JsonResponse(body, safe=False)
    
@api_view(["POST"])
def add_karyawan_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # print(body.get("nama"))
        #id, distributor, contact, alamat
        print(body)
        creator.tambah_karyawan(con, body.get("nama"), body.get("pass"), body.get("level"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)

        return JsonResponse(body, safe=False)
    
@api_view(["DELETE"])
def hapus_karyawan_api(request):
    if request.method == 'DELETE':
        body = json.loads(request.body)
        # print(body.get("nama"))
        #id, distributor, contact, alamat
        
        # uuid_string = body.decode('utf-8')
        creator.hapus_karyawan(con,body.get("id"))
        # cursor = con.cursor()
        # cursor.execute("")
        # data_barang = fetchr.fetch_barang_distrib(id)
        # try:# Memproses data JSON dari body request
        #     # print(data)
        #     return JsonResponse({"status": "success", "data": data_barang})  # Mengembalikan respon JSON
        # except json.JSONDecodeError:
        #     return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)

        return JsonResponse(body, safe=False)