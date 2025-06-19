import os
from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId  
from typing import Optional


load_dotenv()

URI = os.getenv("URI")

@dataclass
class Vehiculo:
    modelo: str
    año: int
    color: str
    placa_id: Optional[ObjectId] = None

    def save(self, coll):
        result = coll.insert_one( asdict(self) )
        return result.inserted_id

def get_collection(uri, db, col):
    client = MongoClient(  
        uri
        , server_api = ServerApi("1")
        , tls = True
        , tlsAllowInvalidCertificates = True
    )
    
    client.admin.command("ping")
    
    return client[db][col]

def actualizar_vehiculo_placa(coll_vehiculos, vehiculo_id, nueva_placa_id):
    filtro = {"_id": ObjectId(vehiculo_id)}
    nuevos_valores = {"$set": {"placa_id": ObjectId(nueva_placa_id)}}
    resultado = coll_vehiculos.update_one(filtro, nuevos_valores)
    
    if resultado.matched_count > 0:
       print("vehiculo actualizado con nueva placa correctamente")
    else:
        print("No se encontró vehiculo con ese ID.")
    return resultado



