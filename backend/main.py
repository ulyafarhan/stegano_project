import io
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Impor layanan baru berdasarkan dokumen desain Anda
import crypto_service 
import steganography_service

# Impor utilitas yang sudah ada untuk menangani paket nama file
from utils import create_package, extract_package

app = FastAPI(title="VertexGuard API (AES-EOF)")

# Konfigurasi CORS (sesuai dokumen desain)
origins = [
    "http://localhost:5173",
    # "https://nama-app-anda.vercel.app" 
]

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

@app.post("/encode")
async def http_encode(
    key: str = Form(...),
    payload_file: UploadFile = File(...),
    host_file: UploadFile = File(...)
):
    try:
        payload_data = await payload_file.read()
        host_data = await host_file.read()

        # 1. Bungkus payload DENGAN nama filenya (dari utils.py)
        packaged_data = create_package(payload_data, payload_file.filename)
        
        # 2. Enkripsi paket (menggunakan AES-256 baru)
        encrypted_package = crypto_service.encrypt(packaged_data, key)
        
        # 3. Sisipkan (EOF Appending baru)
        combined_file_bytes = steganography_service.encode(host_data, encrypted_package)
        
        output_buffer = io.BytesIO(combined_file_bytes)
        output_filename = f"encoded_{host_file.filename}"

        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )
    except Exception as e:
        logger.error(f"Encode error: {e}")
        raise HTTPException(status_code=500, detail=f"Enkripsi gagal: {str(e)}")

@app.post("/decode")
async def http_decode(
    key: str = Form(...),
    host_file: UploadFile = File(...)
):
    try:
        combined_file_bytes = await host_file.read()
        
        # 1. Ekstrak (EOF Appending baru)
        encrypted_package = steganography_service.decode(combined_file_bytes)
        
        # 2. Dekripsi (menggunakan AES-256 baru)
        decrypted_package = crypto_service.decrypt(encrypted_package, key)
        
        # 3. Buka bungkusan paket untuk mendapatkan file asli + nama filenya (dari utils.py)
        original_content, original_filename = extract_package(decrypted_package)

        output_buffer = io.BytesIO(original_content)
        
        # Kirim kembali nama file asli di header, seperti yang diharapkan frontend
        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{original_filename}\""}
        )

    except ValueError as e:
        # Tangani error spesifik dari service (sesuai dokumen desain)
        logger.warning(f"Decode error: {e}")
        detail = str(e)
        if "Password salah" in detail:
            raise HTTPException(status_code=401, detail="Password salah atau data rusak.")
        if "marker tidak ada" in detail:
            raise HTTPException(status_code=404, detail="Tidak ada data tersembunyi yang ditemukan.")
        raise HTTPException(status_code=400, detail=detail)
    except Exception as e:
        logger.error(f"Internal decode error: {e}")
        raise HTTPException(status_code=500, detail="Terjadi error internal.")

@app.get("/")
def read_root():
    return {"status": "Steganography API (AES-EOF) is running."}