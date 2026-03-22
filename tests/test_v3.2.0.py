#!/usr/bin/env python3
"""
Token经济大师 v3.2.0 综合测试
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

from analyzer.unified_analyzer import TokenAnalyzer
from analyzer.mcp_analyzer import MCPAnalyzer, MCPOptimizer
from analyzer.sql_analyzer import SQLAnalyzer, SQLOptimizer
from resiliency import RetryManager, RetryConfig, FallbackManager
from billing import UsageTracker, QuotaManager

def test_mcp_analysis():
    """测试 MCP 分析"""
    print("\n" + "="*60)
    print("🧪 测试 MCP 分析")
    print("="*60)
    
    mcp_config = '''{
        "tools": [
            {
                "name": "get_weather_tool",
                "description": "这是一个用于获取天气的工具",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        ]
    }'''
    
    analyzer = MCPAnalyzer()
    result = analyzer.analyze(mcp_config)
    
    print(f"✅ MCP 分析完成")
    print(f"   发现问题: {result['metrics']['total_issues']}")
    print(f"   严重程度: {result['severity']}")
    
    # 测试优化
    optimizer = MCPOptimizer()
    optimized = optimizer.optimize(mcp_config)
    
    orig_len = len(mcp_config)
    opt_len = len(optimized)
    savings = (1 - opt_len/orig_len) * 100
    
    print(f"✅ MCP 优化完成")
    print(f"   原始大小: {orig_len} 字节")
    print(f"   优化后: {opt_len} 字节")
    print(f"   节省: {savings:.1f}%")
    
    return True

def test_sql_analysis():
    """测试 SQL 分析"""
    print("\n" + "="*60)
    print("🧪 测试 SQL 分析")
    print("="*60)
    
    sql = """
    SELECT *
    FROM users
    WHERE status = 'active'
    ORDER BY created_at DESC
    """
    
    analyzer = SQLAnalyzer()
    result = analyzer.analyze(sql)
    
    print(f"✅ SQL 分析完成")
    print(f"   发现问题: {len(result['issues'])}")
    for issue in result['issues']:
        print(f"   - {issue['type']}: {issue['message']}")
    
    # 测试优化
    optimizer = SQLOptimizer()
    optimized = optimizer.optimize(sql)
    savings = optimizer.get_savings(sql, optimized)
    
    print(f"✅ SQL 优化完成")
    print(f"   原始Token: {savings['original_tokens']}")
    print(f"   优化后Token: {savings['optimized_tokens']}")
    print(f"   节省: {savings['savings_rate']:.1f}%")
    
    return True

def test_resiliency():
    """测试弹性容错"""
    print("\n" + "="*60)
    print("🧪 测试弹性容错")
    print("="*60)
    
    # 测试重试
    config = RetryConfig(max_attempts=3, base_delay=0.1)
    retry = RetryManager(config)
    
    call_count = 0
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception(f"模拟失败 #{call_count}")
        return "成功!"
    
    try:
        result = retry.execute(flaky_func)
        print(f"✅ 重试机制工作正常")
        print(f"   调用次数: {call_count}")
        print(f"   结果: {result}")
    except Exception as e:
        print(f"❌ 重试失败: {e}")
        return False
    
    # 测试降级
    fallback = FallbackManager()
    
    def main_func():
        raise Exception("主功能失败")
    
    def fallback_func():
        return "降级结果"
    
    fallback.register('main_func', fallback_func)
    result = fallback.execute_with_fallback(main_func)
    
    print(f"✅ 降级策略工作正常")
    print(f"   结果: {result}")
    
    return True

def test_billing():
    """测试计费统计"""
    print("\n" + "="*60)
    print("🧪 测试计费统计")
    print("="*60)
    
    tracker = UsageTracker()
    
    # 记录使用
    tracker.record('optimize', 1000, 600, 'python', True)
    tracker.record('optimize', 2000, 1200, 'python', True)
    tracker.record('analyze', 500, 300, 'json', True)
    
    # 获取统计
    stats = tracker.get_stats(30)
    
    print(f"✅ 使用统计工作正常")
    print(f"   总调用: {stats['total_calls']}")
    print(f"   输入Token: {stats['total_input_tokens']}")
    print(f"   输出Token: {stats['total_output_tokens']}")
    print(f"   节省比例: {stats['savings_rate']:.1f}%")
    
    # 测试配额
    quota = QuotaManager()
    quota.set_quota('user_001', 10000)
    
    can_use = quota.check_quota('user_001', 5000)
    remaining = quota.get_remaining('user_001')
    
    print(f"✅ 配额管理工作正常")
    print(f"   用户配额: 10000")
    print(f"   检查5000: {'通过' if can_use else '拒绝'}")
    print(f"   剩余配额: {remaining}")
    
    return True

def test_unified_analyzer():
    """测试统一分析器"""
    print("\n" + "="*60)
    print("🧪 测试统一分析器 v3.2.0")
    print("="*60)
    
    analyzer = TokenAnalyzer()
    
    # 测试 MCP 检测
    mcp_content = '{"tools": [{"name": "test"}]}'
    result = analyzer.analyze(mcp_content)
    assert result['content_type'] == 'mcp', f"期望mcp, 得到{result['content_type']}"
    print(f"✅ MCP 类型检测正确")
    
    # 测试 SQL 检测
    sql_content = 'SELECT * FROM users'
    result = analyzer.analyze(sql_content)
    assert result['content_type'] == 'sql', f"期望sql, 得到{result['content_type']}"
    print(f"✅ SQL 类型检测正确")
    
    # 测试 Agent 检测
    agent_content = '请分析一下这个数据'
    result = analyzer.analyze(agent_content)
    assert result['content_type'] == 'agent', f"期望agent, 得到{result['content_type']}"
    print(f"✅ Agent 类型检测正确")
    
    return True

def main():
    print("\n" + "="*60)
    print("🚀 Token经济大师 v3.2.0 综合测试")
    print("="*60)
    
    tests = [
        ("MCP 分析", test_mcp_analysis),
        ("SQL 分析", test_sql_analysis),
        ("弹性容错", test_resiliency),
        ("计费统计", test_billing),
        ("统一分析器", test_unified_analyzer),
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
        print("\n✅ 所有测试通过！v3.2.0 功能正常。")
        return 0
    else:
        print(f"\n❌ {failed} 个测试失败，需要修复。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
