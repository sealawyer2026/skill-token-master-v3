"""
Resiliency Module - 弹性与容错
Token经济大师 v3.2.0
"""

import time
import random
from typing import Callable, Any, Optional
from functools import wraps

class RetryConfig:
    """重试配置"""
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

class RetryManager:
    """指数退避重试管理器"""
    
    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """执行带重试的函数"""
        last_exception = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.config.max_attempts:
                    break
                
                # 计算延迟
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
        
        # 所有重试失败
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """计算退避延迟"""
        delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))
        delay = min(delay, self.config.max_delay)
        
        if self.config.jitter:
            # 添加随机抖动 (0.5-1.5倍)
            delay *= random.uniform(0.5, 1.5)
        
        return delay

def with_retry(config: RetryConfig = None):
    """重试装饰器"""
    manager = RetryManager(config)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return manager.execute(func, *args, **kwargs)
        return wrapper
    return decorator

class FallbackManager:
    """降级策略管理器"""
    
    def __init__(self):
        self.fallbacks = {}
    
    def register(self, func_name: str, fallback_func: Callable):
        """注册降级函数"""
        self.fallbacks[func_name] = fallback_func
    
    def execute_with_fallback(self, func: Callable, *args, **kwargs) -> Any:
        """执行带降级的函数"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            func_name = func.__name__
            if func_name in self.fallbacks:
                print(f"⚠️  主功能失败，执行降级策略: {func_name}")
                return self.fallbacks[func_name](*args, **kwargs)
            raise e

class CircuitBreaker:
    """熔断器"""
    
    STATE_CLOSED = 'closed'      # 正常
    STATE_OPEN = 'open'          # 熔断
    STATE_HALF_OPEN = 'half_open'  # 半开
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = self.STATE_CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """带熔断保护的调用"""
        if self.state == self.STATE_OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = self.STATE_HALF_OPEN
                self.half_open_calls = 0
            else:
                raise Exception(f"熔断器开启，服务暂时不可用")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """成功处理"""
        if self.state == self.STATE_HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = self.STATE_CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """失败处理"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == self.STATE_HALF_OPEN:
            self.state = self.STATE_OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = self.STATE_OPEN
