#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ollama Toolkit 演示程序
展示如何使用Ollama Toolkit进行文本生成、聊天和图片分析等功能
"""

from ollama_toolkit.ollama_client import OllamaClient
import os
import sys
import io

# 确保中文显示正常
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_separator(title=None):
    """打印分隔线，使输出更清晰"""
    if title:
        print(f"\n{'='*50}\n{title}\n{'='*50}")
    else:
        print("\n" + "="*50 + "\n")


def main():
    """主程序入口"""
    print("Ollama Toolkit 演示程序\n")
    print("这个演示程序将展示如何使用Ollama Toolkit进行以下操作：")
    print("1. 列出可用模型")
    print("2. 基本文本生成")
    print("3. 聊天模式")
    print("4. 图片分析\n")
    
    # 创建客户端实例
    print("正在连接到Ollama服务器...")
    try:
        # 默认连接到本地Ollama服务器，使用qwen3模型
        client = OllamaClient(base_url="http://localhost:11434", default_model="qwen3")
        print("连接成功！\n")
    except Exception as e:
        print(f"连接Ollama服务器失败: {str(e)}")
        print("请确保Ollama服务器已启动，并且地址正确")
        return
    
    # 1. 列出可用模型
    try:
        print_separator("1. 可用模型列表")
        models = client.list_models()
        if models:
            print(f"检测到 {len(models)} 个可用模型：")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model['name']}")
        else:
            print("未检测到可用模型，请先使用'ollama pull'命令下载模型")
    except Exception as e:
        print(f"获取模型列表失败: {str(e)}")
    
    # 2. 基本文本生成
    try:
        print_separator("2. 基本文本生成示例")
        prompt = "请简单解释什么是人工智能，并列举两个实际应用场景"
        print(f"提问: {prompt}")
        response = client.generate(prompt, stream=True)  # 使用流式输出
        print(f"生成结果: {response}")
    except Exception as e:
        print(f"文本生成出错：{str(e)}")
    
    # 3. 聊天模式
    try:
        print_separator("3. 聊天模式示例")
        # 创建一个简单的对话历史
        messages = [
            {"role": "user", "content": "你好，我是新来的用户"},
            {"role": "assistant", "content": "你好！我是你的AI助手，很高兴认识你。有什么我可以帮助你的吗？"}
        ]
        
        # 显示对话历史
        print("对话历史:")
        for msg in messages:
            print(f"{msg['role'].capitalize()}: {msg['content']}")
        
        # 继续对话
        new_question = "你能给我推荐几个学习Python的网站吗？"
        messages.append({"role": "user", "content": new_question})
        print(f"\nUser: {new_question}")
        
        response = client.chat(messages, stream=True)  # 使用流式输出
        print(f"Assistant: {response}")
        
        # 将AI的回复添加到对话历史中，以便后续对话
        messages.append({"role": "assistant", "content": response})
    except Exception as e:
        print(f"聊天出错：{str(e)}")
    
    # 4. 图片分析
    try:
        print_separator("4. 图片分析示例")
        print("注意：Ollama处理图片可能需要较多系统资源，特别是对于较大的图片或复杂的模型")
        print("      如果遇到'500 Internal Server Error'或'model runner has unexpectedly stopped'错误")
        print("      这通常是由于系统内存不足导致的，请尝试关闭其他程序或使用更小的模型")
        
        # 这里可以修改为你自己的图片路径
        image_path = input("请输入图片路径 (或直接按回车使用默认路径): ").strip()
        if not image_path:
            # 默认图片路径，用户可以根据自己的实际情况修改
            default_image = r"C:\Users\Administrator\Desktop\test\638948447558127941.png"
            image_path = default_image
            print(f"使用默认图片路径: {image_path}")
        
        # 检查图片文件是否存在
        if os.path.exists(image_path):
            # 确保使用支持图片的多模态模型，例如qwen2.5vl:latest
            # 查找支持多模态的模型
            multimodal_models = [model['name'] for model in models if any(keyword in model['name'].lower() for keyword in ['llava', 'vl', 'vision'])]
            
            if multimodal_models:
                # 使用找到的第一个多模态模型
                multimodal_model = multimodal_models[0]
                print(f"使用多模态模型: {multimodal_model}")
                
                # 创建消息并调用chat方法进行图片分析
                image_messages = [{"role": "user", "content": "详细分析这张图片里有什么内容？"}]
                response = client.chat(
                    model=multimodal_model,
                    messages=image_messages,
                    images=[image_path],
                    stream=True  # 对于长文本回复，禁用流式输出可能更易于阅读
                )
                print(f"图片分析结果：{response}")
            else:
                print("未找到支持图片分析的多模态模型")
                print("请使用命令'ollama pull llava:latest'或'ollama pull qwen2-vl:latest'下载支持图片的模型")
        else:
            print(f"错误：图片文件不存在: {image_path}")
            print("请检查图片路径是否正确")
    except Exception as e:
        print(f"图片分析出错：{str(e)}")
        print("\n可能的解决方法：")
        print("1. 关闭其他占用大量内存的程序")
        print("2. 尝试使用更小的多模态模型")
        print("3. 增加系统内存")
        print("4. 重启Ollama服务")
        print("5. 检查Ollama服务器日志获取更多详细信息")
    
    print_separator()
    print("演示完成！")
    print("\n你可以根据自己的需求修改这个示例程序，体验Ollama Toolkit的更多功能")
    print("更多详细信息请参考README.md文件")


if __name__ == "__main__":
    main()