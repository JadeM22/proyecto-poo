import os
from dotenv import load_dotenv
from datetime import datetime
from vehiculo import Vehiculo, get_collection as get_collection_vehiculo, actualizar_vehiculo_placa
from placa import Placa, get_collection as get_collection_placa, actualizar_placa_vehiculo

load_dotenv()
URI = os.getenv("URI")

def main():
    coll_vehiculos = get_collection_vehiculo(URI, db="test_db", col="vehiculos_test")
    coll_placas = get_collection_placa(URI, db="test_db", col="placas_test")

    print("INGRESO DE DATOS DEL VEHÍCULO")
    modelo = input("Modelo del vehículo: ")
    año = int(input("Año del vehículo: "))
    color = input("Color del vehículo: ")

    vehiculo = Vehiculo(modelo=modelo, año=año, color=color)
    id_vehiculo = vehiculo.save(coll_vehiculos)
    print(f" Vehículo guardado con ID: {id_vehiculo}")

    print("\nINGRESO DE DATOS DE LA PLACA")
    codigo = input("Código de la placa: ")
    expira_str = input("Fecha de expiración (YYYY-MM-DD): ")
    pais = input("País de la placa: ")

    try:
        expira = datetime.strptime(expira_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Fecha inválida. Usar YYYY-MM-DD.")
        return

    placa = Placa(codigo=codigo, expira=expira, pais=pais, vehiculo_id=id_vehiculo)
    id_placa = placa.save(coll_placas)
    print(f" Placa guardada con ID: {id_placa}")

    resultado_vehiculo = actualizar_vehiculo_placa(coll_vehiculos, id_vehiculo, id_placa)
    resultado_placa = actualizar_placa_vehiculo(coll_placas, id_placa, id_vehiculo)

    if resultado_vehiculo.matched_count > 0:
        print(" Vehículo actualizado con ID de la placa.")
    else:
        print(" No se encontró el vehículo para actualizar.")

    if resultado_placa.matched_count > 0:
        print(" Placa actualizada con ID del vehículo.")
    else:
        print(" No se encontró la placa para actualizar.")

if __name__ == "__main__":
    main()








