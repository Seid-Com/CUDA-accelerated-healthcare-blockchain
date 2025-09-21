import json
import hashlib
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid

class SmartContract:
    """Base smart contract class for blockchain execution"""
    
    def __init__(self, contract_id: str, creator: str, contract_code: str):
        self.contract_id = contract_id
        self.creator = creator
        self.contract_code = contract_code
        self.state = {}
        self.created_at = datetime.now().isoformat()
        self.execution_log = []
        self.gas_used = 0
    
    def execute(self, function_name: str, params: Dict[str, Any], caller: str) -> Dict[str, Any]:
        """Execute a smart contract function"""
        start_time = time.time()
        
        # Log the execution attempt
        execution_entry = {
            'execution_id': str(uuid.uuid4()),
            'function_name': function_name,
            'caller': caller,
            'params': params,
            'timestamp': datetime.now().isoformat(),
            'gas_limit': 1000000,  # Simulated gas limit
            'status': 'pending'
        }
        
        try:
            # Check if function exists
            if not hasattr(self, function_name):
                raise Exception(f"Function '{function_name}' not found in contract")
            
            # Execute the function
            result = getattr(self, function_name)(caller, **params)
            
            # Calculate gas used (simplified)
            execution_time = time.time() - start_time
            gas_used = int(execution_time * 21000)  # Simplified gas calculation
            self.gas_used += gas_used
            
            execution_entry.update({
                'status': 'success',
                'result': result,
                'gas_used': gas_used,
                'execution_time': execution_time
            })
            
            return {
                'success': True,
                'result': result,
                'gas_used': gas_used,
                'execution_id': execution_entry['execution_id']
            }
            
        except Exception as e:
            execution_entry.update({
                'status': 'failed',
                'error': str(e),
                'gas_used': 21000  # Base gas for failed transactions
            })
            
            return {
                'success': False,
                'error': str(e),
                'gas_used': 21000,
                'execution_id': execution_entry['execution_id']
            }
        
        finally:
            self.execution_log.append(execution_entry)

