from flask import Flask, render_template, request, jsonify
import logging
from config import ConfigManager
from prompt_generator import PromptGenerator, APIError, NetworkError, AuthenticationError
from quote_generator import QuoteGenerator
from file_manager import FileManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化配置管理器
config_manager = ConfigManager()

try:
    config_manager.load_config()
    logger.info("配置加载成功")
except Exception as e:
    logger.error(f"配置加载失败: {str(e)}")


@app.route('/')
def index():
    """返回 HTML 页面"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    处理文案生成请求
    
    请求体:
        {
            "topic": str,  # 用户输入的主题
            "custom_prompt": str | null  # 可选的自定义提示词
        }
    
    返回:
        {
            "success": bool,
            "quotes": List[str],  # 成功时返回
            "error": str,         # 失败时返回
            "saved": bool         # 是否成功保存到文件
        }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': '请求参数错误：缺少主题'
            }), 400
        
        topic = data['topic'].strip()
        custom_prompt = data.get('custom_prompt', '').strip() if data.get('custom_prompt') else None
        
        # 验证主题非空
        if not topic:
            return jsonify({
                'success': False,
                'error': '请输入主题'
            }), 400
        
        logger.info(f"开始生成文案，主题: {topic}, 自定义提示词: {'是' if custom_prompt else '否'}")
        
        # 获取配置
        api_key = config_manager.get_api_key()
        api_endpoint = config_manager.get_api_endpoint()
        quote_template = config_manager.get_quote_generation_template()
        
        # 判断是否使用自定义提示词
        if custom_prompt:
            # 使用自定义提示词，跳过第一阶段
            logger.info("使用自定义提示词，跳过提示词生成阶段")
            prompt = custom_prompt
        else:
            # 第一阶段：生成提示词
            logger.info("第一阶段：生成提示词")
            prompt_template = config_manager.get_prompt_generation_template()
            prompt_generator = PromptGenerator(api_key, api_endpoint, prompt_template)
            prompt = prompt_generator.generate_prompt(topic)
            logger.info(f"提示词生成成功: {prompt[:100]}...")
        
        # 第二阶段：生成语录
        logger.info("第二阶段：生成语录")
        quote_generator = QuoteGenerator(api_key, api_endpoint, quote_template)
        quotes = quote_generator.generate_quotes(prompt)
        logger.info(f"语录生成成功，共 {len(quotes)} 条")
        
        # 第三阶段：保存到文件
        saved = False
        save_error = None
        try:
            logger.info("第三阶段：保存到文件")
            file_manager = FileManager()
            file_manager.save_quotes(topic, quotes, prompt)
            saved = True
            logger.info("文案保存成功")
        except Exception as e:
            save_error = str(e)
            logger.error(f"文件保存失败: {save_error}")
        
        # 返回成功响应
        response = {
            'success': True,
            'quotes': quotes,
            'saved': saved
        }
        
        if save_error:
            response['save_error'] = save_error
        
        return jsonify(response)
    
    except AuthenticationError as e:
        logger.error(f"认证失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'认证失败: {str(e)}'
        }), 401
    
    except NetworkError as e:
        logger.error(f"网络错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'网络错误: {str(e)}'
        }), 503
    
    except (APIError, ValueError) as e:
        logger.error(f"API 错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"未知错误: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
