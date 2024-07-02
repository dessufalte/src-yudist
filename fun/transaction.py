from . import creator,cryptr,connection,fetcher
import json
import datetime



def buat_transaksi(listoftuplebarang, id_karyawan, harga_total, id_distributor):
    con = connection.connect()
    cursor = con.cursor()
    id_transaksi = cryptr.generate_id()
    now = datetime.datetime.now()
    if id_distributor == None:
        id_distributor = '12e4d28c-d0d1-46ca-8997-b53de5605dfd'
    # Kurangi stok barang dan hitung total harga
    # for item in listoftuplebarang:
    #     barang_id = item[0]
    #     jumlah = item[3]
    #     creator.kurangi_stok(con, barang_id, jumlah)

    # Tambahkan header transaksi
    query_header = """
    INSERT INTO header_trans2 (id_transaksi, tanggal, total_transaksi, id_karyawan, status, id_distributor) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_header, (id_transaksi, now, harga_total, id_karyawan, False, id_distributor))
   

    query_detail = """
    INSERT INTO detail_transaksi2 (id_transaksi, id_barang, jumlah, total_harga) 
    VALUES (%s, %s, %s, %s)
    """

    for item in listoftuplebarang:
        barang_id = item[0]
        jumlah = item[3]
        total_harga = item[4]
        cursor.execute(query_detail, (id_transaksi, barang_id, jumlah, total_harga))

    con.commit()
    cursor.close()
    
    return True, "Transaksi berhasil ditambahkan"

def acc_transaction(transaksi_id, id_karyawan):
    con = connection.connect()
    data_barang = fetcher.fetch_detail_transaksi(transaksi_id)
    for data in data_barang:
        id_distrib = creator.getDisId(con, transaksi_id)
        print(id_distrib)
        if(str(id_distrib) =="12e4d28c-d0d1-46ca-8997-b53de5605dfd"):
            print("BERHASIL")
            creator.kurangi_stok(con, data[1],data[2])
        else:
            print("BERTAMBAH")
            creator.kurangi_stok(con, data[1],data[2]*-1)
    creator.acc_flag_yes(con, transaksi_id, id_karyawan)
 


# def buat_transaksi_distrib(listoftuplebarang, id_karyawan, harga_total, id_distributor):
#     con = connection.connect()
#     cursor = con.cursor()
#     id_transaksi = cryptr.generate_id()
#     now = datetime.datetime.now()
    
#     query_header = """
#     INSERT INTO distrib_trans_header (id_transaksi, tanggal, id_karyawan, total_harga, status, id_distributor) 
#     VALUES (%s, %s, %s, %s, %s, %s)
#     """
#     cursor.execute(query_header, (id_transaksi, now, id_karyawan, harga_total, False, id_distributor))
    
#     # Tambahkan detail transaksi
#     query_detail = """
#     INSERT INTO detail_transaksi_distrib (id_transaksi, id_barang, jumlah, harga_total) 
#     VALUES (%s, %s, %s, %s)
#     """
#     for item in listoftuplebarang:
#         barang_id = creator.getIdBrg(con, item[0])
#         jumlah = int(item[1])
#         total_harga = jumlah * creator.getIdBrgHrg(con, barang_id)
#         cursor.execute(query_detail, (id_transaksi, barang_id, jumlah, total_harga))

#     con.commit()
#     cursor.close()
    
#     return True, "Transaksi berhasil ditambahkan"

