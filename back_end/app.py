from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from logic.image_preprocess import preprocess_image
from logic.piece_detection import detect_chess_pieces
from logic.fen_generator import generate_fen
from logic.move_recommend import get_best_move

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recognize")
async def recognize(image: UploadFile = File(...)):
    img_bytes = await image.read()

    # 预处理，得到棋盘图像np.ndarray
    processed_image = preprocess_image(img_bytes)

    # 棋子识别，得到8x8数组
    board = detect_chess_pieces(processed_image)

    # 生成FEN
    fen = generate_fen(board)

    # 计算最佳走法
    best_move = get_best_move(fen)

    return {
        "fen": fen,
        "best_move": best_move
    }
