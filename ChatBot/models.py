from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class VisitorSession(models.Model):
    """Track visitor sessions and website usage"""
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    total_duration = models.DurationField(default=timezone.timedelta)
    page_views = models.IntegerField(default=0)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['ip_address', 'session_key']
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.ip_address} - {self.first_visit.strftime('%Y-%m-%d %H:%M')}"

class PageVisit(models.Model):
    """Track individual page visits"""
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='visits')
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True)
    visit_time = models.DateTimeField(auto_now_add=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['-visit_time']
    
    def __str__(self):
        return f"{self.session.ip_address} visited {self.page_url}"

class ServiceUsage(models.Model):
    """Track which cryptography services users used"""
    SERVICE_CHOICES = [
        ('caesar', 'Caesar Cipher'),
        ('vigenere', 'Vigenère Cipher'),
        ('hill', 'Hill Cipher'),
        ('playfair', 'Playfair Cipher'),
        ('aes', 'AES Encryption'),
        ('des', 'DES Encryption'),
        ('rsa', 'RSA Encryption'),
        ('md5', 'MD5 Hash'),
        ('sha256', 'SHA-256 Hash'),
        ('sha512', 'SHA-512 Hash'),
        ('hmac', 'HMAC'),
        ('diffie_hellman', 'Diffie-Hellman Key Exchange'),
        ('chatbot', 'AI Chatbot'),
    ]
    
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    usage_time = models.DateTimeField(auto_now_add=True)
    input_data = models.TextField(blank=True)  # Store what they encrypted/decrypted
    output_data = models.TextField(blank=True)
    operation = models.CharField(max_length=20, blank=True)  # encrypt/decrypt/hash
    
    class Meta:
        ordering = ['-usage_time']
    
    def __str__(self):
        return f"{self.session.ip_address} used {self.get_service_type_display()}"

class ChatConversation(models.Model):
    """Track chatbot conversations"""
    session = models.ForeignKey(VisitorSession, on_delete=models.CASCADE, related_name='conversations')
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message_hash = models.CharField(max_length=32)  # MD5 hash for duplicate detection
    response_time = models.FloatField(null=True, blank=True)  # Response time in seconds
    tokens_used = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.session.ip_address} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class SecurityAlert(models.Model):
    """Track security incidents and blocked attempts"""
    ALERT_TYPES = [
        ('rate_limit', 'Rate Limit Exceeded'),
        ('malicious_content', 'Malicious Content Detected'),
        ('spam', 'Spam Attempt'),
        ('suspicious_activity', 'Suspicious Activity'),
    ]
    
    ip_address = models.GenericIPAddressField()
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)
    blocked_content = models.TextField(blank=True)
    severity = models.IntegerField(default=1)  # 1-5 scale
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Security Alert: {self.ip_address} - {self.get_alert_type_display()}"
