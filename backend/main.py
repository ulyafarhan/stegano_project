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

origins = ["http://localhost:5173"]

# --- PERBAIKAN UTAMA DI SINI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Baris ini WAJIB agar Frontend bisa baca nama file dari header
    expose_headers=["Content-Disposition"] 
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return HTTPException(status_code=500, detail="Terjadi error internal.")

def get_file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def resolve_format(file_data: bytes, filename: str) -> str:
    # 1. Deteksi Magic Bytes (Prioritas Utama)
    detected_ext = detect_file_type(file_data[:32])
    if detected_ext:
        return detected_ext
    # 2. Fallback ke nama file
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
        
        # Gunakan resolver cerdas (atasi file tanpa ekstensi)
        host_ext = resolve_format(host_data, host_file.filename)
        if not host_ext:
             raise ValueError(f"Format file host tidak dikenali. Gunakan: .png, .jpg, .pdf, .wav")

        # 1. Bungkus payload dengan nama aslinya
        packaged_data = create_package(payload_data, payload_file.filename)

        # 2. Enkripsi
        encrypted_package = crypto.encrypt(packaged_data, key)
        
        host_buffer = io.BytesIO(host_data)
        
        # 3. Sisipkan
        output_buffer = stegano_service.encode(host_buffer, encrypted_package, host_ext)
        
        # Pastikan nama output valid
        output_filename = f"encoded_{host_file.filename}"
        if not output_filename.lower().endswith(host_ext):
            output_filename += host_ext

        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )

    except (ValueError, NotImplementedError) as e:
        logger.warning(f"Encode failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Encode error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/decode")
async def http_decode(
    key: int = Form(...),
    host_file: UploadFile = File(...)
):
    try:
        host_data = await host_file.read()
        
        # Gunakan resolver cerdas (atasi file yang di-rename salah)
        host_ext = resolve_format(host_data, host_file.filename)
        if not host_ext:
            raise ValueError("Format file tidak dikenali atau rusak.")

        host_buffer = io.BytesIO(host_data)
        
        # 1. Ekstrak
        encrypted_package = stegano_service.decode(host_buffer, host_ext)
        
        # 2. Dekripsi
        decrypted_package = crypto.decrypt(encrypted_package, key)
        
        # 3. Ambil Nama Asli
        # Jika ini file lama (belum dipaket), dia akan auto-detect dan kasih nama "hasil_ekstraksi.jpg"
        original_content, original_filename = extract_package(decrypted_package)
        
        output_buffer = io.BytesIO(original_content)
        
        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{original_filename}\""}
        )

    except (ValueError, NotImplementedError) as e:
        logger.warning(f"Decode failed: {e}")
        msg = str(e)
        # Deteksi salah kunci (biasanya hasil decrypt jadi sampah & UTF-8 error)
        if "codec" in msg or "padding" in msg or "short" in msg:
            msg = "Kunci salah atau data rusak."
        raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        logger.error(f"Decode error: {e}")
        raise HTTPException(status_code=500, detail="Gagal memproses file.")

@app.get("/")
def read_root():
    return {"status": "Steganography API is running."}