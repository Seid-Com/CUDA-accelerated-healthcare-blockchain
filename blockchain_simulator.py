import hashlib
import time
import json
from datetime import datetime
import random
from merkle_tree import HealthcareMerkleTree

class BlockchainSimulator:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the genesis block"""
        genesis_block = {
            'index': 0,
            'timestamp': datetime.now().isoformat(),
            'data': 'Genesis Block - Healthcare Blockchain',
            'previous_hash': '',
            'nonce': 0,
            'hash': ''
        }
        genesis_block['hash'] = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def calculate_hash(self, block):
        """Calculate SHA-256 hash of a block"""
        # Include Merkle root in hash calculation if available
        hash_data = {
            'index': block['index'],
            'timestamp': block['timestamp'],
            'data': block['data'],
            'previous_hash': block['previous_hash'],
            'nonce': block['nonce']
        }
        
        # Add Merkle root to hash if present (for enhanced blocks)
        if 'merkle_root' in block:
            hash_data['merkle_root'] = block['merkle_root']
            hash_data['transaction_count'] = block['transaction_count']
        
        block_string = json.dumps(hash_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, data, difficulty, mining_mode="CPU"):
        """Mine a single block with specified difficulty"""
        previous_block = self.chain[-1]
        
        # Parse healthcare data if it's a string
        if isinstance(data, str):
            try:
                parsed_data = json.loads(data)
                # If parsed data is already a list, use it directly
                if isinstance(parsed_data, list):
                    healthcare_records = parsed_data
                else:
                    healthcare_records = [parsed_data]
            except json.JSONDecodeError:
                healthcare_records = [{'raw_data': data}]
        else:
            healthcare_records = [data] if not isinstance(data, list) else data
        
        # Create Merkle tree for the data
        merkle_tree = HealthcareMerkleTree(healthcare_records)
        
        new_block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'merkle_root': merkle_tree.get_root_hash(),
            'transaction_count': len(healthcare_records),
            'merkle_tree_stats': merkle_tree.get_healthcare_statistics(),
            'previous_hash': previous_block['hash'],
            'nonce': 0,
            'hash': ''
        }
        
        target = "0" * difficulty
        start_time = time.time()
        hash_attempts = 0
        
        # Simulate different mining speeds for CPU vs GPU
        if mining_mode == "CPU":
            # CPU mining simulation - slower hash rate
            base_delay = 0.0001  # 100 microseconds per hash
        else:  # GPU
            # GPU mining simulation - much faster hash rate
            base_delay = 0.000001  # 1 microsecond per hash (100x faster)
        
        while True:
            new_block['hash'] = self.calculate_hash(new_block)
            hash_attempts += 1
            
            if new_block['hash'].startswith(target):
                mining_time = time.time() - start_time
                hash_rate = hash_attempts / mining_time if mining_time > 0 else hash_attempts
                
                self.chain.append(new_block)
                
                return {
                    'block': new_block,
                    'mining_time': mining_time,
                    'hash_attempts': hash_attempts,
                    'hash_rate': hash_rate
                }
            
            new_block['nonce'] += 1
            
            # Add realistic delay based on mining mode
            if hash_attempts % 1000 == 0:  # Check every 1000 hashes
                time.sleep(base_delay * 1000)
    
    def mine_blocks(self, num_blocks, difficulty, block_size_kb, mining_mode="CPU"):
        """Mine multiple blocks and return performance metrics"""
        results = {
            'blocks': [],
            'block_times': [],
            'total_hashes': 0,
            'total_time': 0
        }
        
        start_time = time.time()
        
        for i in range(num_blocks):
            # Generate healthcare data for the block
            healthcare_data = self.generate_healthcare_data(block_size_kb)
            
            # Mine the block
            block_result = self.mine_block(healthcare_data, difficulty, mining_mode)
            
            results['blocks'].append(block_result['block'])
            results['block_times'].append(block_result['mining_time'])
            results['total_hashes'] += block_result['hash_attempts']
        
        results['total_time'] = time.time() - start_time
        results['avg_block_time'] = sum(results['block_times']) / len(results['block_times'])
        results['hash_rate'] = results['total_hashes'] / results['total_time'] if results['total_time'] > 0 else 0
        
        return results
    
    def generate_healthcare_data(self, size_kb):
        """Generate simulated healthcare data of specified size"""
        base_record = {
            'patient_id': f'PATIENT_{random.randint(1000, 9999)}',
            'record_type': random.choice(['lab_result', 'diagnosis', 'prescription', 'vital_signs']),
            'timestamp': datetime.now().isoformat(),
            'provider_id': f'PROVIDER_{random.randint(100, 999)}',
            'encrypted': True,
            'ipfs_hash': f'Qm{hashlib.sha256(str(random.random()).encode()).hexdigest()[:44]}'
        }
        
        # Pad the data to reach the desired size
        padding_size = max(0, (size_kb * 1024) - len(json.dumps(base_record)))
        base_record['data_payload'] = 'x' * padding_size
        
        return json.dumps(base_record)
    
    def verify_merkle_integrity(self, block_index):
        """Verify Merkle tree integrity for a specific block"""
        if block_index >= len(self.chain) or block_index < 0:
            return {'valid': False, 'error': 'Block index out of range'}
        
        block = self.chain[block_index]
        
        # Skip genesis block or blocks without Merkle root
        if 'merkle_root' not in block:
            return {'valid': True, 'note': 'Block does not have Merkle tree (legacy format)'}
        
        # Reconstruct Merkle tree from block data
        try:
            if isinstance(block['data'], str):
                parsed_data = json.loads(block['data'])
                # If parsed data is already a list, use it directly
                if isinstance(parsed_data, list):
                    healthcare_records = parsed_data
                else:
                    healthcare_records = [parsed_data]
            else:
                healthcare_records = [block['data']] if not isinstance(block['data'], list) else block['data']
            
            reconstructed_tree = HealthcareMerkleTree(healthcare_records)
            reconstructed_root = reconstructed_tree.get_root_hash()
            
            return {
                'valid': reconstructed_root == block['merkle_root'],
                'stored_root': block['merkle_root'],
                'computed_root': reconstructed_root,
                'transaction_count': block.get('transaction_count', 0),
                'tree_stats': reconstructed_tree.get_healthcare_statistics()
            }
        except Exception as e:
            return {'valid': False, 'error': f'Error verifying Merkle tree: {str(e)}'}
    
    def get_merkle_proof(self, block_index, record_data):
        """Generate Merkle proof for a specific record in a block"""
        if block_index >= len(self.chain) or block_index < 0:
            return {'success': False, 'error': 'Block index out of range'}
        
        block = self.chain[block_index]
        
        if 'merkle_root' not in block:
            return {'success': False, 'error': 'Block does not have Merkle tree'}
        
        try:
            if isinstance(block['data'], str):
                parsed_data = json.loads(block['data'])
                # If parsed data is already a list, use it directly
                if isinstance(parsed_data, list):
                    healthcare_records = parsed_data
                else:
                    healthcare_records = [parsed_data]
            else:
                healthcare_records = [block['data']] if not isinstance(block['data'], list) else block['data']
            
            tree = HealthcareMerkleTree(healthcare_records)
            record_string = json.dumps(record_data, sort_keys=True)
            proof = tree.generate_proof(record_string)
            
            return {
                'success': True,
                'proof': proof,
                'root_hash': tree.get_root_hash(),
                'record_verified': tree.verify_proof(record_string, proof, tree.get_root_hash())
            }
        except Exception as e:
            return {'success': False, 'error': f'Error generating proof: {str(e)}'}
    
    def get_chain_stats(self):
        """Get blockchain statistics"""
        return {
            'total_blocks': len(self.chain),
            'latest_block_hash': self.chain[-1]['hash'] if self.chain else None,
            'chain_valid': self.is_chain_valid()
        }
    
    def is_chain_valid(self):
        """Validate the blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is valid
            if current_block['hash'] != self.calculate_hash(current_block):
                return False
            
            # Check if current block points to previous block
            if current_block['previous_hash'] != previous_block['hash']:
                return False
        
        return True
