import json
import os
import sys

# Add the root directory to sys.path to make 'src' importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.file_handler import load_config, list_files, save_json
from src.ocr_engine.paddle_processor import OCRProcessor
from src.llm_engine.connector import LLMClient
from src.llm_engine.prompts import INVOICE_EXTRACTION_PROMPT


def main():
    # Change to project root directory for correct relative paths
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # 1. Load Config
    config = load_config()

    # 2. Initialize Engines
    ocr = OCRProcessor(config)
    llm = LLMClient(config)

    input_dir = config['paths']['input_dir']
    output_dir = config['paths']['output_dir']

    print(f"🚀 Starting Extraction Pipeline on {input_dir}...")

    # 3. Process Files
    for file_path in list_files(input_dir):
        file_name = os.path.basename(file_path)
        print(f"Processing: {file_name}")

        # Step A: OCR Extraction
        raw_ocr_result = ocr.extract_text(file_path)

        # Step B: Serialize for LLM (Text only)
        clean_text_block = ocr.serialize_for_llm(raw_ocr_result)

        if not clean_text_block.strip():
            print(f"⚠️ No text found in {file_name}")
            continue

        # Step C: LLM Enhancement
        print("   -> Sending to LLM for enhancement...")
        extracted_json_str = llm.enhance_extraction(clean_text_block, INVOICE_EXTRACTION_PROMPT)

        # Step D: Save Result
        try:
            # Parse string to JSON object to ensure validity
            final_data = json.loads(extracted_json_str)

            # Construct output path
            out_name = os.path.splitext(file_name)[0] + ".json"
            out_path = os.path.join(output_dir, out_name)

            save_json(final_data, out_path)
            print(f"   ✅ Saved to {out_path}")

        except json.JSONDecodeError:
            print(f"   ❌ LLM returned invalid JSON for {file_name}")


if __name__ == "__main__":
    main()
