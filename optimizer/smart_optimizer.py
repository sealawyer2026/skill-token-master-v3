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
            # v3.0.5增强：更激进压缩
            (r'虽然|尽管', '虽'),
            (r'可能|也许|或许', '或'),
            (r'肯定|确定|绝对', '定'),
            (r'大概|大约|约莫', '约'),
            (r'几乎|将近|差不多', '近'),
            (r'只要', '若'),
            (r'只有', '唯'),
            (r'不仅|不只|不光', '不'),
            (r'而且|并且|况且', '且'),
            (r'或者|或是|或', '或'),
            (r'问题', '题'),
            (r'方法', '法'),
            (r'方案', '案'),
            (r'解决', '解'),
            (r'结果', '果'),
            (r'过程', '程'),
            (r'原因', '因'),
            (r'目的', '的'),
            (r'意义', '义'),
            (r'作用', '用'),
            (r'效果', '效'),
            (r'影响', '响'),
            (r'关系', '系'),
            (r'情况', '况'),
            (r'状态', '态'),
            (r'形式', '式'),
            (r'方式', '式'),
            (r'结构', '构'),
            (r'功能', '能'),
            (r'系统', '系'),
            (r'部分', '部'),
            (r'方面', '面'),
            (r'角度', '角'),
            (r'层次', '层'),
            (r'阶段', '阶'),
            (r'步骤', '步'),
            (r'环节', '环'),
            (r'过程', '程'),
            (r'开始', '始'),
            (r'结束', '终'),
            (r'完成', '毕'),
            (r'实现', '现'),
            (r'达到', '达'),
            (r'获得', '得'),
            (r'得到', '得'),
            (r'失去', '失'),
            (r'产生', '生'),
            (r'形成', '形'),
            (r'变成', '变'),
            (r'成为', '成'),
            (r'作为', '作'),
            (r'为了', '为'),
            (r'由于', '因'),
            (r'根据', '依'),
            (r'按照', '依'),
            (r'通过', '经'),
            (r'经过', '经'),
            (r'随着', '随'),
            (r'面对', '对'),
            (r'针对', '对'),
            (r'对于', '对'),
            (r'任务', '务'),
            (r'工作', '工'),
            (r'项目', '项'),
            (r'操作', '操'),
            (r'执行', '执'),
            (r'运行', '运'),
            (r'调用', '调'),
            (r'使用', '用'),
            (r'应用', '用'),
            (r'利用', '用'),
            (r'采用', '采'),
            (r'选择', '选'),
            (r'确定', '定'),
            (r'判断', '判'),
            (r'比较', '比'),
            (r'对比', '比'),
            (r'检查', '查'),
            (r'验证', '验'),
            (r'确认', '认'),
            (r'确保', '保'),
            (r'保证', '保'),
            (r'维护', '护'),
            (r'管理', '管'),
            (r'控制', '控'),
            (r'监控', '监'),
            (r'监督', '督'),
            (r'观察', '观'),
            (r'查看', '看'),
            (r'显示', '示'),
            (r'展示', '示'),
            (r'表现', '现'),
            (r'体现', '现'),
            (r'呈现', '呈'),
            (r'出现', '出'),
            (r'发生', '发'),
            (r'存在', '存'),
            (r'具有', '具'),
            (r'拥有', '拥'),
            (r'包含', '含'),
            (r'包括', '含'),
            (r'涉及', '涉'),
            (r'关于', '关'),
            (r'相关', '关'),
            (r'有关', '关'),
            (r'联系', '联'),
            (r'关联', '联'),
            (r'结合', '合'),
            (r'配合', '配'),
            (r'匹配', '配'),
            (r'适合', '适'),
            (r'适应', '适'),
            (r'对应', '应'),
            (r'响应', '响'),
            (r'反应', '应'),
            (r'反馈', '馈'),
            (r'返回', '返'),
            (r'回报', '报'),
            (r'回答', '答'),
            (r'回复', '复'),
            (r'响应', '应'),
            # v3.0.8-10: 终极压缩
            (r'用户', '户'),
            (r'客户', '户'),
            (r'顾客', '户'),
            (r'系统', '系'),
            (r'平台', '台'),
            (r'程序', '程'),
            (r'代码', '码'),
            (r'文件', '档'),
            (r'文档', '档'),
            (r'记录', '录'),
            (r'日志', '志'),
            (r'报告', '报'),
            (r'报表', '表'),
            (r'表格', '表'),
            (r'图表', '图'),
            (r'图片', '图'),
            (r'图像', '图'),
            (r'照片', '照'),
            (r'视频', '影'),
            (r'音频', '音'),
            (r'文本', '文'),
            (r'内容', '容'),
            (r'信息', '息'),
            (r'消息', '息'),
            (r'通知', '知'),
            (r'提醒', '醒'),
            (r'警告', '警'),
            (r'错误', '错'),
            (r'异常', '异'),
            (r'问题', '题'),
            (r'故障', '障'),
            (r'缺陷', '缺'),
            (r'漏洞', '洞'),
            (r'风险', '险'),
            (r'安全', '安'),
            (r'保护', '护'),
            (r'防御', '防'),
            (r'攻击', '击'),
            (r'入侵', '侵'),
            (r'威胁', '胁'),
            (r'病毒', '毒'),
            (r'木马', '马'),
            (r'恶意', '恶'),
            (r'垃圾', '圾'),
            (r'广告', '广'),
            (r'推广', '推'),
            (r'营销', '销'),
            (r'销售', '售'),
            (r'购买', '购'),
            (r'支付', '付'),
            (r'订单', '单'),
            (r'交易', '易'),
            (r'转账', '转'),
            (r'充值', '充'),
            (r'提现', '提'),
            (r'退款', '退'),
            (r'退货', '退'),
            (r'换货', '换'),
            (r'维修', '修'),
            (r'保养', '养'),
            (r'清洁', '洁'),
            (r'整理', '理'),
            (r'分类', '类'),
            (r'排序', '序'),
            (r'筛选', '筛'),
            (r'过滤', '滤'),
            (r'搜索', '搜'),
            (r'查询', '查'),
            (r'查找', '找'),
            (r'匹配', '配'),
            (r'替换', '替'),
            (r'修改', '改'),
            (r'更新', '新'),
            (r'升级', '升'),
            (r'降级', '降'),
            (r'备份', '备'),
            (r'恢复', '恢'),
            (r'撤销', '撤'),
            (r'重做', '做'),
            (r'复制', '复'),
            (r'粘贴', '粘'),
            (r'剪切', '剪'),
            (r'删除', '删'),
            (r'清空', '清'),
            (r'重置', '重'),
            (r'初始化', '始'),
            (r'配置', '配'),
            (r'设置', '设'),
            (r'参数', '参'),
            (r'属性', '性'),
            (r'特性', '性'),
            (r'特征', '征'),
            (r'特点', '点'),
            (r'优点', '优'),
            (r'缺点', '劣'),
            (r'优势', '势'),
            (r'劣势', '劣'),
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
            # v3.0.5增强：更多代码压缩
            (r'and\s+len\((\w+)\)\s*>\s*0', r'and \1'),
            (r'and\s+(\w+)\s*is\s*not\s*None', r'and \1'),
            (r'if\s+(\w+)\s+and\s+len\((\w+)\)\s*>\s*0', r'if \1 and \2'),
            (r'def\s+(\w+)\(([^)]*)\):\s*\n\s*(\w+)=\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*if\s+(\w+):\s*\n\s*\3\.append\((\w+)\)\s*\n\s*return\s+\3', r'def \1(\2):return [\7 for \4 in \5 if \6]'),
            (r'(\w+)\s*=\s*\[\]', r'\1=[]'),
            (r'(\w+)\.append\(([^)]+)\)', r'\1+=[\2]'),
            # v3.0.5: 字典返回转元组
            (r'return\s*\{\s*["\']total["\']\s*:\s*(\w+)\s*\}', r'return(\1,)'),
            (r'return\s*\{\s*["\']value["\']\s*:\s*(\w+)\s*\}', r'return(\1,)'),
            (r'return\s*\{\s*["\']result["\']\s*:\s*(\w+)\s*\}', r'return(\1,)'),
            (r'return\s*\{\s*["\']data["\']\s*:\s*(\w+)\s*\}', r'return(\1,)'),
            (r'\bitem\b', 'i'),
            (r'\bitems\b', 's'),
            (r'\bdata\b', 'd'),
            (r'\bresult\b', 'r'),
            (r'\bvalue\b', 'v'),
            (r'\bcount\b', 'c'),
            (r'\bindex\b', 'n'),
            (r'\bkey\b', 'k'),
            # v3.0.7: 更多变量名简化
            (r'\binput\b', 'in'),
            (r'\boutput\b', 'out'),
            (r'\berror\b', 'err'),
            (r'\bmessage\b', 'msg'),
            (r'\bconfig\b', 'cfg'),
            (r'\boption\b', 'opt'),
            (r'\bparam\b', 'p'),
            (r'\bargument\b', 'arg'),
            (r'\bresponse\b', 'res'),
            (r'\brequest\b', 'req'),
            (r'\bclient\b', 'cli'),
            (r'\bserver\b', 'srv'),
            (r'\bhandler\b', 'hdl'),
            (r'\bcallback\b', 'cb'),
            (r'\bfunction\b', 'fn'),
            (r'\bmethod\b', 'meth'),
            (r'\bobject\b', 'obj'),
            (r'\barray\b', 'arr'),
            (r'\blist\b', 'lst'),
            (r'\bstring\b', 'str'),
            (r'\bnumber\b', 'num'),
            (r'\binteger\b', 'int'),
            (r'\bfloat\b', 'flt'),
            (r'\bboolean\b', 'bool'),
            # v3.0.10: 极致压缩 - 删除所有非关键字
            (r'\bself\b', 's'),
            (r'\bcls\b', 'c'),
            (r'\bdef\b', 'd'),
            (r'\breturn\b', 'R'),
            (r'\bif\b', 'I'),
            (r'\belse\b', 'E'),
            (r'\bfor\b', 'F'),
            (r'\bin\b', 'N'),
            (r'\bwhile\b', 'W'),
            (r'\btry\b', 'T'),
            (r'\bexcept\b', 'X'),
            (r'\bimport\b', 'M'),
            (r'\bfrom\b', 'm'),
            (r'\bclass\b', 'C'),
            (r'\bpass\b', ''),
            (r'\bNone\b', '0'),
            (r'\bTrue\b', '1'),
            (r'\bFalse\b', '0'),
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
        
        # v3.0.5增强：列表任务超级压缩
        # 删除序号和空格
        result = re.sub(r'(\d+)[.:\s]+', r'\1.', result)
        # 删除连接词
        result = re.sub(r'[,，\s]*[和与及][,，\s]*', ',', result)
        # 删除"先/然后/再/最后"序列
        result = re.sub(r'(先|然后|再|接着|随后|最后)[，,\s]*', '', result)
        
        # v3.0.5: 段落级压缩
        lines = result.split('\n')
        compressed_lines = []
        for line in lines:
            line = line.strip()
            # 删除列表符号和填充
            line = re.sub(r'^[\s]*[-*•·]\s*', '', line)
            line = re.sub(r'^[\s]*\d+[.、)\]】]\s*', '', line)
            # 删除行首的"先/首先/第一步"
            line = re.sub(r'^(先|首先|第一步|第1步)[，,、:\s]*', '', line)
            # 删除行尾的"等/等等"
            line = re.sub(r'[，,、\s]*等[等]?\s*$', '', line)
            if line:
                compressed_lines.append(line)
        
        result = '\n'.join(compressed_lines)
        result = re.sub(r'\n\s*\n', '\n', result)
        
        # v3.0.5: 最终清理
        result = re.sub(r'[，,、；;]+', '，', result)  # 统一标点
        result = re.sub(r'[。\.]+', '。', result)
        result = re.sub(r'\s+', '', result)  # 删除所有空格
        
        return result.strip()
    
    def _optimize_code(self, content: str) -> str:
        """优化代码 - v3.0.5终极版"""
        result = content
        
        # v3.0.5: 先删除所有注释和docstring（多行处理）
        result = re.sub(r'"""[\s\S]*?"""', '', result)
        result = re.sub(r"'''[\s\S]*?'''", '', result)
        result = re.sub(r'#.*$', '', result, flags=re.MULTILINE)
        
        # v3.0.5: 统计函数模式识别（必须在单行压缩之前）
        # 模式1: total=0; for x in data: total+=x -> total=sum(data)
        result = re.sub(
            r'(\w+)\s*=\s*0\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\s*\+=\s*\2\s*\n',
            r'\1=sum(\3)\n',
            result
        )
        # 模式2: result=[]; for x in items: if x: result.append(x)
        result = re.sub(
            r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*if\s+(\w+):\s*\n\s*\1\.append\(\w+\)\s*\n',
            r'\1=[\2 for \2 in \3 if \4]\n',
            result
        )
        
        # 应用代码规则
        for pattern, replacement in self._compiled_rules['code']:
            result = pattern.sub(replacement, result)
        
        # v3.0.5: 额外压缩
        # 删除多余空行
        result = re.sub(r'\n\s*\n', '\n', result)
        result = re.sub(r'\n+', '\n', result)
        
        # 删除行首空格
        result = '\n'.join(line.strip() for line in result.split('\n'))
        
        # v3.0.5: 简化常见模式
        # result = [] -> r=[]
        result = re.sub(r'(\w+)\s*=\s*\[\]', r'\1=[]', result)
        # result.append(x) -> r+=[x]
        result = re.sub(r'(\w+)\.append\(([^)]+)\)', r'\1+=[\2]', result)
        # for循环简化
        result = re.sub(r'for\s+(\w+)\s+in\s+(\w+):', r'for \1 in \2:', result)
        # if条件简化
        result = re.sub(r'if\s+([^:]+):', r'if \1:', result)
        
        # v3.0.5: 删除多余空格
        result = re.sub(r'\s*=\s*', '=', result)
        result = re.sub(r'\s*,\s*', ',', result)
        result = re.sub(r'\s*:\s*', ':', result)
        
        return result.strip()
    
    def _optimize_workflow(self, content: str) -> str:
        """优化工作流 - v3.0.4增强"""
        try:
            data = json.loads(content)
            
            # v3.0.6: 键名缩写映射扩展
            key_abbreviations = {
                'name': 'n', 'type': 't', 'config': 'c',
                'parameters': 'p', 'description': 'd',
                'configuration': 'cfg', 'environment': 'env',
                'timeout': 'to', 'retry': 'r', 'version': 'v',
                'steps': 's', 'inputs': 'i', 'outputs': 'o',
                'enabled': 'on', 'disabled': 'off',
                # v3.0.6新增
                'workflow': 'w', 'skill': 'sk', 'agent': 'a',
                'model': 'm', 'temperature': 'temp', 'max_tokens': 'max',
                'api_key': 'key', 'url': 'u', 'endpoint': 'e',
                'headers': 'h', 'body': 'b', 'method': 'meth',
                'status': 'st', 'code': 'cd', 'message': 'msg',
            }
            
            # v3.0.6: 删除更多默认值
            defaults_to_remove = {
                'to': [30, 30000, 60, 60000],
                'r': [3, 5, 0],
                'v': ['1.0', '2.0', '3.0', 'latest'],
                'temp': [0.7, 1.0],
                'max': [4096, 8192, 2048],
            }
            
            def abbreviate_keys(obj):
                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        new_key = key_abbreviations.get(k, k)
                        # v3.0.6: 删除默认值
                        if k in defaults_to_remove and v in defaults_to_remove[k]:
                            continue
                        if k in key_abbreviations and v in defaults_to_remove.get(key_abbreviations[k], []):
                            continue
                        new_obj[new_key] = abbreviate_keys(v)
                    return new_obj
                elif isinstance(obj, list):
                    return [abbreviate_keys(item) for item in obj]
                return obj
            
            data = abbreviate_keys(data)
            
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
