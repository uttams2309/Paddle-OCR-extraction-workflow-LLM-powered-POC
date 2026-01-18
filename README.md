# Paddle OCR Extraction Workflow (LLM-Powered POC)

This project is a Proof of Concept (POC) that builds an automated pipeline for extracting structured data from documents (specifically invoices) using a combination of **PaddleOCR** for optical character recognition and **Large Language Models (LLMs)** for data structuring.

## 🚀 Features

- **OCR Engine**: Utilizes [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for high-accuracy text detection and recognition.
- **LLM Integration**: Connects to OpenAI's GPT models (e.g., GPT-4o) to parse unstructured OCR output into clean, structured JSON.
- **Automated Pipeline**: 
  - Scans input directory for images.
  - Extracts text using OCR.
  - Sends text to LLM for semantic extraction.
  - Saves structured results as JSON files.
- **Configurable**: Easy-to-adjust settings via `config/config.yaml` for model selection, paths, and processing parameters.

## 🛠️ Prerequisites

- Python 3.8 or higher
- [PaddlePaddle](https://www.paddlepaddle.org.cn/en/install/quick) installed (CPU or GPU version)
- An OpenAI API Key

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/uttams2309/Paddle-OCR-extraction-workflow-LLM-powered-POC.git
   cd Paddle-OCR-extraction-workflow-LLM-powered-POC
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## ⚙️ Configuration

The project is configured via `config/config.yaml`. You can modify:

- **OCR Settings**: Enable/disable GPU, set language.
- **LLM Settings**: Choose the model (e.g., `gpt-4o`, `gpt-3.5-turbo`), temperature, and token limits.
- **Paths**: Define input and output directories.

```yaml
ocr:
  use_gpu: false
  lang: "en"

llm:
  model: "gpt-4o"
  temperature: 0.0

paths:
  input_dir: "data/raw_documents"
  output_dir: "data/output_json"
```

## 🏃 Usage

1. **Prepare Data**: Place your invoice images (PNG, JPG) in the `data/raw_documents/` directory.

2. **Run the Pipeline**:
   Execute the main pipeline script:
   ```bash
   python src/pipeline.py
   ```

3. **Check Results**: Structured JSON files will be generated in `data/output_json/`.

## 📂 Project Structure

```
├── config/
│   ├── config.yaml          # Main configuration file
│   └── logging.conf         # Logging configuration
├── data/
│   ├── raw_documents/       # Input images
│   └── output_json/         # Extracted JSON results
├── src/
│   ├── llm_engine/          # LLM connection and prompts
│   ├── ocr_engine/          # PaddleOCR wrapper and logic
│   ├── utils/               # Helper functions (file handling, visualization)
│   └── pipeline.py          # Main execution script
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.
