from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Action(BaseModel):
    type: str
    selector: Optional[str] = None
    value: Optional[Any] = None
    milliseconds: Optional[int] = None
    text: Optional[str] = None
    key: Optional[str] = None
    script: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[int] = None
    all: Optional[bool] = None
    fullPage: Optional[bool] = None
    quality: Optional[int] = None
    viewport: Optional[Dict[str, int]] = None
    format: Optional[str] = None
    landscape: Optional[bool] = None
    scale: Optional[float] = None
    timeout: Optional[int] = None
    ignoreError: Optional[bool] = Field(default=True)
