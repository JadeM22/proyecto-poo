import unittest
import os
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
from vehiculo import Vehiculo, get_collection as get_vehiculos, actualizar_vehiculo_placa
from placa import Placa, get_collection as get_placas, actualizar_placa_vehiculo

load_dotenv()
URI = os.getenv("URI")

class TestVehiculoPlaca(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vehiculos_coll = get_vehiculos(URI, "test_db", "vehiculos_test")
        cls.placas_coll = get_placas(URI, "test_db", "placas_test")

    def setUp(self):
        self.vehiculos_coll.delete_many({})
        self.placas_coll.delete_many({})

    def test_creacion_y_relacion(self):
        vehiculo = Vehiculo("Toyota Corolla", 2022, "Negro")
        vehiculo_id = vehiculo.save(self.vehiculos_coll)

        placa = Placa("HND-123", datetime(2030, 5, 1), "Honduras")
        placa_id = placa.save(self.placas_coll)

        actualizar_vehiculo_placa(self.vehiculos_coll, vehiculo_id, placa_id)
        actualizar_placa_vehiculo(self.placas_coll, placa_id, vehiculo_id)

        vehiculo_doc = self.vehiculos_coll.find_one({"_id": vehiculo_id})
        placa_doc = self.placas_coll.find_one({"_id": placa_id})

        self.assertIsNotNone(vehiculo_doc)
        self.assertIsNotNone(placa_doc)
        self.assertEqual(vehiculo_doc.get("placa_id"), placa_id)
        self.assertEqual(placa_doc.get("vehiculo_id"), vehiculo_id)

if __name__ == "__main__":
    unittest.main()

