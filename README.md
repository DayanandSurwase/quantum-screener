# 📈 Quantum Screener
**An AI-Powered FinTech & EdTech Terminal built for the Indian Market.**

Quantum Screener is a production-grade algorithmic assessment tool designed to mimic the workflow of institutional investment teams. It combines real-time financial data with a highly optimized Unified AI Architecture to provide objective stock analysis, while seamlessly integrating an EdTech module to educate beginner investors.

---

## Key Features

* **Unified Multi-Agent AI Pipeline:** Simulates three distinct financial personas (The Optimistic Bull, The Skeptical Bear, and The Chief Investment Officer) in a single, rate-limit-optimized API call using Llama-3.
* **🇮🇳 Hyper-Localized for India:** Automatically converts foreign stock data (like Nasdaq's NVDA) into Indian Rupees (₹) and formats massive financial figures into readable Lakhs and Crores.
* **Quantum Academy (EdTech):** A dynamic AI flashcard generator. Enter any financial topic, and the system generates a custom 20-card 3D-flipping deck to teach market fundamentals in real-time.
* **Contextual RAG Chatbot:** Ask highly specific questions about the currently active stock, and the AI will retrieve the live context to answer accurately.
* **Dynamic Data Visualization:** Implements smooth, tension-adjusted historical price charts with institutional gradients and dynamic sentiment doughnut charts using Chart.js.
* **Live Market Intelligence:** Instantly fetches the daily percentage changes of top market heavyweights on load to display trending assets.

---

## Technology Stack

**Frontend:**
* HTML5 & CSS3 (Advanced Glassmorphism & 3D Transforms)
* Vanilla JavaScript (Asynchronous DOM Manipulation)
* Chart.js (Interactive Data Visualization)

**Backend:**
* Python 3.10+
* FastAPI (High-performance API routing)
* Yahoo Finance API (`yfinance` with `curl_cffi` for advanced rate-limit bypassing)
* Groq API (Llama-3.3-70b for instantaneous neural inference)

---

## System Architecture

Quantum Screener abandons the traditional "single prompt" AI approach. Instead, it utilizes a **Unified JSON Prompting Architecture**.

1.  **Data Ingestion:** The FastAPI backend securely scrapes live market metrics and historical action.
2.  **Parallel Persona Processing:** The data is fed into a single prompt engineered to act as three distinct agents:
    * **The Bull:** Identifies growth metrics and undervalued potential.
    * **The Bear:** Flags macroeconomic headwinds and overvaluation risks.
    * **The Judge:** Weighs both arguments against the data to deliver a final `BUY`, `HOLD`, or `SELL` verdict.
3.  **JSON Serialization:** The AI's output is strictly formatted as a JSON object, parsed by the backend, and piped to the glassmorphism UI for instant rendering.

---

## Installation & Setup

Want to run Quantum Screener locally? Follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/quantum-screener.git](https://github.com/yourusername/quantum-screener.git)
cd quantum-screener
```

### 2. Set up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3.Install Dependencies
```bash
pip install -r requirements.txt
```
Note: Ensure you have fastapi, uvicorn, yfinance, curl_cffi, requests, and python-dotenv installed

### 4.Configure Environment Variables
```bash
GROQ_API_KEY=your_api_key_here
```

### 5.Start the Server
```bash
uvicorn backend.main:app --reload
```

---

### 💡 Usage Guide
1. **Analyze an Asset:** Enter a ticker symbol (e.g., RELIANCE.NS or AAPL) in the Screener tab and click Initialize Analysis.

2. **Chat with Data:** Once an asset is loaded, use the chat terminal on the right to ask the AI deeper questions about the company's financials.

3. **Learn:** Navigate to the Learn tab, type a topic like "Mutual Funds," and click Generate Deck to interact with the 3D study cards.

---

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---

## License
This project is open-source and available under the MIT License.
