import os
from datetime import datetime
from typing import List


class FileManager:
    """文件管理器，负责将生成的文案保存到文件系统"""
    
    def __init__(self, output_file: str = "文案.md"):
        """
        初始化文件管理器
        
        Args:
            output_file: 输出文件路径，默认为"文案.md"
        """
        self.output_file = output_file
    
    def save_quotes(self, topic: str, quotes: List[str], prompt: str = None) -> None:
        """
        将语录保存到文件
        
        Args:
            topic: 文案主题
            quotes: 语录列表（应包含 20 条）
            prompt: 使用的提示词（可选）
            
        Raises:
            IOError: 文件写入失败
        """
        try:
            # 生成时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构造内容
            content = f"\n## {topic}\n"
            content += f"**生成时间**: {timestamp}\n\n"
            
            # 添加提示词（如果有）
            if prompt:
                content += f"**使用的提示词**:\n```\n{prompt}\n```\n\n"
            
            # 添加语录列表
            content += "**生成的语录**:\n\n"
            for i, quote in enumerate(quotes, 1):
                content += f"{i}. {quote}\n"
            
            content += "\n---\n"
            
            # 以追加模式写入文件
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(content)
        
        except IOError as e:
            raise IOError(f"文件写入失败: {str(e)}")
        except Exception as e:
            raise IOError(f"保存文案时发生错误: {str(e)}")
