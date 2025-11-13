from .interface import SteganographyStrategy
import io
from mutagen.mp4 import MP4
import base64

class MP4Handler(SteganographyStrategy):
    # Menggunakan 'free-form atom' (----)
    METADATA_KEY = "----:com.stegano:data"
    MAX_CAPACITY_BYTES = 128 * 1024 # Batas aman 128KB

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        return payload_size <= self.MAX_CAPACITY_BYTES

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        encoded_payload = base64.b64encode(payload) # Butuh bytes
        
        try:
            audio = MP4(host_file)
        except Exception as e:
            raise ValueError(f"Gagal memuat MP4: {e}")
        
        audio[self.METADATA_KEY] = [encoded_payload]
        
        output_buffer = io.BytesIO()
        audio.save(output_buffer)
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        try:
            audio = MP4(host_file)
        except Exception as e:
            raise ValueError(f"Gagal memuat MP4: {e}")

        if self.METADATA_KEY not in audio:
            raise ValueError("Tidak ada data steganografi (atom) ditemukan.")
            
        encoded_payload_bytes = audio[self.METADATA_KEY][0]
        
        try:
            return base64.b64decode(encoded_payload_bytes)
        except Exception:
            raise ValueError("Data metadata rusak atau format base64 salah.")