class HealthcareAccessContract(SmartContract):
    """Smart contract for healthcare data access control"""
    
    def __init__(self, contract_id: str, creator: str):
        super().__init__(contract_id, creator, "HealthcareAccessControl v1.0")
        
        # Initialize state with role definitions
        self.state = {
            'access_tokens': {},  # Token registry for tracking active tokens
            'audit_log': [],      # Dedicated audit trail
            'roles': {
                'Doctor': {
                    'permissions': ['read', 'write', 'update', 'delete', 'prescribe'],
                    'data_types': ['all'],
                    'patient_access': 'assigned_patients',
                    'audit_level': 'detailed'
                },
                'Nurse': {
                    'permissions': ['read', 'write', 'update'],
                    'data_types': ['vital_signs', 'nursing_notes', 'medication_admin'],
                    'patient_access': 'ward_patients',
                    'audit_level': 'detailed'
                },
                'Lab Technician': {
                    'permissions': ['read', 'write'],
                    'data_types': ['lab_results', 'test_orders'],
                    'patient_access': 'test_patients',
                    'audit_level': 'standard'
                },
                'Patient': {
                    'permissions': ['read'],
                    'data_types': ['own_records'],
                    'patient_access': 'self_only',
                    'audit_level': 'basic'
                },
                'Insurance Provider': {
                    'permissions': ['read'],
                    'data_types': ['billing', 'claims', 'diagnosis'],
                    'patient_access': 'insured_patients',
                    'audit_level': 'detailed'
                },
                'Researcher': {
                    'permissions': ['read'],
                    'data_types': ['anonymized_data'],
                    'patient_access': 'anonymized_only',
                    'audit_level': 'research'
                }
            },
            'user_assignments': {},
            'patient_assignments': {},
            'access_rules': {},
            'consent_records': {},
            'audit_settings': {
                'log_all_access': True,
                'require_justification': ['Doctor', 'Nurse'],
                'max_session_duration': 8 * 3600,  # 8 hours
                'require_two_factor': ['Insurance Provider', 'Researcher']
            },
            'patient_assignments': {}  # Track actual patient assignments
        }
    
    def assign_role(self, caller: str, user_id: str, role: str, assigned_by: str) -> Dict[str, Any]:
        """Assign a role to a user"""
        # Check if caller has permission to assign roles
        if caller != self.creator and not self._has_admin_permission(caller):
            raise Exception("Unauthorized: Only admins can assign roles")
        
        if role not in self.state['roles']:
            raise Exception(f"Invalid role: {role}")
        
        # Assign the role - use authenticated caller, not user-supplied assigned_by
        self.state['user_assignments'][user_id] = {
            'role': role,
            'assigned_by': caller,  # Use authenticated caller to prevent spoofing
            'assigned_at': datetime.now().isoformat(),
            'status': 'active',
            'last_access': None
        }
        
        # Log role assignment - use authenticated caller, not user-supplied assigned_by
        self._log_access_event(caller, user_id, 'role_assignment', 'role_assigned', 
                             f"Assigned role: {role}")
        
        return {
            'user_id': user_id,
            'role': role,
            'assigned_by': caller,  # Use authenticated caller
            'status': 'assigned'
        }
    
    def assign_patient(self, caller: str, user_id: str, patient_id: str, reason: str = "") -> Dict[str, Any]:
        """Assign a patient to a healthcare provider"""
        
        # Only admins can assign patients
        if not self._has_admin_permission(caller):
            raise Exception("Unauthorized: Only admin can assign patients")
        
        # Ensure user exists and has appropriate role
        user_info = self.state['user_assignments'].get(user_id)
        if not user_info:
            raise Exception("User not found or not assigned a role")
        
        role = user_info['role']
        if role not in ['Doctor', 'Nurse', 'Lab Technician', 'Insurance Provider']:
            raise Exception(f"Role '{role}' cannot be assigned patients")
        
        # Add patient to user's assignment list
        if user_id not in self.state['patient_assignments']:
            self.state['patient_assignments'][user_id] = []
        
        if patient_id not in self.state['patient_assignments'][user_id]:
            self.state['patient_assignments'][user_id].append(patient_id)
        
        # Log patient assignment
        self._log_access_event(caller, patient_id, 'patient_assignment', 'patient_assigned', 
                             f"Assigned to {user_id} ({role}): {reason}")
        
        return {
            'user_id': user_id,
            'patient_id': patient_id,
            'assigned_by': caller,
            'assigned_at': datetime.now().isoformat(),
            'reason': reason
        }
    
    def request_access(self, caller: str, patient_id: str, data_type: str, 
                      justification: str = "", session_duration: int = 3600, 
                      two_factor_verified: bool = False) -> Dict[str, Any]:
        """Request access to patient data"""
        
        # Get caller's role
        user_info = self.state['user_assignments'].get(caller)
        if not user_info:
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"User not found or not assigned a role: {justification}")
            raise Exception("User not found or not assigned a role")
        
        role = user_info['role']
        role_permissions = self.state['roles'][role]
        
        # Enforce compliance settings
        audit_settings = self.state['audit_settings']
        
        # Check session duration limit
        max_duration = audit_settings['max_session_duration']
        if session_duration > max_duration:
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"Session duration {session_duration}s exceeds maximum {max_duration}s")
            raise Exception(f"Session duration {session_duration}s exceeds maximum {max_duration}s")
        
        # Check justification requirement
        if role in audit_settings['require_justification'] and not justification.strip():
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"Role '{role}' requires justification for data access")
            raise Exception(f"Role '{role}' requires justification for data access")
        
        # Check two-factor authentication requirement
        if role in audit_settings['require_two_factor'] and not two_factor_verified:
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"Role '{role}' requires two-factor authentication")
            raise Exception(f"Role '{role}' requires two-factor authentication")
        
        # Check if user can access this data type
        if not self._can_access_data_type(role, data_type):
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"Role '{role}' not authorized for data type '{data_type}'")
            raise Exception(f"Role '{role}' not authorized for data type '{data_type}'")
        
        # Check patient access permissions
        if not self._can_access_patient(caller, patient_id, role):
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"No permission to access patient {patient_id}")
            raise Exception(f"No permission to access patient {patient_id}")
        
        # Check consent if required
        consent_status = self._check_patient_consent(patient_id, caller, data_type)
        if not consent_status['granted']:
            # Log failed access attempt
            self._log_access_event(caller, patient_id, data_type, 'access_denied', 
                                 f"Patient consent required: {consent_status['reason']}")
            raise Exception(f"Patient consent required: {consent_status['reason']}")
        
        # Generate access token
        access_token = self._generate_access_token(caller, patient_id, data_type, session_duration)
        
        # Store token in registry
        self.state['access_tokens'][access_token] = {
            'user_id': caller,
            'patient_id': patient_id,
            'data_type': data_type,
            'issued_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=session_duration)).isoformat(),
            'status': 'active',
            'justification': justification
        }
        
        # Log the access request
        self._log_access_event(caller, patient_id, data_type, 'access_granted', justification)
        
        return {
            'access_granted': True,
            'access_token': access_token,
            'patient_id': patient_id,
            'data_type': data_type,
            'expires_at': (datetime.now() + timedelta(seconds=session_duration)).isoformat(),
            'session_duration': session_duration,
            'permissions': role_permissions['permissions']
        }
    
    def revoke_access(self, caller: str, access_token: str, reason: str = "") -> Dict[str, Any]:
        """Revoke an active access token"""
        
        # Check if token exists
        if access_token not in self.state['access_tokens']:
            raise Exception("Access token not found")
        
        token_info = self.state['access_tokens'][access_token]
        
        # Only admins or the token owner can revoke access
        if not self._has_admin_permission(caller) and not self._owns_token(caller, access_token):
            raise Exception("Unauthorized: Cannot revoke this access token")
        
        # Check if token is already revoked
        if token_info['status'] != 'active':
            raise Exception(f"Token is already {token_info['status']}")
        
        # Mark token as revoked
        token_info['status'] = 'revoked'
        token_info['revoked_by'] = caller
        token_info['revoked_at'] = datetime.now().isoformat()
        token_info['revocation_reason'] = reason
        
        revocation_id = str(uuid.uuid4())
        
        # Log the revocation
        self._log_access_event(caller, token_info['patient_id'], token_info['data_type'], 
                             'access_revoked', reason)
        
        return {
            'revocation_id': revocation_id,
            'access_token': access_token,
            'revoked_by': caller,
            'revoked_at': token_info['revoked_at'],
            'reason': reason
        }
    
    def set_patient_consent(self, caller: str, patient_id: str, data_types: List[str], 
                           authorized_roles: List[str], expiry_date: Optional[str] = None) -> Dict[str, Any]:
        """Set patient consent for data access"""
        
        # Only patients can set their own consent or admins can set on behalf
        if caller != patient_id and not self._has_admin_permission(caller):
            raise Exception("Unauthorized: Only patient or admin can set consent")
        
        consent_id = str(uuid.uuid4())
        consent_record = {
            'consent_id': consent_id,
            'patient_id': patient_id,
            'data_types': data_types,
            'authorized_roles': authorized_roles,
            'granted_at': datetime.now().isoformat(),
            'expiry_date': expiry_date,
            'granted_by': caller,
            'status': 'active'
        }
        
        self.state['consent_records'][patient_id] = consent_record
        
        # Log consent setting
        self._log_access_event(caller, patient_id, ','.join(data_types), 'consent_granted', 
                             f"Authorized roles: {','.join(authorized_roles)}")
        
        return {
            'consent_id': consent_id,
            'patient_id': patient_id,
            'status': 'granted',
            'data_types': data_types,
            'authorized_roles': authorized_roles
        }
    
    def get_audit_log(self, caller: str, patient_id: Optional[str] = None, 
                     start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve audit log for compliance reporting"""
        
        # Check if caller has audit permissions
        if not self._has_audit_permission(caller):
            raise Exception("Unauthorized: Insufficient permissions for audit log access")
        
        # Filter audit log based on parameters
        audit_entries = []
        for entry in self.state['audit_log']:
            # Apply filters
            if patient_id and entry.get('patient_id') != patient_id:
                continue
            
            if start_date and entry['timestamp'] < start_date:
                continue
                
            if end_date and entry['timestamp'] > end_date:
                continue
                
            # Include relevant audit information
            audit_entries.append(entry)
        
        return {
            'audit_entries': audit_entries,
            'total_entries': len(audit_entries),
            'generated_by': caller,
            'generated_at': datetime.now().isoformat(),
            'filters': {
                'patient_id': patient_id,
                'start_date': start_date,
                'end_date': end_date
            }
        }
    
    def _can_access_data_type(self, role: str, data_type: str) -> bool:
        """Check if role can access specific data type"""
        role_permissions = self.state['roles'].get(role, {})
        allowed_types = role_permissions.get('data_types', [])
        return 'all' in allowed_types or data_type in allowed_types
    
    def _can_access_patient(self, user_id: str, patient_id: str, role: str) -> bool:
        """Check if user can access specific patient"""
        role_permissions = self.state['roles'].get(role, {})
        patient_access = role_permissions.get('patient_access', 'none')
        
        if patient_access == 'all':
            return True
        elif patient_access == 'self_only':
            return user_id == patient_id
        elif patient_access == 'anonymized_only':
            # For researchers - only allow anonymized data
            return patient_id.startswith('ANON_')
        elif patient_access in ['assigned_patients', 'ward_patients', 'test_patients', 'insured_patients']:
            # Check actual patient assignments
            user_assignments = self.state['patient_assignments'].get(user_id, [])
            return patient_id in user_assignments
        
        return False
    
    def _check_patient_consent(self, patient_id: str, user_id: str, data_type: str) -> Dict[str, Any]:
        """Check if patient has given consent for this access"""
        consent_record = self.state['consent_records'].get(patient_id)
        
        if not consent_record:
            return {'granted': False, 'reason': 'No consent record found'}
        
        if consent_record['status'] != 'active':
            return {'granted': False, 'reason': 'Consent not active'}
        
        # Check if data type is covered
        if data_type not in consent_record['data_types']:
            return {'granted': False, 'reason': 'Data type not covered by consent'}
        
        # Check if user role is authorized
        user_role = self.state['user_assignments'].get(user_id, {}).get('role')
        if user_role not in consent_record['authorized_roles']:
            return {'granted': False, 'reason': 'User role not authorized by consent'}
        
        # Check expiry date
        if consent_record['expiry_date']:
            expiry = datetime.fromisoformat(consent_record['expiry_date'].replace('Z', '+00:00'))
            if datetime.now() > expiry:
                return {'granted': False, 'reason': 'Consent has expired'}
        
        return {'granted': True, 'reason': 'Valid consent'}
    
    def _generate_access_token(self, user_id: str, patient_id: str, data_type: str, duration: int) -> str:
        """Generate a secure access token"""
        token_data = {
            'user_id': user_id,
            'patient_id': patient_id,
            'data_type': data_type,
            'issued_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=duration)).isoformat()
        }
        
        # Create a hash-based token (simplified)
        token_string = json.dumps(token_data, sort_keys=True)
        return hashlib.sha256(token_string.encode()).hexdigest()
    
    def _log_access_event(self, user_id: str, patient_id: str, data_type: str, action: str, justification: str):
        """Log access events for audit trail"""
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'patient_id': patient_id,
            'data_type': data_type,
            'action': action,
            'justification': justification,
            'ip_address': f'192.168.1.{random.randint(100, 200)}',
            'session_id': hashlib.md5(f'{user_id}{action}{time.time()}'.encode()).hexdigest()[:16]
        }
        self.state['audit_log'].append(audit_entry)
    
    def _has_admin_permission(self, user_id: str) -> bool:
        """Check if user has admin permissions"""
        return user_id == self.creator
    
    def _has_audit_permission(self, user_id: str) -> bool:
        """Check if user can access audit logs"""
        # Only admins can access full audit logs for HIPAA/GDPR compliance
        return self._has_admin_permission(user_id)
    
    def _owns_token(self, user_id: str, access_token: str) -> bool:
        """Check if user owns the access token"""
        if access_token not in self.state['access_tokens']:
            return False
        
        token_info = self.state['access_tokens'][access_token]
        return token_info['user_id'] == user_id

class SmartContractManager:
    """Manager for smart contracts in the healthcare blockchain"""
    
    def __init__(self):
        self.contracts = {}
        self.deployment_log = []
    
    def deploy_contract(self, contract_type: str, creator: str, init_params: Optional[Dict[str, Any]] = None) -> str:
        """Deploy a new smart contract"""
        contract_id = f"CONTRACT_{int(time.time())}_{len(self.contracts)}"
        
        if contract_type == "HealthcareAccess":
            contract = HealthcareAccessContract(contract_id, creator)
        else:
            raise Exception(f"Unknown contract type: {contract_type}")
        
        # Initialize with parameters if provided
        if init_params:
            for key, value in init_params.items():
                if hasattr(contract, 'state'):
                    contract.state[key] = value
        
        self.contracts[contract_id] = contract
        
        # Log deployment
        deployment_entry = {
            'contract_id': contract_id,
            'contract_type': contract_type,
            'creator': creator,
            'deployed_at': datetime.now().isoformat(),
            'init_params': init_params or {}
        }
        self.deployment_log.append(deployment_entry)
        
        return contract_id
    
    def execute_contract(self, contract_id: str, function_name: str, 
                        params: Dict[str, Any], caller: str) -> Dict[str, Any]:
        """Execute a function on a deployed contract"""
        if contract_id not in self.contracts:
            raise Exception(f"Contract {contract_id} not found")
        
        contract = self.contracts[contract_id]
        return contract.execute(function_name, params, caller)
    
    def get_contract_state(self, contract_id: str, caller: str) -> Dict[str, Any]:
        """Get the current state of a contract"""
        if contract_id not in self.contracts:
            raise Exception(f"Contract {contract_id} not found")
        
        contract = self.contracts[contract_id]
        
        # Return public state (filter sensitive information)
        return {
            'contract_id': contract_id,
            'creator': contract.creator,
            'created_at': contract.created_at,
            'total_executions': len(contract.execution_log),
            'total_gas_used': contract.gas_used,
            'state_summary': {
                'roles_defined': len(contract.state.get('roles', {})),
                'users_assigned': len(contract.state.get('user_assignments', {})),
                'consent_records': len(contract.state.get('consent_records', {}))
            }
        }
    
    def get_execution_history(self, contract_id: str, caller: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution history for a contract"""
        if contract_id not in self.contracts:
            raise Exception(f"Contract {contract_id} not found")
        
        contract = self.contracts[contract_id]
        
        # Return recent executions (filtered for privacy)
        executions = contract.execution_log[-limit:]
        return [
            {
                'execution_id': exec['execution_id'],
                'function_name': exec['function_name'],
                'caller': exec['caller'],
                'timestamp': exec['timestamp'],
                'status': exec['status'],
                'gas_used': exec.get('gas_used', 0)
            }
            for exec in executions
        ]