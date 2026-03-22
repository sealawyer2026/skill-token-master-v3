"""
Markdown Optimizer - Markdown文档优化器 v3.2.0
保留结构，压缩内容
"""

import re
from typing import Dict, List, Tuple

class MarkdownOptimizer:
    """Markdown优化器"""
    
    def __init__(self):
        self.rules = self._compile_rules()
    
    def _compile_rules(self) -> List[Tuple[re.Pattern, str]]:
        """编译Markdown优化规则"""
        return [
            # 删除HTML注释
            (re.compile(r'\u003c!--.*?--\u003e', re.DOTALL), ''),
            
            # 简化标题
            (re.compile(r'^#{1,6}\s+', re.MULTILINE), lambda m: '#' * len(m.group().strip()) + ''),
            
            # 简化列表
            (re.compile(r'^[\*\-\+]\s+', re.MULTILINE), '-'),
            (re.compile(r'^\d+\.\s+', re.MULTILINE), '1.'),
            
            # 简化代码块
            (re.compile(r'^```\w+\s*$', re.MULTILINE), '```'),
            
            # 简化强调
            (re.compile(r'\*\*\*'), '**'),  # *** -> **
            (re.compile(r'___'), '__'),     # ___ -> __
            
            # 删除空行（保留结构）
            (re.compile(r'\n{3,}'), '\n\n'),
            
            # 删除行尾空格
            (re.compile(r'\s+$', re.MULTILINE), ''),
            
            # 简化链接 [text](url) -> text (如果url和text相同)
            (re.compile(r'\[([^\]]+)\]\(\1\)'), r'\1'),
            
            # 简化图片 ![alt](url) -> 保留
            # 图片保持原样
            
            # 简化表格分隔符
            (re.compile(r'\|[-:]+\|'), '|'),  # |---|---| -> ||
            
            # 删除引用标记（保留内容）
            (re.compile(r'^\>\s?', re.MULTILINE), ''),
        ]
    
    def optimize(self, content: str) -> str:
        """优化Markdown内容"""
        result = content
        
        # 保护代码块
        code_blocks = []
        def save_code(match):
            code_blocks.append(match.group(0))
            return f'___CODE_BLOCK_{len(code_blocks)-1}___'
        
        result = re.sub(r'```[\s\S]*?```', save_code, result)
        result = re.sub(r'`[^`]+`', save_code, result)
        
        # 应用规则
        for pattern, replacement in self.rules:
            result = pattern.sub(replacement, result)
        
        # 恢复代码块
        for i, block in enumerate(code_blocks):
            result = result.replace(f'___CODE_BLOCK_{i}___', block)
        
        return result.strip()
    
    def get_stats(self, original: str, optimized: str) -> Dict:
        """获取优化统计"""
        orig_lines = len(original.split('\n'))
        opt_lines = len(optimized.split('\n'))
        orig_chars = len(original)
        opt_chars = len(optimized)
        
        return {
            'original_lines': orig_lines,
            'optimized_lines': opt_lines,
            'original_chars': orig_chars,
            'optimized_chars': opt_chars,
            'saved_chars': max(0, orig_chars - opt_chars),
            'compression_ratio': ((orig_chars - opt_chars) / orig_chars * 100) if orig_chars > 0 else 0
        }
