# paddle-ocr-poc

Proof of concept: run PaddleOCR over a document, then hand the raw OCR text to an LLM to
turn it into clean structured JSON. The open-source-OCR counterpart to
`invoice-extraction-tool` (which uses a hosted service instead).

- **Repo:** `github.com/uttams2309/Paddle-OCR-extraction-workflow-LLM-powered-POC`.
- **State:** paused. 4 commits, last Jan 2026, 1 uncommitted file.

## Stack

Python 3.8+ · PaddleOCR ≥2.7 on PaddlePaddle ≥2.6 · OpenAI ≥1.0 (GPT-4o) ·
PyYAML · python-dotenv · opencv-python-headless.

## Setup and run

```sh
pip install -r requirements.txt
# create .env with:  OPENAI_API_KEY=...
python main.py
```

PaddlePaddle is a separate install and is platform-specific (CPU vs GPU builds) — see
https://www.paddlepaddle.org.cn/en/install/quick if `pip install -r requirements.txt`
alone doesn't give you a working `paddle`.

## Configuration

Everything is driven by `config/config.yaml`:

```yaml
ocr:
  use_gpu: false
  lang: "en"
llm:
  model: "gpt-4o"
```

plus temperature, token limits, and the input/output paths. Change behaviour there rather
than in code.

## Layout

- `main.py` — the pipeline: scan input dir → OCR → LLM → write JSON
- `src/` — the implementation
- `config/config.yaml` — all settings
- `data/` — sample input documents

## Gotchas

- `.env` with a live OpenAI key **exists on disk**. Gitignored; don't commit or copy it.
- `.idea/` is committed IntelliJ config, harmless.
- A 291 MB zipped snapshot of this project is parked at
  `archive/Paddle_OCR_extraction_POC.zip` — that size is model/data weight, not source.
