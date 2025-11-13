import struct
from fastapi import HTTPException, status

PAYLOAD_HEADER_SIZE = 4

def pack_payload(data: bytes) -> bytes:
    size_header = struct.pack('>I', len(data))
    return size_header + data

def unpack_payload(data: bytes) -> tuple[bytes, bytes]:
    if len(data) < PAYLOAD_HEADER_SIZE:
        raise HTTPException(status_code=400, detail="Data rusak: header tidak lengkap.")
    payload_size = struct.unpack('>I', data[:PAYLOAD_HEADER_SIZE])[0]
    payload_end = PAYLOAD_HEADER_SIZE + payload_size
    if len(data) < payload_end:
        raise HTTPException(status_code=400, detail="Data rusak: payload terpotong.")
    return data[PAYLOAD_HEADER_SIZE:payload_end], data[payload_end:]

# --- FITUR BARU: Deteksi Jenis File Fleksibel ---
def detect_file_type(header: bytes) -> str:
    """Mendeteksi ekstensi file dengan mencari signature di dalam header (bukan cuma di awal)."""
    # Cari substring magic bytes di 64 byte pertama
    if b'%PDF' in header: return '.pdf'
    if b'PNG' in header and b'\x1a\n' in header: return '.png'
    if b'\xff\xd8\xff' in header: return '.jpg'
    if b'RIFF' in header and b'WAVE' in header: return '.wav'
    if header.startswith(b'ID3') or b'\xff\xfb' in header: return '.mp3'
    if b'ftyp' in header: return '.mp4'
    if b'PK\x03\x04' in header: return '.docx' # Default Office
    return ''

def create_package(file_data: bytes, filename: str) -> bytes:
    filename_bytes = filename.encode('utf-8')
    header = struct.pack('>I', len(filename_bytes))
    return header + filename_bytes + file_data

def extract_package(package_data: bytes) -> tuple[bytes, str]:
    try:
        if len(package_data) < 4: raise ValueError
        filename_len = struct.unpack('>I', package_data[:4])[0]
        if filename_len > 255 or len(package_data) < 4 + filename_len: raise ValueError
        
        filename = package_data[4 : 4 + filename_len].decode('utf-8')
        content = package_data[4 + filename_len :]
        return content, filename
    except Exception:
        # Fallback untuk file lama/tanpa paket nama
        ext = detect_file_type(package_data[:64])
        return package_data, f"hasil_ekstraksi{ext if ext else '.dat'}"