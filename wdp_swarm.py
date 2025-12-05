import time
import random
import os
from wdp_migration import Node

# Цвета для красивого вывода в консоль
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class SwarmNetwork:
    def __init__(self, node_count=20):
        self.nodes = []
        self.dead_nodes = []
        
        print(f"[{YELLOW}SYSTEM{RESET}] Initializing Swarm Network with {node_count} nodes...")
        for i in range(node_count):
            self.nodes.append(Node(f"NODE_{i:02d}"))
            
    def start_simulation(self):
        # 1. Выбираем случайную жертву для старта (Первый Носитель)
        first_carrier = random.choice(self.nodes)
        first_carrier.create_genesis_state(b"CRITICAL_CENSORSHIP_RESISTANT_DATA")
        
        current_carrier = first_carrier
        step = 1

        try:
            while len(self.nodes) > 1:
                os.system('cls' if os.name == 'nt' else 'clear') # Очистка экрана для динамики
                print(f"\n=== WDP SWARM SIMULATION | STEP {step} ===")
                print(f"Alive Nodes: {len(self.nodes)} | Dead Nodes: {len(self.dead_nodes)}")
                print(f"Current Carrier: {GREEN}{current_carrier.node_id}{RESET} (Version: {current_carrier.storage.version})")
                print("-" * 40)

                # 2. Выбор следующей цели (Случайный живой узел, кроме себя)
                candidates = [n for n in self.nodes if n != current_carrier]
                if not candidates:
                    print(f"{RED}[FATAL] No nodes left to migrate to!{RESET}")
                    break
                
                target = random.choice(candidates)
                
                # 3. МИГРАЦИЯ
                success = current_carrier.migrate_to(target)
                
                if success:
                    print(f"{GREEN}>>> JUMP SUCCESSFUL{RESET}")
                    # Старый носитель пуст, новый стал текущим
                    current_carrier = target
                else:
                    print(f"{RED}>>> JUMP FAILED{RESET}")
                    break

                # 4. ХАОС (Случайная смерть узла)
                # С вероятностью 30% убиваем случайный узел (но не носителя, пока что)
                if random.random() < 0.3:
                    victim = random.choice([n for n in self.nodes if n != current_carrier])
                    self.kill_node(victim)

                step += 1
                time.sleep(0.8) # Скорость анимации

        except KeyboardInterrupt:
            print("\n[!] Simulation stopped by user.")

    def kill_node(self, node):
        print(f"\n{RED}[KILL] GOVERNMENT AGENTS SEIZED {node.node_id}!{RESET}")
        self.nodes.remove(node)
        self.dead_nodes.append(node)

if __name__ == "__main__":
    sim = SwarmNetwork(node_count=20)

    sim.start_simulation()
