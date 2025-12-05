import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class WDPState:
    def __init__(self, payload: bytes, version: int = 1):
        """
        Инициализация состояния согласно Spec v1.1 Section 4.2.
        """
        self.payload = payload
        self.version = version
        self.signature = None
        self.signer_public_key = None # Кто подписал это состояние

    def calculate_hash(self) -> bytes:
        """
        Section 8.2: Hash Integrity.
        hash = H(payload || version)[cite: 449].
        """
        # Объединяем версию и данные для хеширования
        data_to_hash = self.version.to_bytes(8, 'big') + self.payload
        return hashlib.sha256(data_to_hash).digest()

    def sign(self, private_key):
        """
        Section 8.3: Signatures.
        Подписываем хеш состояния приватным ключом[cite: 451].
        """
        data_hash = self.calculate_hash()
        self.signature = private_key.sign(data_hash)
        
        # Сохраняем публичный ключ для проверки (в реальной сети он будет в DHT)
        self.signer_public_key = private_key.public_key()
        return self.signature

    def verify(self) -> bool:
        """
        Проверка целостности и подписи репликой[cite: 386].
        """
        if not self.signature or not self.signer_public_key:
            return False
            
        data_hash = self.calculate_hash()
        try:
            self.signer_public_key.verify(self.signature, data_hash)
            return True
        except Exception:
            return False

    def serialize(self) -> dict:
        """
        Простая сериализация для передачи по сети.
        """
        return {
            "ver": self.version,
            "pl": self.payload.hex(),
            "sig": self.signature.hex() if self.signature else None
        }

# --- ТЕСТОВЫЙ ЗАПУСК (СИМУЛЯЦИЯ) ---
if __name__ == "__main__":
    print("--- WDP CORE SYSTEM TEST ---")
    
    # 1. Генерируем ключи "Носителя" (Carrier)
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    print("[+] Keys generated.")

    # 2. Создаем "блуждающие данные"
    secret_data = b"DATA_RESISTANT_TO_CENSORSHIP_v1"
    state = WDPState(payload=secret_data, version=1)
    print(f"[+] State created. Version: {state.version}")

    # 3. Подписываем (как Carrier)
    sig = state.sign(private_key)
    print(f"[+] Signed. Signature sample: {sig.hex()[:10]}...")

    # 4. Проверка (как Replica)
    is_valid = state.verify()
    print(f"[?] Integrity Check: {'PASS' if is_valid else 'FAIL'}")

    # 5. Попытка взлома (изменяем данные в полете)
    print("\n[!] Attempting malicious data modification...")
    state.payload = b"CENSORED_DATA"
    is_valid_after_hack = state.verify()
    print(f"[?] Integrity Check after hack: {'PASS' if is_valid_after_hack else 'FAIL'}")