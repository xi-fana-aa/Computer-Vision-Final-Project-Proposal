import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ChessboardDisplay from './components/ChessboardDisplay';
import FenDisplay from './components/FenDisplay';
import MoveRecommendation from './components/MoveRecommendation';
import './App.css'; // 假设你会有App.css文件来做一些全局样式

function App() {
  const [uploadedImageFile, setUploadedImageFile] = useState(null);
  const [fen, setFen] = useState(''); // 例如: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
  const [recommendedMove, setRecommendedMove] = useState(''); // 例如: 'e2e4'
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImageUpload = async (file) => {
    setUploadedImageFile(file);
    setError('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('image', file);
      
      const response = await fetch('http://localhost:8000/api/recognize', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      
      // 根据 API 响应设置状态
      if (data.fen) {
        setFen(data.fen);
      } else {
        setError('无法识别棋盘位置');
        setFen('');
      }
      
      // 设置推荐走法（可能为 null）
      setRecommendedMove(data.best_move || '');

    } catch (err) {
      console.error("Error processing image:", err);
      setError(`处理图片失败: ${err.message}`);
      setFen('');
      setRecommendedMove('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>国际象棋局面识别与走法推荐</h1>
      </header>
      <main>
        <ImageUpload onImageUpload={handleImageUpload} />
        {isLoading && <p>正在识别和分析，请稍候...</p>}
        {error && <p style={{ color: 'red' }}>错误: {error}</p>}
        {/* 
          ChessboardDisplay 应该基于FEN来渲染。
          目前ChessboardDisplay.jsx中的渲染逻辑是静态的，需要您后续完善FEN解析部分。
        */}
        <ChessboardDisplay fen={fen} />
        <FenDisplay fen={fen} />
        <MoveRecommendation move={recommendedMove} />
      </main>
    </div>
  );
}

export default App;
