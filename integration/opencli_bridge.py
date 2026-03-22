"""
OpenCLI Integration - OpenCLI整合模块 v3.2.0
Token经济大师与OpenCLI的深度整合
"""

import subprocess
import json
from typing import Dict, List, Optional

class OpenCLIBridge:
    """OpenCLI桥接器"""
    
    def __init__(self, opencli_path: str = None):
        self.opencli_path = opencli_path or '/root/.openclaw/workspace/opencli/dist/main.js'
    
    def execute(self, command: str) -> Dict:
        """执行OpenCLI命令"""
        full_cmd = f"node {self.opencli_path} {command}"
        
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except:
                    return {'success': True, 'output': result.stdout}
            else:
                return {'success': False, 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fetch_arxiv(self, query: str, limit: int = 5) -> List[Dict]:
        """抓取arXiv论文"""
        result = self.execute(f'arxiv search "{query}" --limit {limit} -f json')
        if result.get('success') and isinstance(result.get('output'), list):
            return result['output']
        return []
    
    def fetch_stackoverflow(self, limit: int = 5) -> List[Dict]:
        """抓取StackOverflow热榜"""
        result = self.execute(f'stackoverflow hot --limit {limit} -f json')
        if result.get('success') and isinstance(result.get('output'), list):
            return result['output']
        return []

class OptimizedAdapterGenerator:
    """优化适配器生成器"""
    
    def __init__(self):
        self.bridge = OpenCLIBridge()
    
    def generate_adapter(self, source: str, data_type: str = 'json') -> str:
        """生成优化后的适配器代码"""
        
        template = f'''#!/usr/bin/env python3
"""
OpenCLI优化适配器 - 自动生成
数据源: {{source}}
生成时间: {{timestamp}}
"""

import json
from typing import List, Dict

def fetch_data() -> List[Dict]:
    """抓取{{source}}数据"""
    # 使用OpenCLI抓取
    import subprocess
    cmd = "node {{opencli_path}} {{command}}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

def process_data(data: List[Dict]) -> Dict:
    """处理数据 - Token优化版本"""
    r = {{'c': len(data), 'i': []}}
    for x in data:
        r['i'].append({{'t': x.get('title', '')[:30], 'y': x.get('year', '')}})
    return r

def main():
    d = fetch_data()
    p = process_data(d)
    print(json.dumps(p))
    return p

if __name__ == '__main__':
    main()
'''
        
        from datetime import datetime
        
        code = template.format(
            source=source,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            opencli_path=self.bridge.opencli_path,
            command=self._get_command(source)
        )
        
        # 应用Token优化
        from ..optimizer.smart_optimizer import SmartOptimizer
        optimizer = SmartOptimizer()
        return optimizer.optimize_code_ast(code)
    
    def _get_command(self, source: str) -> str:
        """获取对应源的命令"""
        commands = {
            'arxiv': 'arxiv search "AI" --limit 5 -f json',
            'stackoverflow': 'stackoverflow hot --limit 5 -f json',
        }
        return commands.get(source, f'{source} list')
    
    def generate_optimized_pipeline(self, sources: List[str]) -> str:
        """生成优化数据处理流水线"""
        
        pipeline_code = '''#!/usr/bin/env python3
"""
OpenCLI优化流水线 - 自动生成
"""

import json
import subprocess
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

def fetch_source(source: str) -> List[Dict]:
    """抓取单个源"""
    cmds = {
        'arxiv': 'arxiv search "AI" --limit 5 -f json',
        'stackoverflow': 'stackoverflow hot --limit 5 -f json',
    }
    cmd = f"node /root/.openclaw/workspace/opencli/dist/main.js {{cmds.get(source, source)}}"
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode == 0:
        try:
            return json.loads(r.stdout)
        except:
            pass
    return []

def optimize_data(data: List[Dict]) -> Dict:
    """Token优化数据处理"""
    r = {{'t': len(data), 'd': []}}
    for x in data[:10]:  # 只处理前10条
        r['d'].append({{
            't': x.get('title', x.get('name', ''))[:20],
            's': x.get('score', x.get('year', 0))
        }})
    return r

def main():
    sources = {{sources}}
    
    # 并行抓取
    with ThreadPoolExecutor(max_workers=len(sources)) as e:
        results = list(e.map(fetch_source, sources))
    
    # 合并处理
    all_data = []
    for r in results:
        all_data.extend(r)
    
    optimized = optimize_data(all_data)
    print(json.dumps(optimized, ensure_ascii=False))
    return optimized

if __name__ == '__main__':
    main()
'''
        
        from datetime import datetime
        from ..optimizer.smart_optimizer import SmartOptimizer
        
        code = pipeline_code.format(
            sources=sources,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        optimizer = SmartOptimizer()
        return optimizer.optimize_code_ast(code)

class DataPipeline:
    """数据处理流水线"""
    
    def __init__(self):
        self.bridge = OpenCLIBridge()
        self.sources = []
        self.processors = []
    
    def add_source(self, source: str):
        """添加数据源"""
        self.sources.append(source)
    
    def add_processor(self, processor):
        """添加处理器"""
        self.processors.append(processor)
    
    def run(self) -> Dict:
        """运行流水线"""
        # 抓取数据
        all_data = []
        for source in self.sources:
            if source == 'arxiv':
                data = self.bridge.fetch_arxiv('AI', 5)
            elif source == 'stackoverflow':
                data = self.bridge.fetch_stackoverflow(5)
            else:
                data = []
            all_data.extend(data)
        
        # 处理数据
        result = {'total': len(all_data), 'items': all_data}
        for processor in self.processors:
            result = processor(result)
        
        return result
