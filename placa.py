import os
from dataclasses import dataclass, asdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional


load_dotenv()

URI = os.getenv("URI")

@dataclass
class Placa:
    codigo: str
    expira: datetime
    pais: str
    vehiculo_id: Optional[ObjectId] = None

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

def actualizar_placa_vehiculo(coll_placas, placa_id, nuevo_vehiculo_id):
   
    filtro = {"_id": ObjectId(placa_id)}
    nuevos_valores = {"$set": {"vehiculo_id": ObjectId(nuevo_vehiculo_id)}}
    resultado = coll_placas.update_one(filtro, nuevos_valores)

    if resultado.matched_count > 0:
        print("Placa actualizada con vehículo correctamente.")
    else:
        print("No se encontró una placa con ese ID.")
    return resultado

