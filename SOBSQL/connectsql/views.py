from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pyodbc
import json


def welcome_page(request):
    return render(request, 'index.html')

# Database connection parameters
DB_CONFIG = {
    'server': 'sobsql.database.windows.net',
    'database': 'sobsqldb',
    'username': 'livindl',
    'password': 'Cherussery999#',
    'driver': '{ODBC Driver 18 for SQL Server}'
}

def get_db_connection():
    return pyodbc.connect(
        f'DRIVER={DB_CONFIG["driver"]};'
        f'SERVER=tcp:{DB_CONFIG["server"]};'
        f'PORT=1433;'
        f'DATABASE={DB_CONFIG["database"]};'
        f'UID={DB_CONFIG["username"]};'
        f'PWD={DB_CONFIG["password"]}'
    )

@csrf_exempt
def insert_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert each item into the submitform table
        for item in data['items']:
            cursor.execute('''
                INSERT INTO dbo.submitform (shop, deliveryMode, creditDays, discountPercentage, remarks, itemName, quantity, price, total)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                data['shop'],               # Parameter 1
                data['deliveryMode'],       # Parameter 2
                data['creditDays'],         # Parameter 3
                data['discountPercentage'], # Parameter 4
                data['remarks'],            # Parameter 5
                item['itemName'],           # Parameter 6
                item['quantity'],           # Parameter 7
                item['price'],              # Parameter 8
                item['total']               # Parameter 9
            )

        conn.commit()
        cursor.close()
        conn.close()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
def fetch_data(request):
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch unique branches from InputDatas table
        # cursor.execute('SELECT DISTINCT branch FROM dbo.InputDatas')
        # branches = [row[0] for row in cursor.fetchall()]

        # Fetch unique shops from InputDatas table
        cursor.execute('SELECT DISTINCT shopname FROM dbo.InputDatas')
        shops = [row[0] for row in cursor.fetchall()]

        # Fetch unique delivery modes from InputDatas table
        cursor.execute('SELECT DISTINCT deliveryMode FROM dbo.InputDatas')
        delivery_modes = [row[0] for row in cursor.fetchall()]

        # Fetch item names and rates from InputDatas table
        cursor.execute('SELECT itemName, rate FROM dbo.InputDatas')
        items = [{'itemName': row[0], 'rate': row[1]} for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        data = {
            # 'branches': branches,
            'shops': shops,
            'delivery_modes': delivery_modes,
            'items': items,
        }

        return JsonResponse(data)

    return JsonResponse({'status': 'fail'}, status=400)
