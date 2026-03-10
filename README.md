# 小红书文案生成器

基于 DeepSeek API 的智能文案生成系统，专为小红书读文博主设计。

## 功能特点

- 🎯 **两阶段生成**：先生成提示词，再生成语录，确保内容质量
- 📝 **一键生成**：输入主题，点击按钮，自动完成全流程
- 💾 **自动保存**：生成的文案自动追加到"文案.md"文件
- 🎨 **精美界面**：响应式设计，支持移动端访问
- 📋 **一键复制**：点击语录即可复制到剪贴板

## 技术栈

- **后端**：Python + Flask
- **前端**：HTML + CSS + JavaScript
- **AI 服务**：DeepSeek API
- **配置管理**：python-dotenv

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd xiaohongshu-copywriting-generator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

复制 `.env.example` 文件为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 DeepSeek API 密钥：

```env
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_API_ENDPOINT=https://api.deepseek.com/v1/chat/completions
```

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 使用说明

1. 打开浏览器访问 `http://localhost:5000`
2. 在输入框中输入文案主题（例如：励志、爱情、生活感悟）
3. 点击"一键生成"按钮
4. 等待系统生成 20 条语录
5. 点击任意语录即可复制到剪贴板
6. 生成的文案会自动保存到"文案.md"文件

## 项目结构

```
.
├── app.py                  # Flask 应用主文件
├── config.py               # 配置管理模块
├── prompt_generator.py     # 提示词生成模块
├── quote_generator.py      # 语录生成模块
├── file_manager.py         # 文件保存模块
├── templates/
│   └── index.html         # HTML 页面
├── static/
│   ├── style.css          # 样式文件
│   └── app.js             # 前端交互逻辑
├── .env                    # 配置文件（需自行创建）
├── .env.example           # 配置文件模板
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明
```

## 故障排除

### 配置错误

如果看到"配置错误：未找到 DEEPSEEK_API_KEY"，请检查：
- `.env` 文件是否存在
- `.env` 文件中是否正确配置了 `DEEPSEEK_API_KEY`

### 网络错误

如果看到"网络连接失败"，请检查：
- 网络连接是否正常
- DeepSeek API 服务是否可访问

### API 认证失败

如果看到"API 密钥无效"，请检查：
- API 密钥是否正确
- API 密钥是否有效且未过期

## 开发说明

### 运行测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest
```

### 开发模式

Flask 应用默认以 debug 模式运行，代码修改后会自动重启。

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue。
