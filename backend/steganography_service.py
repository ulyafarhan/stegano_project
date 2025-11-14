# steganography_service.py
import struct
import os

# --- Definisi marker (Sama seperti sebelumnya) ---
MAGIC_MARKER = b"AES-EOF"
MARKER_LEN = len(MAGIC_MARKER)
# 8 bytes (unsigned long long) untuk menyimpan ukuran payload
SIZE_LEN = 8 

def encode(host_file_path: str, payload_bytes: bytes):
    """
    Menyisipkan payload ke AKHIR file host yang ada di disk.
    Tidak memuat seluruh file host ke memori.
    """
    try:
        # 'Q' adalah 8-byte unsigned long long
        payload_size_bytes = struct.pack('>Q', len(payload_bytes))
        
        # Buka file host dalam mode 'append binary' (ab)
        with open(host_file_path, 'ab') as f:
            # Sesuai desain: [PAYLOAD] + [UKURAN PAYLOAD] + [MAGIC]
            f.write(payload_bytes)
            f.write(payload_size_bytes)
            f.write(MAGIC_MARKER)
            
    except IOError as e:
        raise ValueError(f"Gagal menulis ke file host: {e}")


def decode(combined_file_path: str) -> bytes:
    """
    Mengekstrak payload dari file di disk tanpa memuat seluruh file ke memori.
    Menggunakan file.seek() untuk membaca dari akhir.
    """
    try:
        with open(combined_file_path, 'rb') as f:
            # --- 1. Cek Magic Marker ---
            # Pindah ke akhir file dikurangi panjang marker
            f.seek(-MARKER_LEN, os.SEEK_END) 
            marker = f.read(MARKER_LEN)
            if marker != MAGIC_MARKER:
                raise ValueError("Tidak ada data tersembunyi yang ditemukan (marker tidak ada).")

            # --- 2. Ekstrak Ukuran Payload ---
            # Pindah ke posisi sebelum marker dan size
            f.seek(-(MARKER_LEN + SIZE_LEN), os.SEEK_END)
            payload_size_bytes = f.read(SIZE_LEN)
            payload_size = struct.unpack('>Q', payload_size_bytes)[0]
            
            # --- 3. Ekstrak Payload ---
            # Pindah ke posisi awal payload
            payload_index_start = -(MARKER_LEN + SIZE_LEN + payload_size)
            f.seek(payload_index_start, os.SEEK_END)
            
            # Baca payload
            payload_bytes = f.read(payload_size)
            
            # Validasi akhir
            if len(payload_bytes) != payload_size:
                raise IndexError("Ukuran payload tidak cocok dengan metadata (file korup).")

            return payload_bytes
            
    except (struct.error, IndexError, IOError) as e:
        raise ValueError(f"File korup atau format metadata tidak valid: {e}")
    except FileNotFoundError:
        raise ValueError("File host tidak ditemukan.")