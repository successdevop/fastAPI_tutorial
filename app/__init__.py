from typing import Any
from fastapi import FastAPI, HTTPException, status
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


@app.post("/shipment")
def submit_shipment(data: dict) -> dict[str, int]:
    content = data["content"]
    weight = data["weight"]

    if weight > 300:
        raise HTTPException(
            detail="Maximum weight limit is 300 kgs",
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )

    ship_id = max(shipment_db.keys()) + 1
    shipment_db[ship_id] = {
        "content": content,
        "weight": weight,
        "status": "placed"
    }

    return {"id": ship_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {
        field: shipment_db[id][field]
    }


@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipment_db:
        raise HTTPException(
            detail=f"shipment with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return shipment_db[id]

@app.put("/shipment/{id}")
def updated_replace_shipment(id: int, request_body: dict) -> dict[str, Any]:

    if id not in shipment_db:
        raise HTTPException(
            detail="ID not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    shipment_db[id] = request_body
    return shipment_db[id]


@app.patch("/shipment")
def patch_shipment(id: int, req_body: dict) -> dict[str, Any]:
    if id not in shipment_db:
        raise HTTPException(
            detail="ID not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    shipment = shipment_db[id]
    if "weight" in req_body:
        shipment["weight"] = req_body["weight"]
    if "content" in req_body:
        shipment["content"] = req_body["content"]
    if "status" in req_body:
        shipment["status"] = req_body["status"]

    return shipment
    # for k, v in shipment.items():
    #     setattr(req_body, k, v)
    #
    # return shipment


@app.delete("/shipment")
def delete_shipment(id: int):
    deleted_shipemnt = shipment_db.pop(id)
    return deleted_shipemnt



@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )