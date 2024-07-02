import connection, cryptr

con = connection.connect()

def tambah_role(conn, role, lvl):
    cursor = conn.cursor()
    id = cryptr.generate_id()
    query = """
    INSERT INTO jabatan (id_jabatan, jabatan, level) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (id, role, lvl))
    conn.commit()
    cursor.close()

tambah_role(con, "Owner", 100)
tambah_role(con, "Manager", 80)
tambah_role(con, "Kasir", 60)