"""Token经济大师 v3.0 - 智能优化器"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any

class SmartOptimizer:
    """智能优化器 v3.0 - 终极优化版"""
    
    def __init__(self):
        self.optimization_log = []
        self._cache = {}
        self._compiled_rules = None
        self._init_rules()
    
    def _init_rules(self):
        """初始化并预编译规则"""
        # 提示词优化规则 - v3.0增强
        self.prompt_rules = [
            # 填充词删除（保留字的紧凑形式）
            (r'\s*的\s+', '之'),
            (r'\s*了\s+', '毕'),
            (r'\s*是\s+', '乃'),
            (r'\s*有\s+', '具'),
            # 冗余副词
            (r'非常|特别|十分|极其|相当|很是?', ''),
            # 客套话
            (r'请', ''),
            (r'谢谢|感谢', ''),
            (r'麻烦您|劳驾', ''),
            (r'帮我?', ''),
            (r'给我?', ''),
            # 程度副词
            (r'仔细地?|认真地?|好好地?', ''),
            (r'快速地?|慢慢地?', ''),
            # 单字替换
            (r'因为|由于|鉴于', '因'),
            (r'所以|因此|于是', '故'),
            (r'但是|然而|可是', '但'),
            (r'如果|假如|若是', '若'),
            (r'必须|务必|一定', '须'),
            (r'可以|能够|可能', '可'),
            (r'需要|要求|需求', '需'),
            (r'应该|应当|应', '应'),
            (r'已经|已然|业已', '已'),
            (r'正在|现在|当前', '正'),
            # 常用词简化 - v3.0.2自迭代增强
            (r'一下', ''),
            (r'进行', '行'),
            (r'处理', '处'),
            (r'分析', '析'),
            (r'处理', '处'),
            # v3.0.2新增：长句压缩规则
            (r'一个', ''),  # "一个复杂的问题" → "复杂之问题"
            (r'然后', ''),  # 删除连接词
            (r'接着', ''),
            (r'之后', '后'),
            (r'之前', '前'),
            (r'提出', '出'),
            (r'给出', '出'),
            (r'完成', '毕'),
            # v3.0.2新增：常用短语压缩
            (r'分析一下', '析'),
            (r'处理一下', '处'),
            (r'检查一下', '检'),
            (r'整理一下', '理'),
            (r'详细地?', '详'),
            (r'复杂的?', '繁'),
            (r'简单的?', '简'),
            (r'重要的?', '重'),
            (r'输入之?', '入'),
            (r'输出之?', '出'),
            # v3.0.3新增：更多长句压缩
            (r'对于', '对'),
            (r'关于', '关'),
            (r'根据', '依'),
            (r'按照', '依'),
            (r'通过', '经'),
            (r'经过', '经'),
            (r'根据', '依'),
            (r'基于', '基'),
            (r'针对', '对'),
            (r'涉及', '涉'),
            (r'包括', '含'),
            (r'包含', '含'),
            (r'以及', '及'),
            (r'或者', '或'),
            (r'还是', '或'),
            (r'虽然', '虽'),
            (r'尽管', '虽'),
            (r'不但', '不'),
            (r'不仅', '不'),
            (r'而且', '且'),
            (r'并且', '且'),
            (r'或者', '或'),
        ]
        
        # 代码优化规则 - v3.0.3进一步增强
        self.code_rules = [
            # 删除注释
            (r'#.*$', ''),
            (r'"""[\s\S]*?"""', ''),
            (r"'''[\s\S]*?'''", ''),
            # 简化比较
            (r'len\((\w+)\)\s*>\s*0', r'\1'),
            (r'len\((\w+)\)\s*==\s*0', r'not \1'),
            # v3.0.2新增：代码模式简化
            (r'if\s+(\w+)\s*:\s*return\s+True\s*\n\s*return\s+False', r'return bool(\1)'),
            (r'if\s+(\w+)\s*:\s*return\s+False\s*\n\s*return\s+True', r'return not \1'),
            (r'return\s+\{\s*["\']total["\']\s*:\s*(\w+)\s*,\s*["\']active["\']\s*:\s*(\w+)\s*\}', r'return \1,\2'),
            (r'for\s+(\w+)\s+in\s+(\w+):', r'for \1 in \2:'),
            (r'if\s+(\w+)\s+is\s+not\s+None:', r'if \1:'),
            # v3.0.3新增：激进代码压缩
            (r'is\s+not\s+None', ''),
            (r'==\s*True', ''),
            (r'==\s*False', ''),
            (r'if\s+(\w+):\s*return\s+True\s*else:\s*return\s+False', r'return bool(\1)'),
            (r'if\s+not\s+(\w+):\s*return\s+False\s*else:\s*return\s+True', r'return bool(\1)'),
        ]
        
        self._compiled_rules = {
            'prompt': [(re.compile(p), r) for p, r in self.prompt_rules],
            'code': [(re.compile(p, re.MULTILINE), r) for p, r in self.code_rules]
        }
    
    def optimize(self, content: str, content_type: str = 'auto') -> Dict[str, Any]:
        """执行优化"""
        if content_type == 'auto':
            content_type = self._detect_type(content)
        
        original_tokens = self._estimate_tokens(content)
        
        # 根据类型选择优化策略
        if content_type == 'agent':
            optimized = self._optimize_prompt(content)
        elif content_type == 'skill':
            optimized = self._optimize_code(content)
        elif content_type == 'workflow':
            optimized = self._optimize_workflow(content)
        else:
            optimized = content
        
        optimized_tokens = self._estimate_tokens(optimized)
        saving = original_tokens - optimized_tokens
        saving_pct = (saving / original_tokens * 100) if original_tokens > 0 else 0
        
        return {
            'original': content,
            'optimized': optimized,
            'original_tokens': original_tokens,
            'optimized_tokens': optimized_tokens,
            'saving': saving,
            'saving_percentage': round(saving_pct, 1),
            'content_type': content_type
        }
    
    def _detect_type(self, content: str) -> str:
        """检测内容类型"""
        content_lower = content.lower()
        
        if any(kw in content for kw in ['workflow', 'steps', 'yaml']):
            return 'workflow'
        
        code_keywords = ['def ', 'class ', 'import ', 'function', 'return', 'if ', 'for ']
        if sum(1 for kw in code_keywords if kw in content) >= 2:
            return 'skill'
        
        return 'agent'
    
    def _estimate_tokens(self, text: str) -> int:
        """估算Token数量"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 1.5 + other_chars / 4)
    
    def _optimize_prompt(self, content: str) -> str:
        """优化提示词 - v3.0.3终极版"""
        result = content
        
        # 应用预编译规则
        for pattern, replacement in self._compiled_rules['prompt']:
            result = pattern.sub(replacement, result)
        
        # 删除多余空格
        result = re.sub(r' +', ' ', result)
        
        # v3.0.3: 额外压缩 - 删除数字序号后的空格
        result = re.sub(r'(\d+)\.\s+', r'\1.', result)
        
        # v3.0.3: 删除常见冗余结构
        result = re.sub(r'之[助势]', '', result)  # "之助" "之势" 等冗余
        result = re.sub(r'毕[成了]', '毕', result)  # "完成了" → "毕"
        
        # v3.0.3: 列表项压缩
        lines = result.split('\n')
        compressed_lines = []
        for line in lines:
            line = line.strip()
            # 删除列表项中的填充词
            line = re.sub(r'^[\s]*[-*]\s*', '', line)  # 删除列表符号
            if line:
                compressed_lines.append(line)
        
        result = '\n'.join(compressed_lines)
        result = re.sub(r'\n\s*\n', '\n', result)
        
        return result.strip()
    
    def _optimize_code(self, content: str) -> str:
        """优化代码"""
        lines = content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # 跳过纯注释行（保留空行用于可读性）
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('#!'):
                continue
            
            # 删除行内注释
            if '#' in line and not line.strip().startswith('#'):
                line = line[:line.index('#')].rstrip()
            
            # 简化空格
            line = re.sub(r'\s*=\s*', '=', line)
            line = re.sub(r'\s*,\s*', ',', line)
            line = re.sub(r'\s*:\s*', ':', line)
            
            optimized_lines.append(line)
        
        result = '\n'.join(optimized_lines)
        
        # 应用代码规则
        for pattern, replacement in self._compiled_rules['code']:
            result = pattern.sub(replacement, result)
        
        # 删除多余空行
        result = re.sub(r'\n\s*\n', '\n', result)
        
        return result.strip()
    
    def _optimize_workflow(self, content: str) -> str:
        """优化工作流"""
        try:
            data = json.loads(content)
            
            # 压缩JSON（删除空格）
            return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        except json.JSONDecodeError:
            # 如果是YAML或其他格式，返回原内容
            return content
