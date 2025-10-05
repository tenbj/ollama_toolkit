import requests
import json
import sys
import os

class OllamaClient:
    """
    Ollama客户端，用于调用本地或远程的Ollama模型，并支持流式输出。
    """
    def __init__(self, base_url="http://localhost:11434", default_model="qwen3"):
        """
        初始化Ollama客户端
        
        Args:
            base_url (str): Ollama API的基础URL
            default_model (str): 默认使用的模型名称
        """
        self.base_url = base_url.rstrip('/')
        self.default_model = default_model
        self.session = requests.Session()
    
    def generate(self, prompt, model=None, stream=True, images=None, files=None, **kwargs):
        """
        调用Ollama模型生成响应
        
        Args:
            prompt (str): 提示文本
            model (str, optional): 要使用的模型名称，如果为None则使用默认模型
            stream (bool, optional): 是否启用流式输出，默认为True
            images (list, optional): 图片文件路径列表
            files (list, optional): 其他文件路径列表
            **kwargs: 其他传递给Ollama API的参数
        
        Returns:
            str: 完整的响应文本
        """
        if model is None:
            model = self.default_model
        
        url = f"{self.base_url}/api/generate"
        
        # 准备请求数据
        data = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        # 处理文件上传
        files_dict = {}
        
        # 处理图片
        if images:
            for i, image_path in enumerate(images):
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        files_dict[f"image_{i}"] = (os.path.basename(image_path), f)
        
        # 处理其他文件
        if files:
            for i, file_path in enumerate(files):
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        files_dict[f"file_{i}"] = (os.path.basename(file_path), f)
        
        # 发送请求
        response = self.session.post(url, json=data if not files_dict else None,
                                    files=files_dict if files_dict else None, 
                                    stream=stream)
        
        response.raise_for_status()
        
        full_response = ""
        
        # 处理流式响应
        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        # 提取响应文本
                        if "response" in chunk:
                            print(chunk["response"], end="", flush=True)
                            full_response += chunk["response"]
                        # 检查是否完成
                        if chunk.get("done", False):
                            print()  # 输出换行
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            # 非流式响应
            result = response.json()
            full_response = result.get("response", "")
            print(full_response)
        
        return full_response
    
    def list_models(self):
        """
        列出可用的模型
        
        Returns:
            list: 模型列表
        """
        url = f"{self.base_url}/api/tags"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("models", [])
    
    def chat(self, messages, model=None, stream=True, **kwargs):
        """
        使用聊天模式与模型交互
        
        Args:
            messages (list): 消息历史列表，每个消息包含role和content
            model (str, optional): 要使用的模型名称，如果为None则使用默认模型
            stream (bool, optional): 是否启用流式输出，默认为True
            **kwargs: 其他传递给Ollama API的参数
        
        Returns:
            str: 最新的响应文本
        """
        if model is None:
            model = self.default_model
        
        url = f"{self.base_url}/api/chat"
        
        # 准备请求数据
        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        # 发送请求
        response = self.session.post(url, json=data, stream=stream)
        
        response.raise_for_status()
        
        full_response = ""
        
        # 处理流式响应
        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        # 提取响应文本
                        if "message" in chunk and "content" in chunk["message"]:
                            print(chunk["message"]["content"], end="", flush=True)
                            full_response += chunk["message"]["content"]
                        # 检查是否完成
                        if chunk.get("done", False):
                            print()  # 输出换行
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            # 非流式响应
            result = response.json()
            if "message" in result and "content" in result["message"]:
                full_response = result["message"]["content"]
                print(full_response)
        
        return full_response