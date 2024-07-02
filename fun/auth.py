from . import connection,cryptr
from django.http import HttpResponse

con = connection.connect()

def authen(username, password):
    cursor = con.cursor()
    query = "SELECT pass, id_karyawan  FROM karyawan3 WHERE karyawan = %s"
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        id_karyawan = row[1]
        hashed_password = row[0]
        if cryptr.verify_password(hashed_password,password):
            return id_karyawan
        else:
            return False
    else:
        return False

def degreeAuth(id_karyawan):
    cursor = con.cursor()
    query = """
        SELECT jabatan.level
        FROM karyawan3
        JOIN jabatan ON karyawan3.id_jabatan = jabatan.id_jabatan
        WHERE karyawan3.id_karyawan = %s
    """
    cursor.execute(query, (id_karyawan,))
    row = cursor.fetchone()
    cursor.close()
    dataForOwner = {
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': True,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_distrans':True,
        'show_logout': True,
        'show_login': False,
    }
    dataForKasir = {
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': False,
        'show_inventory': False,
        'show_organization': True,
        'show_transaction_history': True,
        'show_distrans':False,
        'show_logout': True,
        'show_login': False,
    }
    dataForManager = {
        'show_shopping_cart': False,
        'show_promo': False,
        'show_contact': False,
        'show_karyawan': False,
        'show_inventory': True,
        'show_organization': True,
        'show_transaction_history': True,
        'show_distrans':True,
        'show_logout': True,
        'show_login': False,
    }
    if row:
        level = int(row[0])
        return level
    else:
        return None 
    
def showKaryawan(level):
    if level > 99:
        return True
    elif level <= 99 and level > 50:
        return False
    else:
        return False
    
def showTrans(level):
    if level > 99:
        return True
    elif level <= 99 and level > 50:
        return True
    else:
        return False