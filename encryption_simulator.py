import time
import hashlib
import json
import random
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class EncryptionSimulator:
    def __init__(self):
        self.backend = default_backend()
    
    def simulate_encryption(self, record_count, record_size_kb, encryption_mode, processing_unit, data_types):
        """Simulate encryption of healthcare records"""
        
        total_size_mb = (record_count * record_size_kb) / 1024
        
        results = {
            'total_size_mb': total_size_mb,
            'record_count': record_count,
            'record_size_kb': record_size_kb
        }
        
        if processing_unit == "Both":
            # Run both CPU and GPU simulations
            cpu_time = self.simulate_cpu_encryption(total_size_mb, encryption_mode)
            gpu_time = self.simulate_gpu_encryption(total_size_mb, encryption_mode)
            
            results.update({
                'cpu_time': cpu_time,
                'gpu_time': gpu_time,
                'speedup': cpu_time / gpu_time if gpu_time > 0 else 1,
                'cpu_throughput': total_size_mb / cpu_time if cpu_time > 0 else 0,
                'gpu_throughput': total_size_mb / gpu_time if gpu_time > 0 else 0
            })
        
        elif processing_unit == "CPU":
            encryption_time = self.simulate_cpu_encryption(total_size_mb, encryption_mode)
            results.update({
                'encryption_time': encryption_time,
                'throughput': total_size_mb / encryption_time if encryption_time > 0 else 0,
                'records_per_sec': record_count / encryption_time if encryption_time > 0 else 0
            })
        
        else:  # GPU
            encryption_time = self.simulate_gpu_encryption(total_size_mb, encryption_mode)
            results.update({
                'encryption_time': encryption_time,
                'throughput': total_size_mb / encryption_time if encryption_time > 0 else 0,
                'records_per_sec': record_count / encryption_time if encryption_time > 0 else 0
            })
        
        return results
    
    def simulate_cpu_encryption(self, data_size_mb, encryption_mode):
        """Simulate CPU encryption performance"""
        start_time = time.time()
        
        # Simulate CPU encryption with realistic performance characteristics
        # Based on research paper findings: CPU encryption is slower
        
        if encryption_mode == "AES-CTR":
            # CPU AES-CTR: ~50-100 MB/s on modern CPU
            throughput_mb_per_sec = random.uniform(50, 100)
        elif encryption_mode == "AES-GCM":
            # CPU AES-GCM: ~30-80 MB/s (more overhead)
            throughput_mb_per_sec = random.uniform(30, 80)
        else:  # Comparison mode
            throughput_mb_per_sec = random.uniform(40, 90)
        
        # Calculate encryption time
        encryption_time = data_size_mb / throughput_mb_per_sec
        
        # Add some realistic processing time
        time.sleep(min(encryption_time * 0.01, 0.5))  # Sleep for up to 0.5 seconds
        
        actual_time = time.time() - start_time
        return max(encryption_time, actual_time)
    
    def simulate_gpu_encryption(self, data_size_mb, encryption_mode):
        """Simulate GPU encryption performance"""
        start_time = time.time()
        
        # Simulate GPU encryption with CUDA acceleration
        # Based on research paper: 5x to 100x improvement
        
        if encryption_mode == "AES-CTR":
            # GPU AES-CTR: ~500-2000 MB/s with CUDA optimization
            throughput_mb_per_sec = random.uniform(500, 2000)
        elif encryption_mode == "AES-GCM":
            # GPU AES-GCM: ~400-1500 MB/s
            throughput_mb_per_sec = random.uniform(400, 1500)
        else:  # Comparison mode
            throughput_mb_per_sec = random.uniform(450, 1800)
        
        # Calculate encryption time
        encryption_time = data_size_mb / throughput_mb_per_sec
        
        # GPU has less overhead for large data
        time.sleep(min(encryption_time * 0.001, 0.1))  # Much shorter sleep
        
        actual_time = time.time() - start_time
        return max(encryption_time, actual_time)
    
    def generate_sample_record(self, data_type):
        """Generate a sample healthcare record"""
        
        base_records = {
            "Patient Demographics": {
                "patient_id": "P001234",
                "name": "John Doe",
                "date_of_birth": "1980-05-15",
                "gender": "M",
                "address": "123 Main St, City, State",
                "phone": "555-0123",
                "email": "john.doe@email.com",
                "emergency_contact": "Jane Doe - 555-0124"
            },
            "Lab Results": {
                "patient_id": "P001234",
                "test_date": "2025-09-21",
                "test_type": "Complete Blood Count",
                "results": {
                    "WBC": "7.2 K/uL",
                    "RBC": "4.8 M/uL",
                    "Hemoglobin": "14.2 g/dL",
                    "Hematocrit": "42.1%",
                    "Platelets": "285 K/uL"
                },
                "reference_ranges": {
                    "WBC": "4.5-11.0 K/uL",
                    "RBC": "4.5-5.9 M/uL"
                },
                "lab_id": "LAB001",
                "ordering_physician": "Dr. Smith"
            },
            "Clinical Notes": {
                "patient_id": "P001234",
                "encounter_date": "2025-09-21",
                "provider": "Dr. Johnson",
                "chief_complaint": "Annual physical examination",
                "history_present_illness": "Patient reports feeling well...",
                "review_of_systems": "Negative for fever, chills...",
                "physical_exam": "Alert, oriented x3...",
                "assessment_plan": "Continue current medications...",
                "note_type": "Progress Note"
            },
            "Medical Images": {
                "patient_id": "P001234",
                "study_date": "2025-09-21",
                "modality": "CT",
                "body_part": "Chest",
                "study_description": "CT Chest without contrast",
                "image_count": 120,
                "file_size_mb": 85.6,
                "radiologist": "Dr. Wilson",
                "findings": "No acute abnormalities detected",
                "dicom_series": "1.2.840.113..."
            },
            "Prescriptions": {
                "patient_id": "P001234",
                "prescription_id": "RX789123",
                "medication_name": "Lisinopril",
                "dosage": "10mg",
                "frequency": "Once daily",
                "quantity": 30,
                "refills": 2,
                "prescribing_physician": "Dr. Smith",
                "pharmacy": "ABC Pharmacy",
                "date_prescribed": "2025-09-21"
            },
            "Vital Signs": {
                "patient_id": "P001234",
                "timestamp": "2025-09-21T10:30:00",
                "blood_pressure_systolic": 128,
                "blood_pressure_diastolic": 78,
                "heart_rate": 72,
                "respiratory_rate": 16,
                "temperature_f": 98.6,
                "oxygen_saturation": 98,
                "weight_kg": 75.2,
                "height_cm": 175,
                "bmi": 24.6
            }
        }
        
        original_record = base_records.get(data_type, base_records["Patient Demographics"])
        
        # Simulate encryption
        record_json = json.dumps(original_record)
        
        # Create a simple hash for demonstration (in real implementation, this would be actual AES encryption)
        encrypted_data = hashlib.sha256(record_json.encode()).hexdigest()
        
        # Generate encryption metadata
        encrypted_record = {
            "record_id": f"ENC_{random.randint(100000, 999999)}",
            "encrypted_data": encrypted_data,
            "encryption_algorithm": "AES-256-CTR",
            "key_id": f"KEY_{random.randint(1000, 9999)}",
            "initialization_vector": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
            "timestamp": datetime.now().isoformat(),
            "data_hash": hashlib.sha256(record_json.encode()).hexdigest()[:16],
            "original_size_bytes": len(record_json),
            "encrypted_size_bytes": len(encrypted_data)
        }
        
        return {
            "original": original_record,
            "encrypted": encrypted_record
        }
    
    def benchmark_real_encryption(self, data_size_kb):
        """Perform actual AES encryption benchmark for comparison"""
        
        # Generate test data
        test_data = os.urandom(data_size_kb * 1024)
        
        # Generate random key and IV
        key = os.urandom(32)  # 256-bit key
        iv = os.urandom(16)   # 128-bit IV
        
        # AES-CTR encryption
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        
        start_time = time.time()
        encrypted_data = encryptor.update(test_data) + encryptor.finalize()
        encryption_time = time.time() - start_time
        
        return {
            'encryption_time': encryption_time,
            'data_size_kb': data_size_kb,
            'throughput_mb_per_sec': (data_size_kb / 1024) / encryption_time if encryption_time > 0 else 0,
            'original_size': len(test_data),
            'encrypted_size': len(encrypted_data)
        }
