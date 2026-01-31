#courier_stub.py

from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Courier Stub API")

API_KEY = "DEV_KEY"


def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


class CourierOrderCreate(BaseModel):
    order_id: str
    source: str
    client_tg_id: int
    client_name: str
    client_phone: str
    pickup_address: str
    delivery_address: str
    pickup_eta_at: str
    city: str
    comment: Optional[str] = None


@app.post("/api/v1/orders", dependencies=[Depends(require_api_key)])
def create_order(payload: CourierOrderCreate):
    print("[COURIER STUB] create order", payload.order_id)
    return {
        "status": "ok",
        "delivery_order_id": payload.order_id,
    }


@app.post(
    "/api/v1/orders/{order_id}/status",
    dependencies=[Depends(require_api_key)],
)
@app.post(
    "/api/v1/orders/{order_id}/status",
    dependencies=[Depends(require_api_key)],
)
def update_status(order_id: str, payload: dict):
    print("[COURIER STUB] status update", order_id, payload)

    status = payload.get("status")

    # 🧪 STUB: эмулируем proof_image_file_id при delivered
    if status == "delivered":
        payload.setdefault(
            "proof_image_file_id",
            "AgACAgUAAxkBAAMvaXy56qSlwCN6yzQ9HAegHvZlvLAAAnANaxtDw-BXeRz7KoYq2swBAAMCAAN5AAM4BA"
        )

    return {
        "status": "ok",
        "echo": payload,
    }
