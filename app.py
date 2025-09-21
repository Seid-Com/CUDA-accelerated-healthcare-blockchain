import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import hashlib
import time
import json
from datetime import datetime, timedelta

from blockchain_simulator import BlockchainSimulator
from encryption_simulator import EncryptionSimulator
from compliance_simulator import ComplianceSimulator
from performance_metrics import PerformanceMetrics
from merkle_tree import HealthcareMerkleTree
from smart_contract_simulator import SmartContractManager
from quantum_resistance_analyzer import QuantumResistanceAnalyzer

def main():
    st.set_page_config(
        page_title="CUDA-Accelerated Healthcare Blockchain Prototype",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 CUDA-Accelerated Healthcare Blockchain Prototype")
    st.markdown("Interactive demonstration of GPU-accelerated blockchain concepts for secure healthcare data management")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Overview", "Performance Comparison", "Blockchain Mining", "Merkle Tree Demo", "Smart Contract Demo", "Encryption Simulation", "Compliance Demo", "Quantum Resistance Analysis"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Performance Comparison":
        show_performance_comparison()
    elif page == "Blockchain Mining":
        show_blockchain_mining()
    elif page == "Merkle Tree Demo":
        show_merkle_tree_demo()
    elif page == "Smart Contract Demo":
        show_smart_contract_demo()
    elif page == "Encryption Simulation":
        show_encryption_simulation()
    elif page == "Compliance Demo":
        show_compliance_demo()
    elif page == "Quantum Resistance Analysis":
        show_quantum_resistance_analysis()

def show_overview():
    st.header("System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Research Highlights")
        st.markdown("""
        - **5× to 100× throughput improvement** with GPU acceleration
        - **CUDA-optimized Proof-of-Work** for healthcare blockchain
        - **AES-CTR encryption** with hybrid CPU-GPU processing
        - **HIPAA/GDPR compliance** through off-chain storage
        - **Sub-second encryption** of 1.2GB medical files
        """)
        
    with col2:
        st.subheader("System Architecture")
        st.markdown("""
        1. **Healthcare Data Layer**: Medical record preprocessing
        2. **Encryption Module**: AES-CTR with GPU acceleration
        3. **Blockchain Core**: GPU-based PoW mining engine
        4. **Off-Chain Storage**: IPFS for encrypted records
        5. **Validator Pool**: PoW-based consensus mechanism
        6. **Compliance Layer**: Smart contract audit mechanisms
        """)
    
    # Performance metrics summary
    st.subheader("Key Performance Metrics")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("GPU vs CPU Speedup", "5x - 100x", "↑ 90% improvement")
    
    with metrics_col2:
        st.metric("Block Formation Time", "< 30 seconds", "↓ vs 600s Bitcoin")
    
    with metrics_col3:
        st.metric("Encryption Speed", "< 1 second", "for 1.2GB files")
    
    with metrics_col4:
        st.metric("TPS Capability", "1000+", "transactions/second")

def show_performance_comparison():
    st.header("GPU vs CPU Performance Comparison")
    
    # Initialize performance metrics
    perf_metrics = PerformanceMetrics()
    
    # File size selection
    st.subheader("Configure Test Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        file_sizes = st.multiselect(
            "Select file sizes (MB):",
            [1, 10, 50, 100, 500, 1000, 1200],
            default=[1, 100, 500, 1200]
        )
    
    with col2:
        operation = st.selectbox(
            "Select operation type:",
            ["AES-CTR Encryption", "SHA-256 Mining", "Both"]
        )
    
    if st.button("Run Performance Benchmark"):
        with st.spinner("Running benchmark simulations..."):
            results = perf_metrics.run_benchmark(file_sizes, operation)
            speedup_data = []  # Initialize speedup_data
            
            # Display results
            if operation in ["AES-CTR Encryption", "Both"]:
                st.subheader("AES-CTR Encryption Performance")
                
                # Create comparison chart
                fig_encryption = go.Figure()
                
                fig_encryption.add_trace(go.Scatter(
                    x=results['file_sizes'],
                    y=results['cpu_encryption_times'],
                    mode='lines+markers',
                    name='CPU',
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ))
                
                fig_encryption.add_trace(go.Scatter(
                    x=results['file_sizes'],
                    y=results['gpu_encryption_times'],
                    mode='lines+markers',
                    name='GPU (Simulated)',
                    line=dict(color='green', width=3),
                    marker=dict(size=8)
                ))
                
                fig_encryption.update_layout(
                    title="Encryption Time Comparison: CPU vs GPU",
                    xaxis_title="File Size (MB)",
                    yaxis_title="Encryption Time (seconds)",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_encryption, use_container_width=True)
                
                # Speedup visualization
                if results['cpu_encryption_times'] and results['gpu_encryption_times']:
                    speedup_data = [cpu/gpu for cpu, gpu in zip(results['cpu_encryption_times'], results['gpu_encryption_times'])]
                else:
                    speedup_data = []
                
                if speedup_data:
                    fig_speedup = go.Figure(data=[
                        go.Bar(
                            x=results['file_sizes'],
                            y=speedup_data,
                            text=[f"{x:.1f}x" for x in speedup_data],
                            textposition='auto',
                            marker_color='blue'
                        )
                    ])
                    
                    fig_speedup.update_layout(
                        title="GPU Speedup Factor for AES-CTR Encryption",
                        xaxis_title="File Size (MB)",
                        yaxis_title="Speedup Factor (GPU vs CPU)"
                    )
                    
                    st.plotly_chart(fig_speedup, use_container_width=True)
            
            if operation in ["SHA-256 Mining", "Both"]:
                st.subheader("SHA-256 Mining Performance")
                
                # Mining throughput comparison
                fig_mining = go.Figure()
                
                fig_mining.add_trace(go.Bar(
                    x=['CPU Mining', 'GPU Mining (Simulated)'],
                    y=[results['cpu_mining_throughput'], results['gpu_mining_throughput']],
                    text=[f"{results['cpu_mining_throughput']:.1f} MH/s", f"{results['gpu_mining_throughput']:.1f} MH/s"],
                    textposition='auto',
                    marker_color=['red', 'green']
                ))
                
                fig_mining.update_layout(
                    title="Mining Throughput Comparison",
                    yaxis_title="Hash Rate (MH/s)"
                )
                
                st.plotly_chart(fig_mining, use_container_width=True)
                
                # Performance summary table
                st.subheader("Performance Summary")
                # Build summary data conditionally
                summary_metrics = []
                cpu_values = []
                gpu_values = []
                
                # Add encryption speedup only if we have encryption data
                if operation in ["AES-CTR Encryption", "Both"] and speedup_data:
                    summary_metrics.append('Average Encryption Speedup')
                    cpu_values.append('-')
                    gpu_values.append(f"{np.mean(speedup_data):.1f}x faster")
                
                # Always add mining metrics for mining operations
                summary_metrics.extend(['Mining Throughput Improvement', 'Block Formation Time'])
                cpu_values.extend([f"{results['cpu_mining_throughput']:.1f} MH/s", '~600 seconds (Bitcoin-like)'])
                gpu_values.extend([f"{results['gpu_mining_throughput']:.1f} MH/s", '<30 seconds'])
                
                summary_data = {
                    'Metric': summary_metrics,
                    'CPU': cpu_values,
                    'GPU': gpu_values
                }
                
                st.table(pd.DataFrame(summary_data))

def show_blockchain_mining():
    st.header("Blockchain Mining Simulation")
    
    # Initialize blockchain simulator
    blockchain = BlockchainSimulator()
    
    # Mining configuration
    st.subheader("Mining Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulty = st.slider("Mining Difficulty", 1, 6, 3, help="Number of leading zeros required in hash")
    
    with col2:
        block_size = st.slider("Block Size (KB)", 1, 100, 10, help="Size of healthcare data in each block")
    
    with col3:
        num_blocks = st.slider("Number of Blocks to Mine", 1, 10, 3)
    
    # Mining mode selection
    mining_mode = st.radio("Mining Mode:", ["CPU Simulation", "GPU Simulation", "Comparison"])
    
    if st.button("Start Mining Simulation"):
        with st.spinner("Mining blocks..."):
            if mining_mode == "Comparison":
                # Run both CPU and GPU simulations
                cpu_results = blockchain.mine_blocks(num_blocks, difficulty, block_size, "CPU")
                gpu_results = blockchain.mine_blocks(num_blocks, difficulty, block_size, "GPU")
                
                # Display comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("CPU Mining Results")
                    st.write(f"Total Time: {cpu_results['total_time']:.2f} seconds")
                    st.write(f"Average Block Time: {cpu_results['avg_block_time']:.2f} seconds")
                    st.write(f"Total Hash Attempts: {cpu_results['total_hashes']:,}")
                
                with col2:
                    st.subheader("GPU Mining Results")
                    st.write(f"Total Time: {gpu_results['total_time']:.2f} seconds")
                    st.write(f"Average Block Time: {gpu_results['avg_block_time']:.2f} seconds")
                    st.write(f"Total Hash Attempts: {gpu_results['total_hashes']:,}")
                
                # Visualization
                comparison_data = {
                    'Mining Mode': ['CPU', 'GPU'],
                    'Total Time (s)': [cpu_results['total_time'], gpu_results['total_time']],
                    'Avg Block Time (s)': [cpu_results['avg_block_time'], gpu_results['avg_block_time']],
                    'Hash Rate (H/s)': [cpu_results['hash_rate'], gpu_results['hash_rate']]
                }
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=comparison_data['Mining Mode'],
                    y=comparison_data['Avg Block Time (s)'],
                    name='Avg Block Time',
                    marker_color=['red', 'green']
                ))
                
                fig.update_layout(
                    title="Block Mining Time Comparison",
                    yaxis_title="Average Block Time (seconds)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show blockchain state
                st.subheader("Blockchain State")
                blockchain_data = []
                for i, block in enumerate(blockchain.chain[-num_blocks:]):
                    blockchain_data.append({
                        'Block #': i + 1,
                        'Hash': block['hash'][:16] + '...',
                        'Previous Hash': block['previous_hash'][:16] + '...' if block['previous_hash'] else 'Genesis',
                        'Timestamp': block['timestamp'],
                        'Nonce': block['nonce'],
                        'Data Size (KB)': block_size
                    })
                
                st.dataframe(pd.DataFrame(blockchain_data), use_container_width=True)
                
            else:
                # Single mode mining
                results = blockchain.mine_blocks(num_blocks, difficulty, block_size, mining_mode.split()[0])
                
                st.success(f"Successfully mined {num_blocks} blocks!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Mining Time", f"{results['total_time']:.2f}s")
                with col2:
                    st.metric("Average Block Time", f"{results['avg_block_time']:.2f}s")
                with col3:
                    st.metric("Hash Rate", f"{results['hash_rate']:.0f} H/s")
                
                # Block timeline
                block_times = results['block_times']
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(1, len(block_times) + 1)),
                    y=block_times,
                    mode='lines+markers',
                    name='Block Mining Time',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="Block Mining Time Progression",
                    xaxis_title="Block Number",
                    yaxis_title="Mining Time (seconds)"
                )
                
                st.plotly_chart(fig, use_container_width=True)

