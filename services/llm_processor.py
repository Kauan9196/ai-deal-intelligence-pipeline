import json
from groq import Groq
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from config.settings import settings
from config.logger import setup_logger
from models.schemas import LLMOutput

logger = setup_logger(__name__)

client = Groq(api_key=settings.GROQ_API_KEY)

class GroqServiceError(Exception):
    pass

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(GroqServiceError),
    reraise=True
)
def extract_deal_info(clean_text: str) -> LLMOutput:
    logger.info("Sending payload to Groq LLM...")
    
    prompt = f"""
    Extraia as seguintes informações do texto e retorne um objeto JSON estrito.
    Chaves obrigatórias:
    - "product_name": string (o nome do produto ou categoria principal)
    - "price": float ou null (apenas o valor numérico, sem moedas. Se não houver preço final exato, retorne null)
    - "store_name": string (nome da loja, ex: Amazon, Netshoes, Kabum)
    - "coupon_code": string ou null (o código do cupom, se houver no texto)
    - "optimized_title": string (crie um título altamente persuasivo e contextual em português do Brasil)

    REGRAS PARA O OPTIMIZED_TITLE:
    - Crie um "Gancho Temático" criativo no início seguido por dois pontos (ex: "Upgrade no Setup:", "ALERTA FASHION:", "Looks de Inverno:", "Pisando Fofo:").
    - Mencione o benefício principal (ex: "15% OFF", "R$400 OFF") e o produto/categoria.
    - Se houver um cupom e o nome do cupom remeter a algo, use isso no contexto.
    - Se houver condições (ex: "Acima de R$90"), coloque de forma resumida.
    - Adicione urgência no final se fizer sentido (ex: "Esgotando!", "Corre!").
    - NÃO seja genérico. Exemplo bom: "Conforto Nike: 15% OFF (acima de R$90) em Tênis usando cupom. Corre!"

    Texto da oferta:
    {clean_text}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é um Copywriter Especialista em Conversão (CTR) focado em promoções. Você sempre responde apenas com um JSON válido e estrito. Nunca adicione marcação markdown em volta do JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        response_content = chat_completion.choices[0].message.content
        data = json.loads(response_content)
        
        # Validate through Pydantic to ensure all keys are present and types are correct
        return LLMOutput(**data)
        
    except Exception as e:
        logger.error(f"Groq API Error or JSON parsing failed: {e}")
        # Reraise as a custom exception to trigger Tenacity retry
        raise GroqServiceError(f"Failed to process with LLM: {e}")
