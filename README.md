# AI Cloud Agent

## Clone repository

```bash
git clone https://github.com/luking-developer/ai-cloud-agent.git
```

## Quick start

### Create virtual environment

```bash
cd ai-cloud-agent/
python -m venv .venv
```

### Activate

```bash
source .venv/bin/activate
```

### Install dependecies

```bash
pip install google-genai streamlit openpyxl
```

## Configure API Key

Create a new Gemini API Key visiting https://aistudio.google.com/api-keys. Then replace `"your_gemini_api_key"` with your own.

```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

or create a `.env` file in the root of your project:

```bash
echo GEMINI_API_KEY="your_gemini_api_key" > .env
```

## Run

```bash
streamlit run app.py
```

