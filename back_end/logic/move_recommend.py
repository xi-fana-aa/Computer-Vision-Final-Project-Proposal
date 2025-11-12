import chess
import chess.engine
import os
import subprocess

def get_best_move(fen,
                  stockfish_path="./stockfish/stockfish-windows-x86-64-avx2.exe",
                  depth=30,
                  syzygy_path="C:/syzygy_tb",
                  timeout=30.0,
                  think_time=5.0):
    try:
        board = chess.Board(fen)
        if not board.is_valid():
            print("错误：非法FEN格式")
            return None
    except ValueError as e:
        print(f"FEN解析错误: {e}")
        return None

    if not os.path.exists(stockfish_path):
        print(f"错误：引擎文件不存在于 {stockfish_path}")
        return None

    try:
        process = subprocess.Popen(
            [stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  
            bufsize=1, 
        )

        # 发送 UCI 初始化命令
        def send(cmd):
            process.stdin.write(cmd + "\n")
            process.stdin.flush()

        def read_lines():
            # 读取多行，直到收到 "readyok"
            lines = []
            while True:
                line = process.stdout.readline().strip()
                if line == "":
                    break
                lines.append(line)
                if line == "readyok":
                    break
            return lines

        send("uci")
        read_lines()  # 读完uci的响应

        send("isready")
        read_lines()  # 等待readyok

        send(f"ucinewgame")
        send(f"position fen {fen}")
        send(f"go movetime {int(think_time*1000)}")

        # 等待bestmove返回
        best_move = None
        while True:
            line = process.stdout.readline().strip()
            if line.startswith("bestmove"):
                best_move = line.split()[1]
                break

        # 关闭进程
        send("quit")
        process.stdin.close()
        process.stdout.close()
        process.stderr.close()
        process.wait()

        return best_move

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"分析错误: {e}")
        return None
