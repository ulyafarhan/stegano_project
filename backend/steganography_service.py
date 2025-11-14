# steganography_service.py
import struct

# Kita gunakan marker yang deskriptif
MAGIC_MARKER = b"AES-EOF"
MARKER_LEN = len(MAGIC_MARKER)
# 8 bytes (unsigned long long) untuk menyimpan ukuran payload
SIZE_LEN = 8 

def encode(host_bytes: bytes, payload_bytes: bytes) -> bytes:
    # 'Q' adalah 8-byte unsigned long long
    payload_size_bytes = struct.pack('>Q', len(payload_bytes))
    
    # Sesuai desain: [HOST] + [PAYLOAD] + [UKURAN PAYLOAD] + [MAGIC]
    return host_bytes + payload_bytes + payload_size_bytes + MAGIC_MARKER

def decode(combined_bytes: bytes) -> bytes:
    # 1. Cek Magic Marker
    if combined_bytes[-MARKER_LEN:] != MAGIC_MARKER:
        raise ValueError("Tidak ada data tersembunyi yang ditemukan (marker tidak ada).")
    
    try:
        # 2. Ekstrak Ukuran Payload (8 bytes sebelum marker)
        size_bytes_index_start = -(MARKER_LEN + SIZE_LEN)
        size_bytes_index_end = -MARKER_LEN
        
        payload_size_bytes = combined_bytes[size_bytes_index_start:size_bytes_index_end]
        payload_size = struct.unpack('>Q', payload_size_bytes)[0]
        
        # 3. Ekstrak Payload
        payload_index_start = -(MARKER_LEN + SIZE_LEN + payload_size)
        payload_index_end = -(MARKER_LEN + SIZE_LEN)
        
        # Validasi keamanan dasar
        if abs(payload_index_start) > len(combined_bytes):
            raise IndexError("Indeks payload kalkulasi tidak valid.")

        payload_bytes = combined_bytes[payload_index_start:payload_index_end]
        
        # Validasi akhir
        if len(payload_bytes) != payload_size:
            raise IndexError("Ukuran payload tidak cocok dengan metadata.")

        return payload_bytes
        
    except (struct.error, IndexError) as e:
        raise ValueError(f"File korup atau format metadata tidak valid: {e}")