"""Token经济大师 v3.0 - 测试套件"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skill-token-master-v3')

from analyzer.unified_analyzer import TokenAnalyzer
from optimizer.smart_optimizer import SmartOptimizer
from learner.evolution_engine import EvolutionEngine

def test_analyzer():
    """测试分析器"""
    print("🧪 测试分析器...")
    analyzer = TokenAnalyzer()
    
    # 测试提示词分析
    prompt = "请你非常仔细地帮我分析一下这个问题，非常感谢你的帮助。"
    result = analyzer.analyze(prompt, 'agent')
    assert result['content_type'] == 'agent'
    assert result['issue_count'] >= 1
    print("  ✅ 提示词分析通过")
    
    # 测试代码分析
    code = """def example():
    # 这是一个示例函数
    x = 1  # 初始化
    return x
"""
    result = analyzer.analyze(code, 'skill')
    assert result['content_type'] == 'skill'
    print("  ✅ 代码分析通过")
    
    return True

def test_optimizer():
    """测试优化器"""
    print("🧪 测试优化器...")
    optimizer = SmartOptimizer()
    
    # 测试提示词优化
    prompt = "请你非常仔细地帮我分析一下这个问题，非常感谢你的帮助。"
    result = optimizer.optimize(prompt, 'agent')
    assert result['saving_percentage'] > 0
    assert len(result['optimized']) < len(result['original'])
    print(f"  ✅ 提示词优化通过 (节省 {result['saving_percentage']}%)")
    
    # 测试代码优化
    code = """def example():
    # 这是一个示例函数
    x = 1  # 初始化
    return x
"""
    result = optimizer.optimize(code, 'skill')
    assert result['saving_percentage'] >= 0
    print(f"  ✅ 代码优化通过 (节省 {result['saving_percentage']}%)")
    
    return True

def test_learner():
    """测试学习系统"""
    print("🧪 测试学习系统...")
    import tempfile
    import shutil
    
    # 使用临时目录，避免状态累积
    temp_dir = tempfile.mkdtemp()
    try:
        learner = EvolutionEngine(data_dir=temp_dir)
        
        # 模拟优化记录
        evolution_triggered = False
        for i in range(105):  # 超过100触发进化
            result = learner.record_optimization(
                original="test " * 100,
                optimized="test" * 50,
                saving_pct=50.0,
                content_type='agent'
            )
            if result:  # 进化触发
                evolution_triggered = True
                print(f"  ✅ 进化触发成功 (第{result['evolution_number']}次)")
        
        assert evolution_triggered, "进化应该被触发"
        
        report = learner.get_learning_report()
        assert report['total_usage'] == 105
        print(f"  ✅ 学习报告正常 (使用次数: {report['total_usage']})")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return True

def deep_evaluate():
    """深度评测"""
    print("\n🔬 深度评测...")
    optimizer = SmartOptimizer()
    
    # 测试1: 提示词优化
    test_prompts = [
        ("非常仔细地分析", 30),
        ("请你帮忙处理一下这个问题", 25),
        ("非常感谢你的帮助和支持", 20),
    ]
    
    prompt_savings = []
    for prompt, min_saving in test_prompts:
        result = optimizer.optimize(prompt, 'agent')
        prompt_savings.append(result['saving_percentage'])
        assert result['saving_percentage'] >= min_saving, f"优化不足: {result['saving_percentage']}% < {min_saving}%"
    
    avg_prompt_saving = sum(prompt_savings) / len(prompt_savings)
    print(f"  ✅ 提示词优化平均节省: {avg_prompt_saving:.1f}%")
    
    # 测试2: 代码优化
    test_code = '''
def calculate_sum(numbers):
    # 计算数字列表的和
    result = 0  # 初始化结果
    for num in numbers:  # 遍历每个数字
        result += num  # 累加
    return result  # 返回结果
'''
    result = optimizer.optimize(test_code, 'skill')
    assert result['saving_percentage'] >= 20
    print(f"  ✅ 代码优化节省: {result['saving_percentage']:.1f}%")
    
    print("\n🎉 所有深度评测通过!")
    return True

def main():
    print("=" * 60)
    print("🚀 Token经济大师 v3.0 - 测试套件")
    print("=" * 60)
    
    try:
        test_analyzer()
        test_optimizer()
        test_learner()
        deep_evaluate()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！技能质量优秀")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n💥 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
