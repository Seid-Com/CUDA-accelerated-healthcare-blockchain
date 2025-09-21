import time
import random
import math
import hashlib
from datetime import datetime

class PerformanceMetrics:
    def __init__(self):
        # Performance characteristics based on research paper
        self.cpu_aes_throughput_range = (50, 100)  # MB/s
        self.gpu_aes_throughput_range = (500, 2000)  # MB/s (5x-40x improvement)
        self.cpu_mining_hashrate = (1, 5)  # MH/s
        self.gpu_mining_hashrate = (50, 500)  # MH/s (50x-500x improvement)
    
    def run_benchmark(self, file_sizes_mb, operation_type):
        """Run performance benchmark simulation"""
        
        results = {
            'file_sizes': file_sizes_mb,
            'cpu_encryption_times': [],
            'gpu_encryption_times': [],
            'cpu_mining_throughput': 0,
            'gpu_mining_throughput': 0
        }
        
        # Encryption benchmarks
        if operation_type in ["AES-CTR Encryption", "Both"]:
            for size_mb in file_sizes_mb:
                # CPU encryption simulation
                cpu_throughput = random.uniform(*self.cpu_aes_throughput_range)
                cpu_time = size_mb / cpu_throughput
                
                # Add some variability based on file size (larger files are more efficient)
                efficiency_factor = min(1.2, 1 + (size_mb / 1000) * 0.2)
                cpu_time /= efficiency_factor
                
                results['cpu_encryption_times'].append(cpu_time)
                
                # GPU encryption simulation
                gpu_throughput = random.uniform(*self.gpu_aes_throughput_range)
                gpu_time = size_mb / gpu_throughput
                
                # GPU efficiency improves significantly with larger files
                gpu_efficiency_factor = min(2.0, 1 + (size_mb / 500) * 1.0)
                gpu_time /= gpu_efficiency_factor
                
                results['gpu_encryption_times'].append(gpu_time)
        
        # Mining benchmarks
        if operation_type in ["SHA-256 Mining", "Both"]:
            results['cpu_mining_throughput'] = random.uniform(*self.cpu_mining_hashrate)
            results['gpu_mining_throughput'] = random.uniform(*self.gpu_mining_hashrate)
        
        return results
    
    def calculate_throughput_improvement(self, cpu_time, gpu_time):
        """Calculate throughput improvement factor"""
        if gpu_time <= 0:
            return 100  # Maximum improvement cap
        
        improvement = cpu_time / gpu_time
        return min(100, improvement)  # Cap at 100x as mentioned in paper
    
    def simulate_real_world_performance(self, workload_type, data_size_mb):
        """Simulate real-world performance scenarios"""
        
        scenarios = {
            'hospital_ehr_daily': {
                'description': 'Daily EHR processing at medium hospital',
                'record_count': 5000,
                'avg_record_size_kb': 25,
                'concurrent_users': 100,
                'peak_hours': 8
            },
            'clinic_records': {
                'description': 'Small clinic daily records',
                'record_count': 500,
                'avg_record_size_kb': 15,
                'concurrent_users': 20,
                'peak_hours': 6
            },
            'medical_imaging': {
                'description': 'Medical imaging department',
                'record_count': 200,
                'avg_record_size_kb': 5000,  # Large image files
                'concurrent_users': 30,
                'peak_hours': 10
            },
            'research_dataset': {
                'description': 'Research dataset processing',
                'record_count': 100000,
                'avg_record_size_kb': 10,
                'concurrent_users': 10,
                'peak_hours': 24  # Continuous processing
            }
        }
        
        scenario = scenarios.get(workload_type, scenarios['hospital_ehr_daily'])
        
        # Calculate total data volume
        total_data_mb = (scenario['record_count'] * scenario['avg_record_size_kb']) / 1024
        
        # Simulate CPU performance
        cpu_throughput = random.uniform(*self.cpu_aes_throughput_range)
        cpu_total_time = total_data_mb / cpu_throughput
        
        # Simulate GPU performance
        gpu_throughput = random.uniform(*self.gpu_aes_throughput_range)
        gpu_total_time = total_data_mb / gpu_throughput
        
        # Account for concurrent access
        concurrency_factor = math.log(scenario['concurrent_users'] + 1)
        cpu_total_time *= concurrency_factor
        gpu_total_time *= (concurrency_factor * 0.3)  # GPU handles concurrency better
        
        return {
            'scenario': scenario,
            'total_data_mb': total_data_mb,
            'cpu_processing_time_hours': cpu_total_time / 3600,
            'gpu_processing_time_hours': gpu_total_time / 3600,
            'time_savings_hours': (cpu_total_time - gpu_total_time) / 3600,
            'throughput_improvement': cpu_total_time / gpu_total_time if gpu_total_time > 0 else 1,
            'cost_efficiency': self._calculate_cost_efficiency(cpu_total_time, gpu_total_time)
        }
    
    def _calculate_cost_efficiency(self, cpu_time, gpu_time):
        """Calculate cost efficiency of GPU vs CPU"""
        
        # Simplified cost model ($/hour)
        cpu_cost_per_hour = 0.50  # CPU computing cost
        gpu_cost_per_hour = 2.00  # GPU computing cost (higher but much faster)
        
        cpu_total_cost = (cpu_time / 3600) * cpu_cost_per_hour
        gpu_total_cost = (gpu_time / 3600) * gpu_cost_per_hour
        
        return {
            'cpu_cost_dollars': cpu_total_cost,
            'gpu_cost_dollars': gpu_total_cost,
            'cost_savings_dollars': cpu_total_cost - gpu_total_cost,
            'cost_efficiency_ratio': cpu_total_cost / gpu_total_cost if gpu_total_cost > 0 else 1
        }
    
    def benchmark_hash_functions(self):
        """Benchmark different hash functions used in blockchain"""
        
        test_data = b"Healthcare blockchain test data " * 1000  # ~32KB test data
        iterations = 1000
        
        results = {}
        
        # SHA-256 benchmark
        start_time = time.time()
        for _ in range(iterations):
            hashlib.sha256(test_data).hexdigest()
        sha256_time = time.time() - start_time
        
        results['SHA-256'] = {
            'time_seconds': sha256_time,
            'hashes_per_second': iterations / sha256_time,
            'mb_per_second': (len(test_data) * iterations / (1024 * 1024)) / sha256_time
        }
        
        # SHA-3 benchmark
        start_time = time.time()
        for _ in range(iterations):
            hashlib.sha3_256(test_data).hexdigest()
        sha3_time = time.time() - start_time
        
        results['SHA-3'] = {
            'time_seconds': sha3_time,
            'hashes_per_second': iterations / sha3_time,
            'mb_per_second': (len(test_data) * iterations / (1024 * 1024)) / sha3_time
        }
        
        # MD5 benchmark (for comparison)
        start_time = time.time()
        for _ in range(iterations):
            hashlib.md5(test_data).hexdigest()
        md5_time = time.time() - start_time
        
        results['MD5'] = {
            'time_seconds': md5_time,
            'hashes_per_second': iterations / md5_time,
            'mb_per_second': (len(test_data) * iterations / (1024 * 1024)) / md5_time
        }
        
        return results
    
    def predict_scalability(self, current_tps, target_tps, improvement_factor):
        """Predict system scalability with GPU acceleration"""
        
        current_gpu_tps = current_tps * improvement_factor
        
        if current_gpu_tps >= target_tps:
            return {
                'achievable': True,
                'current_cpu_tps': current_tps,
                'current_gpu_tps': current_gpu_tps,
                'target_tps': target_tps,
                'headroom_factor': current_gpu_tps / target_tps,
                'recommendation': 'Target achievable with current GPU acceleration'
            }
        else:
            additional_improvement_needed = target_tps / current_gpu_tps
            return {
                'achievable': False,
                'current_cpu_tps': current_tps,
                'current_gpu_tps': current_gpu_tps,
                'target_tps': target_tps,
                'additional_improvement_needed': additional_improvement_needed,
                'recommendation': f'Need {additional_improvement_needed:.1f}x more improvement or additional GPU resources'
            }
