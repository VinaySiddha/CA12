"""
Logging configuration and utilities
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
from app.core.config import settings


def setup_logging():
    """Setup application logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    return root_logger


class ContextualLogger:
    """Logger that includes contextual information"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context = {}
    
    def set_context(self, **kwargs):
        """Set context for subsequent log messages"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear all context"""
        self.context.clear()
    
    def _format_message(self, message: str) -> str:
        """Format message with context"""
        if self.context:
            context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{message} | {context_str}"
        return message
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context"""
        self.logger.debug(self._format_message(message), **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message with context"""
        self.logger.info(self._format_message(message), **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context"""
        self.logger.warning(self._format_message(message), **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message with context"""
        self.logger.error(self._format_message(message), **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message with context"""
        self.logger.critical(self._format_message(message), **kwargs)


class APILogger:
    """Specialized logger for API requests and responses"""
    
    def __init__(self):
        self.logger = logging.getLogger("api")
    
    def log_request(self, method: str, path: str, user_id: str = None, **kwargs):
        """Log API request"""
        context = {
            "method": method,
            "path": path,
            "user_id": user_id or "anonymous",
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.info(f"API Request: {method} {path}", extra=context)
    
    def log_response(self, method: str, path: str, status_code: int, 
                    response_time: float, user_id: str = None, **kwargs):
        """Log API response"""
        context = {
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "user_id": user_id or "anonymous",
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        log_level = logging.ERROR if status_code >= 500 else logging.WARNING if status_code >= 400 else logging.INFO
        self.logger.log(log_level, f"API Response: {method} {path} - {status_code}", extra=context)
    
    def log_error(self, method: str, path: str, error: Exception, user_id: str = None, **kwargs):
        """Log API error"""
        context = {
            "method": method,
            "path": path,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "user_id": user_id or "anonymous",
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.error(f"API Error: {method} {path} - {type(error).__name__}: {error}", extra=context)


class MatchmakingLogger:
    """Specialized logger for matchmaking operations"""
    
    def __init__(self):
        self.logger = logging.getLogger("matchmaking")
    
    def log_match_request(self, user_id: str, match_type: str, topics: list, **kwargs):
        """Log match request"""
        context = {
            "user_id": user_id,
            "match_type": match_type,
            "topics": topics,
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.info(f"Match request: {user_id} seeking {match_type} for {topics}", extra=context)
    
    def log_match_found(self, user_id: str, partner_id: str, score: float, **kwargs):
        """Log successful match"""
        context = {
            "user_id": user_id,
            "partner_id": partner_id,
            "compatibility_score": score,
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.info(f"Match found: {user_id} <-> {partner_id} (score: {score:.3f})", extra=context)
    
    def log_match_failure(self, user_id: str, reason: str, **kwargs):
        """Log match failure"""
        context = {
            "user_id": user_id,
            "failure_reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.warning(f"Match failed for {user_id}: {reason}", extra=context)


class SecurityLogger:
    """Specialized logger for security events"""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
        
        # Create security-specific file handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        security_handler = logging.handlers.RotatingFileHandler(
            log_dir / "security.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        security_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        security_handler.setFormatter(formatter)
        
        self.logger.addHandler(security_handler)
        self.logger.setLevel(logging.INFO)
    
    def log_login_attempt(self, username: str, success: bool, ip_address: str = None, **kwargs):
        """Log login attempt"""
        context = {
            "username": username,
            "success": success,
            "ip_address": ip_address or "unknown",
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Login {status}: {username} from {ip_address}", extra=context)
    
    def log_permission_denied(self, user_id: str, resource: str, action: str, **kwargs):
        """Log permission denied"""
        context = {
            "user_id": user_id,
            "resource": resource,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.warning(f"Permission denied: {user_id} tried to {action} {resource}", extra=context)
    
    def log_suspicious_activity(self, user_id: str, activity: str, details: str = None, **kwargs):
        """Log suspicious activity"""
        context = {
            "user_id": user_id,
            "activity": activity,
            "details": details or "",
            "timestamp": datetime.utcnow().isoformat()
        }
        context.update(kwargs)
        
        self.logger.warning(f"Suspicious activity: {activity} by {user_id}", extra=context)


# Global logger instances
def get_logger(name: str) -> logging.Logger:
    """Get a standard logger"""
    return logging.getLogger(name)


def get_contextual_logger(name: str) -> ContextualLogger:
    """Get a contextual logger"""
    return ContextualLogger(name)


def get_api_logger() -> APILogger:
    """Get API logger"""
    return APILogger()


def get_matchmaking_logger() -> MatchmakingLogger:
    """Get matchmaking logger"""
    return MatchmakingLogger()


def get_security_logger() -> SecurityLogger:
    """Get security logger"""
    return SecurityLogger()


# Initialize logging when module is imported
setup_logging()