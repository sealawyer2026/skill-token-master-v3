"""
Billing Module - 计费与统计
Token经济大师 v3.2.0
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os

@dataclass
class UsageRecord:
    """使用记录"""
    timestamp: float
    operation: str
    input_tokens: int
    output_tokens: int
    saved_tokens: int
    file_type: str
    success: bool

class UsageTracker:
    """使用统计追踪器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.expanduser('~/.token_master_v3/usage_db.json')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.records: List[UsageRecord] = []
        self._load()
    
    def _load(self):
        """加载历史记录"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.records = [UsageRecord(**r) for r in data]
            except:
                self.records = []
    
    def _save(self):
        """保存记录"""
        with open(self.db_path, 'w') as f:
            json.dump([asdict(r) for r in self.records], f, indent=2)
    
    def record(
        self,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        file_type: str = 'unknown',
        success: bool = True
    ):
        """记录一次使用"""
        saved = max(0, input_tokens - output_tokens)
        record = UsageRecord(
            timestamp=time.time(),
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            saved_tokens=saved,
            file_type=file_type,
            success=success
        )
        self.records.append(record)
        self._save()
        return record
    
    def get_stats(self, days: int = 30) -> Dict:
        """获取统计信息"""
        cutoff = time.time() - (days * 24 * 3600)
        recent = [r for r in self.records if r.timestamp > cutoff]
        
        if not recent:
            return {
                'total_calls': 0,
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_saved_tokens': 0,
                'savings_rate': 0,
                'success_rate': 0
            }
        
        total_input = sum(r.input_tokens for r in recent)
        total_output = sum(r.output_tokens for r in recent)
        total_saved = sum(r.saved_tokens for r in recent)
        success_count = sum(1 for r in recent if r.success)
        
        return {
            'total_calls': len(recent),
            'total_input_tokens': total_input,
            'total_output_tokens': total_output,
            'total_saved_tokens': total_saved,
            'savings_rate': (total_saved / total_input * 100) if total_input > 0 else 0,
            'success_rate': (success_count / len(recent) * 100) if recent else 0,
            'period_days': days
        }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """获取每日统计"""
        cutoff = time.time() - (days * 24 * 3600)
        recent = [r for r in self.records if r.timestamp > cutoff]
        
        # 按天分组
        daily = {}
        for r in recent:
            day = datetime.fromtimestamp(r.timestamp).strftime('%Y-%m-%d')
            if day not in daily:
                daily[day] = {'input': 0, 'output': 0, 'saved': 0, 'calls': 0}
            daily[day]['input'] += r.input_tokens
            daily[day]['output'] += r.output_tokens
            daily[day]['saved'] += r.saved_tokens
            daily[day]['calls'] += 1
        
        # 转换为列表
        result = []
        for day in sorted(daily.keys()):
            d = daily[day]
            result.append({
                'date': day,
                'calls': d['calls'],
                'input_tokens': d['input'],
                'output_tokens': d['output'],
                'saved_tokens': d['saved'],
                'savings_rate': (d['saved'] / d['input'] * 100) if d['input'] > 0 else 0
            })
        
        return result
    
    def print_report(self):
        """打印使用报告"""
        stats = self.get_stats(30)
        daily = self.get_daily_stats(7)
        
        print("\n" + "="*60)
        print("📊 Token经济大师 - 使用报告")
        print("="*60)
        print(f"\n过去30天统计:")
        print(f"  总调用次数: {stats['total_calls']}")
        print(f"  输入Token: {stats['total_input_tokens']:,}")
        print(f"  输出Token: {stats['total_output_tokens']:,}")
        print(f"  节省Token: {stats['total_saved_tokens']:,}")
        print(f"  节省比例: {stats['savings_rate']:.1f}%")
        print(f"  成功率: {stats['success_rate']:.1f}%")
        
        print(f"\n过去7天每日统计:")
        for d in daily:
            print(f"  {d['date']}: {d['calls']}次调用, 节省{d['savings_rate']:.1f}%")
        
        print("="*60)

class QuotaManager:
    """配额管理器"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.expanduser('~/.token_master_v3/quota.json')
        self.quotas = {}
        self.usage = {}
        self._load()
    
    def _load(self):
        """加载配额"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.quotas = data.get('quotas', {})
                    self.usage = data.get('usage', {})
            except:
                pass
    
    def _save(self):
        """保存配额"""
        with open(self.db_path, 'w') as f:
            json.dump({'quotas': self.quotas, 'usage': self.usage}, f, indent=2)
    
    def set_quota(self, user_id: str, monthly_limit: int):
        """设置用户配额"""
        self.quotas[user_id] = monthly_limit
        self._save()
    
    def check_quota(self, user_id: str, tokens: int) -> bool:
        """检查配额"""
        if user_id not in self.quotas:
            return True  # 无配额限制
        
        # 获取本月使用
        current_month = datetime.now().strftime('%Y-%m')
        key = f"{user_id}:{current_month}"
        used = self.usage.get(key, 0)
        
        return (used + tokens) <= self.quotas[user_id]
    
    def record_usage(self, user_id: str, tokens: int):
        """记录使用"""
        current_month = datetime.now().strftime('%Y-%m')
        key = f"{user_id}:{current_month}"
        self.usage[key] = self.usage.get(key, 0) + tokens
        self._save()
    
    def get_remaining(self, user_id: str) -> int:
        """获取剩余配额"""
        if user_id not in self.quotas:
            return -1  # 无限制
        
        current_month = datetime.now().strftime('%Y-%m')
        key = f"{user_id}:{current_month}"
        used = self.usage.get(key, 0)
        
        return max(0, self.quotas[user_id] - used)
