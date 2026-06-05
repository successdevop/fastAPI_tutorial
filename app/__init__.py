from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.seller_api import seller_router
from app.api.shipment_api import shipment_router
from app.database.session import create_db_tables, engine
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await create_db_tables()
    print("Database tables created...")

    yield
    print("Server has been stopped")
    await engine.dispose()
    print("server connection closed")


version = "v1"
app = FastAPI(
    title="Shipment Application",
    description="A REST API for a web shipment service",
    version=version,
    lifespan=lifespan
)

app.include_router(shipment_router, prefix=f"/api/{version}/shipments", tags=["Shipments"])
app.include_router(seller_router, prefix=f"/api/{version}/sellers", tags=["Sellers"])

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )

# shipment_db = {
#
#         123:{
#             "id": 12789,
#             "weight": 0.6,
#             "content": "glassware",
#             "status": "placed"
#         },
#         124:{
#             "id": 12790,
#             "weight": 0.8,
#             "content": "ceramics",
#             "status": "placed"
#         },
#         125:{
#             "id": 12791,
#             "weight": 1.2,
#             "content": "electronics",
#             "status": "shipped"
#         },
#         126:{
#             "id": 12792,
#             "weight": 0.5,
#             "content": "textiles",
#             "status": "pending"
#         },
#         127:{
#             "id": 12793,
#             "weight": 2.0,
#             "content": "furniture",
#             "status": "delivered"
#         }
# }


# @app.get("/shipment/latest", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def get_latest_shipment():
#     ship_id = max(shipment_db.keys())
#     return shipment_db[ship_id]
#
#
# @app.post("/shipment", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def submit_shipment(data: ShipmentCreate):
#     content = data.content
#     weight = data.weight
#
#     ship_id = max(shipment_db.keys()) + 1
#     shipment_db[ship_id] = {
#         "content": content,
#         "weight": weight,
#         "status": "placed"
#     }
#
#     return shipment_db[ship_id]
#
#
# @app.get("/shipment/{field}", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def get_shipment_field(field: str, ship_id: int, val: str):
#     shipment_db[ship_id][field] = val
#     return shipment_db[ship_id]
#
# @app.get("/shipment", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def get_shipment(ship_id: int):
#     if ship_id not in shipment_db:
#         raise HTTPException(
#             detail=f"shipment with id {ship_id} not found",
#             status_code=status.HTTP_404_NOT_FOUND
#         )
#
#     return shipment_db[ship_id]
#
# @app.put("/shipment/{ship_id}", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def updated_replace_shipment(ship_id: int, request_body: ShipmentRead):
#
#     if ship_id not in shipment_db:
#         raise HTTPException(
#             detail="ID not found",
#             status_code=status.HTTP_404_NOT_FOUND
#         )
#
#     shipment_db[ship_id].update(request_body)
#     return shipment_db[ship_id]
#
#
# @app.patch("/shipment", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
# def patch_shipment(ship_id: int, req_body: ShipmentUpdate):
#     print(req_body.status.value)
#
#     if ship_id not in shipment_db:
#         raise HTTPException(
#             detail="ID not found",
#             status_code=status.HTTP_404_NOT_FOUND
#         )
#
#     shipment_db[ship_id]["status"] =req_body.status.value
#     return shipment_db[ship_id]
#
#
# @app.delete("/shipment", status_code=status.HTTP_202_ACCEPTED)
# def delete_shipment(ship_id: int) -> dict[str, str]:
#     shipment_db.pop(ship_id)
#     return {"message":"Shipment deleted successfully"}
#
#