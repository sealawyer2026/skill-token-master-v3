#!/usr/bin/env python3
"""
Token经济大师 v3.2.0 完整测试
包含Day 1-6所有功能
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

def test_all_features():
    """测试所有功能"""
    print("\n" + "="*70)
    print("🚀 Token经济大师 v3.2.0 完整功能测试")
    print("="*70)
    
    tests_passed = 0
    tests_total = 0
    
    # 1. 基础功能测试
    print("\n【Day 1-2】基础框架功能")
    print("-"*70)
    
    try:
        from resiliency import RetryManager, FallbackManager
        retry = RetryManager()
        print("✅ 弹性容错模块加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 弹性容错模块失败: {e}")
    tests_total += 1
    
    try:
        from billing import UsageTracker, QuotaManager
        tracker = UsageTracker()
        print("✅ 计费统计模块加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 计费统计模块失败: {e}")
    tests_total += 1
    
    # 2. 分析器功能
    try:
        from analyzer.mcp_analyzer import MCPAnalyzer
        from analyzer.sql_analyzer import SQLAnalyzer
        mcp = MCPAnalyzer()
        sql = SQLAnalyzer()
        print("✅ MCP/SQL分析器加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"❌ MCP/SQL分析器失败: {e}")
    tests_total += 1
    
    # 3. Day 3-4 优化功能
    print("\n【Day 3-4】核心优化功能")
    print("-"*70)
    
    try:
        from optimizer.extreme_compressor import ExtremeCompressor
        compressor = ExtremeCompressor()
        text = "请帮我分析一下数据"
        compressed = compressor.compress(text)
        stats = compressor.get_stats(text, compressed)
        print(f"✅ 极致压缩: {stats['compression_ratio']:.1f}% 节省")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 极致压缩失败: {e}")
    tests_total += 1
    
    try:
        from optimizer.ast_optimizer import ASTOptimizer
        ast_opt = ASTOptimizer()
        code = "def test(): return 1"
        optimized = ast_opt.optimize(code)
        print("✅ AST优化器工作正常")
        tests_passed += 1
    except Exception as e:
        print(f"❌ AST优化失败: {e}")
    tests_total += 1
    
    try:
        from optimizer.markdown_optimizer import MarkdownOptimizer
        md_opt = MarkdownOptimizer()
        md = "# 标题\n\n内容"
        optimized = md_opt.optimize(md)
        print("✅ Markdown优化器工作正常")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Markdown优化失败: {e}")
    tests_total += 1
    
    # 4. Day 5-6 整合功能
    print("\n【Day 5-6】整合与计费功能")
    print("-"*70)
    
    try:
        from integration.opencli_bridge import OpenCLIBridge
        bridge = OpenCLIBridge()
        print("✅ OpenCLI桥接器加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"❌ OpenCLI桥接器失败: {e}")
    tests_total += 1
    
    try:
        from billing.billing_engine import BillingEngine, UsageDashboard
        billing = BillingEngine()
        billing.set_user_tier('test_user', 'pro')
        dashboard = UsageDashboard(billing)
        print("✅ 计费引擎加载成功")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 计费引擎失败: {e}")
    tests_total += 1
    
    # 5. SmartOptimizer v3.2.0
    print("\n【SmartOptimizer v3.2.0】统一接口")
    print("-"*70)
    
    try:
        from optimizer.smart_optimizer import SmartOptimizer
        optimizer = SmartOptimizer()
        
        # 测试所有新方法
        text = "请帮我分析"
        result = optimizer.optimize_extreme(text)
        print(f"✅ optimize_extreme: {len(result)}字符")
        
        code = "def f(x): return x"
        result = optimizer.optimize_code_ast(code)
        print(f"✅ optimize_code_ast: 成功")
        
        md = "# 标题"
        result = optimizer.optimize_markdown(md)
        print(f"✅ optimize_markdown: {len(result)}字符")
        
        mcp = '{"tools":[]}'
        result = optimizer.optimize_mcp(mcp)
        print(f"✅ optimize_mcp: 成功")
        
        sql = "SELECT * FROM t"
        result = optimizer.optimize_sql(sql)
        print(f"✅ optimize_sql: 成功")
        
        tests_passed += 1
    except Exception as e:
        print(f"❌ SmartOptimizer v3.2.0失败: {e}")
    tests_total += 1
    
    # 最终结果
    print("\n" + "="*70)
    print("📊 测试结果汇总")
    print("="*70)
    print(f"通过: {tests_passed}/{tests_total}")
    print(f"失败: {tests_total - tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 所有功能正常！v3.2.0 升级完成！")
        return True
    else:
        print(f"\n⚠️  {tests_total - tests_passed} 个功能需要修复")
        return False

def main():
    success = test_all_features()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
