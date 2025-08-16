from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class Wallet(BaseModel):
    label: str
    chain: str
    address: str
    private_key: Optional[str] = Field(default="")  # keep empty if watch-only
