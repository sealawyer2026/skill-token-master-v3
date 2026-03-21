"""Token经济大师 v3.0 - 智能监控器"""

import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class IntelligentMonitor:
    """智能监控器 - 实时监控Token使用情况"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.baseline = {}
        self.current = {}
        self.alert_threshold = 10  # 10%增长触发预警
    
    def scan_project(self) -> Dict[str, Any]:
        """扫描项目Token使用情况"""
        stats = {
            'total_files': 0,
            'total_chars': 0,
            'total_tokens': 0,
            'file_breakdown': {}
        }
        
        for ext in ['*.py', '*.md', '*.json', '*.yaml', '*.yml']:
            for file_path in self.project_path.rglob(ext):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    chars = len(content)
                    tokens = chars // 4  # 粗略估算
                    
                    stats['total_files'] += 1
                    stats['total_chars'] += chars
                    stats['total_tokens'] += tokens
                    
                    rel_path = str(file_path.relative_to(self.project_path))
                    stats['file_breakdown'][rel_path] = {
                        'chars': chars,
                        'tokens': tokens
                    }
                except Exception:
                    pass
        
        return stats
    
    def set_baseline(self):
        """设置基线"""
        self.baseline = self.scan_project()
        print(f"📊 基线已设置: {self.baseline['total_tokens']} tokens")
    
    def check_changes(self) -> Optional[Dict[str, Any]]:
        """检查变化"""
        if not self.baseline:
            return None
        
        current = self.scan_project()
        
        baseline_tokens = self.baseline['total_tokens']
        current_tokens = current['total_tokens']
        
        change = current_tokens - baseline_tokens
        change_pct = (change / baseline_tokens * 100) if baseline_tokens > 0 else 0
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'baseline_tokens': baseline_tokens,
            'current_tokens': current_tokens,
            'change': change,
            'change_percentage': round(change_pct, 1),
            'alert': abs(change_pct) > self.alert_threshold
        }
        
        if result['alert']:
            direction = '增长' if change > 0 else '下降'
            print(f"⚠️ 预警: Token使用{direction} {abs(change_pct):.1f}%!")
        
        return result
    
    def watch(self, interval: int = 60):
        """持续监控"""
        print(f"👁️ 开始监控: {self.project_path}")
        print(f"⏱️ 检查间隔: {interval}秒")
        
        self.set_baseline()
        
        try:
            while True:
                time.sleep(interval)
                result = self.check_changes()
                if result and result['alert']:
                    print(f"🚨 检测到显著变化: {result['change_percentage']:+.1f}%")
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
