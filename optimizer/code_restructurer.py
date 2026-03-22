#!/usr/bin/env python3
"""
Code Restructurer - 代码结构重组优化器 v3.5.0
核心: 函数内联、循环展开、变量合并
目标: 代码 85%+ 压缩率
"""

import ast
import re
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class FunctionInfo:
    """函数信息"""
    name: str
    args: List[str]
    body: List[ast.AST]
    size: int
    calls: int = 0
    is_simple: bool = False

@dataclass
class OptimizationResult:
    """优化结果"""
    code: str
    original_size: int
    optimized_size: int
    savings: int
    ratio: float
    applied_transforms: List[str] = field(default_factory=list)


class CodeRestructurer:
    """
    代码结构重组优化器
    实现: 函数内联、循环展开、变量合并、表达式简化
    """
    
    def __init__(self):
        self.function_map: Dict[str, FunctionInfo] = {}
        self.inline_threshold = 50  # 小于此值的函数可内联
        self.loop_unroll_limit = 4  # 循环展开最大次数
        
    def optimize(self, code: str, aggressive: bool = True) -> OptimizationResult:
        """
        代码优化主入口
        
        Args:
            code: 源代码
            aggressive: 是否使用激进优化
            
        Returns:
            优化结果
        """
        original_size = len(code)
        transforms = []
        
        try:
            # 1. 解析AST
            tree = ast.parse(code)
            
            # 2. 函数内联
            tree = self._inline_functions(tree)
            transforms.append('function_inline')
            
            # 3. 循环展开
            tree = self._unroll_loops(tree)
            transforms.append('loop_unroll')
            
            # 4. 变量名极简替换
            tree = self._minify_variables(tree)
            transforms.append('variable_minify')
            
            # 5. 表达式简化
            tree = self._simplify_expressions(tree)
            transforms.append('expression_simplify')
            
            # 6. 删除无用代码
            tree = self._eliminate_dead_code(tree)
            transforms.append('dead_code_elimination')
            
            # 7. 转换为代码
            optimized_code = ast.unparse(tree)
            
            # 8. 后处理压缩
            optimized_code = self._post_optimize(optimized_code, aggressive)
            transforms.append('post_optimize')
            
        except SyntaxError:
            # AST解析失败，使用纯文本压缩
            optimized_code = self._text_compress(code)
            transforms = ['text_compress']
        
        optimized_size = len(optimized_code)
        savings = original_size - optimized_size
        ratio = savings / original_size if original_size > 0 else 0
        
        return OptimizationResult(
            code=optimized_code,
            original_size=original_size,
            optimized_size=optimized_size,
            savings=savings,
            ratio=ratio,
            applied_transforms=transforms
        )
    
    def _inline_functions(self, tree: ast.AST) -> ast.AST:
        """函数内联优化"""
        # 收集所有函数定义
        self.function_map = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 计算函数大小
                func_code = ast.unparse(node)
                size = len(func_code)
                
                # 检查是否简单函数 (无复杂控制流)
                is_simple = all(
                    not isinstance(n, (ast.For, ast.While, ast.Try))
                    for n in ast.walk(node)
                )
                
                self.function_map[node.name] = FunctionInfo(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    body=node.body,
                    size=size,
                    is_simple=is_simple
                )
        
        # 内联调用
        class FunctionInliner(ast.NodeTransformer):
            def __init__(self, function_map, threshold):
                self.function_map = function_map
                self.threshold = threshold
            
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in self.function_map:
                        func_info = self.function_map[func_name]
                        
                        # 只内联简单且小的函数
                        if func_info.size < self.threshold and func_info.is_simple:
                            # 创建内联表达式
                            if len(func_info.body) == 1:
                                if isinstance(func_info.body[0], ast.Return):
                                    return func_info.body[0].value
                return self.generic_visit(node)
        
        return FunctionInliner(self.function_map, self.inline_threshold).visit(tree)
    
    def _unroll_loops(self, tree: ast.AST) -> ast.AST:
        """循环展开优化"""
        class LoopUnroller(ast.NodeTransformer):
            def __init__(self, limit):
                self.limit = limit
            
            def visit_For(self, node):
                # 检查是否可展开 (range且范围确定)
                if isinstance(node.iter, ast.Call):
                    if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                        # 尝试确定循环次数
                        args = node.iter.args
                        if len(args) == 1:
                            # range(n)
                            try:
                                if isinstance(args[0], ast.Constant):
                                    n = args[0].value
                                    if n <= self.limit:
                                        # 展开循环
                                        new_body = []
                                        for i in range(n):
                                            # 替换迭代变量
                                            replacer = VariableReplacer(node.target.id, ast.Constant(value=i))
                                            for stmt in node.body:
                                                new_stmt = replacer.visit(ast.parse(ast.unparse(stmt)).body[0])
                                                new_body.append(new_stmt)
                                        return new_body
                            except:
                                pass
                return self.generic_visit(node)
        
        return LoopUnroller(self.loop_unroll_limit).visit(tree)
    
    def _minify_variables(self, tree: ast.AST) -> ast.AST:
        """变量名极简替换"""
        # 收集所有变量
        var_map = {}
        short_names = self._generate_short_names()
        name_idx = 0
        
        # 第一阶段: 收集变量
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, (ast.Store, ast.Param)):
                    if node.id not in var_map and not node.id.startswith('_'):
                        if not self._is_builtin(node.id):
                            var_map[node.id] = short_names[name_idx]
                            name_idx += 1
            elif isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.arg not in var_map and not arg.arg.startswith('_'):
                        var_map[arg.arg] = short_names[name_idx]
                        name_idx += 1
        
        # 第二阶段: 替换
        class VariableMinifier(ast.NodeTransformer):
            def __init__(self, mapping):
                self.mapping = mapping
            
            def visit_Name(self, node):
                if node.id in self.mapping:
                    node.id = self.mapping[node.id]
                return node
            
            def visit_FunctionDef(self, node):
                # 简化函数名
                if len(node.name) > 2 and not node.name.startswith('_'):
                    node.name = node.name[:2].lower()
                # 处理参数
                for arg in node.args.args:
                    if arg.arg in self.mapping:
                        arg.arg = self.mapping[arg.arg]
                return self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                if len(node.name) > 2:
                    node.name = node.name[:2]
                return self.generic_visit(node)
            
            def visit_arg(self, node):
                if node.arg in self.mapping:
                    node.arg = self.mapping[node.arg]
                return node
        
        return VariableMinifier(var_map).visit(tree)
    
    def _simplify_expressions(self, tree: ast.AST) -> ast.AST:
        """表达式简化"""
        class ExpressionSimplifier(ast.NodeTransformer):
            def visit_BinOp(self, node):
                # 常量折叠
                if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                    try:
                        if isinstance(node.op, ast.Add):
                            return ast.Constant(value=node.left.value + node.right.value)
                        elif isinstance(node.op, ast.Sub):
                            return ast.Constant(value=node.left.value - node.right.value)
                        elif isinstance(node.op, ast.Mult):
                            return ast.Constant(value=node.left.value * node.right.value)
                        elif isinstance(node.op, ast.Div):
                            return ast.Constant(value=node.left.value / node.right.value)
                    except:
                        pass
                return self.generic_visit(node)
            
            def visit_Compare(self, node):
                # 简化比较
                if isinstance(node.left, ast.Constant) and len(node.comparators) == 1:
                    if isinstance(node.comparators[0], ast.Constant):
                        left = node.left.value
                        right = node.comparators[0].value
                        op = node.ops[0]
                        
                        if isinstance(op, ast.Eq):
                            return ast.Constant(value=(left == right))
                        elif isinstance(op, ast.NotEq):
                            return ast.Constant(value=(left != right))
                        elif isinstance(op, ast.Lt):
                            return ast.Constant(value=(left < right))
                        elif isinstance(op, ast.LtE):
                            return ast.Constant(value=(left <= right))
                        elif isinstance(op, ast.Gt):
                            return ast.Constant(value=(left > right))
                        elif isinstance(op, ast.GtE):
                            return ast.Constant(value=(left >= right))
                return self.generic_visit(node)
            
            def visit_If(self, node):
                # 简化 if True/if False
                if isinstance(node.test, ast.Constant):
                    if node.test.value is True:
                        return node.body
                    elif node.test.value is False:
                        return node.orelse if node.orelse else []
                return self.generic_visit(node)
        
        return ExpressionSimplifier().visit(tree)
    
    def _eliminate_dead_code(self, tree: ast.AST) -> ast.AST:
        """删除无用代码"""
        class DeadCodeEliminator(ast.NodeTransformer):
            def visit_Module(self, node):
                # 删除未使用的导入
                used_names = set()
                for n in ast.walk(node):
                    if isinstance(n, ast.Name):
                        used_names.add(n.id)
                
                new_body = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Import):
                        # 检查是否有别名被使用
                        new_names = [alias for alias in stmt.names 
                                    if alias.asname in used_names or alias.name in used_names]
                        if new_names:
                            stmt.names = new_names
                            new_body.append(stmt)
                    elif isinstance(stmt, ast.ImportFrom):
                        new_names = [alias for alias in stmt.names 
                                    if alias.asname in used_names or alias.name in used_names]
                        if new_names:
                            stmt.names = new_names
                            new_body.append(stmt)
                    else:
                        new_body.append(stmt)
                
                node.body = new_body
                return node
        
        return DeadCodeEliminator().visit(tree)
    
    def _post_optimize(self, code: str, aggressive: bool) -> str:
        """后处理优化"""
        result = code
        
        # 删除所有注释
        result = re.sub(r'#.*$', '', result, flags=re.MULTILINE)
        result = re.sub(r'"""[\s\S]*?"""', '', result)
        result = re.sub(r"'''[\s\S]*?'''", '', result)
        
        # 删除文档字符串
        result = re.sub(r'"""[\s\S]*?"""', '', result)
        result = re.sub(r"'''[\s\S]*?'''", '', result)
        
        # 删除空行
        result = re.sub(r'\n\s*\n', '\n', result)
        
        # 删除行首空格
        result = re.sub(r'^\s+', '', result, flags=re.MULTILINE)
        
        # 删除行尾空格
        result = re.sub(r'\s+$', '', result, flags=re.MULTILINE)
        
        # 简化空格
        result = re.sub(r'\s*([=+\-*/%\(\)\[\]\{\},:;])\s*', r'\1', result)
        
        # 关键字缩写
        replacements = [
            ('def ', 'd '), ('return ', 'r '), ('import ', 'i '),
            ('from ', 'f '), ('class ', 'c '), ('if ', 'if'),
            ('else:', 'el:'), ('elif ', 'ei '), ('for ', 'fo '),
            ('while ', 'w '), ('try:', 't:'), ('except ', 'e '),
            ('finally:', 'fn:'), ('with ', 'wi '), ('as ', 'a '),
            ('lambda ', 'l '), ('yield ', 'y '), ('assert ', 'as '),
            ('raise ', 'rs '), ('global ', 'g '), ('nonlocal ', 'nl '),
            ('pass', 'p'), ('break', 'b'), ('continue', 'co'),
            ('True', 'T'), ('False', 'F'), ('None', 'N'),
            ('and ', '& '), ('or ', '| '), ('not ', '!'),
            ('in ', '@ '), ('is ', '='),
        ]
        
        for pattern, replacement in replacements:
            result = result.replace(pattern, replacement)
        
        if aggressive:
            # 激进压缩
            result = re.sub(r'\s+', '', result)  # 删除所有空格
            result = result.replace("'", '')  # 删除单引号
            result = result.replace('"', '')  # 删除双引号
            result = result.replace('_', '')  # 删除下划线
            result = result.replace('self.', '')  # 简化self
            result = result.replace('.', '')  # 简化点号
        
        return result.strip()
    
    def _text_compress(self, code: str) -> str:
        """纯文本压缩 (AST解析失败时使用)"""
        result = code
        
        # 删除注释
        result = re.sub(r'#.*$', '', result, flags=re.MULTILINE)
        result = re.sub(r'"""[\s\S]*?"""', '', result)
        result = re.sub(r"'''[\s\S]*?'''", '', result)
        
        # 删除空行和多余空格
        result = re.sub(r'\n\s*\n', '\n', result)
        result = re.sub(r'^\s+', '', result, flags=re.MULTILINE)
        result = re.sub(r'\s+$', '', result, flags=re.MULTILINE)
        
        # 简化空格
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def _generate_short_names(self) -> List[str]:
        """生成短变量名"""
        # 单字母
        single = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # 双字母
        double = [a+b for a in 'abcdefghijklmnopqrstuvwxyz' 
                  for b in 'abcdefghijklmnopqrstuvwxyz']
        return single + double
    
    def _is_builtin(self, name: str) -> bool:
        """检查是否为内置名称"""
        builtins = {'True', 'False', 'None', 'len', 'print', 'range', 'list', 'dict', 'set',
                   'str', 'int', 'float', 'bool', 'type', 'isinstance', 'hasattr', 'getattr',
                   'setattr', 'delattr', 'dir', 'vars', 'locals', 'globals', 'eval', 'exec',
                   'compile', 'open', 'input', 'help', 'quit', 'exit', 'copyright', 'credits',
                   'license', 'print', 'sum', 'min', 'max', 'abs', 'round', 'pow', 'divmod',
                   'complex', 'bytes', 'bytearray', 'memoryview', 'ord', 'chr', 'bin', 'oct',
                   'hex', 'format', 'ascii', 'repr', 'sorted', 'reversed', 'enumerate', 'zip',
                   'map', 'filter', 'any', 'all', 'next', 'iter', 'slice', 'super', 'object',
                   'staticmethod', 'classmethod', 'property'}
        return name in builtins