def show_merkle_tree_demo():
    st.header("Merkle Tree Data Integrity Demo")
    
    st.subheader("What are Merkle Trees?")
    st.markdown("""
    Merkle trees provide efficient and secure verification of large data structures. In our healthcare blockchain:
    - Each block contains a Merkle tree of all transactions
    - The Merkle root in the block header ensures data integrity
    - Individual records can be verified without downloading the entire block
    - Any tampering with data is immediately detectable
    """)
    
    # Sample healthcare data for demonstration
    sample_records = [
        {
            'patient_id': 'PATIENT_001',
            'record_type': 'lab_result',
            'test': 'Blood Sugar',
            'value': '95 mg/dL',
            'timestamp': '2025-09-21T10:00:00'
        },
        {
            'patient_id': 'PATIENT_002', 
            'record_type': 'prescription',
            'medication': 'Metformin 500mg',
            'dosage': 'Twice daily',
            'timestamp': '2025-09-21T10:15:00'
        },
        {
            'patient_id': 'PATIENT_003',
            'record_type': 'vital_signs',
            'blood_pressure': '120/80',
            'heart_rate': '72 bpm',
            'timestamp': '2025-09-21T10:30:00'
        }
    ]
    
    # Demo tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Tree Construction", "Integrity Verification", "Merkle Proofs", "Blockchain Integration"])
    
    with tab1:
        st.subheader("Build Merkle Tree from Healthcare Records")
        
        num_records = st.slider("Number of records to include:", 1, len(sample_records), 3)
        selected_records = sample_records[:num_records]
        
        if st.button("Build Merkle Tree"):
            # Create Merkle tree
            merkle_tree = HealthcareMerkleTree(selected_records)
            
            # Display tree statistics
            stats = merkle_tree.get_healthcare_statistics()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Nodes", stats['total_nodes'])
            with col2:
                st.metric("Leaf Nodes", stats['leaf_nodes'])
            with col3:
                st.metric("Tree Height", stats['tree_height'])
            
            # Show root hash
            st.write("**Merkle Root Hash:**")
            st.code(merkle_tree.get_root_hash())
            
            # Display tree structure
            st.subheader("Tree Structure")
            tree_viz = merkle_tree.get_tree_visualization()
            st.json(tree_viz)
            
            # Show records
            st.subheader("Healthcare Records")
            for i, record in enumerate(selected_records):
                with st.expander(f"Record {i+1}: {record['record_type'].title()}"):
                    st.json(record)
    
    with tab2:
        st.subheader("Data Integrity Verification")
        st.markdown("Demonstrate how any tampering with data is immediately detected.")
        
        # Create original tree
        original_tree = HealthcareMerkleTree(sample_records)
        original_root = original_tree.get_root_hash()
        
        st.write("**Original Merkle Root:**")
        st.code(original_root)
        
        # Allow user to modify a record
        st.write("**Simulate Data Tampering:**")
        tampered_records = sample_records.copy()
        
        record_to_modify = st.selectbox("Select record to modify:", range(len(sample_records)))
        field_to_modify = st.selectbox("Select field to modify:", list(sample_records[record_to_modify].keys()))
        new_value = st.text_input("New value:", sample_records[record_to_modify][field_to_modify])
        
        if st.button("Apply Modification"):
            # Modify the record
            tampered_records[record_to_modify][field_to_modify] = new_value
            
            # Create new tree with tampered data
            tampered_tree = HealthcareMerkleTree(tampered_records)
            tampered_root = tampered_tree.get_root_hash()
            
            st.write("**Tampered Merkle Root:**")
            st.code(tampered_root)
            
            # Compare roots
            if original_root == tampered_root:
                st.success("✅ Merkle roots match - Data integrity verified")
            else:
                st.error("❌ Merkle roots do not match - Data tampering detected!")
                
                st.write("**Comparison:**")
                comparison_df = pd.DataFrame({
                    'Version': ['Original', 'Tampered'],
                    'Merkle Root': [original_root, tampered_root],
                    'Match': ['✅ Valid', '❌ Invalid']
                })
                st.table(comparison_df)
    
    with tab3:
        st.subheader("Merkle Proof Generation & Verification")
        st.markdown("Generate cryptographic proofs that a record exists in the tree without revealing other data.")
        
        # Create tree for proof demo
        proof_tree = HealthcareMerkleTree(sample_records)
        
        # Select record for proof
        record_index = st.selectbox("Select record to prove:", range(len(sample_records)))
        selected_record = sample_records[record_index]
        
        if st.button("Generate Merkle Proof"):
            # Generate proof
            proof = proof_tree.generate_proof(json.dumps(selected_record, sort_keys=True))
            
            st.write("**Selected Record:**")
            st.json(selected_record)
            
            st.write("**Merkle Proof:**")
            if proof:
                for i, step in enumerate(proof):
                    st.write(f"Step {i+1}: {step['position']} sibling - `{step['hash'][:16]}...`")
            else:
                st.write("No proof needed (single record tree)")
            
            # Verify proof
            is_valid = proof_tree.verify_proof(
                json.dumps(selected_record, sort_keys=True),
                proof,
                proof_tree.get_root_hash()
            )
            
            if is_valid:
                st.success("✅ Proof verification successful - Record authenticity confirmed")
            else:
                st.error("❌ Proof verification failed")
            
            # Show proof details
            st.write("**Proof Details:**")
            proof_details = {
                'Record Hash': hashlib.sha256(json.dumps(selected_record, sort_keys=True).encode()).hexdigest(),
                'Root Hash': proof_tree.get_root_hash(),
                'Proof Steps': len(proof),
                'Verification': '✅ Valid' if is_valid else '❌ Invalid'
            }
            st.json(proof_details)
    
    with tab4:
        st.subheader("Blockchain Integration with Merkle Trees")
        st.markdown("See how Merkle trees are integrated into blockchain blocks for enhanced security.")
        
        # Initialize blockchain
        blockchain = BlockchainSimulator()
        
        # Mine a block with healthcare data
        if st.button("Mine Block with Merkle Tree"):
            with st.spinner("Mining block with Merkle tree integration..."):
                # Create combined healthcare data
                combined_data = json.dumps(sample_records)
                
                # Mine block (this will automatically create Merkle tree)
                result = blockchain.mine_block(combined_data, 2, "GPU")
                
                st.success("Block mined successfully with Merkle tree!")
                
                # Display block information
                block = result['block']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Block Information:**")
                    block_info = {
                        'Block Index': block['index'],
                        'Block Hash': block['hash'][:32] + '...',
                        'Merkle Root': block['merkle_root'][:32] + '...',
                        'Transaction Count': block['transaction_count'],
                        'Mining Time': f"{result['mining_time']:.2f} seconds"
                    }
                    st.json(block_info)
                
                with col2:
                    st.write("**Merkle Tree Statistics:**")
                    st.json(block['merkle_tree_stats'])
                
                # Verify Merkle integrity
                st.subheader("Merkle Tree Integrity Verification")
                verification = blockchain.verify_merkle_integrity(block['index'])
                
                if verification['valid']:
                    st.success("✅ Merkle tree integrity verified")
                    st.write("**Verification Details:**")
                    st.json({
                        'Stored Root': verification['stored_root'][:32] + '...',
                        'Computed Root': verification['computed_root'][:32] + '...',
                        'Transaction Count': verification['transaction_count']
                    })
                else:
                    st.error("❌ Merkle tree integrity check failed")
                    if 'error' in verification:
                        st.write(f"Error: {verification['error']}")

