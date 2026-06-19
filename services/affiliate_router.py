from config.logger import setup_logger
from config.settings import settings
import urllib.parse

logger = setup_logger(__name__)

def generate_affiliate_link(store_name: str, sanitized_url: str) -> str:
    """
    Routes the base URL to the correct affiliate network format based on the store name.
    """
    store_lower = store_name.lower().strip()
    
    if "amazon" in store_lower:
        logger.info(f"Routing {store_name} via Amazon Associates")
        separator = "&" if "?" in sanitized_url else "?"
        return f"{sanitized_url}{separator}tag={settings.AMAZON_AFFILIATE_TAG}"
        
    elif "kabum" in store_lower or "steam" in store_lower:
        logger.info(f"Routing {store_name} via generic affiliate network (e.g., Awin/Rakuten)")
        encoded_url = urllib.parse.quote(sanitized_url)
        return f"https://awin.com/click?network_id={settings.AWIN_NETWORK_ID}&url={encoded_url}"
        
    else:
        logger.warning(f"Store not mapped: {store_name}. Keeping original clean link.")
        return sanitized_url
