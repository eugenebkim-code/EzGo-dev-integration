#webapi_adapter.py

import os
import httpx
import logging

log = logging.getLogger("webapi_adapter")

WEB_API_URL = os.getenv("WEB_API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "DEV_KEY")

from typing import Optional, Dict, Any

async def send_status_to_webapi(
    order_id: str,
    status: str,
    proof_image_file_id: Optional[str] = None,
    proof_image_message_id: Optional[str] = None,
):
    payload: Dict[str, Any] = {"status": status}

    if proof_image_file_id:
        payload["proof_image_file_id"] = proof_image_file_id
    if proof_image_message_id:
        payload["proof_image_message_id"] = proof_image_message_id

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{WEB_API_URL}/api/v1/orders/{order_id}/status",
                json=payload,
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
