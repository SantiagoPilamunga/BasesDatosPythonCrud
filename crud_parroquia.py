# crud_parroquia.py
"""
CRUD Parroquia - usa config.json para la conexión
"""

import os
import json
import pyodbc

# ------------------ Helpers para configuración y conexión ------------------
def leer_config(config_path='config.json'):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No se encontró {config_path} en {os.getcwd()}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def crear_conexion_desde_config(config_path='config.json'):
    cfg = leer_config(config_path)
    driver = cfg.get('driver', 'ODBC Driver 17 for SQL Server')
    server = cfg.get('server')
    database = cfg.get('database')
    trusted = cfg.get('trusted_connection', False)
    username = cfg.get('username', '')
    password = cfg.get('password', '')

    if not server or not database:
        raise ValueError("El archivo config.json debe contener 'server' y 'database'.")

    if trusted:
        conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    else:
        conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    return pyodbc.connect(conn_str)

# ------------------ CRUD Parroquia ------------------
def consultar_registros(conexion):
    try:
        print("\n\t\tCONSULTA PARROQUIAS:\n")
        SQL = """
        SELECT parroquiaID, nombreParro, direccionParro, telefonoParro, emailParro
        FROM Parroquia
        """
        cursor = conexion.cursor()
        cursor.execute(SQL)
        rows = cursor.fetchall()

        if not rows:
            print("No hay registros.")
            return

        for r in rows:
            try:
                print(f"{r.parroquiaID}\t{r.nombreParro}\t{r.direccionParro}\t{r.telefonoParro}\t{r.emailParro}")
            except:
                print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}")
    except Exception as e:
        print("\nError al consultar SQL Server:\n", e)

def insertar_registro(conexion):
    try:
        print("\n\t\tINSERTAR PARROQUIA:\n")
        SQL = """
        INSERT INTO Parroquia (parroquiaID, nombreParro, direccionParro, telefonoParro, emailParro)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = conexion.cursor()

        l_id = int(input("Ingrese ID Parroquia: "))
        l_nombre = input("Ingrese Nombre Parroquia: ").strip()
        l_direccion = input("Ingrese Dirección Parroquia: ").strip()
        l_tel = input("Ingrese Teléfono Parroquia (opcional): ").strip()
        l_email = input("Ingrese Email Parroquia: ").strip()

        telefono = int(l_tel) if l_tel else None

        cursor.execute(SQL, (l_id, l_nombre, l_direccion, telefono, l_email))
        conexion.commit()
        print("\nParroquia insertada correctamente.\n")
    except Exception as e:
        try: conexion.rollback()
        except: pass
        print("\nError al insertar en SQL Server:\n", e)

def actualizar_registro(conexion):
    try:
        print("\n\t\tACTUALIZAR EMAIL DE PARROQUIA:\n")
        SQL = """UPDATE Parroquia SET emailParro = ? WHERE parroquiaID = ?"""

        cursor = conexion.cursor()
        l_id = int(input("Ingrese ID de la Parroquia: "))
        l_email = input("Ingrese nuevo Email: ").strip()

        cursor.execute(SQL, (l_email, l_id))
        conexion.commit()

        print("\nParroquia actualizada correctamente.\n")
    except Exception as e:
        try: conexion.rollback()
        except: pass
        print("\nError al actualizar SQL Server:\n", e)

def eliminar_registro(conexion):
    try:
        print("\n\t\tELIMINAR PARROQUIA:\n")
        SQL = """DELETE FROM Parroquia WHERE parroquiaID = ?"""

        cursor = conexion.cursor()
        l_id = int(input("Ingrese ID de la Parroquia a eliminar: "))

        cursor.execute(SQL, (l_id,))
        conexion.commit()

        print("\nParroquia eliminada correctamente.\n")
    except Exception as e:
        try: conexion.rollback()
        except: pass
        print("\nError al eliminar en SQL Server:\n", e)

def mostrar_opciones_crud():
    print("\t*********************************")
    print("\t**     SISTEMA CRUD PARROQUIA  **")
    print("\t*********************************")
    print("\t1. Crear parroquia")
    print("\t2. Consultar parroquias")
    print("\t3. Actualizar parroquia")
    print("\t4. Eliminar parroquia")
    print("\t5. Salir\n\n")

# ------------------ Programa Principal ------------------
if __name__ == '__main__':
    try:
        conexion = crear_conexion_desde_config('config.json')
        print("Conexión Exitosa.")
    except Exception as e:
        print("\nError al conectar a SQL Server:\n", e)
        raise SystemExit(1)

    try:
        while True:
            mostrar_opciones_crud()
            op = input("Seleccione opción 1-5: ").strip()

            if op == '1': insertar_registro(conexion)
            elif op == '2': consultar_registros(conexion)
            elif op == '3': actualizar_registro(conexion)
            elif op == '4': eliminar_registro(conexion)
            elif op == '5':
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nInterrupción por teclado.")
    finally:
        try:
            conexion.close()
            print("Conexión cerrada.")
        except:
            pass
