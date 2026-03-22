"""
MCP Analyzer - Model Context Protocol 分析器
Token经济大师 v3.2.0
"""

import re
import json
from typing import Dict, List, Tuple, Optional

class MCPAnalyzer:
    """MCP协议分析器"""
    
    def __init__(self):
        self.issues = []
        self.metrics = {}
    
    def analyze(self, content: str) -> Dict:
        """分析 MCP 协议配置"""
        self.issues = []
        
        try:
            mcp_config = json.loads(content)
        except:
            return {'error': 'Invalid JSON'}
        
        # 检测问题
        self._detect_redundant_descriptions(mcp_config)
        self._detect_duplicate_tools(mcp_config)
        self._detect_inefficient_schemas(mcp_config)
        self._detect_verbose_names(mcp_config)
        
        # 计算指标
        self._calculate_metrics(mcp_config)
        
        return {
            'type': 'mcp',
            'issues': self.issues,
            'metrics': self.metrics,
            'severity': self._calculate_severity()
        }
    
    def _detect_redundant_descriptions(self, config: Dict):
        """检测冗余描述"""
        tools = config.get('tools', [])
        for tool in tools:
            desc = tool.get('description', '')
            # 检测填充词
            if any(word in desc for word in ['这是一个', '用于', '可以']):
                self.issues.append({
                    'type': 'redundant_description',
                    'tool': tool.get('name'),
                    'message': '工具描述包含冗余词汇',
                    'severity': 'medium'
                })
    
    def _detect_duplicate_tools(self, config: Dict):
        """检测重复工具"""
        tools = config.get('tools', [])
        names = [t.get('name') for t in tools]
        duplicates = set([n for n in names if names.count(n) > 1])
        
        for dup in duplicates:
            self.issues.append({
                'type': 'duplicate_tool',
                'tool': dup,
                'message': f'工具名称重复: {dup}',
                'severity': 'high'
            })
    
    def _detect_inefficient_schemas(self, config: Dict):
        """检测低效 Schema"""
        tools = config.get('tools', [])
        for tool in tools:
            schema = tool.get('inputSchema', {})
            properties = schema.get('properties', {})
            
            # 检测未使用的 required 字段
            required = schema.get('required', [])
            for prop in properties:
                if prop in required and 'default' in properties[prop]:
                    self.issues.append({
                        'type': 'inefficient_schema',
                        'tool': tool.get('name'),
                        'property': prop,
                        'message': 'required 字段不应有默认值',
                        'severity': 'low'
                    })
    
    def _detect_verbose_names(self, config: Dict):
        """检测冗长名称"""
        tools = config.get('tools', [])
        for tool in tools:
            name = tool.get('name', '')
            if len(name) > 30:
                self.issues.append({
                    'type': 'verbose_name',
                    'tool': name,
                    'message': f'工具名称过长 ({len(name)}字符)',
                    'severity': 'low'
                })
    
    def _calculate_metrics(self, config: Dict):
        """计算指标"""
        tools = config.get('tools', [])
        self.metrics = {
            'total_tools': len(tools),
            'total_issues': len(self.issues),
            'high_severity': sum(1 for i in self.issues if i['severity'] == 'high'),
            'medium_severity': sum(1 for i in self.issues if i['severity'] == 'medium'),
            'low_severity': sum(1 for i in self.issues if i['severity'] == 'low')
        }
    
    def _calculate_severity(self) -> str:
        """计算整体严重程度"""
        if any(i['severity'] == 'high' for i in self.issues):
            return 'high'
        elif any(i['severity'] == 'medium' for i in self.issues):
            return 'medium'
        elif self.issues:
            return 'low'
        return 'none'

class MCPOptimizer:
    """MCP协议优化器"""
    
    def __init__(self):
        self.rules = self._compile_rules()
    
    def _compile_rules(self):
        """编译优化规则"""
        return [
            (re.compile(r'这是一个'), ''),
            (re.compile(r'用于'), ''),
            (re.compile(r'可以'), ''),
            (re.compile(r'的'), ''),
            (re.compile(r'了'), ''),
        ]
    
    def optimize(self, content: str) -> str:
        """优化 MCP 配置"""
        try:
            config = json.loads(content)
        except:
            return content
        
        # 优化工具描述
        tools = config.get('tools', [])
        for tool in tools:
            if 'description' in tool:
                tool['description'] = self._optimize_description(tool['description'])
            
            # 优化工具名称
            if 'name' in tool:
                tool['name'] = self._optimize_name(tool['name'])
        
        return json.dumps(config, ensure_ascii=False, separators=(',', ':'))
    
    def _optimize_description(self, desc: str) -> str:
        """优化描述"""
        for pattern, replacement in self.rules:
            desc = pattern.sub(replacement, desc)
        return desc.strip()
    
    def _optimize_name(self, name: str) -> str:
        """优化名称"""
        # 简化常见前缀
        name = re.sub(r'^get_', '', name)
        name = re.sub(r'^fetch_', '', name)
        name = re.sub(r'^(tool_|function_)', '', name)
        return name
