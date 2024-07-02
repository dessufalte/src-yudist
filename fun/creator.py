
from . import connection,cryptr,fetcher

con = connection.connect()

def tambah_barang(conn, nama_brg, harga, stock, id_cat, id_distributor):
    cursor = conn.cursor()
    id_barang = cryptr.generate_id()
    query = """
    INSERT INTO barang2 (id_barang, nama_brg, harga, stock, id_cat, id_distributor) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_barang, nama_brg, harga, stock, id_cat, id_distributor))
    conn.commit()
    cursor.close()



def hapus_barang(conn, id_barang):
    cursor = conn.cursor()
    query = """
    DELETE FROM barang2 WHERE id_barang = %s
    """
    cursor.execute(query, (id_barang,))
    conn.commit()
    cursor.close()

def hapus_nbarang(conn, nm_barang):
    cursor = conn.cursor()
    query = """
    DELETE FROM barang2 WHERE nama_brg = %s
    """
    cursor.execute(query, (nm_barang,))
    conn.commit()
    cursor.close()

def tambah_karyawan(conn, karyawan, passw, lvl):
    cursor = conn.cursor()
    id_karyawan = cryptr.generate_id()
    en_pass = cryptr.hash_password(passw)
    if int(lvl) > 99:
        id_jabatan = '2a0d1c8d-1143-43f6-8f09-6290d863ed2f'
    elif int(lvl) > 80 and int(lvl) < 99:
        id_jabatan = '0046cd2b-c74a-441b-a83c-fd02b1f1e93a'
    else:
        id_jabatan = '67727196-c67a-4ffd-a655-4646ff23d0e0'
    query = """
    INSERT INTO karyawan3 (id_karyawan, karyawan, pass, id_jabatan) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id_karyawan, karyawan, en_pass, id_jabatan))
    conn.commit()
    cursor.close()
# tambah_karyawan(con, "Imam Ali Yaasin","test","Kasir")

def hapus_karyawan(conn, id_karyawan):
    cursor = conn.cursor()
    query = "DELETE FROM karyawan3 WHERE id_karyawan = %s"
    cursor.execute(query, (id_karyawan,))
    conn.commit()
    cursor.close()

# hapus_karyawan(con,'c8112249-2d10-4eb2-9adb-f979fd7c66a9')
def tambah_kategory(conn, cat):
    cursor = conn.cursor()
    id_kategory = cryptr.generate_id()
    query = """
    INSERT INTO category2 (id_cat, cat) 
    VALUES (%s, %s)
    """
    cursor.execute(query, (id_kategory, cat))
    conn.commit()
    cursor.close()

def tambah_distributor(conn, distributor, contact, alamat):
    cursor = conn.cursor()
    id_distributor = cryptr.generate_id()
    query = """
    INSERT INTO distributor2 (id_distributor, distributor, contact, alamat) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id_distributor, distributor, contact, alamat))
    conn.commit()
    cursor.close()

def getIdCat(conn, cat):
    cursor = conn.cursor()
    query = """
    SELECT id_cat FROM category2 WHERE cat = %s
    """
    cursor.execute(query, (cat,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None


def getIdDis(conn, distributor):
    cursor = conn.cursor()
    query = """
    SELECT id_distributor FROM distributor2 WHERE distributor = %s
    """
    cursor.execute(query, (distributor,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None


def getIdBrg(conn, barang):
    cursor = conn.cursor()
    query = """
    SELECT id_barang FROM barang2 WHERE nama_brg = %s
    """
    cursor.execute(query, (barang,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None

def getIdBrgHrg(conn, id_barang):
    cursor = conn.cursor()
    query = """
    SELECT harga FROM barang2 WHERE id_barang = %s
    """
    cursor.execute(query, (id_barang,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None


def getBrgId(conn, id_barang):
    cursor = conn.cursor()
    query = """
    SELECT nama_brg FROM barang2 WHERE id_barang = %s
    """
    cursor.execute(query, (id_barang,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None

def getDisNam(conn, id_distrib):
    cursor = conn.cursor()
    query = """
    SELECT distributor FROM distributor2 WHERE id_distributor = %s
    """
    cursor.execute(query, (id_distrib,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None

def getKryId(conn, Id_kry):
    cursor = conn.cursor()
    query = """
    SELECT karyawan FROM karyawan3 WHERE id_karyawan = %s
    """
    cursor.execute(query, (Id_kry,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None

def tambah_transaksi(conn, tanggal, total_transaksi, id_karyawan, id_transaksi):
    cursor = conn.cursor()
    query = """
    INSERT INTO header_trans2 (id_transaksi, tanggal, total_transaksi, id_karyawan) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id_transaksi, tanggal, total_transaksi, id_karyawan))
    conn.commit()
    cursor.close()

def tambah_detail(conn, id_transaksi, id_barang, total_harga):
    cursor = conn.cursor()
    query = """
    INSERT INTO detail_transaksi2 (id_transaksi, id_barang, total_harga) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (id_transaksi, id_barang, total_harga))
    conn.commit()
    cursor.close()

def kurangi_stok(conn, id_barang, jumlah):
    cursor = conn.cursor()
    
    # Cek stok barang
    query_cek_stok = "SELECT stock FROM barang2 WHERE id_barang = %s"
    cursor.execute(query_cek_stok, (id_barang,))
    stok = cursor.fetchone()[0]
    
    if stok < jumlah:
        cursor.close()
        return False, f"Stok barang dengan ID {id_barang} tidak mencukupi. Stok tersedia: {stok}, jumlah yang diminta: {jumlah}"
    
    # Kurangi stok barang
    query_kurangi_stok = "UPDATE barang2 SET stock = stock - %s WHERE id_barang = %s"
    cursor.execute(query_kurangi_stok, (jumlah, id_barang))
    conn.commit()
    cursor.close()
    
    return True, "Stok berhasil dikurangi"

def acc_flag_yes(conn, id_transaksi, id_karyawan):
    cursor = conn.cursor()
    query = """
        UPDATE header_trans2 
        SET status = %s,
        id_karyawan = %s
        WHERE id_transaksi = %s
    """
    cursor.execute(query, (True,id_karyawan, id_transaksi))
    conn.commit()
    cursor.close()

def cek_id_transaksi(id_transaksi):
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_distributor
        FROM distrib_trans_header
        WHERE id_transaksi = %s
    ''', (id_transaksi,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]  # Mengembalikan id_distributor
    else:
        return "Tidak Ada (Layanan Pelanggan)" 
    
def getDisId(conn, id_transaksi):
    cursor = conn.cursor()
    query = """
    SELECT id_distributor FROM header_trans2 WHERE id_transaksi = %s
    """
    cursor.execute(query, (id_transaksi,))
    nilai = cursor.fetchone()
    cursor.close()
    return nilai[0] if nilai else None


# cats = getIdCat(con,"Makanan")
# distrib = getIdDis(con,"Malikul Saleh Tbk")

# tambah_barang(con, "Roti Selai Jeruk Nipis 100gr",12000,30,cats,distrib)

# hapus_nbarang(con,"Roti Selai Margarin 100gr")