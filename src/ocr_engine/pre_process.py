from paddleocr import PaddleOCR, PPStructure

class OCRProcessor:
    def __init__(self, mode='structure', lang='en'):
        if mode == 'structure':
            # PP-Structure for tables/layout analysis
            self.engine = PPStructure(show_log=False, image_orientation=True)
        else:
            # Standard OCR for plain text
            self.engine = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)

    def extract(self, img_path):
        result = self.engine(img_path)
        # PP-Structure returns a list of regions (tables, text, figures)
        # Standard OCR returns a list of text lines and coordinates
        return result