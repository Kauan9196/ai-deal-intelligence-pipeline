# AI-Powered Deal Intelligence Pipeline

## 🚀 Business Impact & Overview

This project represents a structural shift from no-code visual automations (like n8n) to a **production-ready, highly resilient Software Engineering architecture**.

In the highly competitive niche of "Hardware & Gaming Deal Intelligence," time-to-market is critical. The previous workflow—receiving a raw deal from a curator in Slack, manually cleaning links, generating high-CTR copy, injecting the correct affiliate tags, and publishing—could take several minutes and was prone to human error.

This pipeline automates the entire lifecycle, reducing the processing time from minutes to **milliseconds**, ensuring a 100% accurate integration with affiliate networks, and utilizing LLMs for cognitive tasks (like copywriting and data extraction) with strict safeguards.

## 🏗️ Architecture & Core Modules

The architecture follows Separation of Concerns, dependency injection readiness, and is highly modularized for future scaling.

### 1. Ingestion & Sanitization (`utils/sanitizer.py`)
- Receives raw payloads (e.g., from Slack webhooks) via a FastAPI endpoint.
- Uses robust Regex to parse strings and isolate the root URL.
- Cleanses dirty tracking parameters (like `?utm_source=...`) ensuring we have a pristine link before affiliate routing.

### 2. AI Data Extraction & Copywriting (`services/llm_processor.py`)
- Integrates with the **Groq API** running Llama 3 (8b-8192) for blazing-fast inference.
- **Strict JSON Mode**: The LLM is forced by prompt and API parameters to return a deterministic JSON object matching a strict Pydantic schema (`product_name`, `price`, `store_name`, `optimized_title`).
- **Resilience**: Engineered with Exponential Backoff (`tenacity`). If the Groq API returns a 429 (Rate Limit) or 503 (Service Unavailable), the system automatically retries gracefully rather than crashing the pipeline.

### 3. Dynamic Affiliate Router (`services/affiliate_router.py`)
- Analyzes the `store_name` returned by the LLM and dynamically routes the clean URL through the correct affiliate network.
- **Amazon Associates**: Automatically appends the tracking `&tag=`.
- **Awin / Rakuten (Kabum, Steam)**: Wraps the deep link in the network's required query structure.
- Unmapped stores are logged as warnings and preserved without mutation to avoid dead links.

### 4. Publisher Webhooks (`services/publisher.py` & `main.py`)
- Acts as the egress point. Simulates database insertion and triggers downstream webhooks (like a WhatsApp or Telegram bot) with the final formatted payload.

## 🛠️ Tech Stack & Best Practices

- **Python 3.10+**: Core logic.
- **FastAPI & Pydantic**: For high-performance async endpoints and strict data validation schemas.
- **Groq API**: For ultra-low latency LLM interactions.
- **Tenacity**: For exponential backoff and retry logic, ensuring pipeline stability.
- **Python-Dotenv**: No secrets are hardcoded; everything is managed via environment variables.
- **Standard Logging**: The built-in `logging` module is configured globally, replacing fragile `print()` statements, providing context (INFO, WARNING, ERROR) for observability.

## 💻 Running the Project Locally

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd deal-intelligence-pipeline
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template file and fill in your keys:
```bash
cp .env.example .env
```

### 5. Run the Server
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000/docs` (Swagger UI).
