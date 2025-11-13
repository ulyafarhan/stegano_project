from .interface import SteganographyStrategy
import io
import wave
from utils import pack_payload, unpack_payload, PAYLOAD_HEADER_SIZE

class WAVHandler(SteganographyStrategy):

    def get_max_capacity(self, wav_file: wave.Wave_read) -> int:
        n_frames = wav_file.getnframes()
        sampwidth = wav_file.getsampwidth()
        return (n_frames * sampwidth) // 8

    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        host_file.seek(0)
        try:
            with wave.open(host_file, 'rb') as wh:
                max_bytes = self.get_max_capacity(wh)
                total_required = payload_size + PAYLOAD_HEADER_SIZE
                return total_required <= max_bytes
        except wave.Error:
            return False

    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        host_file.seek(0)
        packed_payload = pack_payload(payload)
        data_to_embed = ''.join(f'{byte:08b}' for byte in packed_payload)
        data_len = len(data_to_embed)
        
        with wave.open(host_file, 'rb') as wh:
            params = wh.getparams()
            frames = bytearray(wh.readframes(wh.getnframes()))

        data_index = 0
        for i in range(len(frames)):
            if data_index < data_len:
                frame_byte = frames[i]
                new_byte = (frame_byte & ~1) | int(data_to_embed[data_index])
                frames[i] = new_byte
                data_index += 1
            else:
                break
        
        output_buffer = io.BytesIO()
        with wave.open(output_buffer, 'wb') as wh_out:
            wh_out.setparams(params)
            wh_out.writeframes(frames)
            
        output_buffer.seek(0)
        return output_buffer

    def decode(self, host_file: io.BytesIO) -> bytes:
        host_file.seek(0)
        with wave.open(host_file, 'rb') as wh:
            frames = wh.readframes(wh.getnframes())
            
        binary_data = ""
        header_bits_needed = PAYLOAD_HEADER_SIZE * 8
        payload_size = 0
        bits_read = 0

        for byte in frames:
            binary_data += str(byte & 1)
            bits_read += 1
            
            if bits_read == header_bits_needed:
                header_bytes = int(binary_data, 2).to_bytes(PAYLOAD_HEADER_SIZE, 'big')
                payload_size = int.from_bytes(header_bytes, 'big')
                if payload_size == 0:
                    raise ValueError("Ukuran payload 0, data tidak valid.")
            elif bits_read > header_bits_needed:
                if len(binary_data) == header_bits_needed + (payload_size * 8):
                    break
        
        if payload_size == 0 or len(binary_data) < header_bits_needed + (payload_size * 8):
            raise ValueError("Tidak ada data ditemukan atau data korup.")
            
        payload_binary = binary_data[header_bits_needed:]
        payload_bytes = int(payload_binary, 2).to_bytes(payload_size, 'big')
        
        return payload_bytes