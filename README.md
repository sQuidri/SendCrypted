# SendCrypted

## Description
A secure file sending app utilizing the concepts of the RMIT Class, Introduction to Cyber Security (INTE2625) 

## Authors
**Sadiq Quadri** (s4100453)  
**Chirag Wadehra** (s4014390)

## Goal
The primary goal is to implement a graphical application that can connect to another instance of itself over a TCP network and securely transmit files using:

- **AES encryption** for encrypting file contents before transfer.
- **RSA-based key exchange** to securely share the AES encryption key.
- **SHA-256 hashing** to verify file integrity after transmission.

## Milestones

| Milestone | Description |
|----------|-------------|
| ✅ **M0: GUI Setup** | Build a basic graphical user interface with options to select mode (Client/Server), enter IP/port, and pick files. No backend functionality yet—just the frontend layout. |
| **M1: Local File Transfer** | Establish basic TCP socket connection between client and server. Enable sending and receiving of raw files over the same local network. |
| **M2: AES Encryption** | Encrypt files using AES-256 before transmission and decrypt them upon reception. |
| **M3: RSA Key Exchange** | Securely exchange the AES encryption key using RSA public-key cryptography. |
| **M4: File Integrity Verification** | Generate and compare SHA-256 hashes before and after transfer to verify file integrity. |
| **M5: Cloud-Based Cross-Network Support** | Implement Cross-Network Support by using a Cloud-Hosted VM as a relay. |
