from .interface import SteganographyStrategy
import io
import piexif
from PIL import Image

class JPGHandler(SteganographyStrategy):
    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        # Kapasitas Metadata JPEG terbatas (~60KB untuk aman)
        return payload_size <= 60 * 1024 

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        # 1. Baca Image
        try:
            img = Image.open(host_file)
            img.verify() # Cek validitas
            host_file.seek(0)
            img = Image.open(host_file)
        except Exception:
            raise ValueError("File bukan gambar JPG yang valid.")

        # 2. Siapkan Metadata EXIF
        try:
            exif_dict = piexif.load(host_file.read())
        except:
            # Jika tidak ada EXIF, buat baru
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        # 3. Masukkan Payload ke UserComment (Tag ID 37510)
        # Kita simpan sebagai bytes murni
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = payload

        # 4. Dump EXIF baru ke bytes
        exif_bytes = piexif.dump(exif_dict)

        # 5. Simpan Gambar Baru dengan EXIF tersebut
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", exif=exif_bytes, quality=95)
        output_buffer.seek(0)
        
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        
        # 1. Coba Load EXIF
        try:
            # Baca bytes langsung agar piexif tidak bingung
            file_bytes = host_file.read()
            exif_dict = piexif.load(file_bytes)
        except Exception:
            # Ini terjadi jika file JPG valid tapi tidak punya header EXIF standar
            raise ValueError("File ini tidak memiliki metadata EXIF (Pesan tidak ditemukan).")

        # 2. Cari UserComment (Tag tempat kita simpan rahasia)
        if "Exif" in exif_dict and piexif.ExifIFD.UserComment in exif_dict["Exif"]:
            secret_data = exif_dict["Exif"][piexif.ExifIFD.UserComment]
            
            # Validasi tipe data
            if isinstance(secret_data, bytes):
                # Hapus header 'ASCII\0\0\0' jika ada (standar EXIF)
                if secret_data.startswith(b'ASCII\x00\x00\x00'):
                    return secret_data[8:]
                return secret_data
            
            raise ValueError("Format data di dalam EXIF tidak dikenali.")
            
        else:
            raise ValueError("Tidak ditemukan pesan rahasia di dalam file JPG ini.")