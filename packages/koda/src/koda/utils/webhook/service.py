import asyncio
from worldline import structlog
from typing import Any, Callable, Dict, Optional
import functools
import inspect
from pydantic import BaseModel

import httpx

from koda.utils.webhook.schema import Webhook, WebhookEvent

logger = structlog.get_logger(__name__)



def _serialize_files(obj: Any) -> Any:
    from koda.utils.file.main import File
    if isinstance(obj, File):
        return obj.presigned_url or obj.base64
    elif isinstance(obj, dict):
        return {k: _serialize_files(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_files(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(_serialize_files(v) for v in obj)
    return obj

async def dispatch_webhook(
    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
) -> None:
    """Trigger an HTTP callback based on the webhook spec asynchronously."""
    if not webhook:
        return

    if webhook.events and event not in webhook.events:
        return

    request_payload = {"event": event.value, "payload": _serialize_files(payload)}
    if webhook.metadata:
        request_payload["metadata"] = webhook.metadata

    headers = webhook.headers or {}

    async def _send() -> None:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    str(webhook.url),
                    json=request_payload,
                    headers=headers,
                )
                response.raise_for_status()
        except Exception as e:
            logger.warning("Failed to trigger webhook for event %s: %s", event.value, e)

    await _send()


def webhook_dispatch(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        sig = inspect.signature(func)
        try:
            bound = sig.bind(*args, **kwargs)
        except TypeError:
            return await func(*args, **kwargs)
            
        bound.apply_defaults()
        
        webhook_raw = None
        var_kwarg_name = None
        request_obj = None
        for param in sig.parameters.values():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                var_kwarg_name = param.name
                
        if "webhook" in bound.arguments:
            webhook_raw = bound.arguments["webhook"]
        elif var_kwarg_name and "webhook" in bound.arguments.get(var_kwarg_name, {}):
            webhook_raw = bound.arguments[var_kwarg_name]["webhook"]
        else:
            for arg_val in bound.arguments.values():
                if isinstance(arg_val, BaseModel) and hasattr(arg_val, "webhook"):
                    webhook_raw = getattr(arg_val, "webhook")
                    request_obj = arg_val
                    break
            
        webhook = None
        if webhook_raw:
            if isinstance(webhook_raw, dict):
                webhook = Webhook(**webhook_raw)
            elif isinstance(webhook_raw, Webhook):
                webhook = webhook_raw
                
        # Inject parsed webhook back
        if "webhook" in bound.arguments:
            bound.arguments["webhook"] = webhook
        elif var_kwarg_name and "webhook" in bound.arguments.get(var_kwarg_name, {}):
            bound.arguments[var_kwarg_name]["webhook"] = webhook
        elif request_obj is not None:
            setattr(request_obj, "webhook", webhook)

        payload = {}
        for k, v in bound.arguments.items():
            if k == var_kwarg_name:
                if isinstance(v, dict):
                    for kw_k, kw_v in v.items():
                        if isinstance(kw_v, BaseModel):
                            payload[kw_k] = kw_v.model_dump(by_alias=True, exclude_none=True)
                        else:
                            payload[kw_k] = kw_v
            else:
                if isinstance(v, BaseModel):
                    payload[k] = v.model_dump(by_alias=True, exclude_none=True)
                else:
                    payload[k] = v
        
        if webhook:
            await dispatch_webhook(
                webhook=webhook,
                event=WebhookEvent.STARTED,
                payload=payload
            )

        try:
            response = await func(*bound.args, **bound.kwargs)
        except Exception as e:
            if webhook:
                payload["error"] = str(e)
                await dispatch_webhook(
                    webhook=webhook,
                    event=WebhookEvent.FAILED,
                    payload=payload
                )
            raise e

        if isinstance(response, BaseModel) or hasattr(response, "model_dump"):
            response_dict = response.model_dump(by_alias=True, exclude_none=True)
        elif isinstance(response, dict):
            response_dict = response
        else:
            response_dict = {"data": response}

        success = response_dict.get("success", True)
        event = WebhookEvent.COMPLETED if success else WebhookEvent.FAILED
        if webhook:
            await dispatch_webhook(
                webhook=webhook,
                event=event,
                payload=response_dict
            )
        return response

    return wrapper
