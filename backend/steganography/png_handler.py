from .interface import SteganographyStrategy
import io
from PIL import Image
from utils import pack_payload, unpack_payload, PAYLOAD_HEADER_SIZE

class PNGHandler(SteganographyStrategy):
    
    def get_max_capacity(self, img: Image.Image) -> int:
        width, height = img.size
        return (width * height * 3) // 8

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        host_file.seek(0)
        try:
            with Image.open(host_file) as img:
                img = img.convert('RGB')
                max_bytes = self.get_max_capacity(img)
                total_required = payload_size + PAYLOAD_HEADER_SIZE
                return total_required <= max_bytes
        except Exception:
            return False

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        img = Image.open(host_file).convert('RGB')
        
        packed_payload = pack_payload(payload)
        data_to_embed = ''.join(f'{byte:08b}' for byte in packed_payload)
        data_len = len(data_to_embed)
        
        pixels = img.load()
        data_index = 0
        
        for y in range(img.height):
            for x in range(img.width):
                if data_index < data_len:
                    r, g, b = pixels[x, y]
                    
                    new_r = (r & ~1) | int(data_to_embed[data_index])
                    data_index += 1
                    if data_index >= data_len:
                        pixels[x, y] = (new_r, g, b)
                        break
                        
                    new_g = (g & ~1) | int(data_to_embed[data_index])
                    data_index += 1
                    if data_index >= data_len:
                        pixels[x, y] = (new_r, new_g, b)
                        break
                        
                    new_b = (b & ~1) | int(data_to_embed[data_index])
                    data_index += 1
                    
                    pixels[x, y] = (new_r, new_g, new_b)
                else:
                    break
            if data_index >= data_len:
                break
                
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        img = Image.open(host_file).convert('RGB')
        pixels = img.load()
        
        binary_data = ""
        header_bits_needed = PAYLOAD_HEADER_SIZE * 8
        payload_size = 0
        bits_read = 0
        
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                
                binary_data += str(r & 1)
                bits_read += 1
                if bits_read == header_bits_needed:
                    header_bytes = int(binary_data, 2).to_bytes(PAYLOAD_HEADER_SIZE, 'big')
                    payload_size = int.from_bytes(header_bytes, 'big')
                elif bits_read > header_bits_needed:
                    if len(binary_data) == header_bits_needed + (payload_size * 8):
                        break
                
                binary_data += str(g & 1)
                bits_read += 1
                if bits_read > header_bits_needed:
                    if len(binary_data) == header_bits_needed + (payload_size * 8):
                        break

                binary_data += str(b & 1)
                bits_read += 1
                if bits_read > header_bits_needed:
                    if len(binary_data) == header_bits_needed + (payload_size * 8):
                        break
            
            if payload_size > 0 and len(binary_data) == header_bits_needed + (payload_size * 8):
                break
        
        if payload_size == 0 or len(binary_data) < header_bits_needed + (payload_size * 8):
            raise ValueError("Tidak ada data ditemukan atau data korup.")
            
        payload_binary = binary_data[header_bits_needed:]
        payload_bytes = int(payload_binary, 2).to_bytes(payload_size, 'big')
        
        return payload_bytes