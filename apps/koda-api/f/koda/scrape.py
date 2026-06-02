import asyncio
import wmill
from typing import Optional, List, Dict, Any, Union

from koda import KodaClient, ScrapeRequest, Action, WebhookConfig

async def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Dict[str, Any]] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/team_scoop/s3",
    webhook: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Scrape a single URL and extract information using Koda.
    """
    # 1. Normalize S3 config
    s3_config = None
    if s3_resource:
        s3_config = wmill.get_resource(s3_resource)
        if not s3_config:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}

        # Adapt windmill resource keys to what our FileService expects if needed
        s3_config["access_key"] = s3_config.get("accessKey", s3_config.get("access_key"))
        s3_config["secret_key"] = s3_config.get("secretKey", s3_config.get("secret_key"))
        s3_config["endpoint_url"] = s3_config.get("endPoint", s3_config.get("endpoint_url"))
        s3_config["path_style"] = s3_config.get("pathStyle", s3_config.get("path_style", True))

    # 2. Parse Actions
    koda_actions = []
    if actions:
        for a in actions:
            action_type = a.get("type")
            if action_type:
                koda_actions.append(Action(
                    type=action_type,
                    selector=a.get("selector"),
                    value=a.get("value"),
                    milliseconds=a.get("milliseconds"),
                    text=a.get("text"),
                    key=a.get("key"),
                    script=a.get("script"),
                    direction=a.get("direction"),
                    all=a.get("all"),
                    fullPage=a.get("fullPage"),
                    quality=a.get("quality"),
                    viewport=a.get("viewport"),
                    format=a.get("format"),
                    landscape=a.get("landscape"),
                    scale=a.get("scale")
                ))

    # 3. Normalize Formats
    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))

    # 4. Parse Webhook
    koda_webhook = None
    if webhook and isinstance(webhook, dict):
        koda_webhook = WebhookConfig(
            url=webhook.get("url"),
            headers=webhook.get("headers"),
            metadata=webhook.get("metadata")
        )

    # 5. Instantiate Koda Client and Scrape
    try:
        async with KodaClient(global_timeout=timeout) as client:
            request = ScrapeRequest(
                url=url,
                formats=normalized_formats,
                only_main_content=onlyMainContent,
                actions=koda_actions,
                timeout=timeout,
                s3_config=s3_config,
                webhook=koda_webhook
            )
            response = await client.scrape(request)
            
            if response.error:
                return {
                    "success": False,
                    "error": response.error
                }
                
            data = {}
            if response.markdown is not None:
                data["markdown"] = response.markdown
            if response.html is not None:
                data["html"] = response.html
            if response.links is not None:
                data["links"] = response.links
            if response.images is not None:
                data["images"] = response.images
            if response.metadata is not None:
                data["metadata"] = response.metadata
            if response.screenshot is not None:
                data["screenshot"] = response.screenshot
            if response.action_results is not None:
                data["actions"] = response.action_results
                
            return {
                "success": True,
                "data": data
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
