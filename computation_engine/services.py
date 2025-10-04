"""
Computation Engine Services - Abstract Service Layer
Pure Python services for different computation types
"""

import json
import hashlib
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from django.utils import timezone

from .models import ComputationSession, ComputationResult, ComputationTemplate

logger = logging.getLogger(__name__)


class BaseComputationService(ABC):
    """
    Abstract base class for all computation services
    """
    
    def __init__(self, user=None, session_type=None):
        self.user = user
        self.session_type = session_type or self.get_session_type()
        self.session = None
    
    @abstractmethod
    def get_session_type(self):
        """Return the session type for this service"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass
    
    @abstractmethod
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual computation"""
        pass
    
    def execute_with_session(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute computation with session tracking
        """
        try:
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            # Check for cached result
            cached_result = self.get_cached_result(input_data)
            if cached_result:
                logger.info(f"Using cached result for {self.session_type}")
                return cached_result
            
            # Create computation session
            self.session = self.create_session(input_data)
            
            # Execute computation
            start_time = time.time()
            result = self.execute_computation(input_data)
            processing_time = time.time() - start_time
            
            # Update session with results
            self.session.mark_completed(result)
            self.session.processing_time_seconds = processing_time
            self.session.save()
            
            # Cache the result
            self.cache_result(input_data, result, processing_time)
            
            logger.info(f"Computation completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Computation failed: {str(e)}")
            if self.session:
                self.session.mark_failed(str(e))
            raise
    
    def create_session(self, input_data: Dict[str, Any]) -> ComputationSession:
        """Create a new computation session"""
        session = ComputationSession.objects.create(
            user=self.user,
            session_type=self.session_type,
            input_data=input_data,
            status='processing',
            started_at=timezone.now()
        )
        return session
    
    def get_cached_result(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check for cached computation result"""
        input_hash = self.generate_input_hash(input_data)
        
        try:
            cached = ComputationResult.objects.get(
                input_hash=input_hash,
                session_type=self.session_type,
                is_valid=True
            )
            
            # Check if expired
            if cached.is_expired:
                cached.is_valid = False
                cached.save()
                return None
            
            # Increment access count
            cached.increment_access()
            return cached.output_data
            
        except ComputationResult.DoesNotExist:
            return None  
    def cache_result(self, input_data: Dict[str, Any], output_data: Dict[str, Any], 
                    processing_time: float):
        """Cache computation result"""
        input_hash = self.generate_input_hash(input_data)
        
        # Set expiration time (24 hours for most computations)
        expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        ComputationResult.objects.update_or_create(
            input_hash=input_hash,
            session_type=self.session_type,
            defaults={
                'input_data': input_data,
                'output_data': output_data,
                'computation_time': processing_time,
                'expires_at': expires_at,
                'is_valid': True
            }
        )
    
    def generate_input_hash(self, input_data: Dict[str, Any]) -> str:
        """Generate hash for input data"""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(input_data, sort_keys=True)
        return hashlib.sha256(sorted_data.encode()).hexdigest()


class BudgetCalculationService(BaseComputationService):
    """
    Service for budget calculations and financial planning
    """
    
    def get_session_type(self):
        return 'budget_calculation'
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate budget calculation input"""
        required_fields = ['income', 'expenses', 'period']
        
        for field in required_fields:
            if field not in input_data:
                return False
        
        # Validate income and expenses are positive numbers
        try:
            income = float(input_data['income'])
            expenses = float(input_data['expenses'])
            
            if income < 0 or expenses < 0:
                return False
                
        except (ValueError, TypeError):
            return False
        
        return True
    
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute budget calculation"""
        income = float(input_data['income'])
        expenses = float(input_data['expenses'])
        period = input_data.get('period', 'monthly')
        
        # Basic budget calculations
        net_income = income - expenses
        savings_rate = (net_income / income * 100) if income > 0 else 0
        
        # Calculate recommendations
        recommendations = []
        if savings_rate < 10:
            recommendations.append("در نظر بگیرید هزینه‌های خود را کاهش دهید")
        elif savings_rate > 30:
            recommendations.append("می‌توانید بخشی از پس‌انداز را سرمایه‌گذاری کنید")
        
        # Calculate future projections
        monthly_savings = net_income
        yearly_savings = monthly_savings * 12
        five_year_savings = yearly_savings * 5
        
        result = {
            'net_income': net_income,
            'savings_rate': round(savings_rate, 2),
            'recommendations': recommendations,
            'projections': {
                'monthly_savings': monthly_savings,
                'yearly_savings': yearly_savings,
                'five_year_savings': five_year_savings
            },
            'period': period,
            'calculated_at': timezone.now().isoformat()
        }
        
        return result


class SecurityAnalysisService(BaseComputationService):
    """
    Service for security analysis and vulnerability assessment
    """
    
    def get_session_type(self):
        return 'security_analysis'
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate security analysis input"""
        required_fields = ['target_type', 'analysis_type']
        
        for field in required_fields:
            if field not in input_data:
                return False
        
        return True
    
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute security analysis"""
        target_type = input_data['target_type']
        analysis_type = input_data['analysis_type']
        
        # Simulate security analysis
        vulnerabilities = []
        security_score = 85  # Base score
        
        if target_type == 'website':
            vulnerabilities.extend([
                {'type': 'SSL Certificate', 'severity': 'medium', 'description': 'SSL certificate expires in 30 days'},
                {'type': 'SQL Injection', 'severity': 'low', 'description': 'Potential SQL injection vulnerability detected'}
            ])
            security_score -= 15
        
        elif target_type == 'network':
            vulnerabilities.extend([
                {'type': 'Open Ports', 'severity': 'high', 'description': 'Multiple unnecessary ports are open'},
                {'type': 'Weak Passwords', 'severity': 'critical', 'description': 'Default passwords detected'}
            ])
            security_score -= 25
        
        # Generate recommendations
        recommendations = []
        if security_score < 70:
            recommendations.append("امنیت سیستم نیاز به بهبود فوری دارد")
        elif security_score < 85:
            recommendations.append("برخی مسائل امنیتی نیاز به توجه دارند")
        else:
            recommendations.append("امنیت سیستم در سطح قابل قبولی است")
        
        result = {
            'security_score': max(0, security_score),
            'vulnerabilities': vulnerabilities,
            'recommendations': recommendations,
            'analysis_type': analysis_type,
            'target_type': target_type,
            'analyzed_at': timezone.now().isoformat()
        }
        
        return result


class AIInferenceService(BaseComputationService):
    """
    Service for AI inference and machine learning predictions
    """
    
    def get_session_type(self):
        return 'ai_inference'
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate AI inference input"""
        required_fields = ['model_type', 'input_data']
        
        for field in required_fields:
            if field not in input_data:
                return False
        
        return True
    
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI inference"""
        model_type = input_data['model_type']
        data = input_data['input_data']
        
        # Simulate AI inference based on model type
        if model_type == 'sentiment_analysis':
            # Simple sentiment analysis simulation
            text = data.get('text', '')
            positive_words = ['خوب', 'عالی', 'ممتاز', 'عالی', 'بسیار خوب']
            negative_words = ['بد', 'ضعیف', 'مشکل', 'خراب', 'بد']
            
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            if positive_count > negative_count:
                sentiment = 'positive'
                confidence = 0.8
            elif negative_count > positive_count:
                sentiment = 'negative'
                confidence = 0.8
            else:
                sentiment = 'neutral'
                confidence = 0.6
            
            result = {
                'sentiment': sentiment,
                'confidence': confidence,
                'model_type': model_type,
                'processed_at': timezone.now().isoformat()
            }
            
        elif model_type == 'classification':
            # Simple classification simulation
            categories = ['تکنولوژی', 'ورزش', 'سیاست', 'اقتصاد', 'سلامت']
            predicted_category = categories[len(data) % len(categories)]
            confidence = 0.75 + (len(data) % 25) / 100
            
            result = {
                'predicted_category': predicted_category,
                'confidence': round(confidence, 2),
                'all_categories': categories,
                'model_type': model_type,
                'processed_at': timezone.now().isoformat()
            }
        
        else:
            # Generic AI inference
            result = {
                'prediction': 'AI inference completed',
                'model_type': model_type,
                'confidence': 0.7,
                'processed_at': timezone.now().isoformat()
            }
        
        return result


class DataProcessingService(BaseComputationService):
    """
    Service for data processing and transformation
    """
    
    def get_session_type(self):
        return 'data_processing'
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate data processing input"""
        required_fields = ['data', 'operation']
        
        for field in required_fields:
            if field not in input_data:
                return False
        
        return True
    
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data processing"""
        data = input_data['data']
        operation = input_data['operation']
        
        # Simulate data processing
        if operation == 'aggregation':
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                result = {
                    'sum': sum(data),
                    'average': sum(data) / len(data),
                    'min': min(data),
                    'max': max(data),
                    'count': len(data),
                    'operation': operation,
                    'processed_at': timezone.now().isoformat()
                }
            else:
                result = {
                    'error': 'Invalid data type for aggregation',
                    'operation': operation,
                    'processed_at': timezone.now().isoformat()
                }
        
        elif operation == 'filter':
            # Simple filtering simulation
            filtered_data = [item for item in data if isinstance(item, str) and len(item) > 3]
            result = {
                'original_count': len(data),
                'filtered_count': len(filtered_data),
                'filtered_data': filtered_data[:10],  # Limit output
                'operation': operation,
                'processed_at': timezone.now().isoformat()
            }
        
        else:
            result = {
                'message': f'Data processing completed for operation: {operation}',
                'data_size': len(data) if isinstance(data, list) else 1,
                'operation': operation,
                'processed_at': timezone.now().isoformat()
            }
        
        return result


class PerformanceTestService(BaseComputationService):
    """
    Service for performance testing and benchmarking
    """
    
    def get_session_type(self):
        return 'performance_test'
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate performance test input"""
        required_fields = ['test_type', 'duration']
        
        for field in required_fields:
            if field not in input_data:
                return False
        
        return True
    
    def execute_computation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute performance test"""
        test_type = input_data['test_type']
        duration = int(input_data['duration'])
        
        # Simulate performance test
        start_time = time.time()
        
        # Simulate different types of tests
        if test_type == 'cpu_intensive':
            # Simulate CPU intensive task
            iterations = duration * 1000000
            result_sum = sum(i * i for i in range(iterations))
            
        elif test_type == 'memory_intensive':
            # Simulate memory intensive task
            data_size = duration * 1024 * 1024  # MB
            test_data = [0] * data_size
            result_sum = sum(test_data)
            
        elif test_type == 'io_intensive':
            # Simulate IO intensive task
            time.sleep(duration / 10)  # Simulate IO delay
            result_sum = duration
            
        else:
            # Generic test
            time.sleep(duration / 5)
            result_sum = duration
        
        actual_duration = time.time() - start_time
        
        # Calculate performance metrics
        cpu_usage = min(100, duration * 10)  # Simulated CPU usage
        memory_usage = min(1024, duration * 50)  # Simulated memory usage in MB
        
        result = {
            'test_type': test_type,
            'requested_duration': duration,
            'actual_duration': round(actual_duration, 2),
            'cpu_usage_percent': cpu_usage,
            'memory_usage_mb': memory_usage,
            'throughput': round(duration / actual_duration, 2),
            'status': 'completed',
            'tested_at': timezone.now().isoformat()
        }
        
        return result