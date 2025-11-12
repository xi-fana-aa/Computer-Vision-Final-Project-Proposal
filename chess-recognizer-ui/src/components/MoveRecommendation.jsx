import React from 'react';

const MoveRecommendation = ({ move }) => {
  if (!move) {
    return (
      <div className="move-recommendation-container" style={{ marginTop: '20px' }}>
        <h3>4. 推荐走法 (来自Stockfish)</h3>
        <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: 'gray' }}>
          无法计算最佳走法
        </div>
      </div>
    );
  }

  // 假设 move 的格式是类似 "e2e4" (起始格目标格)
  // 你可能需要根据Stockfish的实际输出调整解析逻辑
  const formatMove = (uciMove) => {
    if (uciMove && uciMove.length >= 4) {
      const from = uciMove.substring(0, 2);
      const to = uciMove.substring(2, 4);
      // 可以在这里添加更复杂的棋子晋升等逻辑的解析
      return `${from} → ${to}`;
    }
    return uciMove; // 如果格式不符合预期，直接返回原始字符串
  };

  return (
    <div className="move-recommendation-container" style={{ marginTop: '20px' }}>
      <h3>4. 推荐走法 (来自Stockfish)</h3>
      <div style={{ fontSize: '1.2em', fontWeight: 'bold', color: 'green' }}>
        {formatMove(move)}
      </div>
    </div>
  );
};

export default MoveRecommendation; 