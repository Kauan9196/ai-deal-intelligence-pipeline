from config.logger import setup_logger
from models.schemas import ProcessedDeal

logger = setup_logger(__name__)

def publish_deal(deal: ProcessedDeal) -> bool:
    """
    Simulates sending the processed deal to an internal database and secondary webhooks.
    """
    logger.info(f"Publishing Deal: {deal.optimized_title}")
    
    # 1. Mock Database Save
    logger.info(f"-> Saved to Database (Store: {deal.store_name}, Price: {deal.price})")
    
    # 2. Mock Webhook (e.g., Slack/WhatsApp notification)
    logger.info(f"-> Triggered Webhook. Payload: {deal.model_dump_json()}")
    
    return True
