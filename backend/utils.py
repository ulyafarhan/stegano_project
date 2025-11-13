# utils.py
import struct
from fastapi import HTTPException, status

PAYLOAD_HEADER_SIZE = 4  # 4 bytes for 32-bit integer

def pack_payload(data: bytes) -> bytes:
    size_header = struct.pack('>I', len(data))
    return size_header + data

def unpack_payload(data: bytes) -> tuple[bytes, bytes]:
    if len(data) < PAYLOAD_HEADER_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data rusak: header tidak lengkap."
        )
    
    payload_size = struct.unpack('>I', data[:PAYLOAD_HEADER_SIZE])[0]
    payload_end = PAYLOAD_HEADER_SIZE + payload_size
    
    if len(data) < payload_end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data rusak: payload terpotong."
        )
        
    payload = data[PAYLOAD_HEADER_SIZE:payload_end]
    remaining_data = data[payload_end:]
    
    return payload, remaining_data