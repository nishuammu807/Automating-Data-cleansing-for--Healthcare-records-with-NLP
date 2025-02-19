import React from "react";

const FileUpload = ({ onFileUpload }) => {
  const handleChange = (e) => {
    if (e.target.files.length > 0) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <input type="file" accept=".csv" onChange={handleChange} className="mb-4" />
    </div>
  );
};

export default FileUpload;