def show_smart_contract_demo():
    st.header("Smart Contract Access Control Demo")
    
    st.subheader("What are Smart Contracts?")
    st.markdown("""
    Smart contracts are self-executing contracts with terms directly written into code. In our healthcare blockchain:
    - **Automated access control** based on user roles and permissions
    - **Enforced patient consent** requirements before data access
    - **Audit trail** of all contract executions and data access
    - **Role-based permissions** for different healthcare professionals
    """)
    
    # Initialize smart contract manager in session state
    if 'contract_manager' not in st.session_state:
        st.session_state.contract_manager = SmartContractManager()
        # Deploy the healthcare access contract
        st.session_state.contract_id = st.session_state.contract_manager.deploy_contract(
            "HealthcareAccess", 
            "ADMIN_001"
        )
    
    contract_manager = st.session_state.contract_manager
    contract_id = st.session_state.contract_id
    
    # Demo tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Contract Management", "Role Assignment", "Access Control", "Audit & Compliance"])
    
    with tab1:
        st.subheader("Smart Contract Deployment & Management")
        
        # Show contract information
        try:
            contract_state = contract_manager.get_contract_state(contract_id, "ADMIN_001")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Executions", contract_state['total_executions'])
            with col2:
                st.metric("Gas Used", contract_state['total_gas_used'])
            with col3:
                st.metric("Roles Defined", contract_state['state_summary']['roles_defined'])
            
            st.write("**Contract Details:**")
            st.json({
                'Contract ID': contract_state['contract_id'],
                'Creator': contract_state['creator'],
                'Created At': contract_state['created_at'],
                'State Summary': contract_state['state_summary']
            })
            
        except Exception as e:
            st.error(f"Error retrieving contract state: {str(e)}")
        
        # Show recent executions
        st.subheader("Recent Contract Executions")
        try:
            execution_history = contract_manager.get_execution_history(contract_id, "ADMIN_001", 5)
            if execution_history:
                df_executions = pd.DataFrame(execution_history)
                st.dataframe(df_executions, use_container_width=True)
            else:
                st.write("No executions yet.")
        except Exception as e:
            st.error(f"Error retrieving execution history: {str(e)}")
    
    with tab2:
        st.subheader("Role Assignment & Management")
        
        # Role assignment form
        st.write("**Assign Role to User:**")
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("User ID:", "USER_001")
            role = st.selectbox("Select Role:", 
                              ["Doctor", "Nurse", "Lab Technician", "Patient", "Insurance Provider", "Researcher"])
        
        with col2:
            assigned_by = st.text_input("Assigned By:", "ADMIN_001")
        
        if st.button("Assign Role"):
            try:
                result = contract_manager.execute_contract(
                    contract_id,
                    "assign_role",
                    {
                        "user_id": user_id,
                        "role": role,
                        "assigned_by": assigned_by
                    },
                    "ADMIN_001"
                )
                
                if result['success']:
                    st.success(f"Role '{role}' assigned to {user_id} successfully!")
                    st.json(result['result'])
                else:
                    st.error(f"Role assignment failed: {result['error']}")
            
            except Exception as e:
                st.error(f"Error assigning role: {str(e)}")
        
        # Show role definitions
        st.subheader("Role Definitions & Permissions")
        role_info = {
            "Doctor": {
                "Permissions": "read, write, update, delete, prescribe",
                "Data Types": "all",
                "Patient Access": "assigned patients"
            },
            "Nurse": {
                "Permissions": "read, write, update",
                "Data Types": "vital signs, nursing notes, medication admin",
                "Patient Access": "ward patients"
            },
            "Lab Technician": {
                "Permissions": "read, write",
                "Data Types": "lab results, test orders",
                "Patient Access": "test patients"
            },
            "Patient": {
                "Permissions": "read",
                "Data Types": "own records only",
                "Patient Access": "self only"
            },
            "Insurance Provider": {
                "Permissions": "read",
                "Data Types": "billing, claims, diagnosis",
                "Patient Access": "insured patients"
            },
            "Researcher": {
                "Permissions": "read",
                "Data Types": "anonymized data only",
                "Patient Access": "anonymized only"
            }
        }
        
        for role_name, permissions in role_info.items():
            with st.expander(f"{role_name} Permissions"):
                for key, value in permissions.items():
                    st.write(f"**{key}:** {value}")
    
    with tab3:
        st.subheader("Access Control & Data Requests")
        
        # Patient consent setup
        st.write("**Set Patient Consent:**")
        col1, col2 = st.columns(2)
        
        with col1:
            consent_patient_id = st.text_input("Patient ID:", "PATIENT_001", key="consent_patient")
            consent_data_types = st.multiselect("Data Types:", 
                                               ["lab_results", "vital_signs", "prescriptions", "medical_images", "clinical_notes"],
                                               default=["lab_results", "vital_signs"])
        
        with col2:
            consent_roles = st.multiselect("Authorized Roles:",
                                         ["Doctor", "Nurse", "Lab Technician"],
                                         default=["Doctor", "Nurse"])
            consent_expiry = st.date_input("Consent Expiry Date:")
        
        if st.button("Set Patient Consent"):
            try:
                result = contract_manager.execute_contract(
                    contract_id,
                    "set_patient_consent",
                    {
                        "patient_id": consent_patient_id,
                        "data_types": consent_data_types,
                        "authorized_roles": consent_roles,
                        "expiry_date": consent_expiry.isoformat()
                    },
                    consent_patient_id  # Patient setting their own consent
                )
                
                if result['success']:
                    st.success("Patient consent set successfully!")
                    st.json(result['result'])
                else:
                    st.error(f"Failed to set consent: {result['error']}")
                    
            except Exception as e:
                st.error(f"Error setting consent: {str(e)}")
        
        st.divider()
        
        # Access request simulation
        st.write("**Request Data Access:**")
        col1, col2 = st.columns(2)
        
        with col1:
            requester_id = st.text_input("Requester ID:", "USER_001", key="requester")
            target_patient_id = st.text_input("Patient ID:", "PATIENT_001", key="target_patient")
        
        with col2:
            requested_data_type = st.selectbox("Data Type:", 
                                             ["lab_results", "vital_signs", "prescriptions", "medical_images", "clinical_notes"])
            justification = st.text_area("Justification:", "Routine patient care")
        
        if st.button("Request Access"):
            try:
                result = contract_manager.execute_contract(
                    contract_id,
                    "request_access",
                    {
                        "patient_id": target_patient_id,
                        "data_type": requested_data_type,
                        "justification": justification,
                        "session_duration": 3600
                    },
                    requester_id
                )
                
                if result['success']:
                    st.success("Access granted!")
                    access_info = result['result']
                    
                    st.write("**Access Details:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Patient ID:** {access_info['patient_id']}")
                        st.write(f"**Data Type:** {access_info['data_type']}")
                        st.write(f"**Expires At:** {access_info['expires_at']}")
                    
                    with col2:
                        st.write(f"**Permissions:** {', '.join(access_info['permissions'])}")
                        st.write(f"**Session Duration:** {access_info['session_duration']} seconds")
                    
                    st.write(f"**Access Token:** `{access_info['access_token'][:32]}...`")
                else:
                    st.error(f"Access denied: {result['error']}")
                    
            except Exception as e:
                st.error(f"Error requesting access: {str(e)}")
    
    with tab4:
        st.subheader("Audit Trail & Compliance Reporting")
        
        # Audit log retrieval
        st.write("**Generate Compliance Report:**")
        col1, col2 = st.columns(2)
        
        with col1:
            audit_requester = st.text_input("Auditor ID:", "ADMIN_001")
            audit_patient_id = st.text_input("Patient ID (optional):", "", key="audit_patient")
        
        with col2:
            audit_start_date = st.date_input("Start Date:", datetime.now().date() - timedelta(days=7))
            audit_end_date = st.date_input("End Date:", datetime.now().date())
        
        if st.button("Generate Audit Report"):
            try:
                result = contract_manager.execute_contract(
                    contract_id,
                    "get_audit_log",
                    {
                        "patient_id": audit_patient_id if audit_patient_id else None,
                        "start_date": audit_start_date.isoformat(),
                        "end_date": audit_end_date.isoformat()
                    },
                    audit_requester
                )
                
                if result['success']:
                    audit_data = result['result']
                    
                    st.success(f"Generated audit report with {audit_data['total_entries']} entries")
                    
                    # Show audit summary
                    st.write("**Audit Summary:**")
                    summary_col1, summary_col2 = st.columns(2)
                    
                    with summary_col1:
                        st.metric("Total Entries", audit_data['total_entries'])
                        st.write(f"**Generated By:** {audit_data['generated_by']}")
                    
                    with summary_col2:
                        st.write(f"**Generated At:** {audit_data['generated_at']}")
                        st.write(f"**Date Range:** {audit_start_date} to {audit_end_date}")
                    
                    # Show audit entries
                    if audit_data['audit_entries']:
                        st.subheader("Audit Entries")
                        df_audit = pd.DataFrame(audit_data['audit_entries'])
                        st.dataframe(df_audit, use_container_width=True)
                        
                        # Visualizations
                        if len(audit_data['audit_entries']) > 1:
                            st.subheader("Audit Visualizations")
                            
                            # Function usage chart
                            function_counts = df_audit['function_name'].value_counts()
                            fig_functions = go.Figure(data=[
                                go.Bar(x=function_counts.index, y=function_counts.values)
                            ])
                            fig_functions.update_layout(
                                title="Smart Contract Function Usage",
                                xaxis_title="Function Name",
                                yaxis_title="Execution Count"
                            )
                            st.plotly_chart(fig_functions, use_container_width=True)
                            
                            # User activity chart
                            user_counts = df_audit['caller'].value_counts()
                            fig_users = go.Figure(data=[
                                go.Pie(labels=user_counts.index, values=user_counts.values, hole=0.3)
                            ])
                            fig_users.update_layout(title="User Activity Distribution")
                            st.plotly_chart(fig_users, use_container_width=True)
                    else:
                        st.write("No audit entries found for the specified criteria.")
                else:
                    st.error(f"Failed to generate audit report: {result['error']}")
                    
            except Exception as e:
                st.error(f"Error generating audit report: {str(e)}")
        
        # Compliance metrics
        st.subheader("Compliance Metrics")
        
        # Simulate compliance metrics
        compliance_metrics = {
            'HIPAA Compliance Score': '95%',
            'GDPR Compliance Score': '92%',
            'Access Requests Logged': '100%',
            'Consent Verification Rate': '98%',
            'Audit Trail Completeness': '100%'
        }
        
        metric_cols = st.columns(len(compliance_metrics))
        for i, (metric, value) in enumerate(compliance_metrics.items()):
            with metric_cols[i]:
                st.metric(metric, value)

