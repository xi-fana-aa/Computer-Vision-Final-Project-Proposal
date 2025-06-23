# Computer-Vision-Final-Project
本项目基于 YOLOv8 和 Stockfish 实现了国际象棋局面识别与走法推荐系统。用户上传棋局图片，系统自动完成棋盘检测、棋子识别、FEN 串生成，并调用国际象棋引擎计算最佳走法。

项目描述视频：

项目结构：

project/
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

快速开始：


安装依赖

pip install -r requirements.txt

启动服务

uvicorn app:app --reload

调用接口

POST /api/recognize

Content-Type: multipart/form-data

Body: image=<棋局图片文件>

Response:

{
  "fen": "<FEN字符串>",
  
  "best_move": "<最佳走法>"
}
