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
            # v3.0.4新增：列表/任务压缩
            (r'以下任务', '任务'),
            (r'以下[几步个]?', ''),
            (r'完成[了]?', '毕'),
            (r'帮我?', ''),
            (r'任务[：:]', ''),
            (r'[步骤]\s*', ''),
            (r'第[一二三四五六七八九十]步', ''),
            (r'首先', '首'),
            (r'其次', '次'),
            (r'最后', '末'),
            (r'最终', '末'),
            (r'总之', '总'),
            (r'综上所述', '综上'),
            (r'总体来说', '总'),
            (r'一般[来说]?', ''),
            (r'通常[来说]?', ''),
            (r'基本上', ''),
            (r'原则上', ''),
            (r'理论上', ''),
            (r'实际上', '实'),
            (r'事实上', '实'),
            (r'具体[来说]?', ''),
            (r'特别[是]?', ''),
            (r'尤其[是]?', ''),
            (r'主要[是]?', '主'),
            (r'关键[是]?', '键'),
            (r'重点[是]?', '重'),
            (r'只要[是]?', '若'),
            (r'只有[是]?', '唯'),
            (r'不管', '不'),
            (r'无论', '无'),
            (r'哪怕', '即'),
            (r'除非', '除'),
            (r'除了', '除'),
            (r'鉴于', '鉴'),
            (r'随着', '随'),
            (r'面对', '对'),
            (r'至于', '至'),
            (r'为了', '为'),
            (r'因此', '故'),
            (r'于是', '故'),
            (r'然而', '但'),
            (r'可是', '但'),
            (r'不过', '但'),
            (r'只是', '但'),
            (r'假设', '若'),
            (r'若是', '若'),
            (r'要是', '若'),
        ]
        
        # v3.0.5: 代码优化规则进一步增强
        self.code_rules = [
            # 删除注释
            (r'#.*$', ''),
            (r'"""[\s\S]*?"""', ''),
            (r"'''[\s\S]*?'''", ''),
            # 简化比较
            (r'len\((\w+)\)\s*>\s*0', r'\1'),
            (r'len\((\w+)\)\s*==\s*0', r'not \1'),
            # 返回简化
            (r'if\s+(\w+)\s*:\s*return\s+True\s*\n\s*return\s+False', r'return bool(\1)'),
            (r'if\s+(\w+)\s*:\s*return\s+False\s*\n\s*return\s+True', r'return not \1'),
            (r'return\s+\{\s*["\']total["\']\s*:\s*(\w+)\s*,\s*["\']active["\']\s*:\s*(\w+)\s*\}', r'return \1,\2'),
            (r'for\s+(\w+)\s+in\s+(\w+):', r'for \1 in \2:'),
            (r'if\s+(\w+)\s+is\s+not\s+None:', r'if \1:'),
            # v3.0.3: 激进代码压缩
            (r'is\s+not\s+None', ''),
            (r'==\s*True', ''),
            (r'==\s*False', ''),
            (r'if\s+(\w+):\s*return\s+True\s*else:\s*return\s+False', r'return bool(\1)'),
            (r'if\s+not\s+(\w+):\s*return\s+False\s*else:\s*return\s+True', r'return bool(\1)'),
            # v3.0.5: 统计函数优化
            (r'(\w+)\s*=\s*0\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\s*\+=\s*\2', r'\1=sum(\3)'),
            (r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*if\s+(\w+):\s*\n\s*\1\.append\((\w+)\)', r'\1=[\5 for \2 in \3 if \4]'),
            (r'def\s+(\w+)\(([^)]*)\):\s*\n\s*return\s+sum\((\w+)\)', r'\1=sum'),
            (r'def\s+(\w+)\(([^)]*)\):\s*\n\s*return\s+len\((\w+)\)', r'\1=len'),
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
        """优化代码 - v3.0.4进一步增强"""
        result = content
        
        # v3.0.4: 先删除所有注释和docstring（多行处理）
        result = re.sub(r'"""[\s\S]*?"""', '', result)
        result = re.sub(r"'''[\s\S]*?'''", '', result)
        result = re.sub(r'#.*$', '', result, flags=re.MULTILINE)
        
        # 应用代码规则
        for pattern, replacement in self._compiled_rules['code']:
            result = pattern.sub(replacement, result)
        
        # v3.0.4: 额外压缩
        # 删除多余空行
        result = re.sub(r'\n\s*\n', '\n', result)
        result = re.sub(r'\n+', '\n', result)
        
        # 删除行首空格
        result = '\n'.join(line.strip() for line in result.split('\n'))
        
        # v3.0.4: 简化常见模式
        # result = [] -> r=[]
        result = re.sub(r'(\w+)\s*=\s*\[\]', r'\1=[]', result)
        # result.append(x) -> r+=[x]
        result = re.sub(r'(\w+)\.append\(([^)]+)\)', r'\1+=[\2]', result)
        # for循环简化
        result = re.sub(r'for\s+(\w+)\s+in\s+(\w+):', r'for \1 in \2:', result)
        # if条件简化
        result = re.sub(r'if\s+([^:]+):', r'if \1:', result)
        
        return result.strip()
    
    def _optimize_workflow(self, content: str) -> str:
        """优化工作流 - v3.0.4增强"""
        try:
            data = json.loads(content)
            
            # v3.0.4: 键名缩写映射扩展
            key_abbreviations = {
                'name': 'n', 'type': 't', 'config': 'c',
                'parameters': 'p', 'description': 'd',
                'configuration': 'cfg', 'environment': 'env',
                'timeout': 'to', 'retry': 'r', 'version': 'v',
                'steps': 's', 'inputs': 'i', 'outputs': 'o',
                'enabled': 'on', 'disabled': 'off',
            }
            
            def abbreviate_keys(obj):
                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        new_key = key_abbreviations.get(k, k)
                        new_obj[new_key] = abbreviate_keys(v)
                    return new_obj
                elif isinstance(obj, list):
                    return [abbreviate_keys(item) for item in obj]
                return obj
            
            data = abbreviate_keys(data)
            
            # 删除默认值
            if 'to' in data and data['to'] in [30, 30000]:
                del data['to']
            if 'r' in data and data['r'] == 3:
                del data['r']
            if 'v' in data and data['v'] in ['1.0', '2.0']:
                del data['v']
            
            # 步骤优化
            if 's' in data:
                for step in data['s']:
                    # 删除步骤中的默认值
                    if 'to' in step and step['to'] in [30, 30000]:
                        del step['to']
                    # 简化步骤名
                    if 'n' in step:
                        step['n'] = re.sub(r'^step_?', '', step['n'], flags=re.I)
            
            # 压缩JSON
            return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        except json.JSONDecodeError:
            # 如果不是JSON，尝试通用压缩
            result = re.sub(r'\s+', '', content)
            return result
            
            # 压缩JSON（删除空格）
            return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        except json.JSONDecodeError:
            # 如果是YAML或其他格式，返回原内容
            return content
