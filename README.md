# Ollama Toolkit

一个用于调用Ollama模型的Python工具包，支持流式输出、图片和文件上传，以及指定远程Ollama服务器。

## 特性

- 支持本地和远程Ollama模型调用
- 流式输出响应结果到终端
- 支持上传图片和其他文件作为输入
- 提供命令行接口(CLI)和Python API两种使用方式
- 支持基本生成模式和聊天模式

## 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/ollama_toolkit.git
cd ollama_toolkit
pip install -e .
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

你也可以在Python代码中直接使用这个工具包：

```python
from ollama_toolkit.ollama_client import OllamaClient

# 创建客户端实例
client = OllamaClient(base_url="http://localhost:11434", default_model="llama3")

# 基本文本生成
response = client.generate("请解释量子计算的基本原理")

# 上传图片
response = client.generate("分析这张图片", images=["path/to/image.jpg"])

# 上传其他文件
response = client.generate("分析这个文件", files=["path/to/file.txt"])

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
def chat(self, messages, model=None, stream=True, **kwargs)
```

使用聊天模式与模型交互。

- `messages`: 消息历史列表，每个消息包含role和content
- `model`: 要使用的模型名称，如果为None则使用默认模型
- `stream`: 是否启用流式输出，默认为True
- `**kwargs`: 其他传递给Ollama API的参数
- 返回: 最新的响应文本

#### list_models方法

```python
def list_models(self)
```

列出可用的模型。

- 返回: 模型列表

## 依赖项

- Python 3.6+ 
- requests>=2.25.0

## 许可证

MIT License