# steganography/mp3_handler.py
from .interface import SteganographyStrategy
import io
from mutagen.id3 import ID3, TXXX
import base64

class MP3Handler(SteganographyStrategy):
    ID3_KEY = "STEGANO_DATA"
    MAX_CAPACITY_BYTES = 128 * 1024 # Batas aman 128KB

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        return payload_size <= self.MAX_CAPACITY_BYTES

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        encoded_payload = base64.b64encode(payload).decode('utf-8')

        try:
            audio = ID3(host_file)
        except Exception:
            audio = ID3()
        
        audio.add(TXXX(encoding=3, desc=self.ID3_KEY, text=encoded_payload))
        
        output_buffer = io.BytesIO()
        audio.save(output_buffer)
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        try:
            audio = ID3(host_file)
        except Exception:
            raise ValueError("Gagal membaca tag ID3, file mungkin rusak.")

        tag_key = f"TXXX:{self.ID3_KEY}"
        if tag_key not in audio:
            raise ValueError("Tidak ada data steganografi (ID3) ditemukan.")
            
        encoded_payload = audio[tag_key].text[0]
        
        try:
            return base64.b64decode(encoded_payload)
        except Exception:
            raise ValueError("Data metadata rusak atau format base64 salah.")