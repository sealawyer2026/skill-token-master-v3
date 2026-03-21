"""Token经济大师 v3.0 - 进化引擎（自学习系统）"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class EvolutionEngine:
    """进化引擎 - 实现技能的自我学习和迭代"""
    
    def __init__(self, data_dir: str = '~/.token_master_v3'):
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.learning_db = self.data_dir / 'learning_db.json'
        self.usage_count = 0
        self.evolution_threshold = 100  # 100次触发进化
        
        self._load_data()
    
    def _load_data(self):
        """加载学习数据"""
        if self.learning_db.exists():
            with open(self.learning_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.usage_count = data.get('usage_count', 0)
                self.cases = data.get('cases', [])
        else:
            self.cases = []
    
    def _save_data(self):
        """保存学习数据"""
        data = {
            'usage_count': self.usage_count,
            'cases': self.cases[-1000:],  # 只保留最近1000条
            'last_update': datetime.now().isoformat()
        }
        with open(self.learning_db, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record_optimization(self, original: str, optimized: str, 
                           saving_pct: float, content_type: str):
        """记录优化案例"""
        self.usage_count += 1
        
        case = {
            'timestamp': datetime.now().isoformat(),
            'original_size': len(original),
            'optimized_size': len(optimized),
            'saving_percentage': saving_pct,
            'content_type': content_type
        }
        
        self.cases.append(case)
        self._save_data()
        
        # 检查是否触发进化
        if self.usage_count % self.evolution_threshold == 0:
            return self._evolve()
        
        return None
    
    def _evolve(self) -> Dict[str, Any]:
        """执行进化"""
        print(f"🧬 第{self.usage_count // self.evolution_threshold}次进化触发！")
        
        # 分析最近的案例
        recent_cases = self.cases[-100:]
        
        # 计算各类型平均节省率
        type_stats = {}
        for case in recent_cases:
            ctype = case['content_type']
            if ctype not in type_stats:
                type_stats[ctype] = []
            type_stats[ctype].append(case['saving_percentage'])
        
        # 生成进化报告
        evolution_report = {
            'evolution_number': self.usage_count // self.evolution_threshold,
            'total_usage': self.usage_count,
            'type_performance': {
                ctype: {
                    'avg_saving': round(sum(pcts) / len(pcts), 1),
                    'best_case': round(max(pcts), 1),
                    'case_count': len(pcts)
                }
                for ctype, pcts in type_stats.items()
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ 进化完成！已学习 {len(recent_cases)} 个案例")
        
        return evolution_report
    
    def get_learning_report(self) -> Dict[str, Any]:
        """获取学习报告"""
        if not self.cases:
            return {'status': 'no_data', 'message': '暂无学习数据'}
        
        total_saving = sum(c['saving_percentage'] for c in self.cases)
        avg_saving = total_saving / len(self.cases)
        
        return {
            'status': 'active',
            'total_usage': self.usage_count,
            'total_cases': len(self.cases),
            'evolution_count': self.usage_count // self.evolution_threshold,
            'average_saving': round(avg_saving, 1),
            'next_evolution_in': self.evolution_threshold - (self.usage_count % self.evolution_threshold)
        }
