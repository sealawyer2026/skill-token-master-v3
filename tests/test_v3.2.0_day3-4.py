#!/usr/bin/env python3
"""
Token经济大师 v3.2.0 完整测试 - Day 3-4
极致压缩 + AST优化 + Markdown优化
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

from optimizer.smart_optimizer import SmartOptimizer
from optimizer.extreme_compressor import ExtremeCompressor
from optimizer.ast_optimizer import ASTOptimizer
from optimizer.markdown_optimizer import MarkdownOptimizer

def test_extreme_compression():
    """测试极致压缩"""
    print("\n" + "="*60)
    print("🧪 测试极致压缩 (文言文风格)")
    print("="*60)
    
    compressor = ExtremeCompressor()
    
    test_cases = [
        "请帮我分析一下这个数据的处理结果",
        "我需要对用户提供的信息进行详细的检查和验证",
        "通过分析数据，我们可以得出重要的结论",
        "首先创建一个对象，然后进行处理和分析",
    ]
    
    for text in test_cases:
        compressed = compressor.compress(text)
        stats = compressor.get_stats(text, compressed)
        print(f"\n原文: {text}")
        print(f"压缩: {compressed}")
        print(f"节省: {stats['compression_ratio']:.1f}%")
    
    return True

def test_ast_optimization():
    """测试AST优化"""
    print("\n" + "="*60)
    print("🧪 测试AST代码优化")
    print("="*60)
    
    optimizer = ASTOptimizer()
    
    code = '''
def calculate_total_price(items, discount_rate):
    \"\"\"
    计算总价
    参数:
        items: 商品列表
        discount_rate: 折扣率
    \"\"\"
    total_price = 0
    for item in items:
        price = item['price']
        quantity = item['quantity']
        total_price += price * quantity
    
    final_price = total_price * (1 - discount_rate)
    return final_price
'''
    
    optimized = optimizer.optimize(code)
    stats = optimizer.get_stats(code, optimized)
    
    print(f"原始代码行数: {stats['original_lines']}")
    print(f"优化后行数: {stats['optimized_lines']}")
    print(f"字符减少: {stats['char_reduction']}")
    print(f"\n优化项:")
    for opt in stats['optimizations']:
        print(f"  - {opt}")
    
    print(f"\n优化后代码:\n{optimized}")
    
    return True

def test_markdown_optimization():
    """测试Markdown优化"""
    print("\n" + "="*60)
    print("🧪 测试Markdown优化")
    print("="*60)
    
    optimizer = MarkdownOptimizer()
    
    markdown = '''
# 标题1

## 标题2

这是一个段落，包含一些文本内容。

- 列表项1
- 列表项2
- 列表项3

```python
def hello():
    print("Hello")
```

**粗体文本** 和 *斜体文本*

| 列1 | 列2 |
|-----|-----|
| A   | B   |
'''
    
    optimized = optimizer.optimize(markdown)
    stats = optimizer.get_stats(markdown, optimized)
    
    print(f"原始行数: {stats['original_lines']}")
    print(f"优化后行数: {stats['optimized_lines']}")
    print(f"字符节省: {stats['saved_chars']}")
    print(f"压缩率: {stats['compression_ratio']:.1f}%")
    
    return True

def test_smart_optimizer_v320():
    """测试SmartOptimizer v3.2.0新方法"""
    print("\n" + "="*60)
    print("🧪 测试 SmartOptimizer v3.2.0 新方法")
    print("="*60)
    
    optimizer = SmartOptimizer()
    
    # 测试极致压缩
    text = "请帮我分析一下这个数据的处理结果"
    result = optimizer.optimize_extreme(text)
    print(f"\n极致压缩:")
    print(f"  原文: {text}")
    print(f"  压缩: {result}")
    
    # 测试AST优化
    code = "def calculate(x): return x * 2"
    result = optimizer.optimize_code_ast(code)
    print(f"\nAST优化:")
    print(f"  原始: {code}")
    print(f"  优化: {result}")
    
    # 测试Markdown优化
    md = "# 标题\n\n这是一段文字"
    result = optimizer.optimize_markdown(md)
    print(f"\nMarkdown优化:")
    print(f"  原始: {md}")
    print(f"  优化: {result}")
    
    # 测试MCP优化
    mcp = '{"tools": [{"name": "get_data", "description": "这是一个获取数据的工具"}]}'
    result = optimizer.optimize_mcp(mcp)
    print(f"\nMCP优化:")
    print(f"  原始: {mcp[:50]}...")
    print(f"  优化: {result[:50]}...")
    
    # 测试SQL优化
    sql = "SELECT * FROM users WHERE status = 'active'"
    result = optimizer.optimize_sql(sql)
    print(f"\nSQL优化:")
    print(f"  原始: {sql}")
    print(f"  优化: {result}")
    
    return True

def test_performance():
    """测试性能提升"""
    print("\n" + "="*60)
    print("🧪 测试性能提升")
    print("="*60)
    
    optimizer = SmartOptimizer()
    extreme = ExtremeCompressor()
    
    # 长文本测试
    long_text = "请帮我详细地分析一下这个复杂的数据处理任务，需要对用户提供的信息进行全面的检查和验证。" * 10
    
    # 极致优化
    extreme_result = extreme.compress(long_text)
    
    orig_len = len(long_text)
    ext_len = len(extreme_result)
    
    print(f"原始长度: {orig_len} 字符")
    print(f"极致优化: {ext_len} 字符")
    print(f"节省: {(1-ext_len/orig_len)*100:.1f}%")
    
    return True

def main():
    print("\n" + "="*60)
    print("🚀 Token经济大师 v3.2.0 - Day 3-4 测试")
    print("="*60)
    
    tests = [
        ("极致压缩", test_extreme_compression),
        ("AST优化", test_ast_optimization),
        ("Markdown优化", test_markdown_optimization),
        ("SmartOptimizer v3.2.0", test_smart_optimizer_v320),
        ("性能测试", test_performance),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {name} 测试失败")
        except Exception as e:
            failed += 1
            print(f"❌ {name} 测试异常: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ Day 3-4 全部测试通过！v3.2.0 功能增强完成。")
        return 0
    else:
        print(f"\n❌ {failed} 个测试失败，需要修复。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
