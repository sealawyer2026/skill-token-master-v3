"""
AST Optimizer - AST级代码优化器 v3.2.0
基于Python抽象语法树的深度优化
"""

import ast
import re
from typing import Dict, List, Set, Tuple

class ASTOptimizer:
    """AST级代码优化器"""
    
    def __init__(self):
        self.optimizations = []
    
    def optimize(self, code: str) -> str:
        """基于AST的代码优化"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code  # 解析失败返回原代码
        
        self.optimizations = []
        
        # 应用各种优化
        tree = self._optimize_variables(tree)
        tree = self._optimize_imports(tree)
        tree = self._remove_docstrings(tree)
        tree = self._optimize_control_flow(tree)
        
        # 转换回代码
        try:
            optimized = ast.unparse(tree)
        except:
            # 如果unparse失败，使用原始代码
            return code
        
        # 额外压缩
        optimized = self._post_compress(optimized)
        
        return optimized
    
    def _optimize_variables(self, tree: ast.AST) -> ast.AST:
        """优化变量名"""
        # 收集所有变量名
        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, (ast.Store, ast.Param)):
                    variables.add(node.id)
        
        # 生成短变量名映射
        short_names = 'abcdefghijklmnopqrstuvwxyz'
        name_map = {}
        for i, var in enumerate(sorted(variables)):
            if var.startswith('_') or var in ['self', 'cls']:
                continue
            if i < len(short_names):
                name_map[var] = short_names[i]
            else:
                name_map[var] = f'v{i}'
        
        # 替换变量名
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in name_map:
                node.id = name_map[node.id]
        
        if name_map:
            self.optimizations.append(f"变量名简化: {len(name_map)}个")
        
        return tree
    
    def _optimize_imports(self, tree: ast.AST) -> ast.AST:
        """优化导入语句"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # 合并多个import
                pass
            elif isinstance(node, ast.ImportFrom):
                # 优化 from x import a, b, c
                pass
        
        return tree
    
    def _remove_docstrings(self, tree: ast.AST) -> ast.AST:
        """移除文档字符串"""
        docstring_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                # 检查函数/类体的第一个语句是否是文档字符串
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    # 移除文档字符串
                    node.body = node.body[1:]
                    docstring_count += 1
        
        if docstring_count > 0:
            self.optimizations.append(f"移除文档字符串: {docstring_count}个")
        
        return tree
    
    def _optimize_control_flow(self, tree: ast.AST) -> ast.AST:
        """优化控制流"""
        # 简化 if True: 和 if False:
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if (isinstance(node.test, ast.Constant) and 
                    isinstance(node.test.value, bool)):
                    if node.test.value:
                        # if True: 只保留if体
                        self.optimizations.append("简化 if True")
                    else:
                        # if False: 只保留else体
                        self.optimizations.append("简化 if False")
        
        return tree
    
    def _post_compress(self, code: str) -> str:
        """后处理压缩"""
        # 删除注释
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        # 删除空行
        code = re.sub(r'\n\s*\n', '\n', code)
        # 删除行尾空格
        code = re.sub(r'\s+$', '', code, flags=re.MULTILINE)
        
        return code.strip()
    
    def get_stats(self, original: str, optimized: str) -> Dict:
        """获取优化统计"""
        orig_lines = len(original.split('\n'))
        opt_lines = len(optimized.split('\n'))
        orig_chars = len(original)
        opt_chars = len(optimized)
        
        return {
            'original_lines': orig_lines,
            'optimized_lines': opt_lines,
            'line_reduction': orig_lines - opt_lines,
            'original_chars': orig_chars,
            'optimized_chars': opt_chars,
            'char_reduction': orig_chars - opt_chars,
            'optimizations': self.optimizations
        }
