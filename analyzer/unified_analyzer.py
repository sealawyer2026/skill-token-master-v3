"""Token经济大师 v3.2.0 - 统一分析器"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

# 导入新模块
from .mcp_analyzer import MCPAnalyzer, MCPOptimizer
from .sql_analyzer import SQLAnalyzer, SQLOptimizer

class TokenAnalyzer:
    """Token使用量分析器 v3.2.0"""
    
    def __init__(self):
        self.patterns = {
            'agent': self._analyze_agent,
            'skill': self._analyze_skill,
            'workflow': self._analyze_workflow,
            'mcp': self._analyze_mcp,
            'sql': self._analyze_sql
        }
        self.mcp_analyzer = MCPAnalyzer()
        self.sql_analyzer = SQLAnalyzer()
    
    def analyze(self, content: str, content_type: str = 'auto') -> Dict[str, Any]:
        """分析内容Token使用情况"""
        if content_type == 'auto':
            content_type = self._detect_type(content)
        
        base_info = {
            'total_chars': len(content),
            'total_lines': content.count('\n') + 1,
            'estimated_tokens': self._estimate_tokens(content),
            'content_type': content_type
        }
        
        if content_type in self.patterns:
            specific = self.patterns[content_type](content)
            base_info.update(specific)
        
        return base_info
    
    def _detect_type(self, content: str) -> str:
        """自动检测内容类型 v3.2.0"""
        content_lower = content.lower().strip()
        
        # 检测 MCP 配置
        if content_lower.startswith('{') and '"tools"' in content_lower:
            try:
                data = json.loads(content)
                if 'tools' in data or 'mcpServers' in data:
                    return 'mcp'
            except:
                pass
        
        # 检测 SQL
        sql_keywords = ['select', 'insert', 'update', 'delete', 'from', 'where', 'join']
        if any(kw in content_lower for kw in sql_keywords):
            return 'sql'
        
        # 检测工作流
        if any(kw in content for kw in ['workflow', 'steps', 'pipeline', 'yaml']):
            return 'workflow'
        
        # 检测代码
        if any(kw in content for kw in ['def ', 'class ', 'import ', 'function']):
            return 'skill'
        
        # 默认为智能体提示词
        return 'agent'
    
    def _estimate_tokens(self, text: str) -> int:
        """估算Token数量（近似算法）"""
        # 中文Token估算：约1.5字符/Token
        # 英文Token估算：约4字符/Token
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        
        chinese_tokens = chinese_chars / 1.5
        other_tokens = other_chars / 4
        
        return int(chinese_tokens + other_tokens)
    
    def _analyze_agent(self, content: str) -> Dict:
        """分析智能体提示词"""
        issues = []
        
        # 检测冗余修饰词
        redundant = ['非常', '特别', '十分', '极其', '相当', '很']
        for word in redundant:
            count = content.count(word)
            if count > 0:
                issues.append({'type': 'redundant', 'word': word, 'count': count})
        
        # 检测客套话
        polite = ['请', '麻烦您', '劳驾', '谢谢', '感谢']
        polite_count = sum(content.count(w) for w in polite)
        if polite_count > 3:
            issues.append({'type': 'polite', 'count': polite_count})
        
        # 检测重复内容
        lines = content.split('\n')
        unique_lines = set(lines)
        if len(lines) != len(unique_lines):
            issues.append({'type': 'duplicate', 'count': len(lines) - len(unique_lines)})
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'optimization_potential': min(70, 20 + len(issues) * 5)
        }
    
    def _analyze_skill(self, content: str) -> Dict:
        """分析技能代码"""
        issues = []
        
        # 检测注释
        comment_lines = len(re.findall(r'^\s*#', content, re.MULTILINE))
        docstring_count = content.count('"""') // 2
        
        if comment_lines > 5:
            issues.append({'type': 'comments', 'count': comment_lines})
        if docstring_count > 0:
            issues.append({'type': 'docstring', 'count': docstring_count})
        
        # 检测空行
        empty_lines = len(re.findall(r'^\s*$', content, re.MULTILINE))
        if empty_lines > 10:
            issues.append({'type': 'empty_lines', 'count': empty_lines})
        
        # 检测长变量名
        long_vars = re.findall(r'\b[a-z_]{15,}\b', content)
        if long_vars:
            issues.append({'type': 'long_variables', 'count': len(long_vars)})
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'optimization_potential': min(65, 15 + len(issues) * 8)
        }
    
    def _analyze_workflow(self, content: str) -> Dict:
        """分析工作流配置"""
        issues = []
        
        try:
            data = json.loads(content)
            
            # 检测步骤数量
            if 'steps' in data and len(data['steps']) > 5:
                issues.append({'type': 'many_steps', 'count': len(data['steps'])})
            
            # 检测重复配置
            if 'config' in data:
                config_keys = list(data['config'].keys())
                if len(config_keys) > 10:
                    issues.append({'type': 'verbose_config', 'count': len(config_keys)})
            
        except json.JSONDecodeError:
            pass
        
        # 检测YAML格式冗余
        if content.count(': ') > 20:
            issues.append({'type': 'yaml_verbose', 'count': content.count(': ')})
        
        return {
            'issues': issues,
            'issue_count': len(issues),
            'optimization_potential': min(55, 10 + len(issues) * 10)
        }
    
    def _analyze_mcp(self, content: str) -> Dict:
        """分析 MCP 配置 v3.2.0"""
        return self.mcp_analyzer.analyze(content)
    
    def _analyze_sql(self, content: str) -> Dict:
        """分析 SQL 查询 v3.2.0"""
        return self.sql_analyzer.analyze(content)
