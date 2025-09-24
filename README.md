# 国际象棋局面识别与走法推荐系统

项目描述视频：https://www.bilibili.com/video/BV132KbzKE8G<br>

本项目基于 YOLOv8 和 Stockfish 实现了国际象棋局面识别与走法推荐系统。用户上传棋局图片，系统自动完成棋盘检测、棋子识别、FEN 串生成，并调用国际象棋引擎计算最优走法。

## 项目结构：

后端结构：<br>
```
back_end/
    ├─ app.py                     # 后端主干部分，定义接口
    ├─ logic/
    │  ├─ fen_generator.py        # 将检测结果转为FEN字符串
    │  ├─ image_preprocess.py     # 棋盘检测及透视变换
    │  ├─ move_recommend.py       # 调用Stockfish引擎获取最优走法
    │  └─ piece_detection.py      # 棋子检测及坐标映射
    ├─ stockfish/
    │  └─ stockfish-windows-x86-64-avx2.exe
    ├─ best.pt                    # YOLOv8训练好的棋子识别模型
    ├─ requirements.txt           # 项目依赖库

```
    
前端结构：<br>
```
chess-recognizer-ui/
    ├─ public/           # 静态资源
    ├─ src/              # 源代码
    ├─ .gitignore        # 忽略配置
    ├─ eslint.config.js  # ESLint 配置
    ├─ index.html        # 项目入口
    ├─ package.json      # 依赖和脚本
    ├─ package-lock.json # 锁定依赖
    ├─ pnpm-lock.yaml    # 可选，pnpm锁定文件
    ├─ vite.config.js    # Vite 配置
    ├─ README.md        
```


## 快速开始

下载前端部分front_end.zip、后端部分back_end.zip<br>

后端部分：<br>

进入后端文件夹根目录back_end<br>

安装依赖<br>

`pip install -r requirements.txt`

启动服务<br>

`uvicorn app:app --reload`

<br>

前端部分：<br>

进入前端文件夹根目录chess-recognizer-ui<br>

安装依赖<br>

`npm install`

启动服务<br>

`npm run dev`

默认情况下，会在 http://localhost:5173 启动，浏览器访问该链接即可使用本项目。
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEwODE4NDQ4MTRdfQ==
-->