# backend/utils.py
import struct
from fastapi import HTTPException, status

PAYLOAD_HEADER_SIZE = 4

def pack_payload(data: bytes) -> bytes:
    size_header = struct.pack('>I', len(data))
    return size_header + data

def unpack_payload(data: bytes) -> tuple[bytes, bytes]:
    if len(data) < PAYLOAD_HEADER_SIZE:
        raise HTTPException(status_code=400, detail="Data rusak.")
    payload_size = struct.unpack('>I', data[:PAYLOAD_HEADER_SIZE])[0]
    payload_end = PAYLOAD_HEADER_SIZE + payload_size
    if len(data) < payload_end:
        raise HTTPException(status_code=400, detail="Data terpotong.")
    return data[PAYLOAD_HEADER_SIZE:payload_end], data[payload_end:]

def detect_file_type(header: bytes) -> str:
    if header.startswith(b'%PDF'): return '.pdf'
    if header.startswith(b'\x89PNG\r\n\x1a\n'): return '.png'
    if header.startswith(b'\xff\xd8\xff'): return '.jpg'
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE': return '.wav'
    if header.startswith(b'ID3') or header.startswith(b'\xff\xfb'): return '.mp3'
    if len(header) > 12 and header[4:8] == b'ftyp': return '.mp4'
    if header.startswith(b'PK\x03\x04'): return '.docx'
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
        # Fallback untuk file lama
        ext = detect_file_type(package_data[:32])
        return package_data, f"hasil_ekstraksi{ext if ext else '.dat'}"

# --- FITUR BARU: Deteksi Jenis File Otomatis ---
def detect_file_type(header: bytes) -> str:
    if header.startswith(b'%PDF'): return '.pdf'
    if header.startswith(b'\x89PNG\r\n\x1a\n'): return '.png'
    if header.startswith(b'\xff\xd8\xff'): return '.jpg'
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE': return '.wav'
    if header.startswith(b'ID3') or header.startswith(b'\xff\xfb'): return '.mp3'
    if len(header) > 12 and header[4:8] == b'ftyp': return '.mp4'
    if header.startswith(b'PK\x03\x04'): return '.docx' # Bisa juga xlsx, default docx
    return ''