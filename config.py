import os
from dotenv import load_dotenv

class ConfigManager:
    # 提示词模板配置
    PROMPT_GENERATION_TEMPLATE = """你是一位深谙人心的文案创作者，专门为小红书读文博主创作夜读语录。

用户会给你一个主题，你需要生成一个详细的创作指南，用于生成 20 条语录。

语录风格要求：
1. 简单而有哲理 - 用平实的语言表达深刻的道理
2. 引发共鸣 - 触动人心，让人在夜晚阅读时有所感悟
3. 温暖讨喜 - 语气温柔，给人安慰和力量
4. 长度适中 - 每条 80-200 字
5. 多样化来源 - 可以是名人名言、散文段落、经典语句，或原创哲思

创作方向：
- 关注情感共鸣而非说教
- 用具体意象而非抽象概念
- 保持真诚自然的语气
- 适合夜晚独处时阅读

请针对用户提供的主题，生成一个详细的创作指南。"""

    QUOTE_GENERATION_TEMPLATE = """{prompt}

请生成恰好 20 条语录，每条独立成行，使用数字编号（1. 2. 3. ...）。

要求：
- 每条 120 字左右
- 简单而有哲理
- 温暖、讨喜、引发共鸣
- 适合夜晚阅读
- 风格多样（名言、散文、原创等）"""

    def __init__(self):
        load_dotenv()
        self.config = self.load_config()
    
    def load_config(self):
        """从 .env 文件加载配置"""
        api_key = os.getenv('DEEPSEEK_API_KEY')
        api_endpoint = os.getenv('DEEPSEEK_API_ENDPOINT')
        
        if not api_key:
            raise ValueError("配置错误：未找到 DEEPSEEK_API_KEY")
        if not api_endpoint:
            raise ValueError("配置错误：未找到 DEEPSEEK_API_ENDPOINT")
        
        return {
            'api_key': api_key,
            'api_endpoint': api_endpoint
        }
    
    def get_api_key(self):
        """获取 API 密钥"""
        return self.config['api_key']
    
    def get_api_endpoint(self):
        """获取 API 端点地址"""
        return self.config['api_endpoint']
    
    def get_prompt_generation_template(self):
        """获取提示词生成模板"""
        return self.PROMPT_GENERATION_TEMPLATE
    
    def get_quote_generation_template(self):
        """获取语录生成模板"""
        return self.QUOTE_GENERATION_TEMPLATE
