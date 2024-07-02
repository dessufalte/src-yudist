from . import connection


def search_bar(name_filter, cat_filter):
    con = connection.connect()
    query = """
    SELECT b.nama_brg, b.harga, b.stock, c.cat, d.distributor, 'beli' as beli 
    FROM barang2 b
    JOIN category2 c ON b.id_cat = c.id_cat
    JOIN distributor2 d ON b.id_distributor = d.id_distributor
    WHERE TRUE
    """
    cursor = con.cursor()
    if name_filter:
        query += f" AND b.nama_brg ILIKE '%{name_filter}%'"
    if cat_filter:
        query += f" AND c.cat = '{cat_filter}'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results