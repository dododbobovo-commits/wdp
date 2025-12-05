import time
import random
from cryptography.hazmat.primitives.asymmetric import ed25519
from wdp_core import WDPState

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        self.storage = None # Тут будет лежать State, если узел - Carrier
        print(f"[INIT] Node {self.node_id} online.")

    def create_genesis_state(self, data: bytes):
        """Создает первое состояние (Роль: Первый Carrier)"""
        print(f"[*] Node {self.node_id} generating Genesis State...")
        self.storage = WDPState(payload=data, version=1)
        self.storage.sign(self.private_key)
        print(f"[+] State v1 created by {self.node_id}")

    def migrate_to(self, target_node):
        """Логика миграции (Section 3: Migration Algorithm)"""
        if not self.storage:
            print(f"[ERROR] Node {self.node_id} has nothing to send!")
            return False

        print(f"\n>>> MIGRATION START: {self.node_id} -> {target_node.node_id}")
        
        # 1. Симуляция сетевой передачи (сериализация)
        packet = self.storage
        
        # 2. Получатель принимает и проверяет
        success = target_node.receive_migration(packet)
        
        if success:
            print(f"<<< MIGRATION SUCCESS. {self.node_id} wipes local copy.")
            self.storage = None # Данные ушли, мы больше не Carrier
            return True
        else:
            print(f"[!] Migration Failed.")
            return False

    def receive_migration(self, incoming_state: WDPState):
        """Прием данных новым носителем"""
        print(f"[*] Node {self.node_id} receiving state...")
        
        # 3. Проверка подписи (Integrity Check)
        if incoming_state.verify():
            print(f"[OK] Signature Valid. Integrity verified.")
            
            # 4. Обновление версии (Section 3, step 6)
            # В реальной сети мы бы увеличили версию и переподписали
            incoming_state.version += 1
            incoming_state.sign(self.private_key) # Теперь МЫ подписываем состояние своим ключом
            
            self.storage = incoming_state
            print(f"[+] Node {self.node_id} is now the CARRIER. State Version: {self.storage.version}")
            return True
        else:
            print(f"[FATAL] Integrity Check FAILED! Data corrupted.")
            return False

# --- ЗАПУСК СИМУЛЯЦИИ ---
if __name__ == "__main__":
    print("--- WDP MIGRATION PROTOCOL TEST (v1.0) ---")
    
    # 1. Поднимаем узлы
    node_alpha = Node("ALPHA")
    node_beta = Node("BETA")

    # 2. Alpha создает данные
    node_alpha.create_genesis_state(b"CONFIDENTIAL_GRANT_PROPOSAL_DATA")
    
    # 3. Миграция: Alpha -> Beta
    time.sleep(1)
    node_alpha.migrate_to(node_beta)

    # 4. Проверка: где данные?
    print("\n--- STATUS CHECK ---")
    print(f"Alpha has data: {node_alpha.storage is not None}")
    print(f"Beta has data:  {node_beta.storage is not None}")
    
    # 5. Попытка обратной миграции (Ping-Pong)
    if node_beta.storage:
        time.sleep(1)

        node_beta.migrate_to(node_alpha)
