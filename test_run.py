import os
import sys

# Add the project root to python path so it can find modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.sanitizer import extract_and_clean_urls, clean_text
from services.llm_processor import extract_deal_info
from services.affiliate_router import generate_affiliate_link
from models.schemas import ProcessedDeal

raw_text = """https://www.netshoes.com.br/tenis?mi=hm_ger_mntop_C-TIP-tenis&psn=Menu_Top
Cupom 15% OFF Acima de R$90 em Tênis Nike na Netshoes
Cupom: NETNIKE15"""

def main():
    cleaned_input = clean_text(raw_text)
    urls = extract_and_clean_urls(cleaned_input)
    main_url = urls[0] if urls else ""
    
    print("--- 1. INGESTION & SANITIZATION ---")
    print(f"Cleaned URL:  {main_url}")
    print("")
    
    print("--- 2. LLM PROCESSING ---")
    llm_data = extract_deal_info(cleaned_input)
    print(llm_data.model_dump_json(indent=2))
    print("")
    
    print("--- 3. AFFILIATE ROUTER ---")
    affiliate_url = generate_affiliate_link(llm_data.store_name, main_url)
    print(f"Final Affiliate URL: {affiliate_url}")
    
    print("\n--- 4. FINAL JSON PAYLOAD ---")
    processed_deal = ProcessedDeal(
        original_text=raw_text,
        product_name=llm_data.product_name,
        price=llm_data.price,
        store_name=llm_data.store_name,
        coupon_code=llm_data.coupon_code,
        optimized_title=llm_data.optimized_title,
        affiliate_url=affiliate_url
    )
    print(processed_deal.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
