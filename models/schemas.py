from pydantic import BaseModel
from typing import Optional

class DealPayload(BaseModel):
    raw_text: str
    source: str = "slack"

class LLMOutput(BaseModel):
    product_name: str
    price: Optional[float] = None
    store_name: str
    coupon_code: Optional[str] = None
    optimized_title: str

class ProcessedDeal(BaseModel):
    original_text: str
    product_name: str
    price: Optional[float] = None
    store_name: str
    coupon_code: Optional[str] = None
    optimized_title: str
    affiliate_url: Optional[str]
