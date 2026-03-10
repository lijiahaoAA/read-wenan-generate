import requests
import json


class APIError(Exception):
    """API 调用失败异常"""
    pass


class NetworkError(Exception):
    """网络连接失败异常"""
    pass


class AuthenticationError(Exception):
    """API 密钥无效异常"""
    pass


class PromptGenerator:
    """提示词生成器，负责根据主题生成文案生成提示词"""
    
    def __init__(self, api_key: str, api_endpoint: str, system_prompt: str):
        """
        初始化提示词生成器
        
        Args:
            api_key: DeepSeek API 密钥
            api_endpoint: API 端点地址
            system_prompt: 系统提示词模板
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.system_prompt = system_prompt
    
    def generate_prompt(self, topic: str) -> str:
        """
        根据主题生成文案生成提示词
        
        Args:
            topic: 用户输入的主题
            
        Returns:
            str: 生成的提示词
            
        Raises:
            APIError: API 调用失败
            NetworkError: 网络连接失败
            AuthenticationError: API 密钥无效
        """
        # 构造请求数据
        request_data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"主题：{topic}"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
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
                timeout=30
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
            
            # 提取生成的提示词
            if "choices" in response_data and len(response_data["choices"]) > 0:
                prompt = response_data["choices"][0]["message"]["content"]
                return prompt.strip()
            else:
                raise APIError("API 响应格式错误，未找到生成的内容")
        
        except requests.exceptions.Timeout:
            raise NetworkError("网络连接超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise NetworkError("网络连接失败，请检查网络连接")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络请求失败: {str(e)}")
        except (APIError, AuthenticationError):
            raise
        except Exception as e:
            raise APIError(f"生成提示词时发生错误: {str(e)}")
