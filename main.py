from fastapi import FastAPI, HTTPException
from config.logger import setup_logger
from utils.sanitizer import extract_and_clean_urls, clean_text
from services.llm_processor import extract_deal_info
from services.affiliate_router import generate_affiliate_link
from services.publisher import publish_deal
from models.schemas import DealPayload, ProcessedDeal
import uvicorn

logger = setup_logger(__name__)

app = FastAPI(
    title="AI-Powered Deal Intelligence Pipeline",
    description="Ingests raw deals, sanitizes URLs, uses Groq LLM for extraction, routes to affiliate networks, and publishes.",
    version="1.0.0"
)

@app.post("/api/v1/deals/slack-webhook", response_model=ProcessedDeal)
def process_slack_deal(payload: DealPayload):
    logger.info("Received new deal from Slack webhook")
    
    # 1. Ingestion & Sanitization
    cleaned_input = clean_text(payload.raw_text)
    urls = extract_and_clean_urls(cleaned_input)
    main_url = urls[0] if urls else ""
    
    if not main_url:
        logger.warning("No URL found in the payload.")
        raise HTTPException(status_code=400, detail="No URL found in the payload")
        
    # 2. LLM Processing (Groq Llama 3)
    try:
        llm_data = extract_deal_info(cleaned_input)
    except Exception as e:
        logger.error(f"LLM processing failed definitively: {e}")
        raise HTTPException(status_code=500, detail="LLM processing failed after retries")

    # 3. Affiliate Routing
    affiliate_url = generate_affiliate_link(llm_data.store_name, main_url)
    
    # Create final compiled object
    processed_deal = ProcessedDeal(
        original_text=payload.raw_text,
        product_name=llm_data.product_name,
        price=llm_data.price,
        store_name=llm_data.store_name,
        coupon_code=llm_data.coupon_code,
        optimized_title=llm_data.optimized_title,
        affiliate_url=affiliate_url
    )
    
    # 4. Publish (Mock DB & Webhooks)
    publish_deal(processed_deal)
    
    logger.info("Deal pipeline completed successfully.")
    return processed_deal

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
