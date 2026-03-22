"""
Billing System Prototype - 计费系统原型 v3.2.0
支持使用统计、配额管理、计费计算
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class BillingTier:
    """计费档位"""
    name: str
    monthly_quota: int
    price_cny: float
    features: List[str]

class BillingEngine:
    """计费引擎"""
    
    TIERS = {
        'free': BillingTier('免费版', 50000, 0, ['基础优化', '5万Token/月']),
        'pro': BillingTier('专业版', 500000, 99, ['高级优化', '50万Token/月', 'API访问']),
        'enterprise': BillingTier('企业版', -1, 999, ['无限Token', '私有化部署', '专属支持']),
    }
    
    def __init__(self):
        self.user_tiers = {}  # user_id -> tier
        self.usage_records = []  # 使用记录
    
    def set_user_tier(self, user_id: str, tier: str):
        """设置用户档位"""
        if tier in self.TIERS:
            self.user_tiers[user_id] = tier
    
    def get_user_tier(self, user_id: str) -> BillingTier:
        """获取用户档位"""
        tier_name = self.user_tiers.get(user_id, 'free')
        return self.TIERS[tier_name]
    
    def record_usage(self, user_id: str, tokens: int, operation: str):
        """记录使用"""
        record = {
            'user_id': user_id,
            'timestamp': time.time(),
            'tokens': tokens,
            'operation': operation,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        self.usage_records.append(record)
    
    def get_monthly_usage(self, user_id: str, year_month: str = None) -> int:
        """获取月度使用"""
        if year_month is None:
            year_month = datetime.now().strftime('%Y-%m')
        
        total = sum(
            r['tokens'] for r in self.usage_records
            if r['user_id'] == user_id and r['date'].startswith(year_month)
        )
        return total
    
    def check_quota(self, user_id: str, requested_tokens: int) -> Dict:
        """检查配额"""
        tier = self.get_user_tier(user_id)
        used = self.get_monthly_usage(user_id)
        
        if tier.monthly_quota == -1:  # 无限
            return {'allowed': True, 'remaining': -1}
        
        remaining = tier.monthly_quota - used
        allowed = (used + requested_tokens) <= tier.monthly_quota
        
        return {
            'allowed': allowed,
            'used': used,
            'quota': tier.monthly_quota,
            'remaining': remaining,
            'tier': tier.name
        }
    
    def calculate_cost(self, tokens: int, tier: str = 'pro') -> float:
        """计算成本"""
        # 按量计费: 每1000Token 0.1元
        base_cost = (tokens / 1000) * 0.1
        
        # 档位折扣
        discounts = {'free': 1.0, 'pro': 0.8, 'enterprise': 0.5}
        discount = discounts.get(tier, 1.0)
        
        return base_cost * discount
    
    def generate_invoice(self, user_id: str, year_month: str = None) -> Dict:
        """生成账单"""
        if year_month is None:
            year_month = datetime.now().strftime('%Y-%m')
        
        tier = self.get_user_tier(user_id)
        usage = self.get_monthly_usage(user_id, year_month)
        
        # 计算费用
        if tier.price_cny > 0:
            # 订阅费 + 超额费
            base_fee = tier.price_cny
            overage = max(0, usage - tier.monthly_quota) if tier.monthly_quota > 0 else 0
            overage_fee = self.calculate_cost(overage, self.user_tiers.get(user_id, 'pro'))
            total = base_fee + overage_fee
        else:
            # 免费档
            base_fee = 0
            overage_fee = 0
            total = 0
        
        return {
            'user_id': user_id,
            'period': year_month,
            'tier': tier.name,
            'tier_price': tier.price_cny,
            'usage_tokens': usage,
            'base_fee': base_fee,
            'overage_fee': overage_fee,
            'total': total,
            'currency': 'CNY'
        }

class UsageDashboard:
    """使用统计面板"""
    
    def __init__(self, billing_engine: BillingEngine):
        self.billing = billing_engine
    
    def get_user_stats(self, user_id: str) -> Dict:
        """获取用户统计"""
        tier = self.billing.get_user_tier(user_id)
        usage = self.billing.get_monthly_usage(user_id)
        
        # 计算节省
        saved = self._calculate_savings(user_id)
        
        return {
            'user_id': user_id,
            'tier': tier.name,
            'tier_price': tier.price_cny,
            'monthly_quota': tier.monthly_quota,
            'used_tokens': usage,
            'remaining': tier.monthly_quota - usage if tier.monthly_quota > 0 else -1,
            'usage_percentage': (usage / tier.monthly_quota * 100) if tier.monthly_quota > 0 else 0,
            'tokens_saved': saved,
            'cost_savings': saved * 0.001  # 假设每Token 0.001元
        }
    
    def _calculate_savings(self, user_id: str) -> int:
        """计算节省的Token"""
        # 从使用记录中计算
        records = [r for r in self.billing.usage_records if r['user_id'] == user_id]
        return sum(r.get('saved', 0) for r in records)
    
    def get_system_stats(self) -> Dict:
        """获取系统统计"""
        total_users = len(self.billing.user_tiers)
        total_usage = sum(r['tokens'] for r in self.billing.usage_records)
        
        tier_distribution = {}
        for tier in self.billing.user_tiers.values():
            tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
        
        return {
            'total_users': total_users,
            'total_tokens_processed': total_usage,
            'tier_distribution': tier_distribution,
            'avg_savings_rate': 50.0  # 假设平均节省50%
        }
    
    def print_report(self, user_id: str):
        """打印用户报告"""
        stats = self.get_user_stats(user_id)
        
        print("\n" + "="*60)
        print(f"📊 Token经济大师 - 使用报告")
        print("="*60)
        print(f"用户: {stats['user_id']}")
        print(f"档位: {stats['tier']} (¥{stats['tier_price']}/月)")
        print(f"\n本月使用:")
        print(f"  已用: {stats['used_tokens']:,} Token")
        if stats['remaining'] >= 0:
            print(f"  剩余: {stats['remaining']:,} Token")
            print(f"  使用率: {stats['usage_percentage']:.1f}%")
        else:
            print(f"  剩余: 无限")
        print(f"\n节省统计:")
        print(f"  节省Token: {stats['tokens_saved']:,}")
        print(f"  节省费用: ¥{stats['cost_savings']:.2f}")
        print("="*60)
