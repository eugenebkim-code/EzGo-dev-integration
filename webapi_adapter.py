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
) -> bool:
    payload: Dict[str, Any] = {"status": status}

    if proof_image_file_id:
        payload["proof_image_file_id"] = proof_image_file_id
    if proof_image_message_id:
        payload["proof_image_message_id"] = proof_image_message_id

    url = f"{WEB_API_URL}/api/v1/orders/{order_id}/status"
    
    log.info(
        "WEBAPI STATUS SENDING | order=%s status=%s url=%s has_proof=%s",
        order_id,
        status,
        url,
        bool(proof_image_file_id),
    )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={
                    "X-API-KEY": API_KEY,
                    "X-ROLE": "courier",
                },
            )

        if resp.status_code == 200:
            log.info("WEBAPI STATUS OK | order=%s status=%s", order_id, status)
            return True
        else:
            log.error(
                "WEBAPI STATUS FAILED | order=%s status=%s code=%s body=%s",
                order_id,
                status,
                resp.status_code,
                resp.text[:500],
            )
            return False

    except Exception as e:
        log.exception("WEBAPI STATUS ERROR | order=%s status=%s error=%s", order_id, status, e)
        return False
