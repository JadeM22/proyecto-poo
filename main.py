import os
from datetime import datetime
from dotenv import load_dotenv
from vehiculo import Vehiculo, get_collection as get_collection_vehiculo, actualizar_vehiculo_placa
from placa import Placa, get_collection as get_collection_placa, actualizar_placa_vehiculo

load_dotenv()
URI = os.getenv("URI")

def main():
    coll_vehiculos = get_collection_vehiculo(URI, db="poo_db", col="vehiculos")
    coll_placas = get_collection_placa(URI, db="poo_db", col="placas")

    vehiculo = Vehiculo(modelo="Toyota Corolla", año=2020, color="Rojo")
    id_vehiculo = vehiculo.save(coll_vehiculos)
    print(f"Vehículo guardado con ID: {id_vehiculo}")

    placa = Placa(codigo="ABC123", expira=datetime(2025, 12, 31), pais="Honduras", vehiculo_id=id_vehiculo)
    id_placa = placa.save(coll_placas)
    print(f"Placa guardada con ID: {id_placa}")

    print("\nAntes de actualizar vehículo:")
    vehiculo_antes = coll_vehiculos.find_one({"_id": id_vehiculo})
    print(vehiculo_antes)

    resultado_vehiculo = actualizar_vehiculo_placa(coll_vehiculos, id_vehiculo, id_placa)
    resultado_placa = actualizar_placa_vehiculo(coll_placas, id_placa, id_vehiculo)

    if resultado_vehiculo.matched_count > 0:
        print(" Vehículo actualizado correctamente con la placa.")
    else:
        print(" No se encontró el vehículo para actualizar.")

    if resultado_placa.matched_count > 0:
        print(" Placa actualizada correctamente con el vehículo.")
    else:
        print(" No se encontró la placa para actualizar.")

    print("\nDespués de actualizar vehículo:")
    vehiculo_actualizado = coll_vehiculos.find_one({"_id": id_vehiculo})
    print(vehiculo_actualizado)

    print("\nPlaca actualizada:")
    placa_actualizada = coll_placas.find_one({"_id": id_placa})
    print(placa_actualizada)

if __name__ == "__main__":
    main()








