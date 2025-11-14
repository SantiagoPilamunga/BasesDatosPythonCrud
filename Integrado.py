# crud_estudiantes.py
"""
CRUD Estudiantes - usa config.json para la conexión
Adaptado a partir de tu script: la conexión se crea desde JSON y se pasa a las funciones.
"""

import os
import json
import pyodbc

# ------------------ Helpers para configuración y conexión ------------------
def leer_config(config_path='config.json'):
    """Lee config.json y devuelve un dict."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"No se encontró {config_path} en {os.getcwd()}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def crear_conexion_desde_config(config_path='config.json'):
    """Crea y devuelve una conexión pyodbc usando la configuración del JSON."""
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

    # crear conexión
    return pyodbc.connect(conn_str)

# ------------------ Funciones CRUD (ya no crean la conexión internamente) ------------------
def consultar_registros(conexion):
    try:
        print("\n\t\tCONSULTA ESTUDIANTE:\n")
        SQL_QUERY = """
        SELECT IDEstudiante,NombreEstudiante,ApellidoEstudiante,Email,Telefono
        FROM Estudiantes
        """
        cursor = conexion.cursor()
        cursor.execute(SQL_QUERY)
        records = cursor.fetchall()
        if not records:
            print("No hay registros.")
            return
        for r in records:
            # si el driver no expone nombres, usar índices: r[0], r[1], ...
            try:
                print(f"{r.IDEstudiante}\t{r.NombreEstudiante} \t {r.ApellidoEstudiante}\t{r.Email} \t {r.Telefono}")
            except Exception:
                print(f"{r[0]}\t{r[1]} \t {r[2]}\t{r[3]} \t {r[4]}")
    except Exception as e:
        print("\n \t Ocurrió un error al consultar a SQL Server: \n\n", e)

def insertar_registro(conexion):
    try:
        print("\n\t\tINSERTAR ESTUDIANTE:\n")
        SENTENCIA_SQL = """
        INSERT INTO Estudiantes
        (IDEstudiante,NombreEstudiante,ApellidoEstudiante,Email,Telefono)
        VALUES(?,?,?,?,?)
        """
        micursor = conexion.cursor()
        l_IDEstudiante = int(input("Ingrese ID del Estudiante: \t"))
        l_NombreEstudiante = input("Ingrese Nombre Estudiante: \t").strip()
        l_ApellidoEstudiante = input("Ingrese Apellido Estudiante:\t").strip()
        l_Email = input("Ingrese Email Estudiante: \t").strip()
        l_Telefono = input("Ingrese Telefono Estudiante:\t").strip()
        micursor.execute(SENTENCIA_SQL, (l_IDEstudiante, l_NombreEstudiante, l_ApellidoEstudiante, l_Email, l_Telefono))
        conexion.commit()
        print("\nOk ... Insercion Exitosa: \n")
    except Exception as e:
        try:
            conexion.rollback()
        except:
            pass
        print("\n \t Ocurrió un error al insertar a SQL Server: \n\n", e)

def eliminar_registro(conexion):
    try:
        print("\n\t\tELIMINAR ESTUDIANTE:\n")
        micursor = conexion.cursor()
        SENTENCIA_SQL = """DELETE FROM Estudiantes WHERE IDEstudiante=?"""
        print("\n\t Eliminar Registro Estudiante:\n")
        l_IDEstudiante = int(input("Ingrese ID del Estudiante a Elimnar: \t"))
        micursor.execute(SENTENCIA_SQL, (l_IDEstudiante,))  # tupla de 1 elemento
        conexion.commit()
        print("Ok ... Eliminacion Exitosa: \n")
    except Exception as e:
        try:
            conexion.rollback()
        except:
            pass
        print("\n \t Ocurrió un error al eliminar en SQL Server: \n\n", e)

def actualizar_registro(conexion):
    try:
        print("\n\t\tACTUALIZAR ESTUDIANTE:\n")
        micursor = conexion.cursor()
        SENTENCIA_SQL = """UPDATE Estudiantes SET Email = ? WHERE IDEstudiante= ?"""
        print("\n\t Actualizar Informacion Estudiante:\n")
        l_IDEstudiante = int(input("Ingrese ID del Estudiante: \t"))
        l_Email = input("Ingrese Nuevo E-Mail Estudiante: \t").strip()
        micursor.execute(SENTENCIA_SQL, (l_Email, l_IDEstudiante))
        conexion.commit()
        print("\nOk ... Actualización Exitosa: \n")
    except Exception as e:
        try:
            conexion.rollback()
        except:
            pass
        print("\n \t Ocurrió un error al actualizar en SQL Server: \n\n", e)

def mostrar_opciones_crud():
    print("\t****************************")
    print("\t** SISTEMA CRUD UDEMYTEST **")
    print("\t****************************")
    print("\tOpciones CRUD:\n")
    print("\t1. Crear registro")
    print("\t2. Consultar registros")
    print("\t3. Actualizar registro")
    print("\t4. Eliminar registro")
    print("\t5. Salir\n\n")

# ------------------ Programa principal ------------------
if __name__ == '__main__':
    try:
        conexion = crear_conexion_desde_config('config.json')
        print("Conexion Exitosa:")
    except Exception as e:
        print("\n \t Ocurrió un error al conectar a SQL Server: \n\n", e)
        raise SystemExit(1)

    try:
        while True:
            mostrar_opciones_crud()
            opcion = input("Seleccione una opción 1-5:\t").strip()
            if opcion == '1':
                insertar_registro(conexion)
            elif opcion == '2':
                consultar_registros(conexion)
            elif opcion == '3':
                actualizar_registro(conexion)
            elif opcion == '4':
                eliminar_registro(conexion)
            elif opcion == '5':
                print("Saliendo del programa..\n\n.")
                break
            else:
                print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nInterrupción por teclado.")
    finally:
        try:
            conexion.close()
            print("Conexion Cerrada: \n")
        except Exception:
            pass
