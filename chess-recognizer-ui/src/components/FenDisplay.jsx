import React from 'react';

const FenDisplay = ({ fen }) => {
  if (!fen) {
    return null;
  }

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(fen)
      .then(() => {
        alert('FEN 已复制到剪贴板!');
      })
      .catch(err => {
        console.error('无法复制FEN: ', err);
        alert('复制FEN失败。');
      });
  };

  return (
    <div className="fen-display-container" style={{ marginTop: '20px' }}>
      <h3>3. FEN 结果</h3>
      <div style={{ fontFamily: 'monospace', backgroundColor: '#f5f5f5', padding: '10px', border: '1px solid #ddd', marginBottom: '10px' }}>
        {fen}
      </div>
      <button onClick={handleCopyToClipboard}>复制FEN</button>
    </div>
  );
};

export default FenDisplay; 