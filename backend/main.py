import io
import logging
import tempfile
import shutil
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Impor layanan
import crypto_service 
import steganography_service
from utils import create_package, extract_package

app = FastAPI(title="PrivaSel API (AES-EOF) - Streaming Enabled")

# --- Konfigurasi CORS (Sama seperti sebelumnya) ---
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


# --- FUNGSI UNTUK MEMBERSIHKAN FILE SEMENTARA ---
def cleanup_temp_file(path: str):
    """Fungsi aman untuk menghapus file sementara setelah dikirim."""
    try:
        os.remove(path)
        logger.info(f"File sementara {path} telah dihapus.")
    except Exception as e:
        logger.error(f"Gagal menghapus file sementara {path}: {e}")


@app.post("/encode")
async def http_encode(
    background_tasks: BackgroundTasks,
    key: str = Form(...),
    payload_file: UploadFile = File(...),
    host_file: UploadFile = File(...)
):
    temp_host_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_host_file:
            shutil.copyfileobj(host_file.file, temp_host_file)
            temp_host_path = temp_host_file.name
        
        payload_data = await payload_file.read()
        packaged_data = create_package(payload_data, payload_file.filename)
        encrypted_package = crypto_service.encrypt(packaged_data, key)
        steganography_service.encode(temp_host_path, encrypted_package)
        
        # <-- PERUBAHAN DI SINI: Membersihkan nama file untuk header -->
        # Mengganti karakter non-ASCII dengan '?' agar aman untuk header HTTP
        safe_filename = host_file.filename.encode('ascii', 'replace').decode('ascii')
        output_filename = f"encoded_{safe_filename}"
        # <-- AKHIR PERUBAHAN -->

        response = FileResponse(
            path=temp_host_path,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )
        
        background_tasks.add_task(cleanup_temp_file, temp_host_path)
        
        return response

    except Exception as e:
        # Tangkap error asli dan log
        logger.error(f"Encode error: {e}", exc_info=True) # exc_info=True untuk traceback
        
        # Hapus file sementara jika ada error
        if temp_host_path and os.path.exists(temp_host_path):
            cleanup_temp_file(temp_host_path)
            
        # Kirim respons HTTP yang jelas
        raise HTTPException(status_code=500, detail=f"Enkripsi gagal: {str(e)}")
    finally:
        await payload_file.close()
        await host_file.close()


@app.post("/decode")
async def http_decode(
    key: str = Form(...),
    host_file: UploadFile = File(...)
):
    temp_host_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_host_file:
            shutil.copyfileobj(host_file.file, temp_host_file)
            temp_host_path = temp_host_file.name
        
        encrypted_package = steganography_service.decode(temp_host_path)
        decrypted_package = crypto_service.decrypt(encrypted_package, key)
        original_content, original_filename = extract_package(decrypted_package)

        output_buffer = io.BytesIO(original_content)
        
        # <-- PERUBAHAN DI SINI: Membersihkan nama file untuk header -->
        # Mengganti karakter non-ASCII dengan '?' agar aman untuk header HTTP
        safe_filename = original_filename.encode('ascii', 'replace').decode('ascii')
        # <-- AKHIR PERUBAHAN -->

        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{safe_filename}\""}
        )

    except ValueError as e:
        logger.warning(f"Decode error: {e}")
        detail = str(e)
        if "Password salah" in detail:
            raise HTTPException(status_code=401, detail="Password salah atau data rusak.")
        if "marker tidak ada" in detail:
            raise HTTPException(status_code=404, detail="Tidak ada data tersembunyi yang ditemukan.")
        raise HTTPException(status_code=400, detail=detail)
    except Exception as e:
        logger.error(f"Internal decode error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Terjadi error internal.")
    finally:
        await host_file.close()
        if temp_host_path and os.path.exists(temp_host_path):
            cleanup_temp_file(temp_host_path)


@app.get("/")
def read_root():
    return {"status": "Steganography API (AES-EOF) is running."}