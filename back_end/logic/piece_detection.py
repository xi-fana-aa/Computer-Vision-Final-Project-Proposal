import cv2
from ultralytics import YOLO

def get_chess_notation(pred_name):
    name = pred_name.replace('-', '_').lower()
    return {
        'black_pawn': 'bP', 'black_rook': 'bR', 'black_knight': 'bN',
        'black_bishop': 'bB', 'black_queen': 'bQ', 'black_king': 'bK',
        'white_pawn': 'wP', 'white_rook': 'wR', 'white_knight': 'wN',
        'white_bishop': 'wB', 'white_queen': 'wQ', 'white_king': 'wK'
    }.get(name, '')

def create_empty_board():
    return [['' for _ in range(8)] for _ in range(8)]

def map_to_board_coords(x, y, img_width, img_height):
    col = int(x / (img_width / 8))
    row = int(y / (img_height / 8))
    return col, row

def detect_chess_pieces(processed_image, model_path="best.pt", conf_thres=0.25, iou_thres=0.45):
    """
    接受 np.ndarray 格式的预处理图像，返回8x8二维列表，元素为棋子标记，如 wP, bK 等
    """
    model = YOLO(model_path)
    if processed_image is None:
        raise ValueError("传入图像为空")

    h, w = processed_image.shape[:2]
    board = create_empty_board()

    results = model.predict(
        source=processed_image,
        conf=conf_thres,
        iou=iou_thres,
        save=False
    )

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls)
            label = model.names[cls_id]
            x1, y1, x2, y2 = map(float, box.xyxy[0])
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2 + (y2 - y1) / 4  # 偏下调整
            col, row = map_to_board_coords(x_center, y_center, w, h)
            if 0 <= row < 8 and 0 <= col < 8:
                board[row][col] = get_chess_notation(label)

    return board
