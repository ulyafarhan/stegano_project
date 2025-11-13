# main.py
import io
import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import crypto
from steganography.context import SteganographyService

app = FastAPI(title="Dynamic Steganography API")
stegano_service = SteganographyService()

# Konfigurasi CORS (Sesuai DDA 7.3)
origins = [
    "http://localhost:5173",
    # Ganti dengan domain Vercel/Netlify Anda di production
    # "https://aplikasi-anda.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Terjadi error internal pada server."
    )

def get_file_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

@app.post("/encode")
async def http_encode(
    key: int = Form(...),
    payload_file: UploadFile = File(...),
    host_file: UploadFile = File(...)
):
    try:
        payload_data = await payload_file.read()
        host_data = await host_file.read()
        host_ext = get_file_ext(host_file.filename)
        
        encrypted_payload = crypto.encrypt(payload_data, key)
        
        host_buffer = io.BytesIO(host_data)
        
        output_buffer = stegano_service.encode(host_buffer, encrypted_payload, host_ext)
        
        output_filename = f"encoded_{host_file.filename}"
        
        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )

    except (ValueError, NotImplementedError) as e:
        logger.warning(f"Encode failed (400): {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Encode failed (500): {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")

@app.post("/decode")
async def http_decode(
    key: int = Form(...),
    host_file: UploadFile = File(...)
):
    try:
        host_data = await host_file.read()
        host_ext = get_file_ext(host_file.filename)
        
        host_buffer = io.BytesIO(host_data)
        
        extracted_payload = stegano_service.decode(host_buffer, host_ext)
        
        decrypted_payload = crypto.decrypt(extracted_payload, key)
        
        output_buffer = io.BytesIO(decrypted_payload)
        
        # Sesuai DDA, kita tidak tahu nama file asli di starter-kit ini
        output_filename = f"rahasia.dat" 
        
        return StreamingResponse(
            output_buffer,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=\"{output_filename}\""}
        )

    except (ValueError, NotImplementedError) as e:
        logger.warning(f"Decode failed (400): {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Decode failed (500): {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "Steganography API is running."}