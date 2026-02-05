# webapi_adapter.py

import httpx
import logging
from typing import Optional, Dict, Any

log = logging.getLogger("webapi_adapter")

# 🔒 ЖЕСТКО ФИКСИРУЕМ PROD WEB API
WEB_API_BASE_URL = "https://marketplace-delivery-1-production.up.railway.app"
WEB_API_KEY = "DEV_KEY"
WEB_API_TIMEOUT = 10.0


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

    url = f"{WEB_API_BASE_URL}/api/v1/orders/{order_id}/status"

    log.info(
        "[WEBAPI] courier -> status | order=%s status=%s url=%s has_proof=%s",
        order_id,
        status,
        url,
        bool(proof_image_file_id),
    )

    try:
        async with httpx.AsyncClient(timeout=WEB_API_TIMEOUT) as client:
            resp = await client.post(
                url,
                json=payload,
                headers={
                    "X-API-KEY": WEB_API_KEY,
                    "X-ROLE": "courier",
                },
            )

        if resp.status_code == 200:
            log.info(
                "[WEBAPI] courier status OK | order=%s status=%s",
                order_id,
                status,
            )
            return True

        log.error(
            "[WEBAPI] courier status FAILED | order=%s status=%s code=%s body=%s",
            order_id,
            status,
            resp.status_code,
            resp.text[:500],
        )
        return False

    except Exception as e:
        log.exception(
            "[WEBAPI] courier status ERROR | order=%s status=%s err=%s",
            order_id,
            status,
            e,
        )
        return False