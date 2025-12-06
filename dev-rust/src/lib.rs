// src/lib.rs

//! # WDP Core Library
//! 
//! Implementation of the Wanderer Data Preservation protocol.
//! Focuses on "Moving Target Defense" for data storage.

use serde::{Serialize, Deserialize};
use ed25519_dalek::{Signer, SigningKey};

/// Represents the migrating data packet
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct WandererState {
    pub payload_hash: String,
    pub current_epoch: u64,
    pub carrier_signature: String,
}

/// Core protocol traits
pub trait MigrationProtocol {
    fn verify_integrity(&self) -> bool;
    fn initiate_migration(&self, target_node: &str) -> Result<bool, String>;
}

// TODO: Port logic from wdp_core.py
// TODO: Implement libp2p transport layer