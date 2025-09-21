# CUDA-Accelerated Healthcare Blockchain Prototype

## Overview

This project is an interactive Streamlit-based demonstration platform that showcases GPU-accelerated blockchain concepts specifically designed for secure healthcare data management. The application simulates and compares the performance benefits of CUDA acceleration for various blockchain operations including mining, encryption, and data integrity verification through Merkle trees. It demonstrates how GPU acceleration can significantly improve throughput for cryptographic operations in healthcare blockchain systems while maintaining HIPAA/GDPR compliance standards.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Streamlit Web Interface**: Single-page application with sidebar navigation providing an interactive dashboard for demonstrating blockchain concepts
- **Multi-page Structure**: Organized into distinct sections (Overview, Performance Comparison, Blockchain Mining, Merkle Tree Demo, Encryption Simulation, Compliance Demo)
- **Real-time Visualization**: Uses Plotly for interactive charts and graphs to display performance metrics and comparisons

### Core Simulation Components
- **Blockchain Simulator**: Implements a simplified blockchain with configurable mining difficulty and hash calculation using SHA-256
- **Performance Metrics System**: Simulates CPU vs GPU performance characteristics based on research benchmarks, providing realistic throughput comparisons
- **Encryption Simulator**: Demonstrates AES encryption performance differences between CPU and GPU processing with configurable record sizes and counts
- **Merkle Tree Implementation**: Custom implementation for healthcare data integrity verification with proof generation and validation capabilities

### Healthcare-Specific Features
- **Compliance Simulator**: Implements HIPAA/GDPR compliance checks with role-based access control matrix and comprehensive audit trails
- **Healthcare Data Models**: Specialized data structures for medical records, patient information, and healthcare transactions
- **Privacy-Preserving Design**: Simulates on-chain hash storage with off-chain data references (IPFS-style) to maintain data privacy

### Performance Simulation Model
- **Benchmarking System**: Realistic performance modeling based on academic research showing 5x-40x GPU acceleration for AES encryption and 50x-500x for mining operations
- **Scalability Testing**: Configurable parameters for testing various data volumes and processing requirements
- **Comparative Analysis**: Side-by-side CPU vs GPU performance visualization with throughput and latency metrics

### Data Management Architecture
- **In-Memory Storage**: All data stored in Python data structures for demonstration purposes
- **Sample Data Generation**: Automated generation of realistic healthcare records and blockchain transactions
- **State Management**: Streamlit session state for maintaining application state across page navigation

## External Dependencies

### Core Framework Dependencies
- **Streamlit**: Web application framework for the interactive dashboard interface
- **Plotly**: Visualization library for interactive charts, graphs, and performance metrics display
- **Pandas & NumPy**: Data manipulation and numerical computing for processing simulation results

### Cryptographic Libraries
- **hashlib**: SHA-256 hashing for blockchain operations and data integrity verification
- **cryptography**: AES encryption simulation and cryptographic operations for healthcare data security

### Utility Libraries
- **datetime**: Timestamp management for blockchain blocks and audit trail entries
- **json**: Data serialization for blockchain data structures and healthcare records
- **uuid**: Unique identifier generation for patient records and system entities
- **random**: Performance variation simulation and sample data generation

### Visualization Components
- **plotly.graph_objects & plotly.express**: Interactive plotting capabilities for performance comparison charts and system metrics visualization

Note: This is a demonstration system that simulates GPU acceleration benefits without actual CUDA implementation. In a production environment, this would integrate with actual CUDA libraries and GPU hardware for real acceleration benefits.
