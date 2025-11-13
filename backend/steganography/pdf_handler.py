from .interface import SteganographyStrategy
import io
from pypdf import PdfReader, PdfWriter
import base64

class PDFHandler(SteganographyStrategy):
    METADATA_KEY = "/SteganoData"
    MAX_CAPACITY_BYTES = 64 * 1024  # Batas aman 64KB

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        return payload_size <= self.MAX_CAPACITY_BYTES

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        reader = PdfReader(host_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata(reader.metadata)
        
        encoded_payload = base64.b64encode(payload).decode('utf-8')
        writer.add_metadata({self.METADATA_KEY: encoded_payload})
        
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        reader = PdfReader(host_file)
        
        metadata = reader.metadata
        if self.METADATA_KEY not in metadata:
            raise ValueError("Tidak ada metadata steganografi ditemukan.")
            
        encoded_payload = metadata[self.METADATA_KEY]
        
        try:
            return base64.b64decode(encoded_payload)
        except Exception:
            raise ValueError("Data metadata rusak atau format salah.")def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        try:
            reader = PdfReader(host_file)
        except Exception:
            raise ValueError("File PDF host tampaknya rusak atau tidak valid.")
        
        metadata = reader.metadata
        if self.METADATA_KEY not in metadata:
            raise ValueError("Tidak ada metadata steganografi ditemukan.")
            
        encoded_payload = metadata[self.METADATA_KEY]
        
        try:
            # PERBAIKAN: Tangani kasus jika pypdf mengembalikan bytes
            if isinstance(encoded_payload, bytes):
                encoded_payload = encoded_payload.decode('utf-8')
                
            return base64.b64decode(encoded_payload)
        except Exception:
            raise ValueError("Data metadata rusak atau format base64 salah.")