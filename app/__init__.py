from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


app = FastAPI()

shipment_db = {

        123:{
            "id": 12789,
            "weight": 0.6,
            "content": "glassware",
            "status": "placed"
        },
        124:{
            "id": 12790,
            "weight": 0.8,
            "content": "ceramics",
            "status": "placed"
        },
        125:{
            "id": 12791,
            "weight": 1.2,
            "content": "electronics",
            "status": "shipped"
        },
        126:{
            "id": 12792,
            "weight": 0.5,
            "content": "textiles",
            "status": "pending"
        },
        127:{
            "id": 12793,
            "weight": 2.0,
            "content": "furniture",
            "status": "delivered"
        }
}


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipment_db.keys())
    return shipment_db[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipment_db:
        return {"message":f"shipment with id {id} not found"}
    return shipment_db[id]

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )