import json
import hashlib
import random
import time
from datetime import datetime, timedelta
import uuid

class ComplianceSimulator:
    def __init__(self):
        self.stored_records = []
        self.access_log = []
        self.audit_trail = []
        self.access_control_matrix = {
            "Doctor": ["read", "write", "update", "delete"],
            "Nurse": ["read", "write", "update"],
            "Lab Technician": ["read", "write"],
            "Patient": ["read"],
            "Insurance Provider": ["read"],
            "Researcher": ["read"]  # De-identified data only
        }
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with some sample records for demonstration"""
        for i in range(5):
            self.stored_records.append({
                'record_id': str(uuid.uuid4()),
                'patient_id': f'PATIENT_{i+1:03d}',
                'timestamp': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                'on_chain_hash': hashlib.sha256(f'record_{i}'.encode()).hexdigest(),
                'ipfs_reference': f'QmX{hashlib.md5(f"ipfs_{i}".encode()).hexdigest()[:40]}',
                'status': 'active'
            })
    
    def store_patient_record(self):
        """Simulate storing a patient record with HIPAA/GDPR compliance"""
        
        # Generate patient data
        patient_data = {
            'patient_id': f'PATIENT_{random.randint(1000, 9999)}',
            'medical_record': {
                'diagnosis': 'Type 2 Diabetes',
                'medications': ['Metformin 500mg', 'Lisinopril 10mg'],
                'vital_signs': {
                    'blood_pressure': '130/85',
                    'heart_rate': 75,
                    'temperature': 98.6
                },
                'lab_results': {
                    'glucose': '145 mg/dL',
                    'hba1c': '7.2%'
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Encrypt the data (simulated)
        encrypted_data = hashlib.sha256(json.dumps(patient_data).encode()).hexdigest()
        
        # Generate IPFS reference (simulated)
        ipfs_reference = f"QmX{hashlib.md5(encrypted_data.encode()).hexdigest()[:40]}"
        
        # Store on-chain data (only hashes and references)
        on_chain_data = {
            'record_hash': hashlib.sha256(encrypted_data.encode()).hexdigest(),
            'ipfs_reference': ipfs_reference,
            'patient_id_hash': hashlib.sha256(patient_data['patient_id'].encode()).hexdigest(),
            'timestamp': patient_data['timestamp'],
            'data_classification': 'PHI',  # Protected Health Information
            'encryption_key_id': f'KEY_{random.randint(1000, 9999)}'
        }
        
        # Store off-chain data (encrypted)
        off_chain_data = {
            'encrypted_data': encrypted_data,
            'encryption_key_id': on_chain_data['encryption_key_id'],
            'data_size_bytes': len(json.dumps(patient_data)),
            'storage_location': f'IPFS:{ipfs_reference}',
            'backup_locations': [
                f'AWS_S3:backup/{ipfs_reference}',
                f'AZURE:backup/{ipfs_reference}'
            ]
        }
        
        # Add to stored records
        record_info = {
            'record_id': str(uuid.uuid4()),
            'patient_id': patient_data['patient_id'],
            'timestamp': patient_data['timestamp'],
            'status': 'active',
            'on_chain': on_chain_data,
            'off_chain': off_chain_data
        }
        
        self.stored_records.append({
            'record_id': record_info['record_id'],
            'patient_id': record_info['patient_id'],
            'timestamp': record_info['timestamp'],
            'on_chain_hash': on_chain_data['record_hash'],
            'ipfs_reference': ipfs_reference,
            'status': 'active'
        })
        
        # Log the storage event
        self._log_audit_event('DATA_STORAGE', 'SYSTEM', patient_data['patient_id'], 
                             'Patient record stored with encryption')
        
        return record_info
    
    def request_data_access(self, user_role, patient_id):
        """Simulate access control for healthcare data"""
        
        timestamp = datetime.now().isoformat()
        
        # Check if user role has access permissions
        if user_role not in self.access_control_matrix:
            result = {
                'access_granted': False,
                'reason': 'Unknown user role',
                'timestamp': timestamp,
                'user_role': user_role,
                'patient_id': patient_id
            }
        else:
            # Check if patient record exists
            patient_exists = any(record['patient_id'] == patient_id and record['status'] == 'active' 
                               for record in self.stored_records)
            
            if not patient_exists:
                result = {
                    'access_granted': False,
                    'reason': 'Patient record not found or inactive',
                    'timestamp': timestamp,
                    'user_role': user_role,
                    'patient_id': patient_id
                }
            else:
                # Grant access based on role permissions
                permissions = self.access_control_matrix[user_role]
                
                # Simulate additional checks for sensitive roles
                additional_checks = True
                if user_role in ["Insurance Provider", "Researcher"]:
                    # These roles might need additional authorization
                    additional_checks = random.choice([True, False])  # 50% chance
                
                if additional_checks:
                    result = {
                        'access_granted': True,
                        'permissions': permissions,
                        'timestamp': timestamp,
                        'user_role': user_role,
                        'patient_id': patient_id,
                        'session_token': hashlib.md5(f'{user_role}{patient_id}{timestamp}'.encode()).hexdigest(),
                        'expires_in': 3600,  # 1 hour
                        'data_classification': 'PHI' if user_role != 'Researcher' else 'De-identified',
                        'audit_required': True
                    }
                else:
                    result = {
                        'access_granted': False,
                        'reason': 'Additional authorization required',
                        'timestamp': timestamp,
                        'user_role': user_role,
                        'patient_id': patient_id
                    }
        
        # Log access attempt
        self.access_log.append(result)
        
        # Add to audit trail
        status = 'SUCCESS' if result['access_granted'] else 'DENIED'
        self._log_audit_event('ACCESS_REQUEST', user_role, patient_id, 
                             f'Access {status.lower()}: {result.get("reason", "Granted")}')
        
        return result
    
    def generate_audit_trail(self):
        """Generate HIPAA-compliant audit trail"""
        
        # Add some recent sample events if audit trail is empty
        if len(self.audit_trail) < 10:
            self._generate_sample_audit_events()
        
        return self.audit_trail[-20:]  # Return last 20 events
    
    def _generate_sample_audit_events(self):
        """Generate sample audit events for demonstration"""
        events = [
            ('DATA_ACCESS', 'Doctor', 'PATIENT_001', 'Medical record accessed for treatment'),
            ('DATA_UPDATE', 'Nurse', 'PATIENT_002', 'Vital signs updated'),
            ('DATA_ACCESS', 'Patient', 'PATIENT_001', 'Patient accessed own records'),
            ('ACCESS_DENIED', 'Insurance Provider', 'PATIENT_003', 'Insufficient permissions'),
            ('DATA_EXPORT', 'Researcher', 'PATIENT_004', 'De-identified data exported for study'),
            ('DATA_BACKUP', 'SYSTEM', 'ALL', 'Automated backup completed'),
            ('ENCRYPTION_KEY_ROTATION', 'SYSTEM', 'ALL', 'Encryption keys rotated'),
            ('COMPLIANCE_AUDIT', 'AUDITOR', 'ALL', 'HIPAA compliance audit performed'),
        ]
        
        for event_type, user_role, patient_id, description in events:
            self._log_audit_event(event_type, user_role, patient_id, description,
                                timestamp=datetime.now() - timedelta(days=random.randint(0, 7),
                                                                    hours=random.randint(0, 23)))
    
    def _log_audit_event(self, event_type, user_role, patient_id, description, timestamp=None):
        """Log an audit event"""
        if timestamp is None:
            timestamp = datetime.now()
        
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': timestamp.isoformat(),
            'event_type': event_type,
            'user_role': user_role,
            'patient_id': patient_id,
            'description': description,
            'ip_address': f'192.168.1.{random.randint(100, 200)}',
            'user_agent': 'Healthcare-App/1.0',
            'session_id': hashlib.md5(f'{user_role}{timestamp}'.encode()).hexdigest()[:16],
            'compliance_flags': {
                'hipaa_logged': True,
                'gdpr_consent_checked': True,
                'data_minimization_applied': True
            }
        }
        
        self.audit_trail.append(audit_entry)
    
    def list_stored_records(self):
        """List all stored patient records"""
        return [record for record in self.stored_records if record['status'] == 'active']
    
    def erase_patient_data(self, record_id):
        """Simulate GDPR-compliant data erasure"""
        
        # Find the record
        record_to_erase = None
        for record in self.stored_records:
            if record['record_id'] == record_id:
                record_to_erase = record
                break
        
        if not record_to_erase:
            return {'success': False, 'error': 'Record not found'}
        
        if record_to_erase['status'] != 'active':
            return {'success': False, 'error': 'Record already erased or inactive'}
        
        # Store before state
        before_state = {
            'status': record_to_erase['status'],
            'ipfs_reference': record_to_erase['ipfs_reference'],
            'on_chain_hash': record_to_erase['on_chain_hash'][:16] + '...',
            'accessible': True
        }
        
        # Perform erasure
        # 1. Delete off-chain data (simulated)
        record_to_erase['status'] = 'erased'
        record_to_erase['ipfs_reference'] = 'DELETED'
        record_to_erase['erasure_timestamp'] = datetime.now().isoformat()
        
        # 2. On-chain hash remains for audit purposes (blockchain immutability)
        # 3. Encryption keys are destroyed (simulated)
        
        # After state
        after_state = {
            'status': record_to_erase['status'],
            'ipfs_reference': record_to_erase['ipfs_reference'],
            'on_chain_hash': record_to_erase['on_chain_hash'][:16] + '... (audit only)',
            'accessible': False,
            'erasure_timestamp': record_to_erase['erasure_timestamp']
        }
        
        # Log erasure event
        self._log_audit_event('DATA_ERASURE', 'SYSTEM', record_to_erase['patient_id'],
                             'Patient data erased per GDPR request')
        
        return {
            'success': True,
            'before': before_state,
            'after': after_state,
            'erasure_method': 'Off-chain deletion + key destruction',
            'blockchain_note': 'On-chain hash preserved for audit trail (no personal data)'
        }
    
    def get_compliance_metrics(self):
        """Get compliance-related metrics"""
        
        active_records = len([r for r in self.stored_records if r['status'] == 'active'])
        erased_records = len([r for r in self.stored_records if r['status'] == 'erased'])
        
        return {
            'total_records': len(self.stored_records),
            'active_records': active_records,
            'erased_records': erased_records,
            'total_access_requests': len(self.access_log),
            'successful_access': len([a for a in self.access_log if a['access_granted']]),
            'denied_access': len([a for a in self.access_log if not a['access_granted']]),
            'audit_events': len(self.audit_trail),
            'erasure_requests': erased_records,
            'compliance_score': min(100, (active_records + len(self.audit_trail)) * 2)  # Simple scoring
        }
