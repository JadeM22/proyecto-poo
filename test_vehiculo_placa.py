import os
import unittest
from datetime import datetime
from bson.objectid import ObjectId
from vehiculo import Vehiculo, get_collection, actualizar_vehiculo_placa
from placa import Placa, actualizar_placa_vehiculo
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("URI")

class TestModelo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.coll_vehiculos = get_collection(URI, db="test_db", col="vehiculos_test")
        cls.coll_placas = get_collection(URI, db="test_db", col="placas_test")

    def setUp(self):
        self.coll_vehiculos.delete_many({})
        self.coll_placas.delete_many({})

    def test_crear_instancias_y_guardar(self):
        vehiculo = Vehiculo(modelo="Ford", año=2021, color="Blanco")
        id_vehiculo = vehiculo.save(self.coll_vehiculos)
        self.assertIsInstance(id_vehiculo, ObjectId)

        placa = Placa(codigo="AAA111", expira=datetime.now(), pais="Honduras", vehiculo_id=id_vehiculo)
        id_placa = placa.save(self.coll_placas)
        self.assertIsInstance(id_placa, ObjectId)

        placa_doc = self.coll_placas.find_one({"_id": id_placa})
        self.assertEqual(placa_doc["vehiculo_id"], id_vehiculo)

    def test_actualizar_vehiculo_con_id_placa(self):
       
        vehiculo = Vehiculo(modelo="Chevrolet", año=2020, color="Rojo")
        id_vehiculo = vehiculo.save(self.coll_vehiculos)
        self.assertIsInstance(id_vehiculo, ObjectId)

        placa = Placa(codigo="BBB222", expira=datetime.now(), pais="Honduras")
        id_placa = placa.save(self.coll_placas)
        self.assertIsInstance(id_placa, ObjectId)

        resultado_vehiculo = actualizar_vehiculo_placa(self.coll_vehiculos, id_vehiculo, id_placa)
        self.assertGreaterEqual(resultado_vehiculo.matched_count, 1)

        resultado_placa = actualizar_placa_vehiculo(self.coll_placas, id_placa, id_vehiculo)
        self.assertGreaterEqual(resultado_placa.matched_count, 1)

        vehiculo_actualizado = self.coll_vehiculos.find_one({"_id": id_vehiculo})
        self.assertEqual(vehiculo_actualizado.get("placa_id"), id_placa)

        placa_actualizada = self.coll_placas.find_one({"_id": id_placa})
        self.assertEqual(placa_actualizada.get("vehiculo_id"), id_vehiculo)

if __name__ == "__main__":
    unittest.main()

