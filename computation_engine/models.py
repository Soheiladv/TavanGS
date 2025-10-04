"""
Computation Engine Models - Independent Calculation System
Pure computation service for all TakoTech products
"""

from django.db import models
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()


class ComputationSession(models.Model):
    """
    Track computation sessions for different products
    """
    
    SESSION_TYPES = [
        ('budget_calculation', 'Budget Calculation'),
        ('security_analysis', 'Security Analysis'),
        ('performance_test', 'Performance Test'),
        ('data_processing', 'Data Processing'),
        ('ai_inference', 'AI Inference'),
        ('custom', 'Custom Computation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Session identification
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Computation details
    session_type = models.CharField(max_length=30, choices=SESSION_TYPES)
    product_name = models.CharField(max_length=100, blank=True)
    
    # Input/Output data
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict, blank=True)
    
    # Processing info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_percentage = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    processing_time_seconds = models.FloatField(null=True, blank=True)
    memory_usage_mb = models.FloatField(null=True, blank=True)
    cpu_usage_percent = models.FloatField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    error_code = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Configuration
    configuration = models.JSONField(default=dict, blank=True)
    priority = models.PositiveIntegerField(default=5)  # 1-10, higher = more priority
    
    class Meta:
        verbose_name = 'Computation Session'
        verbose_name_plural = 'Computation Sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'session_type']),
        ]
    
    def __str__(self):
        return f"{self.session_type} - {self.session_id}"
    
    @property
    def duration(self):
        """Calculate session duration"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def update_progress(self, percentage, status=None):
        """Update computation progress"""
        self.progress_percentage = min(100, max(0, percentage))
        if status:
            self.status = status
        self.save(update_fields=['progress_percentage', 'status'])
    
    def mark_completed(self, output_data=None):
        """Mark session as completed"""
        from django.utils import timezone
        
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        
        if output_data:
            self.output_data = output_data
        
        self.save(update_fields=['status', 'progress_percentage', 'completed_at', 'output_data'])
    
    def mark_failed(self, error_message, error_code=None):
        """Mark session as failed"""
        from django.utils import timezone
        
        self.status = 'failed'
        self.error_message = error_message
        if error_code:
            self.error_code = error_code
        self.completed_at = timezone.now()
        
        self.save(update_fields=['status', 'error_message', 'error_code', 'completed_at'])


class ComputationTemplate(models.Model):
    """
    Predefined computation templates for different products
    """
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    session_type = models.CharField(max_length=30, choices=ComputationSession.SESSION_TYPES)
    
    # Template configuration
    input_schema = models.JSONField(default=dict, help_text="JSON schema for input validation")
    output_schema = models.JSONField(default=dict, help_text="Expected output structure")
    default_config = models.JSONField(default=dict, help_text="Default configuration values")
    
    # Processing requirements
    estimated_time_seconds = models.PositiveIntegerField(default=60)
    memory_requirement_mb = models.PositiveIntegerField(default=256)
    cpu_intensive = models.BooleanField(default=False)
    
    # Access control
    required_user_type = models.CharField(
        max_length=20,
        choices=[('free', 'Free'), ('premium', 'Premium'), ('enterprise', 'Enterprise')],
        default='free'
    )
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    success_rate = models.FloatField(default=100.0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Computation Template'
        verbose_name_plural = 'Computation Templates'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def can_be_used_by(self, user):
        """Check if user can use this template"""
        if not user or not user.is_authenticated:
            return self.required_user_type == 'free'
        
        user_type_hierarchy = {
            'free': 0,
            'premium': 1,
            'enterprise': 2,
            'admin': 3
        }
        
        required_level = user_type_hierarchy.get(self.required_user_type, 0)
        user_level = user_type_hierarchy.get(user.user_type, 0)
        
        return user_level >= required_level
    
    def increment_usage(self):
        """Increment usage counter"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class ComputationResult(models.Model):
    """
    Cached computation results for performance optimization
    """
    
    # Input hash for caching
    input_hash = models.CharField(max_length=64, unique=True)
    session_type = models.CharField(max_length=30, choices=ComputationSession.SESSION_TYPES)
    
    # Cached data
    input_data = models.JSONField()
    output_data = models.JSONField()
    configuration = models.JSONField(default=dict)
    
    # Metadata
    computation_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)
    
    # Cache management
    expires_at = models.DateTimeField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Computation Result'
        verbose_name_plural = 'Computation Results'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['input_hash', 'session_type']),
            models.Index(fields=['expires_at', 'is_valid']),
        ]
    
    def __str__(self):
        return f"Cached {self.session_type} - {self.input_hash[:8]}"
    
    @property
    def is_expired(self):
        """Check if cached result is expired"""
        if not self.expires_at:
            return False
        
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def increment_access(self):
        """Increment access counter and update last accessed time"""
        from django.utils import timezone
        
        self.access_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['access_count', 'last_accessed'])


class ComputationMetrics(models.Model):
    """
    System performance metrics for the computation engine
    """
    
    # Time period
    date = models.DateField(unique=True)
    
    # Session statistics
    total_sessions = models.PositiveIntegerField(default=0)
    completed_sessions = models.PositiveIntegerField(default=0)
    failed_sessions = models.PositiveIntegerField(default=0)
    cancelled_sessions = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    average_processing_time = models.FloatField(default=0)
    peak_processing_time = models.FloatField(default=0)
    average_memory_usage = models.FloatField(default=0)
    peak_memory_usage = models.FloatField(default=0)
    
    # Cache statistics
    cache_hit_rate = models.FloatField(default=0)
    cache_miss_count = models.PositiveIntegerField(default=0)
    
    # User statistics
    unique_users = models.PositiveIntegerField(default=0)
    free_user_sessions = models.PositiveIntegerField(default=0)
    premium_user_sessions = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Computation Metrics'
        verbose_name_plural = 'Computation Metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"
    
    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        if self.total_sessions == 0:
            return 0
        return (self.completed_sessions / self.total_sessions) * 100