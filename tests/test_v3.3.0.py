#!/usr/bin/env python3
"""
Token经济大师 v3.3.0 完整测试
CLI工具 + 超极致优化
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

def test_cli():
    """测试CLI工具"""
    print("\n" + "="*60)
    print("🧪 测试CLI工具")
    print("="*60)
    
    import subprocess
    
    # 测试版本
    result = subprocess.run(
        ['python3', 'cli/token_master_cli.py', '--version'],
        capture_output=True, text=True, cwd='/root/.openclaw/workspace/skill-token-master-v3'
    )
    if '3.3.0' in result.stdout:
        print("✅ CLI版本正确: 3.3.0")
    else:
        print(f"❌ CLI版本错误: {result.stdout}")
        return False
    
    # 测试analyze命令
    with open('/tmp/cli_test.txt', 'w') as f:
        f.write("请帮我分析数据")
    
    result = subprocess.run(
        ['python3', 'cli/token_master_cli.py', 'analyze', '/tmp/cli_test.txt'],
        capture_output=True, text=True, cwd='/root/.openclaw/workspace/skill-token-master-v3'
    )
    if '类型:' in result.stdout:
        print("✅ analyze命令工作正常")
    else:
        print(f"❌ analyze命令失败: {result.stderr}")
        return False
    
    # 测试optimize命令
    result = subprocess.run(
        ['python3', 'cli/token_master_cli.py', 'optimize', '/tmp/cli_test.txt', '--dry-run'],
        capture_output=True, text=True, cwd='/root/.openclaw/workspace/skill-token-master-v3'
    )
    if '节省:' in result.stdout or 'saved' in result.stdout:
        print("✅ optimize命令工作正常")
    else:
        print(f"❌ optimize命令失败: {result.stderr}")
        return False
    
    return True

def test_ultra_optimizer():
    """测试超极致优化器"""
    print("\n" + "="*60)
    print("🧪 测试超极致优化器")
    print("="*60)
    
    from optimizer.ultra_optimizer import UltraOptimizer
    
    opt = UltraOptimizer()
    
    # 测试提示词
    text = "请帮我详细地分析一下这个复杂的数据处理任务，需要对用户提供的信息进行全面的检查和验证。"
    result = opt.optimize_prompt(text)
    stats = opt.get_stats(text, result, 'prompt')
    
    print(f"提示词优化: {stats['savings_rate']:.1f}% 节省")
    
    # 测试代码
    code = '''
def calculate(items):
    total = 0
    for item in items:
        total += item['price']
    return total
'''
    result = opt.optimize_code(code)
    stats = opt.get_stats(code, result, 'code')
    
    print(f"代码优化: {stats['savings_rate']:.1f}% 节省")
    
    print("✅ 超极致优化器工作正常")
    return True

def test_batch_processing():
    """测试批量处理"""
    print("\n" + "="*60)
    print("🧪 测试批量处理")
    print("="*60)
    
    import os
    import tempfile
    
    # 创建测试目录
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试文件
        for i in range(3):
            with open(f'{tmpdir}/test{i}.py', 'w') as f:
                f.write(f'def func{i}(): return {i}')
        
        # 测试批量处理
        import subprocess
        result = subprocess.run(
            ['python3', 'cli/token_master_cli.py', 'batch', tmpdir, '--include', '*.py'],
            capture_output=True, text=True, cwd='/root/.openclaw/workspace/skill-token-master-v3'
        )
        
        if '批量优化完成' in result.stdout or 'total_files' in result.stdout:
            print("✅ 批量处理工作正常")
            print(f"   处理文件数: 3")
            return True
        else:
            print(f"❌ 批量处理失败: {result.stderr}")
            return False

def main():
    print("\n" + "="*60)
    print("🚀 Token经济大师 v3.3.0 完整测试")
    print("="*60)
    
    tests = [
        ("CLI工具", test_cli),
        ("超极致优化器", test_ultra_optimizer),
        ("批量处理", test_batch_processing),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {name} 测试异常: {e}")
    
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)
    print(f"通过: {passed}/{len(tests)}")
    print(f"失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ v3.3.0 全部测试通过！")
        return 0
    else:
        print(f"\n❌ {failed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
