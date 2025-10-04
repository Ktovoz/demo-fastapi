#!/usr/bin/env python3
"""
FastAPI 应用运行脚本
解决模块导入问题，可以直接运行此文件启动服务器
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 设置环境变量
os.environ.setdefault("PYTHONPATH", str(current_dir))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    # 加载环境变量
    load_dotenv()

    # 获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "False").lower() == "true"

    print(f"🚀 启动 FastAPI 服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📖 API 文档: http://{host}:{port}/docs")
    print(f"🔄 热重载: {'开启' if reload else '关闭'}")
    print("-" * 50)

    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=[str(current_dir / "app")]
    )