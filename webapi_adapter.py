#webapi_adapter.py

import os
import httpx
import logging

log = logging.getLogger("webapi_adapter")

WEB_API_URL = os.getenv("WEB_API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "DEV_KEY")

async def send_status_to_webapi(order_id: str, status: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{WEB_API_URL}/api/v1/orders/{order_id}/status",
                json={"status": status},
                headers={
                    "X-API-KEY": API_KEY,
                    "X-ROLE": "courier",
                },
            )

        if resp.status_code != 200:
            log.warning(
                "WEBAPI STATUS FAILED | order=%s | %s %s",
                order_id,
                resp.status_code,
                resp.text,
            )

    except Exception:
        log.exception("WEBAPI STATUS ERROR | order=%s", order_id)
