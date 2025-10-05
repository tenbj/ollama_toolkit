# Ollama Toolkit

一个用于调用Ollama模型的Python工具包，支持流式输出、图片和文件上传，以及指定远程Ollama服务器。

## 特性

- 支持本地和远程Ollama模型调用
- 流式输出响应结果到终端
- 支持上传图片和其他文件作为输入
- 提供命令行接口(CLI)和Python API两种使用方式
- 支持基本生成模式和聊天模式
- 提供完整的错误处理和提示信息

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/tenbj/ollama_toolkit.git
cd ollama_toolkit

# 安装依赖
pip install -r requirements.txt

# 安装工具包（开发模式）
pip install -e .
```

### 快速安装依赖

如果您只想安装必要的依赖而不安装整个包：

```bash
pip install requests>=2.25.0
```

## 使用方法

### 命令行接口(CLI)

安装后，可以使用`ollama-tool`命令来调用工具包：

#### 基本使用

```bash
# 使用默认模型和本地Ollama服务
ollama-tool "你的问题"

# 指定模型
ollama-tool "你的问题" --model llama3

# 指定远程Ollama服务器
ollama-tool "你的问题" --url http://remote-server:11434

# 禁用流式输出
ollama-tool "你的问题" --no-stream
```

#### 上传文件

```bash
# 上传图片
ollama-tool "分析这张图片" --image path/to/image.jpg

# 上传多个图片
ollama-tool "比较这两张图片" --image image1.jpg --image image2.jpg

# 上传其他文件
ollama-tool "分析这个文件内容" --file path/to/file.txt
```

#### 列出可用模型

```bash
ollama-tool --list-models
```

#### 聊天模式

```bash
ollama-tool --chat
```

### Python API

您也可以在Python代码中直接使用这个工具包：

```python
from ollama_toolkit.ollama_client import OllamaClient

# 创建客户端实例
client = OllamaClient(base_url="http://localhost:11434", default_model="llama3")

# 基本文本生成
response = client.generate("请解释量子计算的基本原理", stream=True)

# 上传图片进行分析
image_messages = [{"role": "user", "content": "详细分析这张图片"}]
response = client.chat(
    model="qwen2.5vl:latest",
    messages=image_messages,
    images=["path/to/image.jpg"],
    stream=False
)

# 聊天模式
messages = [
    {"role": "user", "content": "你好，我叫小明"},
    {"role": "assistant", "content": "你好小明，我是AI助手"},
    {"role": "user", "content": "请告诉我今天天气如何"}
]
response = client.chat(messages)

# 列出可用模型
models = client.list_models()
```

## 示例程序

项目中包含一个`demo.py`示例程序，展示了工具包的所有主要功能：

```bash
python demo.py
```

这个演示程序将展示如何：
1. 列出可用模型
2. 进行基本文本生成
3. 使用聊天模式进行多轮对话
4. 上传并分析图片

### 示例程序详解

以下是示例程序中的关键代码片段：

#### 创建客户端连接

```python
from ollama_toolkit.ollama_client import OllamaClient

# 创建客户端实例
client = OllamaClient(base_url="http://localhost:11434", default_model="qwen3")
```

#### 列出可用模型

```python
# 列出可用模型
models = client.list_models()
for i, model in enumerate(models, 1):
    print(f"{i}. {model['name']}")
```

#### 基本文本生成

```python
# 基本文本生成
prompt = "请简单解释什么是人工智能，并列举两个实际应用场景"
response = client.generate(prompt, stream=True)
print(f"生成结果: {response}")
```

#### 聊天模式

```python
# 聊天模式
messages = [
    {"role": "user", "content": "你好，我是新来的用户"},
    {"role": "assistant", "content": "你好！我是你的AI助手，很高兴认识你。有什么我可以帮助你的吗？"}
]
# 继续对话
new_question = "你能给我推荐几个学习Python的网站吗？"
messages.append({"role": "user", "content": new_question})
response = client.chat(messages, stream=True)
print(f"Assistant: {response}")
# 将AI的回复添加到对话历史中
messages.append({"role": "assistant", "content": response})
```

#### 图片分析

```python
# 图片分析
image_path = "path/to/your/image.jpg"
if os.path.exists(image_path):
    # 查找支持多模态的模型
    multimodal_models = [model['name'] for model in models if any(keyword in model['name'].lower() for keyword in ['llava', 'vl', 'vision'])]
    if multimodal_models:
        multimodal_model = multimodal_models[0]
        image_messages = [{"role": "user", "content": "详细分析这张图片里有什么内容？"}]
        response = client.chat(
            model=multimodal_model,
            messages=image_messages,
            images=[image_path],
            stream=False
        )
        print(f"图片分析结果：{response}")
```

## API文档

### OllamaClient类

#### 初始化

```python
client = OllamaClient(base_url="http://localhost:11434", default_model="llama3")
```

- `base_url`: Ollama API的基础URL，默认为"http://localhost:11434"
- `default_model`: 默认使用的模型名称，默认为"llama3"

#### generate方法

```python
def generate(self, prompt, model=None, stream=True, images=None, files=None, **kwargs)
```

调用Ollama模型生成响应。

- `prompt`: 提示文本
- `model`: 要使用的模型名称，如果为None则使用默认模型
- `stream`: 是否启用流式输出，默认为True
- `images`: 图片文件路径列表
- `files`: 其他文件路径列表
- `**kwargs`: 其他传递给Ollama API的参数
- 返回: 完整的响应文本

#### chat方法

```python
def chat(self, messages, model=None, stream=True, images=None, **kwargs)
```

使用聊天模式与模型交互。

- `messages`: 消息历史列表，每个消息包含role和content
- `model`: 要使用的模型名称，如果为None则使用默认模型
- `stream`: 是否启用流式输出，默认为True
- `images`: 图片文件路径列表（可选）
- `**kwargs`: 其他传递给Ollama API的参数
- 返回: 最新的响应文本

#### list_models方法

```python
def list_models(self)
```

列出可用的模型。

- 返回: 模型列表

## 常见问题和解决方案

### 1. 连接Ollama服务器失败

- 确保Ollama服务器已启动
- 检查base_url是否正确（默认是http://localhost:11434）
- 确认防火墙没有阻止连接

### 2. 内存不足错误

处理图片或运行大型模型时，可能会遇到内存不足的错误：

- 关闭其他占用大量内存的程序
- 尝试使用更小的模型
- 增加系统内存
- 对于图片分析，尝试使用更小尺寸的图片

### 3. 图片分析失败

- 确保使用的是支持多模态的模型（如llava、qwen2-vl等）
- 检查图片路径是否正确
- 验证图片格式是否受支持

### 4. 模型未找到错误

如果遇到"model 'xxx' not found"错误：

- 使用`ollama pull`命令下载所需模型
- 检查模型名称是否正确

## 测试

项目中的`test`文件夹包含了各种测试脚本：

```bash
cd test
python direct_api_test.py        # 直接测试Ollama API
python list_available_models.py   # 列出可用模型
python test_image_recognition.py  # 测试图片识别功能
python test_generate_with_image.py  # 测试generate方法处理图片
```

## 依赖项

- Python 3.6+
- requests>=2.25.0

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求来改进这个工具包！