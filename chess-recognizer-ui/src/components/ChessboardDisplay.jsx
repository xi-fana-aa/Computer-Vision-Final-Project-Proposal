import React from 'react';
import { Chessboard } from 'react-chessboard';

const ChessboardDisplay = ({ fen }) => {
  if (!fen) {
    return (
      <div className="chessboard-container">
        <h3>2. 识别结果 (棋盘)</h3>
        <div style={{ width: '400px', height: '400px', backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <p>等待上传图片...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chessboard-container">
      <h3>2. 识别结果 (棋盘)</h3>
      <div style={{ width: '400px' }}>
        <Chessboard
          position={fen}
          boardWidth={400}
          arePiecesDraggable={false}
          boardOrientation="white"
        />
      </div>
      <p style={{marginTop: '10px', fontStyle: 'italic'}}>检测到 FEN: {fen}</p>
    </div>
  );
};

export default ChessboardDisplay; 