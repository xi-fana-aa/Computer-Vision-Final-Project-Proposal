import React, { useState } from 'react';

const ImageUpload = ({ onImageUpload }) => {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      setSelectedImage(URL.createObjectURL(file));
      if (onImageUpload) {
        onImageUpload(file);
      }
    }
  };

  return (
    <div className="image-upload-container">
      <h3>1. 上传棋盘图片</h3>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {selectedImage && (
        <div className="image-preview-container">
          <h4>图片预览:</h4>
          <img src={selectedImage} alt="Uploaded Chessboard" style={{ maxWidth: '300px', maxHeight: '300px', border: '1px solid #ccc' }} />
        </div>
      )}
    </div>
  );
};

export default ImageUpload; 