# WDP: Wanderer Data Preservation Protocol (PoC)

> **Status:** Experimental / Proof of Concept  
> **Version:** 0.1.0-alpha  
> **License:** MIT  
> **Spec Reference:** Engineering Specification v1.1

(assets/demo.gif)

## ⚠️ The Problem
In modern distributed systems, static data is vulnerable. If data resides on a specific server (even in decentralized networks like IPFS), that node becomes a target for censorship, seizure, or physical failure. Static storage = Single Point of Failure.

## 🛡️ The Solution: WDP
**Wanderer Data Preservation (WDP)** is a protocol where data is never static. It exists as a "traveling wave" across the network topology. 

Unlike traditional storage, WDP data **must** move to survive.
* **Migration:** Data autonomously moves from node to node based on TTL, latency, or threat detection.
* **Integrity:** Every state transition is cryptographically signed (**Ed25519**) and hashed (**SHA-256**).
* **Resilience:** The protocol mimics biological survival strategies to evade network partitions and node seizures.

### Architecture Flow
```mermaid
graph TD
    %% Этап 1: Исходное состояние
    subgraph Step1_Origin
        A[Node A: CARRIER] -- "1. Trigger (Timer or Threat)" --> A
    end

    %% Этап 2: Передача
    A -- "2. Send State (Payload + Signature)" --> Packet(Encrypted Data)
    Packet --> B[Node B: CANDIDATE]

    %% Этап 3: Проверка
    subgraph Step2_Verification
        B -- "3. Verify Ed25519 Sig" --> Check{Valid?}
        Check -- No --> Reject[Reject & Drop]
        Check -- Yes --> B_Store[Store Data]
    end

    %% Этап 4: Финал
    B_Store -. "4. Send ACK" .-> A
    A -- "5. SECURE WIPE" --> Empty[Node A: EMPTY]
    B_Store --> NewCarrier[Node B: NEW CARRIER]
```

## ⚙️ Protocol Workflow
While the "Swarm" handles topology, the individual node migration follows a strict atomic sequence to prevent data loss or duplication.

```mermaid
sequenceDiagram
    autonumber
    participant A as Node A (Holder)
    participant B as Node B (Receiver)

    Note over A: Has Data (v1.0)

    A->>B: 1. HANDSHAKE_INIT
    B-->>A: 2. READY + PubKey

    Note right of A: Sign(Payload)
    A->>B: 3. TRANSMIT_STATE [Data + Sig]

    Note over B: Verify(Hash + Sig)
    
    alt Integrity OK
        B->>B: Write to Memory
        B-->>A: 4. ACK_COMMIT
        
        Note left of A: Wipe Data
        Note over A: Node A is Empty
        Note over B: Node B is Carrier
    else Integrity FAIL
        B-->>A: ERROR_CORRUPT
        Note over A: Find new Peer
    end
```

## 📂 Repository Structure
This repository contains a Python implementation of the core WDP specifications.

| File | Description |
| :--- | :--- |
| `wdp_core.py` | Defines the `State` object, immutable ledger rules, and crypto-primitives (hashing/signing). |
| `wdp_migration.py` | Implements the node-to-node atomic transfer protocol (Migration Logic). |
| `wdp_swarm.py` | A stress-test simulation of a 20-node network under active attack (random node termination). |

## 🚀 Quick Start

### 1. Prerequisites
You need Python 3.8+ and the cryptography library.

```bash
pip install cryptography
```

### 2. Running the Simulation
Watch the protocol survive in a hostile environment (The Swarm). 
This script simulates a network where nodes are randomly "seized" or disconnected while data attempts to migrate.

```bash
python wdp_swarm.py
```

## 🧪 Simulation Results
In local stress tests with N=20 nodes and random failure injection (P=0.3), the protocol demonstrated:
* **100% Data Availability:** The payload successfully migrated through 50+ hops.
* **Zero-Copy Persistence:** No node held the data for longer than the defined epoch.
* **Tamper Resistance:** Any modified payload was immediately rejected by the swarm.

## 🗺️ Roadmap
This is a Proof-of-Concept. The roadmap for v1.0 includes:

- [x] Core Cryptography & State Definition (Python)
- [x] Basic Atomic Migration Logic
- [x] Swarm Survival Simulation
- [ ] Network Transport Layer (TCP/UDP/WebSocket) implementation
- [ ] DHT Integration (Kademlia) for peer discovery
- [ ] **Rust Port** for production performance and memory safety

---
*Authored by VECTOR (dododbobovo).*