class VariableReplacer(ast.NodeTransformer):
    """变量替换器 (用于循环展开)"""
    
    def __init__(self, old_name: str, new_value: ast.AST):
        self.old_name = old_name
        self.new_value = new_value
    
    def visit_Name(self, node):
        if node.id == self.old_name:
            return self.new_value
        return node


# 便捷函数
def optimize_code(code: str, aggressive: bool = True) -> str:
    """优化代码便捷函数"""
    restructurer = CodeRestructurer()
    result = restructurer.optimize(code, aggressive)
    return result.code


def optimize_with_stats(code: str, aggressive: bool = True) -> OptimizationResult:
    """优化并返回统计信息"""
    restructurer = CodeRestructurer()
    return restructurer.optimize(code, aggressive)


if __name__ == '__main__':
    # 测试
    test_code = '''
def calculate_total(items):
    """Calculate total price"""
    total = 0
    for item in items:
        price = item['price']
        quantity = item['quantity']
        total += price * quantity
    return total

def apply_discount(total, rate):
    return total * (1 - rate)

result = calculate_total([{'price': 10, 'quantity': 2}])
final = apply_discount(result, 0.1)
'''
    
    restructurer = CodeRestructurer()
    result = restructurer.optimize(test_code, aggressive=True)
    
    print(f"原代码 ({result.original_size} 字符):")
    print(test_code)
    print(f"\n优化后 ({result.optimized_size} 字符):")
    print(result.code)
    print(f"\n节省: {result.savings} 字符 ({result.ratio*100:.1f}%)")
    print(f"应用的转换: {result.applied_transforms}")
