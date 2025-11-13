# steganography/interface.py
from abc import ABC, abstractmethod
import io

class SteganographyStrategy(ABC):
    
    @abstractmethod
    def check_capacity(self, host_file: io.BytesIO, payload_size: int) -> bool:
        pass
    
    @abstractmethod
    def encode(self, host_file: io.BytesIO, payload: bytes) -> io.BytesIO:
        pass

    @abstractmethod
    def decode(self, host_file: io.BytesIO) -> bytes:
        pass