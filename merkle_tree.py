import hashlib
import json
from typing import List, Optional, Dict, Any
import math

class MerkleNode:
    """A node in the Merkle tree"""
    def __init__(self, data: Optional[str] = None, left: Optional['MerkleNode'] = None, right: Optional['MerkleNode'] = None):
        self.data = data
        self.left = left
        self.right = right
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the node"""
        if self.data:
            # Leaf node - hash the data
            return hashlib.sha256(self.data.encode()).hexdigest()
        else:
            # Internal node - hash the concatenation of child hashes
            left_hash = self.left.hash if self.left else ""
            right_hash = self.right.hash if self.right else ""
            combined = left_hash + right_hash
            return hashlib.sha256(combined.encode()).hexdigest()
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return self.data is not None and self.left is None and self.right is None

class MerkleTree:
    """Merkle tree implementation for blockchain data integrity"""
    
    def __init__(self, data_list: List[str]):
        self.data_list = data_list.copy()
        self.root = self._build_tree(data_list)
        self.leaf_nodes = self._get_leaf_nodes()
    
    def _build_tree(self, data_list: List[str]) -> Optional[MerkleNode]:
        """Build the Merkle tree from a list of data"""
        if not data_list:
            return None
        
        # Create leaf nodes
        nodes = [MerkleNode(data) for data in data_list]
        
        # Build tree bottom-up
        while len(nodes) > 1:
            next_level = []
            
            # Process pairs of nodes
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else None
                
                # Create internal node
                if right is None:
                    # Duplicate the left node for odd number of nodes
                    parent = MerkleNode(left=left, right=left)
                else:
                    parent = MerkleNode(left=left, right=right)
                next_level.append(parent)
            
            nodes = next_level
        
        return nodes[0] if nodes else None
    
    def _get_leaf_nodes(self) -> List[MerkleNode]:
        """Get all leaf nodes in the tree"""
        if not self.root:
            return []
        
        leaves = []
        
        def collect_leaves(node: MerkleNode):
            if node.is_leaf():
                leaves.append(node)
            else:
                if node.left:
                    collect_leaves(node.left)
                if node.right:
                    collect_leaves(node.right)
        
        collect_leaves(self.root)
        return leaves
    
    def get_root_hash(self) -> str:
        """Get the root hash of the Merkle tree"""
        return self.root.hash if self.root else ""
    
    def generate_proof(self, data: str) -> List[Dict[str, Any]]:
        """Generate Merkle proof for a given data item"""
        if not self.root:
            return []
        
        # Find the leaf node containing the data
        target_leaf = None
        for leaf in self.leaf_nodes:
            if leaf.data == data:
                target_leaf = leaf
                break
        
        if not target_leaf:
            return []  # Data not found
        
        # Generate proof path from leaf to root
        proof = []
        current = target_leaf
        
        def find_proof_path(node: MerkleNode, target: MerkleNode, path: List[Dict[str, Any]]) -> bool:
            if node == target:
                return True
            
            if node.is_leaf():
                return False
            
            # Check left subtree
            if node.left and find_proof_path(node.left, target, path):
                # Target is in left subtree, add right sibling to proof
                if node.right:
                    path.append({
                        'hash': node.right.hash,
                        'position': 'right'
                    })
                return True
            
            # Check right subtree
            if node.right and find_proof_path(node.right, target, path):
                # Target is in left subtree, add left sibling to proof
                if node.left:
                    path.append({
                        'hash': node.left.hash,
                        'position': 'left'
                    })
                return True
            
            return False
        
        find_proof_path(self.root, target_leaf, proof)
        return proof
    
    def verify_proof(self, data: str, proof: List[Dict[str, Any]], root_hash: str) -> bool:
        """Verify a Merkle proof"""
        # Start with the hash of the data
        current_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # If proof is empty, this is only valid for single-leaf trees
        if not proof:
            return current_hash == root_hash
        
        # Apply each proof step
        for step in proof:
            sibling_hash = step['hash']
            position = step['position']
            
            if position == 'left':
                # Sibling is on the left
                combined = sibling_hash + current_hash
            else:
                # Sibling is on the right
                combined = current_hash + sibling_hash
            
            current_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return current_hash == root_hash
    
    def get_tree_visualization(self) -> Dict[str, Any]:
        """Get a visual representation of the tree structure"""
        if not self.root:
            return {}
        
        def serialize_node(node: MerkleNode, level: int = 0) -> Dict[str, Any]:
            node_data = {
                'hash': node.hash[:16] + '...',
                'full_hash': node.hash,
                'level': level,
                'is_leaf': node.is_leaf()
            }
            
            if node.is_leaf():
                node_data['data'] = node.data
            else:
                node_data['children'] = []
                if node.left:
                    node_data['children'].append(serialize_node(node.left, level + 1))
                if node.right:
                    node_data['children'].append(serialize_node(node.right, level + 1))
            
            return node_data
        
        return serialize_node(self.root)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the Merkle tree"""
        if not self.root:
            return {
                'total_nodes': 0,
                'leaf_nodes': 0,
                'tree_height': 0,
                'root_hash': None
            }
        
        def count_nodes(node: Optional[MerkleNode]) -> int:
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        def calculate_height(node: Optional[MerkleNode]) -> int:
            if not node or node.is_leaf():
                return 1
            left_height = calculate_height(node.left) if node.left else 0
            right_height = calculate_height(node.right) if node.right else 0
            return 1 + max(left_height, right_height)
        
        return {
            'total_nodes': count_nodes(self.root),
            'leaf_nodes': len(self.leaf_nodes),
            'tree_height': calculate_height(self.root),
            'root_hash': self.root.hash,
            'data_items': len(self.data_list)
        }

class HealthcareMerkleTree(MerkleTree):
    """Specialized Merkle tree for healthcare data"""
    
    def __init__(self, healthcare_records: List[Dict[str, Any]]):
        # Convert healthcare records to serialized strings
        self.records = healthcare_records
        data_strings = [json.dumps(record, sort_keys=True) for record in healthcare_records]
        super().__init__(data_strings)
    
    def add_healthcare_record(self, record: Dict[str, Any]) -> 'HealthcareMerkleTree':
        """Add a new healthcare record and rebuild the tree"""
        new_records = self.records + [record]
        return HealthcareMerkleTree(new_records)
    
    def verify_record_integrity(self, record: Dict[str, Any]) -> bool:
        """Verify that a healthcare record exists in the tree"""
        record_string = json.dumps(record, sort_keys=True)
        proof = self.generate_proof(record_string)
        return self.verify_proof(record_string, proof, self.get_root_hash())
    
    def get_healthcare_statistics(self) -> Dict[str, Any]:
        """Get healthcare-specific statistics"""
        base_stats = self.get_statistics()
        
        # Analyze record types
        record_types = {}
        total_size = 0
        
        for record in self.records:
            record_type = record.get('record_type', 'unknown')
            record_types[record_type] = record_types.get(record_type, 0) + 1
            total_size += len(json.dumps(record))
        
        base_stats.update({
            'record_types': record_types,
            'total_data_size_bytes': total_size,
            'average_record_size_bytes': total_size / len(self.records) if self.records else 0
        })
        
        return base_stats