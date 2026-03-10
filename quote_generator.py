import requests
import json
from typing import List


class APIError(Exception):
    """API 调用失败异常"""
    pass


class NetworkError(Exception):
    """网络连接失败异常"""
    pass


class AuthenticationError(Exception):
    """API 密钥无效异常"""
    pass


class QuoteGenerator:
    """语录生成器，负责使用提示词生成语录"""
    
    def __init__(self, api_key: str, api_endpoint: str, template: str):
        """
        初始化语录生成器
        
        Args:
            api_key: DeepSeek API 密钥
            api_endpoint: API 端点地址
            template: 语录生成模板
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.template = template
    
    def generate_quotes(self, prompt: str) -> List[str]:
        """
        使用提示词生成 20 条语录
        
        Args:
            prompt: 由 PromptGenerator 生成的提示词
            
        Returns:
            List[str]: 包含 20 条语录的列表
            
        Raises:
            APIError: API 调用失败
            NetworkError: 网络连接失败
            AuthenticationError: API 密钥无效
            ValueError: 返回的语录数量不足 20 条
        """
        # 使用模板构造系统提示词
        system_prompt = self.template.format(prompt=prompt)
        
        # 构造请求数据
        request_data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "请开始生成 20 条语录"}
            ],
            "temperature": 0.8,
            "max_tokens": 3000
        }
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            # 发送 API 请求
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=request_data,
                timeout=60
            )
            
            # 检查认证错误
            if response.status_code == 401:
                raise AuthenticationError("API 密钥无效，请检查配置")
            
            # 检查其他错误
            if response.status_code != 200:
                error_msg = f"API 调用失败，状态码: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f", 错误信息: {error_data['error']}"
                except:
                    pass
                raise APIError(error_msg)
            
            # 解析响应
            response_data = response.json()
            
            # 提取生成的内容
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                
                # 解析语录列表
                quotes = self._parse_quotes(content)
                
                # 验证语录数量
                if len(quotes) < 20:
                    raise ValueError(f"生成的语录数量不足 20 条，实际生成了 {len(quotes)} 条")
                
                # 返回前 20 条
                return quotes[:20]
            else:
                raise APIError("API 响应格式错误，未找到生成的内容")
        
        except requests.exceptions.Timeout:
            raise NetworkError("网络连接超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise NetworkError("网络连接失败，请检查网络连接")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络请求失败: {str(e)}")
        except (APIError, AuthenticationError, ValueError):
            raise
        except Exception as e:
            raise APIError(f"生成语录时发生错误: {str(e)}")
    
    def _parse_quotes(self, content: str) -> List[str]:
        """
        从生成的内容中解析语录列表
        
        Args:
            content: API 返回的文本内容
            
        Returns:
            List[str]: 语录列表
        """
        quotes = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 移除数字编号（如 "1. ", "1、", "1）" 等）
            import re
            cleaned_line = re.sub(r'^\d+[.、\)）]\s*', '', line)
            
            if cleaned_line:
                quotes.append(cleaned_line)
        
        return quotes
