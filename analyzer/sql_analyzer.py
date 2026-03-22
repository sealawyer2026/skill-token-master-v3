"""
SQL Analyzer - SQL查询分析器
Token经济大师 v3.2.0
"""

import re
import sqlparse
from typing import Dict, List, Tuple

class SQLAnalyzer:
    """SQL查询分析器"""
    
    def __init__(self):
        self.issues = []
    
    def analyze(self, sql: str) -> Dict:
        """分析 SQL 查询"""
        self.issues = []
        
        # 格式化 SQL
        formatted = sqlparse.format(sql, reindent=True, keyword_case='upper')
        
        # 检测问题
        self._detect_select_star(sql)
        self._detect_missing_where(sql)
        self._detect_inefficient_joins(sql)
        self._detect_redundant_order_by(sql)
        self._detect_nesting(sql)
        
        # 计算指标
        lines = formatted.split('\n')
        tokens = sql.split()
        
        return {
            'type': 'sql',
            'issues': self.issues,
            'metrics': {
                'total_lines': len(lines),
                'total_tokens': len(tokens),
                'total_issues': len(self.issues)
            },
            'formatted': formatted
        }
    
    def _detect_select_star(self, sql: str):
        """检测 SELECT *"""
        if re.search(r'SELECT\s+\*', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'select_star',
                'message': '使用 SELECT * 会降低性能，建议指定具体字段',
                'severity': 'medium'
            })
    
    def _detect_missing_where(self, sql: str):
        """检测缺少 WHERE 的 UPDATE/DELETE"""
        if re.search(r'(UPDATE|DELETE)\s+\w+\s*$', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'missing_where',
                'message': 'UPDATE/DELETE 缺少 WHERE 条件，危险操作',
                'severity': 'high'
            })
    
    def _detect_inefficient_joins(self, sql: str):
        """检测低效 JOIN"""
        if re.search(r'JOIN\s+\w+\s+ON\s+1\s*=\s*1', sql, re.IGNORECASE):
            self.issues.append({
                'type': 'cartesian_join',
                'message': '检测到笛卡尔积 JOIN，性能极差',
                'severity': 'high'
            })
    
    def _detect_redundant_order_by(self, sql: str):
        """检测冗余 ORDER BY"""
        # 检测子查询中的 ORDER BY
        if re.search(r'\(SELECT.*ORDER BY', sql, re.IGNORECASE | re.DOTALL):
            self.issues.append({
                'type': 'redundant_order_by',
                'message': '子查询中的 ORDER BY 通常无效',
                'severity': 'low'
            })
    
    def _detect_nesting(self, sql: str):
        """检测嵌套层数"""
        depth = 0
        max_depth = 0
        for char in sql:
            if char == '(':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ')':
                depth -= 1
        
        if max_depth > 3:
            self.issues.append({
                'type': 'deep_nesting',
                'message': f'查询嵌套层数过深 ({max_depth}层)，建议优化',
                'severity': 'medium'
            })

class SQLOptimizer:
    """SQL查询优化器"""
    
    def __init__(self):
        self.compaction_rules = [
            # 简化空格
            (re.compile(r'\s+'), ' '),
            # 去除行尾空格
            (re.compile(r'\s*$', re.MULTILINE), ''),
            # 简化注释
            (re.compile(r'/\*.*?\*/', re.DOTALL), ''),
            (re.compile(r'--.*?$', re.MULTILINE), ''),
        ]
    
    def optimize(self, sql: str) -> str:
        """优化 SQL"""
        # 应用压缩规则
        optimized = sql
        for pattern, replacement in self.compaction_rules:
            optimized = pattern.sub(replacement, optimized)
        
        # 格式化（紧凑格式）
        optimized = sqlparse.format(
            optimized,
            reindent=False,
            keyword_case='upper',
            strip_comments=True
        )
        
        return optimized.strip()
    
    def token_count(self, sql: str) -> int:
        """计算 Token 数"""
        # 简化的 Token 计数
        tokens = re.findall(r'\w+|[^\w\s]', sql)
        return len(tokens)
    
    def get_savings(self, original: str, optimized: str) -> Dict:
        """获取节省统计"""
        orig_tokens = self.token_count(original)
        opt_tokens = self.token_count(optimized)
        saved = max(0, orig_tokens - opt_tokens)
        
        return {
            'original_tokens': orig_tokens,
            'optimized_tokens': opt_tokens,
            'saved_tokens': saved,
            'savings_rate': (saved / orig_tokens * 100) if orig_tokens > 0 else 0
        }
