from . import connection


def fetch_barang():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id_barang, b.nama_brg, b.harga, b.stock, c.cat, d.distributor, 'edit' as edit
        FROM barang2 b
        JOIN category2 c ON b.id_cat = c.id_cat
        JOIN distributor2 d ON b.id_distributor = d.id_distributor;
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_barang_by_name(nama_brg):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        SELECT b.nama_brg, b.harga 
        FROM barang2 b
        WHERE b.nama_brg = %s;
    '''
    
    cursor.execute(query, (nama_brg,))
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_barang_by_id(id_barang):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        SELECT *
        FROM barang2
        WHERE id_barang = %s;
    '''
    
    cursor.execute(query, (id_barang,))
    data = cursor.fetchone()
    conn.close()
    return data

def fetch_display():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.nama_brg, b.harga, b.stock, c.cat, d.distributor, 'beli' as beli 
        FROM barang2 b
        JOIN category2 c ON b.id_cat = c.id_cat
        JOIN distributor2 d ON b.id_distributor = d.id_distributor;
    ''')
    data = cursor.fetchall()
    conn.close()
    return data
def fetch_distributor():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_distributor, distributor, alamat, contact FROM distributor2
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


def fetch_category():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_cat, cat FROM category2
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


def fetch_header_transaksi():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id_transaksi, a.tanggal, a.total_transaksi, a.id_karyawan, a.id_distributor, a.status, d.distributor
        FROM header_trans2 a
        JOIN distributor2 d ON a.id_distributor = d.id_distributor
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_karyawan():
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id_karyawan, a.karyawan, a.id_jabatan, d.jabatan, d.level
        FROM karyawan3 a
        JOIN jabatan d ON a.id_jabatan = d.id_jabatan
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_detail_transaksi(id_transaksi):
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id_transaksi, a.id_barang, a.jumlah, a.total_harga, c.nama_brg, c.harga
        FROM detail_transaksi2 a
        JOIN barang2 c ON a.id_barang = c.id_barang
        WHERE a.id_transaksi = %s
    ''', (id_transaksi,))
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_detail_transaksi_header(id_transaksi):
    conn = connection.connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id_transaksi, a.tanggal, a.total_transaksi, a.id_karyawan, a.status, c.karyawan, d.distributor
        FROM header_trans2 a
        JOIN karyawan3 c ON a.id_karyawan = c.id_karyawan
        JOIN distributor2 d ON a.id_distributor = d.id_distributor
        WHERE a.id_transaksi = %s
    ''', (id_transaksi,))
    data = cursor.fetchall()
    conn.close()
    return data[0]

def fetch_barang_distrib(distrib):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        SELECT b.nama_brg, b.harga 
        FROM barang2 b
        WHERE b.id_distributor = %s;
    '''
    
    cursor.execute(query, (distrib,))
    data = cursor.fetchall()
    conn.close()
    return data

def count_rows(con, table_name):
    cur = con.cursor()
    query = f"SELECT COUNT(*) FROM {table_name};"
    cur.execute(query)
    count = cur.fetchone()[0]
    cur.close()
    return count

def fetch_edit_barang(id,nama, harga, kategori, distributor):
    print(id,nama, harga, kategori, distributor)
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        UPDATE barang2
        SET nama_brg = %s,
            harga = %s,
            id_cat = %s,
            id_distributor = %s
        WHERE id_barang = %s;
    '''
    
    cursor.execute(query, (nama, harga, kategori, distributor, id))
    conn.commit()
    conn.close()

def fetch_hapus_barang(id):
    print(id ,"id")
    conn = connection.connect()
    cursor = conn.cursor()
    query = '''
        DELETE FROM barang2 WHERE id_barang = %s
    '''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def fetch_hapus_kategori(id):
    print(id ,"id")
    conn = connection.connect()
    cursor = conn.cursor()
    query = '''
        DELETE FROM category2 WHERE id_cat = %s
    '''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def fetch_hapus_distributor(id):
    print(id ,"KKK")
    conn = connection.connect()
    cursor = conn.cursor()
    query = '''
        DELETE FROM distributor2 WHERE id_distributor = %s
    '''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def fetch_hapus_theader(id):
    print(id ,"id")
    conn = connection.connect()
    cursor = conn.cursor()
    query = '''
        DELETE FROM header_trans2 WHERE id_transaksi = %s
    '''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def fetch_distrib_barang(id_distributor):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        SELECT id_distributor, distributor, contact, alamat 
        FROM distributor2
        WHERE id_distributor = %s;
    '''
    
    cursor.execute(query, (id_distributor,))
    data = cursor.fetchone()
    conn.close()
    return data  

def fetch_nama_karyawan(id_karyawan):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        SELECT karyawan
        FROM karyawan3
        WHERE id_karyawan = %s;
    '''
    
    cursor.execute(query, (id_karyawan,))
    data = cursor.fetchone()
    conn.close()
    return data[0]  

def edit_distributor(id, nama, contact, alamat):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        UPDATE distributor2
        SET id_distributor = %s,
            distributor = %s,
            contact = %s,
            alamat = %s
        WHERE id_distributor = %s;
    '''
    cursor.execute(query, (id, nama, contact,alamat, id))
    conn.commit()
    conn.close()

def edit_category(id, cat):
    conn = connection.connect()
    cursor = conn.cursor()
    
    query = '''
        UPDATE category2
        SET id_cat = %s,
            cat = %s
        WHERE id_cat = %s;
    '''
    cursor.execute(query, (id, cat, id))
    conn.commit()
    conn.close()

def fetch_category_one(id_cat):
    conn = connection.connect()
    cursor = conn.cursor()
    query = '''
        SELECT id_cat, cat FROM category2 WHERE id_cat = %s
    '''
    cursor.execute(query,(id_cat,))
    data = cursor.fetchone()
    conn.close()
    return data