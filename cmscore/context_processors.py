import mysql.connector
from django.core.files.storage import default_storage

class CMI:
    def __init__(self, cmi_id, name, detail, logo):
        self.cmi_id = cmi_id
        self.name = name
        self.detail = detail
        self.logo_url = default_storage.url(logo)

def cmi_list(request):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='testo')
        cursor = conn.cursor()

        query = "SELECT * FROM cmi"
        cursor.execute(query)

        cmi_list = []
        for row in cursor.fetchall():
            cmi = CMI(row[0], row[2], row[8], row[7])
            cmi_list.append(cmi)
    except mysql.connector.errors.Error as e:
        print(f"An error occurred: {e}")
        cmi_list = None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return {'cmi_list': cmi_list} if cmi_list is not None else {}