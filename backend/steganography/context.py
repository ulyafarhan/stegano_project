# steganography/context.py
import io
import os
from .interface import SteganographyStrategy
from .png_handler import PNGHandler
from .pdf_handler import PDFHandler
from .wav_handler import WAVHandler
from .jpg_handler import JPGHandler
from .mp3_handler import MP3Handler
from .docx_handler import DocxHandler
from .xlsx_handler import XlsxHandler
from .mp4_handler import MP4Handler

class SteganographyService:
    def __init__(self):
        self.strategies: dict[str, SteganographyStrategy] = {
            # LSB Handlers
            ".png": PNGHandler(),
            ".wav": WAVHandler(),
            
            # Metadata Handlers
            ".pdf": PDFHandler(),
            ".jpg": JPGHandler(),
            ".jpeg": JPGHandler(), # Alias
            ".mp3": MP3Handler(),
            ".docx": DocxHandler(),
            ".xlsx": XlsxHandler(),
            ".mp4": MP4Handler(),
            ".m4a": MP4Handler(), # Alias
        }

    def get_handler(self, file_extension: str) -> SteganographyStrategy:
        handler = self.strategies.get(file_extension.lower())
        if not handler:
            raise NotImplementedError(f"Format file {file_extension} tidak didukung.")
        return handler

    def encode(self, host_file: io.BytesIO, payload: bytes, file_extension: str) -> io.BytesIO:
        handler = self.get_handler(file_extension)
        
        if not handler.check_capacity(host_file, len(payload)):
            raise ValueError("Payload terlalu besar untuk file host ini.")
        
        return handler.encode(host_file, payload)

    def decode(self, host_file: io.BytesIO, file_extension: str) -> bytes:
        handler = self.get_handler(file_extension)
        return handler.decode(host_file)