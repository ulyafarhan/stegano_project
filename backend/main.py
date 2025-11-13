import io
import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import crypto
from steganography.context import SteganographyService
from utils import create_package, extract_package, detect_file_type

app = FastAPI(title="VertexGuard API")
stegano_service = SteganographyService()

# Konfigurasi CORS (Wajib untuk Frontend)
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def resolve_format(file_data: bytes, filename: str) -> str:
    # Ambil lebih banyak bytes untuk deteksi yang lebih akurat
    detected_ext = detect_file_type(file_data[:64])
    
    print(f"[DEBUG] Filename: {filename}")
    print(f"[DEBUG] Header Bytes: {file_data[:16]}")
    print(f"[DEBUG] Detected Ext: {detected_ext}")
    
    if detected_ext:
        return detected_ext
    
    # Fallback ke ekstensi nama file jika deteksi gagal
    return get_file_ext(filename)

@app.post("/encode")
async def http_encode(
    key: int = Form(...),
    payload_file: UploadFile = File(...),
    host_file: UploadFile = File(...)
):
    try:
        payload_data = await payload_file.read()
        host_data = await host_file.read()
        
        host_ext = resolve_format(host_data, host_file.filename)
        if not host_ext:
             raise ValueError("Format file host tidak dikenali. Gunakan: .png, .jpg, .pdf, .wav")

        packaged_data = create_package(payload_data, payload_file.filename)
        encrypted_package = crypto.encrypt(packaged_data, key)
        
        host_buffer = io.BytesIO(host_data)
        output_buffer = stegano_service.encode(host_buffer, encrypted_package, host_ext)
        
        output_filename = f"encoded_{host_file.filename}"
        if not output_filename.lower().endswith(host_ext):
            output_filename += host_ext

        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )

    except Exception as e:
        logger.error(f"Encode error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.post("/decode")
async def http_decode(
    key: int = Form(...),
    host_file: UploadFile = File(...)
):
    try:
        host_data = await host_file.read()
        
        # RESOLVER BARU: Memprioritaskan isi file daripada nama
        host_ext = resolve_format(host_data, host_file.filename)
        
        if not host_ext:
            raise ValueError("Format file tidak dikenali atau rusak.")

        print(f"[DEBUG] Using Handler for: {host_ext}") # Cek log terminal

        host_buffer = io.BytesIO(host_data)
        
        # 1. Ekstrak
        encrypted_package = stegano_service.decode(host_buffer, host_ext)
        
        # 2. Dekripsi
        decrypted_package = crypto.decrypt(encrypted_package, key)
        
        # 3. Ambil Nama Asli
        # (Jika ini file lama, utils.py akan otomatis memberinya nama 'hasil_ekstraksi.xxx')
        original_content, original_filename = extract_package(decrypted_package)
        
        output_buffer = io.BytesIO(original_content)
        
        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{original_filename}\""}
        )

    except Exception as e:
        logger.error(f"Decode error: {e}")
        msg = str(e)
        # Pesan error lebih manusiawi
        if "codec" in msg or "padding" in msg:
            msg = "Gagal mendekripsi. Kunci (Key) salah."
        elif "metadata" in msg:
            msg = "Tidak ada pesan rahasia ditemukan di file ini."
            
        raise HTTPException(status_code=400, detail=msg)

@app.get("/")
def read_root():
    return {"status": "Steganography API is running."}