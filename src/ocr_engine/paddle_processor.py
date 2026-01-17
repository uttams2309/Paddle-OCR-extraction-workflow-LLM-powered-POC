from paddleocr import PaddleOCR
import logging


class OCRProcessor:
    def __init__(self, config):
        self.use_gpu = config['ocr']['use_gpu']
        self.lang = config['ocr']['lang']
        self.cls = config['ocr']['cls']

        # Initialize PaddleOCR
        # use_angle_cls=True handles rotated text
        self.ocr_engine = PaddleOCR(
            use_angle_cls=self.cls,
            lang=self.lang
        )

    def extract_text(self, img_path):
        """
        Runs OCR on an image.
        Returns: Raw result list from PaddleOCR.
        """
        logging.info(f"Processing image: {img_path}")
        result = self.ocr_engine.ocr(img_path)

        # PaddleOCR returns a list of lists (one per page).
        # We assume single image input here.
        if not result or result[0] is None:
            return []

        return result[0]

    def serialize_for_llm(self, raw_result):
        """
        Converts raw OCR output (boxes + text) into a structured string
        that preserves spatial information (bounding boxes) for the LLM.
        """
        serialized_data = []

        # Check if raw_result is the dictionary format (PaddleX style)
        if isinstance(raw_result, dict) and 'rec_texts' in raw_result:
            texts = raw_result['rec_texts']
            scores = raw_result['rec_scores']
            boxes = raw_result['dt_polys'] # or rec_polys

            for text, score, box in zip(texts, scores, boxes):
                # box is likely a numpy array (4, 2)
                if hasattr(box, 'tolist'):
                    box = box.tolist()
                
                # simplified box: [x_min, y_min, x_max, y_max]
                x_coords = [p[0] for p in box]
                y_coords = [p[1] for p in box]
                bbox = [int(min(x_coords)), int(min(y_coords)), int(max(x_coords)), int(max(y_coords))]

                serialized_data.append({
                    "text": text,
                    "bbox": bbox,
                    "confidence": round(float(score), 3)
                })
        
        # Fallback for standard PaddleOCR list of lists format
        elif isinstance(raw_result, list):
            for line in raw_result:
                # Expecting: [box, (text, confidence)]
                if len(line) < 2: 
                    continue
                    
                box = line[0]
                content = line[1]

                if isinstance(content, (list, tuple)):
                    text = content[0]
                    confidence = content[1]
                else:
                    text = str(content)
                    confidence = 0.0

                # box might be numpy array or list
                if hasattr(box, 'tolist'):
                    box = box.tolist()

                # simplified box: [x_min, y_min, x_max, y_max]
                try:
                    x_coords = [p[0] for p in box]
                    y_coords = [p[1] for p in box]
                    bbox = [int(min(x_coords)), int(min(y_coords)), int(max(x_coords)), int(max(y_coords))]
                except Exception:
                    bbox = []

                serialized_data.append({
                    "text": text,
                    "bbox": bbox,
                    "confidence": round(float(confidence), 3)
                })

        # Return JSON string representation
        import json
        return json.dumps(serialized_data, ensure_ascii=False, indent=2)
