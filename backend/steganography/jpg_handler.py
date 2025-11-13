# steganography/jpg_handler.py
from .interface import SteganographyStrategy
import io
import piexif
import base64

class JPGHandler(SteganographyStrategy):
    EXIF_KEY = piexif.ImageIFD.ImageDescription
    MAX_CAPACITY_BYTES = 60 * 1024 # Batas aman EXIF 60KB

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        return payload_size <= self.MAX_CAPACITY_BYTES

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        encoded_payload = base64.b64encode(payload).decode('utf-8')
        
        try:
            exif_dict = piexif.load(host_file)
        except piexif.InvalidImageDataError:
            exif_dict = {"Image": {}}
        except Exception:
            host_file.seek(0)
            exif_dict = {"Image": {}}

        exif_dict["Image"][self.EXIF_KEY] = encoded_payload
        
        try:
            exif_bytes = piexif.dump(exif_dict)
        except Exception as e:
            raise ValueError(f"Gagal membuat EXIF: {e}")

        output_buffer = io.BytesIO()
        host_file.seek(0)
        
        try:
            piexif.insert(exif_bytes, host_file.read(), output_buffer)
        except Exception as e:
            raise ValueError(f"Gagal menyisipkan EXIF ke JPG: {e}")
            
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        try:
            exif_dict = piexif.load(host_file)
        except Exception:
             raise ValueError("Gagal membaca EXIF, file mungkin rusak atau bukan JPG.")
        
        if self.EXIF_KEY not in exif_dict.get("Image", {}):
            raise ValueError("Tidak ada data steganografi (EXIF) ditemukan.")
            
        encoded_payload = exif_dict["Image"][self.EXIF_KEY]
        
        try:
            # Data dari piexif bisa jadi bytes atau str
            if isinstance(encoded_payload, bytes):
                encoded_payload = encoded_payload.decode('utf-8')
            return base64.b64decode(encoded_payload)
        except Exception:
            raise ValueError("Data metadata rusak atau format base64 salah.")