def show_encryption_simulation():
    st.header("Healthcare Data Encryption Simulation")
    
    # Initialize encryption simulator
    enc_sim = EncryptionSimulator()
    
    st.subheader("Simulation Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        record_count = st.slider("Number of Health Records", 1, 1000, 100)
        record_size = st.selectbox("Average Record Size", ["Small (1KB)", "Medium (10KB)", "Large (100KB)", "X-Large (1MB)"])
    
    with col2:
        encryption_mode = st.selectbox("Encryption Mode", ["AES-CTR", "AES-GCM", "Comparison"])
        processing_unit = st.radio("Processing Unit:", ["CPU", "GPU (Simulated)", "Both"])
    
    # Healthcare data type simulation
    st.subheader("Healthcare Data Types")
    data_types = st.multiselect(
        "Select data types to include:",
        ["Patient Demographics", "Lab Results", "Medical Images", "Clinical Notes", "Prescriptions", "Vital Signs"],
        default=["Patient Demographics", "Lab Results", "Clinical Notes"]
    )
    
    if st.button("Run Encryption Simulation"):
        with st.spinner("Encrypting healthcare records..."):
            # Parse record size
            size_map = {"Small (1KB)": 1, "Medium (10KB)": 10, "Large (100KB)": 100, "X-Large (1MB)": 1000}
            size_kb = size_map[record_size]
            
            results = enc_sim.simulate_encryption(record_count, size_kb, encryption_mode, processing_unit, data_types)
            
            # Display results
            st.success(f"Successfully encrypted {record_count} healthcare records!")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Data Size", f"{results['total_size_mb']:.2f} MB")
            
            with col2:
                if processing_unit == "Both":
                    st.metric("CPU Encryption Time", f"{results['cpu_time']:.2f}s")
                else:
                    st.metric("Encryption Time", f"{results['encryption_time']:.2f}s")
            
            with col3:
                if processing_unit == "Both":
                    st.metric("GPU Encryption Time", f"{results['gpu_time']:.2f}s")
                else:
                    st.metric("Throughput", f"{results['throughput']:.2f} MB/s")
            
            with col4:
                if processing_unit == "Both":
                    st.metric("GPU Speedup", f"{results['speedup']:.1f}x")
                else:
                    st.metric("Records/Second", f"{results['records_per_sec']:.0f}")
            
            # Visualization
            if processing_unit == "Both":
                # Performance comparison
                fig = go.Figure()
                
                categories = ['Encryption Time', 'Throughput (MB/s)']
                cpu_values = [results['cpu_time'], results['cpu_throughput']]
                gpu_values = [results['gpu_time'], results['gpu_throughput']]
                
                fig.add_trace(go.Bar(
                    x=categories,
                    y=cpu_values,
                    name='CPU',
                    marker_color='red'
                ))
                
                fig.add_trace(go.Bar(
                    x=categories,
                    y=gpu_values,
                    name='GPU',
                    marker_color='green'
                ))
                
                fig.update_layout(
                    title="CPU vs GPU Encryption Performance",
                    barmode='group'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Data type breakdown
            if len(data_types) > 1:
                st.subheader("Encryption Performance by Data Type")
                
                # Simulate different performance characteristics for different data types
                type_performance = {}
                base_time = results.get('encryption_time', results.get('gpu_time', 1.0))
                
                for dt in data_types:
                    # Different data types have different encryption characteristics
                    multipliers = {
                        "Patient Demographics": 0.8,  # Structured, compresses well
                        "Lab Results": 1.0,  # Standard
                        "Medical Images": 2.5,  # Large binary data
                        "Clinical Notes": 1.2,  # Text data
                        "Prescriptions": 0.9,  # Small structured data
                        "Vital Signs": 0.7   # Small numeric data
                    }
                    type_performance[dt] = base_time * multipliers.get(dt, 1.0) / len(data_types)
                
                fig_types = go.Figure(data=[
                    go.Bar(
                        x=list(type_performance.keys()),
                        y=list(type_performance.values()),
                        marker_color='blue'
                    )
                ])
                
                fig_types.update_layout(
                    title="Encryption Time by Healthcare Data Type",
                    xaxis_title="Data Type",
                    yaxis_title="Encryption Time (seconds)",
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig_types, use_container_width=True)
            
            # Show sample encrypted data structure
            st.subheader("Sample Encrypted Record Structure")
            sample_record = enc_sim.generate_sample_record(data_types[0] if data_types else "Patient Demographics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Original Structure (Simulated):**")
                st.json(sample_record['original'])
            
            with col2:
                st.write("**Encrypted Structure:**")
                st.json(sample_record['encrypted'])

def show_compliance_demo():
    st.header("HIPAA/GDPR Compliance Simulation")
    
    # Initialize compliance simulator
    compliance = ComplianceSimulator()
    
    st.subheader("Compliance Features")
    
    # Tabs for different compliance aspects
    tab1, tab2, tab3, tab4 = st.tabs(["Data Storage", "Access Control", "Audit Trail", "Data Erasure"])
    
    with tab1:
        st.write("### Off-Chain Storage with On-Chain References")
        st.write("Demonstrates how sensitive data is stored off-chain while maintaining blockchain immutability")
        
        # Simulate patient record storage
        if st.button("Store Patient Record"):
            record_info = compliance.store_patient_record()
            
            st.success("Patient record stored successfully!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**On-Chain Data:**")
                st.json({
                    "record_hash": record_info["on_chain"]["record_hash"],
                    "ipfs_reference": record_info["on_chain"]["ipfs_reference"],
                    "timestamp": record_info["on_chain"]["timestamp"],
                    "patient_id_hash": record_info["on_chain"]["patient_id_hash"]
                })
            
            with col2:
                st.write("**Off-Chain Data (Encrypted):**")
                st.json({
                    "encrypted_data": record_info["off_chain"]["encrypted_data"][:50] + "...",
                    "encryption_key_id": record_info["off_chain"]["encryption_key_id"],
                    "data_size_bytes": record_info["off_chain"]["data_size_bytes"]
                })
    
    with tab2:
        st.write("### Access Control and Authorization")
        st.write("Multi-party key sharing and role-based access control simulation")
        
        # User roles
        user_role = st.selectbox("Select User Role:", 
                                ["Doctor", "Nurse", "Lab Technician", "Patient", "Insurance Provider", "Researcher"])
        
        patient_id = st.text_input("Patient ID:", "PATIENT_001")
        
        if st.button("Request Data Access"):
            access_result = compliance.request_data_access(user_role, patient_id)
            
            if access_result["access_granted"]:
                st.success(f"Access granted for {user_role}")
                st.write("**Access Details:**")
                st.json(access_result)
            else:
                st.error(f"Access denied for {user_role}")
                st.write("**Denial Reason:**", access_result["reason"])
    
    with tab3:
        st.write("### Audit Trail and Logging")
        st.write("HIPAA-compliant audit logging of all data access events")
        
        if st.button("Generate Audit Report"):
            audit_data = compliance.generate_audit_trail()
            
            st.write("**Recent Access Events:**")
            
            # Convert to DataFrame for better display
            df_audit = pd.DataFrame(audit_data)
            st.dataframe(df_audit, use_container_width=True)
            
            # Visualization
            if len(audit_data) > 0:
                # Access by role
                role_counts = df_audit['user_role'].value_counts()
                
                fig_roles = go.Figure(data=[
                    go.Pie(
                        labels=role_counts.index,
                        values=role_counts.values,
                        hole=0.3
                    )
                ])
                
                fig_roles.update_layout(title="Data Access by User Role")
                st.plotly_chart(fig_roles, use_container_width=True)
                
                # Access over time
                df_audit['timestamp'] = pd.to_datetime(df_audit['timestamp'])
                daily_access = df_audit.groupby(df_audit['timestamp'].dt.date).size()
                
                fig_timeline = go.Figure()
                fig_timeline.add_trace(go.Scatter(
                    x=daily_access.index,
                    y=daily_access.values,
                    mode='lines+markers',
                    name='Daily Access Count'
                ))
                
                fig_timeline.update_layout(
                    title="Data Access Timeline",
                    xaxis_title="Date",
                    yaxis_title="Number of Access Events"
                )
                
                st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab4:
        st.write("### GDPR Data Erasure ('Right to be Forgotten')")
        st.write("Demonstrates compliant data erasure while maintaining blockchain integrity")
        
        # List stored records
        stored_records = compliance.list_stored_records()
        
        if stored_records:
            record_to_erase = st.selectbox("Select Record to Erase:", 
                                         [f"Patient {r['patient_id']} - {r['timestamp']}" for r in stored_records])
            
            if st.button("Execute Data Erasure", type="primary"):
                record_index = int(record_to_erase.split(" - ")[0].split(" ")[1]) - 1
                erasure_result = compliance.erase_patient_data(stored_records[record_index]['record_id'])
                
                if erasure_result["success"]:
                    st.success("Data erasure completed successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Before Erasure:**")
                        st.json(erasure_result["before"])
                    
                    with col2:
                        st.write("**After Erasure:**")
                        st.json(erasure_result["after"])
                    
                    st.info("Note: On-chain hash remains for audit purposes, but off-chain data has been permanently deleted.")
                else:
                    st.error("Data erasure failed: " + erasure_result["error"])
        else:
            st.info("No records available for erasure. Store some patient records first in the 'Data Storage' tab.")
    
    # Compliance summary
    st.subheader("Compliance Summary")
    
    compliance_metrics = compliance.get_compliance_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Records Stored", compliance_metrics["total_records"])
    
    with col2:
        st.metric("Access Requests", compliance_metrics["total_access_requests"])
    
    with col3:
        st.metric("Audit Events", compliance_metrics["audit_events"])
    
    with col4:
        st.metric("Data Erasures", compliance_metrics["erasure_requests"])

def show_quantum_resistance_analysis():
    st.header("🔬 Quantum Resistance Analysis")
    st.markdown("Analyzing quantum computing threats to healthcare blockchain systems and post-quantum cryptographic solutions.")
    
    # Initialize analyzer
    analyzer = QuantumResistanceAnalyzer()
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Threat Assessment", 
        "Hash Function Comparison", 
        "Timeline Analysis", 
        "Migration Planning", 
        "Cost Analysis"
    ])
    
    with tab1:
        st.subheader("Current Quantum Threats to Healthcare Blockchain")
        st.markdown("Analysis of how quantum computing threatens current cryptographic systems used in healthcare.")
        
        vulnerabilities = analyzer.analyze_current_vulnerabilities()
        
        # Critical threats
        if vulnerabilities['critical_threats']:
            st.error("🚨 Critical Quantum Threats")
            for threat in vulnerabilities['critical_threats']:
                with st.expander(f"❌ {threat['algorithm']} - {threat['attack_method']}"):
                    st.write(f"**Time Reduction:** {threat['time_reduction']}")
                    st.write(f"**Mitigation:** {threat['mitigation']}")
        
        # Moderate threats
        if vulnerabilities['moderate_threats']:
            st.warning("⚠️ Moderate Quantum Threats")
            for threat in vulnerabilities['moderate_threats']:
                with st.expander(f"🔶 {threat['algorithm']} - {threat['attack_method']}"):
                    st.write(f"**Time Reduction:** {threat['time_reduction']}")
                    st.write(f"**Mitigation:** {threat['mitigation']}")
        
        # Healthcare-specific risks
        st.subheader("Healthcare-Specific Quantum Risks")
        for risk in vulnerabilities['healthcare_specific_risks']:
            with st.expander(f"🏥 {risk['risk']}"):
                st.write(f"**Description:** {risk['description']}")
                st.write(f"**Timeline:** {risk['timeline']}")
                st.write(f"**Mitigation:** {risk['mitigation']}")
    
    with tab2:
        st.subheader("Post-Quantum Hash Function Performance")
        st.markdown("Comparing current and quantum-resistant hash functions for blockchain operations.")
        
        if st.button("Run Hash Function Benchmarks"):
            with st.spinner("Running comprehensive hash function benchmarks..."):
                results = analyzer.benchmark_quantum_resistant_hashes()
            
            # Create comparison table
            comparison_data = []
            for algorithm, data in results.items():
                comparison_data.append({
                    'Algorithm': algorithm,
                    'Type': data['algorithm_type'],
                    'Quantum Resistance': data['quantum_resistance'],
                    'Hashes/Second': f"{data['hashes_per_second']:,.0f}" if isinstance(data['hashes_per_second'], (int, float)) else data['hashes_per_second'],
                    'MB/Second': f"{data['mb_per_second']:.1f}" if isinstance(data['mb_per_second'], (int, float)) else data['mb_per_second'],
                    'Relative Performance': f"{data['relative_performance']:.2f}x" if isinstance(data['relative_performance'], (int, float)) else data['relative_performance'],
                    'Recommendation': data['recommended_action']
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            # Performance visualization
            st.subheader("Performance Comparison Chart")
            
            # Filter numeric data for visualization
            numeric_results = {k: v for k, v in results.items() 
                             if isinstance(v['relative_performance'], (int, float))}
            
            if numeric_results:
                algorithms = list(numeric_results.keys())
                performance = [numeric_results[alg]['relative_performance'] for alg in algorithms]
                
                fig = px.bar(
                    x=algorithms,
                    y=performance,
                    title="Relative Performance vs SHA-256",
                    labels={'x': 'Hash Algorithm', 'y': 'Performance Multiplier'},
                    color=performance,
                    color_continuous_scale='RdYlGn'
                )
                fig.add_hline(y=1.0, line_dash="dash", line_color="gray", 
                             annotation_text="SHA-256 Baseline")
                st.plotly_chart(fig, use_container_width=True)
        
        # Algorithm recommendations
        st.subheader("Migration Recommendations")
        recommendations = [
            {
                'Algorithm': 'SHA-3-256',
                'Priority': 'High',
                'Use Case': 'Immediate migration for new systems',
                'Pros': 'NIST standard, good performance, quantum resistant',
                'Cons': '~20% slower than SHA-256'
            },
            {
                'Algorithm': 'SHA-384',
                'Priority': 'Medium',
                'Use Case': 'Quick upgrade for existing systems',
                'Pros': 'Easy migration, higher security margin',
                'Cons': 'Still uses Merkle-Damgård construction'
            },
            {
                'Algorithm': 'BLAKE3',
                'Priority': 'Future',
                'Use Case': 'Next-generation systems',
                'Pros': 'Extremely fast, parallel processing friendly',
                'Cons': 'Not yet standardized'
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['Algorithm']} - {rec['Priority']} Priority"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Use Case:** {rec['Use Case']}")
                    st.write(f"**Pros:** {rec['Pros']}")
                with col2:
                    st.write(f"**Cons:** {rec['Cons']}")
    
    with tab3:
        st.subheader("Quantum Computing Timeline Impact")
        st.markdown("Projected timeline of quantum computing development and its impact on healthcare blockchain security.")
        
        timeline = analyzer.simulate_quantum_timeline_impact()
        
        # Timeline visualization
        years = list(timeline.keys())
        threat_levels = []
        qubit_counts = []
        
        for year in years:
            data = timeline[year]
            
            # Convert threat level to numeric
            threat_map = {'Minimal': 1, 'Low-Moderate': 2, 'High': 3, 'Critical': 4}
            threat_levels.append(threat_map[data['threat_level']])
            
            # Extract qubit count (rough estimation)
            qubit_str = data['quantum_qubits']
            if '1000' in qubit_str and '~1000' in qubit_str:
                qubit_counts.append(1000)
            elif '10,000' in qubit_str:
                qubit_counts.append(10000)
            elif '100,000' in qubit_str:
                qubit_counts.append(100000)
            elif '1,000,000' in qubit_str:
                qubit_counts.append(1000000)
        
        # Create dual-axis plot
        fig = go.Figure()
        
        # Threat level
        fig.add_trace(go.Scatter(
            x=years,
            y=threat_levels,
            mode='lines+markers',
            name='Threat Level',
            line=dict(color='red', width=3),
            marker=dict(size=10)
        ))
        
        # Qubit count (scaled down for display)
        fig.add_trace(go.Scatter(
            x=years,
            y=[q/250000 for q in qubit_counts],  # Scale down for display
            mode='lines+markers',
            name='Quantum Capability (Scaled)',
            line=dict(color='blue', width=3, dash='dot'),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Quantum Threat Timeline for Healthcare Blockchain",
            xaxis_title="Year",
            yaxis_title="Threat Level",
            yaxis=dict(range=[0, 5], tickvals=[1,2,3,4], ticktext=['Minimal', 'Low-Moderate', 'High', 'Critical']),
            yaxis2=dict(title="Quantum Qubits (Millions)", overlaying='y', side='right', range=[0, 5]),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline details
        for year, data in timeline.items():
            with st.expander(f"{year} - {data['threat_level']} Threat"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Quantum Capability:** {data['quantum_qubits']}")
                    st.write(f"**Healthcare Action:** {data['healthcare_action']}")
                with col2:
                    st.write(f"**Algorithms Affected:** {', '.join(data['algorithms_affected']) if data['algorithms_affected'] else 'None'}")
                    st.write(f"**Recommended Timeline:** {data['recommended_timeline']}")
    
    with tab4:
        st.subheader("Post-Quantum Migration Roadmap")
        st.markdown("Detailed migration plan for transitioning healthcare blockchain systems to post-quantum cryptography.")
        
        roadmap = analyzer.generate_migration_roadmap()
        
        # Roadmap visualization
        phases = list(roadmap.keys())
        phase_names = [roadmap[phase]['name'] for phase in phases]
        durations = [int(roadmap[phase]['duration'].split('-')[0]) for phase in phases]  # Take minimum duration
        
        fig = go.Figure(data=[
            go.Bar(
                x=phase_names,
                y=durations,
                text=[f"{roadmap[phase]['duration']}" for phase in phases],
                textposition='auto',
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            )
        ])
        
        fig.update_layout(
            title="Migration Timeline by Phase",
            xaxis_title="Migration Phase",
            yaxis_title="Duration (Months)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed roadmap
        for phase_id, phase_data in roadmap.items():
            phase_num = phase_id.split('_')[1]
            with st.expander(f"Phase {phase_num}: {phase_data['name']} ({phase_data['duration']})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Objectives:**")
                    for obj in phase_data['objectives']:
                        st.write(f"• {obj}")
                    
                    st.write(f"**Estimated Cost:** {phase_data['estimated_cost']}")
                
                with col2:
                    st.write("**Deliverables:**")
                    for deliverable in phase_data['deliverables']:
                        st.write(f"• {deliverable}")
    
    with tab5:
        st.subheader("Migration Cost Analysis")
        st.markdown("Financial analysis of transitioning to post-quantum cryptography in healthcare organizations.")
        
        # System size selector
        system_size = st.selectbox(
            "Select your organization size:",
            ["small", "medium", "large"],
            format_func=lambda x: f"{x.title()} Organization"
        )
        
        if st.button("Calculate Migration Costs"):
            costs = analyzer.calculate_migration_costs(system_size)
            
            # Cost breakdown
            st.subheader(f"Cost Analysis for {system_size.title()} Organization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Migration Cost", f"${costs['total_cost']:,.0f}")
                st.metric("ROI Timeline", costs['roi_timeline'])
                st.metric("Risk Reduction", costs['risk_reduction'])
            
            with col2:
                # Cost breakdown pie chart
                breakdown = costs['cost_breakdown_percentage']
                fig = px.pie(
                    values=list(breakdown.values()),
                    names=list(breakdown.keys()),
                    title="Cost Breakdown by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed breakdown
            st.subheader("Detailed Cost Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Base Infrastructure Costs:**")
                for category, cost in costs['base_costs'].items():
                    st.write(f"• {category.replace('_', ' ').title()}: ${cost:,.0f}")
            
            with col2:
                st.write("**Healthcare-Specific Costs:**")
                for category, cost in costs['healthcare_specific_costs'].items():
                    st.write(f"• {category.replace('_', ' ').title()}: ${cost:,.0f}")
            
            # Cost-benefit analysis
            st.subheader("Cost-Benefit Analysis")
            
            benefits = [
                "Protection against quantum computing attacks",
                "Compliance with future regulatory requirements",
                "Enhanced patient data security",
                "Future-proofing of healthcare IT infrastructure",
                "Reduced risk of costly security breaches",
                "Competitive advantage in secure healthcare technology"
            ]
            
            risks = [
                "Increased computational overhead (5-20%)",
                "Integration complexity with legacy systems",
                "Staff training and certification requirements",
                "Potential temporary performance impacts during migration",
                "Ongoing maintenance and monitoring costs"
            ]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Benefits:**")
                for benefit in benefits:
                    st.write(f"✅ {benefit}")
            
            with col2:
                st.write("**Considerations:**")
                for risk in risks:
                    st.write(f"⚠️ {risk}")
    
    # Summary and recommendations
    st.subheader("Key Recommendations")
    st.info("""
    **Immediate Actions (2025-2027):**
    • Begin crypto-agility planning and staff training
    • Migrate hash functions to SHA-3 for new systems
    • Evaluate post-quantum signature schemes for smart contracts
    
    **Medium-term Actions (2027-2030):**
    • Implement hybrid classical/post-quantum systems
    • Begin patient data re-encryption with quantum-resistant algorithms
    • Update compliance frameworks for post-quantum requirements
    
    **Long-term Actions (2030-2035):**
    • Complete migration to fully post-quantum systems
    • Regular quantum threat assessments and algorithm updates
    • Maintain crypto-agility for future algorithm changes
    """)

if __name__ == "__main__":
    main()
