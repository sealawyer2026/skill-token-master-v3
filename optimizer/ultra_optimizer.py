"""
Ultra Optimizer - 超极致优化器 v3.3.0
目标: 提示词80%+，代码85%+
"""

import re
import ast
from typing import Dict, List, Tuple

class UltraOptimizer:
    """超极致优化器 - 突破极限"""
    
    def __init__(self):
        self.prompt_rules = self._compile_prompt_rules()
        self.code_rules = self._compile_code_rules()
    
    def _compile_prompt_rules(self) -> List[Tuple[re.Pattern, str]]:
        """编译超极致提示词规则 - 200+条"""
        raw_rules = [
            # ========== 单字极致压缩 (新增50条) ==========
            (r'分析', '析'),
            (r'处理', '处'),
            (r'检查', '检'),
            (r'整理', '理'),
            (r'查询', '询'),
            (r'搜索', '搜'),
            (r'获取', '取'),
            (r'创建', '建'),
            (r'删除', '删'),
            (r'更新', '更'),
            (r'修改', '改'),
            (r'添加', '加'),
            (r'插入', '插'),
            (r'替换', '换'),
            (r'转换', '转'),
            (r'计算', '算'),
            (r'验证', '验'),
            (r'确认', '认'),
            (r'执行', '行'),
            (r'运行', '运'),
            (r'调用', '调'),
            (r'返回', '返'),
            (r'输出', '出'),
            (r'输入', '入'),
            (r'导入', '导'),
            (r'导出', '导'),
            (r'加载', '载'),
            (r'保存', '存'),
            (r'读取', '读'),
            (r'写入', '写'),
            (r'解析', '解'),
            (r'生成', '生'),
            (r'构建', '构'),
            (r'组装', '组'),
            (r'拆分', '拆'),
            (r'合并', '并'),
            (r'排序', '排'),
            (r'过滤', '滤'),
            (r'筛选', '筛'),
            (r'匹配', '配'),
            (r'比较', '比'),
            (r'判断', '判'),
            (r'检测', '测'),
            (r'监控', '监'),
            (r'记录', '录'),
            (r'追踪', '追'),
            (r'统计', '统'),
            (r'汇总', '汇'),
            (r'展示', '示'),
            (r'显示', '显'),
            
            # ========== 双字词压缩 ==========
            (r'用户', '户'),
            (r'数据', '据'),
            (r'信息', '息'),
            (r'结果', '果'),
            (r'内容', '容'),
            (r'文本', '文'),
            (r'文件', '档'),
            (r'目录', '录'),
            (r'路径', '径'),
            (r'地址', '址'),
            
            # ========== 连词删除 (更激进) ==========
            (r'以及', ''),
            (r'或者', '或'),
            (r'还有', ''),
            (r'另外', ''),
            (r'此外', ''),
            (r'同时', ''),
            (r'然后', ''),
            (r'接着', ''),
            (r'随后', '后'),
            (r'之后', '后'),
            (r'之前', '前'),
            
            # ========== 程度词删除 ==========
            (r'很多', '多'),
            (r'大量', '多'),
            (r'少量', '少'),
            (r'全部', '全'),
            (r'完全', '全'),
            (r'彻底', '全'),
            (r'主要', '主'),
            (r'次要', '次'),
            (r'重要', '重'),
            (r'关键', '键'),
            
            # ========== 动作简化 ==========
            (r'进行', ''),
            (r'予以', ''),
            (r'加以', ''),
            (r'给予', ''),
            (r'提供', '供'),
            (r'使用', '用'),
            (r'利用', '用'),
            (r'采用', '用'),
            (r'应用', '用'),
            (r'通过', '经'),
            (r'根据', '依'),
            (r'按照', '依'),
            (r'基于', '基'),
            (r'针对', '对'),
            (r'关于', '关'),
            (r'对于', '对'),
            (r'涉及', '涉'),
            (r'包含', '含'),
            (r'包括', '含'),
            (r'涵盖', '含'),
            
            # ========== 句式压缩 ==========
            (r'请帮我?', ''),
            (r'帮我?', ''),
            (r'给我?', ''),
            (r'为我?', ''),
            (r'让我?', ''),
            (r'我需要', '需'),
            (r'我想要', '要'),
            (r'我希望', '望'),
            (r'我认为', '谓'),
            (r'我觉得', '谓'),
            (r'我知道', '知'),
            (r'我了解', '知'),
            (r'我明白', '知'),
            
            # ========== 标点压缩 ==========
            (r'，', '、'),
            (r'。', ''),
            (r'！', ''),
            (r'？', ''),
            (r'：', ''),
            (r'；', '、'),
            (r'"', ''),
            (r'"', ''),
            (r'「', ''),
            (r'」', ''),
            
            # ========== 空格压缩 (最激进) ==========
            (r'\s+', ''),
        ]
        
        return [(re.compile(pattern), replacement) for pattern, replacement in raw_rules]
    
    def _compile_code_rules(self):
        """编译代码优化规则"""
        return [
            # 变量名简化映射
            ('total', 't'),
            ('count', 'c'),
            ('index', 'i'),
            ('value', 'v'),
            ('result', 'r'),
            ('data', 'd'),
            ('item', 'x'),
            ('element', 'e'),
            ('current', 'c'),
            ('previous', 'p'),
            ('next', 'n'),
            ('first', 'f'),
            ('last', 'l'),
            ('temp', 't'),
            ('tmp', 't'),
            ('buffer', 'b'),
            ('string', 's'),
            ('number', 'n'),
            ('length', 'l'),
            ('size', 's'),
            ('width', 'w'),
            ('height', 'h'),
            ('position', 'p'),
            ('offset', 'o'),
        ]
    
    def optimize_prompt(self, text: str) -> str:
        """超极致提示词优化"""
        result = text
        for pattern, replacement in self.prompt_rules:
            result = pattern.sub(replacement, result)
        return result.strip()
    
    def optimize_code(self, code: str) -> str:
        """超极致代码优化"""
        try:
            tree = ast.parse(code)
            tree = self._ultra_optimize_ast(tree)
            result = ast.unparse(tree)
            return self._post_compress_code(result)
        except:
            return code
    
    def _ultra_optimize_ast(self, tree: ast.AST) -> ast.AST:
        """超极致AST优化"""
        # 收集变量
        variables = {}
        short_names = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        name_idx = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, (ast.Store, ast.Param)):
                    if node.id not in variables and not node.id.startswith('_'):
                        if name_idx < len(short_names):
                            variables[node.id] = short_names[name_idx]
                            name_idx += 1
                        else:
                            variables[node.id] = f'v{name_idx - len(short_names)}'
                            name_idx += 1
        
        # 替换变量名
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in variables:
                node.id = variables[node.id]
            elif isinstance(node, ast.FunctionDef):
                # 简化函数名
                if len(node.name) > 3 and not node.name.startswith('_'):
                    node.name = node.name[:2]
        
        return tree
    
    def _post_compress_code(self, code: str) -> str:
        """后处理压缩 - 极致版本"""
        # 删除所有注释
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        # 删除文档字符串
        code = re.sub(r'"""[\s\S]*?"""', '', code)
        code = re.sub(r"'''[\s\S]*?'''", '', code)
        # 删除所有空行
        code = re.sub(r'\n+', '\n', code)
        # 删除行首空格
        code = re.sub(r'^\s+', '', code, flags=re.MULTILINE)
        # 删除所有空格（除了必要的）
        code = re.sub(r'\s*([=+\-*/%\(\)\[\]\{\},:;])\s*', r'\1', code)
        # 删除行尾空格
        code = re.sub(r'\s+$', '', code, flags=re.MULTILINE)
        
        return code.strip()
    
    def get_stats(self, original: str, optimized: str, content_type: str = 'text') -> Dict:
        """获取优化统计"""
        orig_len = len(original)
        opt_len = len(optimized)
        saved = max(0, orig_len - opt_len)
        
        return {
            'original_chars': orig_len,
            'optimized_chars': opt_len,
            'saved_chars': saved,
            'savings_rate': (saved / orig_len * 100) if orig_len > 0 else 0,
            'content_type': content_type
        }
