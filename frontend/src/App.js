import React, { useState } from "react";
import FileUpload from "./components/FileUpload"; // Modular component
import axios from "axios";
import { Button, CircularProgress } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

const App = () => {
  const [file, setFile] = useState(null);
  const [cleanedData, setCleanedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [columns, setColumns] = useState([]);

  // Handle file selection (from FileUpload component)
  const handleFileUpload = (selectedFile) => {
    console.log("File uploaded:", selectedFile.name);
    setFile(selectedFile);
  };

  // Handle file selection (from input)
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Upload file to backend
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file to upload.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = response.data;
      
      if (data.length > 0) {
        const columnNames = Object.keys(data[0]).map((key) => ({
          field: key,
          headerName: key,
          width: 150,
        }));
        setColumns(columnNames);
        setCleanedData(data.map((row, id) => ({ id, ...row })));
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    }
    setLoading(false);
  };

  // Download cleaned CSV
  const handleDownload = async () => {
    if (!file) return;

    const filename = `cleaned_${file.name}`;
    try {
      const response = await axios.get(`http://127.0.0.1:5000/download/${filename}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error downloading file:", error);
      alert("Failed to download cleaned file.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Healthcare Data Cleaner</h1>

      {/* File Upload Component */}
       
      <br></br>
      
      {/* Alternative File Input */}
      <input type="file" accept=".csv" onChange={handleFileChange} className="mb-4" />
      <br></br>
      {/* Upload Button */}
      <div className="but">
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={loading}
        className="mt-4"
      >
        {loading ? <CircularProgress size={24} /> : "Upload & Clean"}
      </Button>
      </div>
      {/* Data Preview Table */}
      {cleanedData && (
        <div className="w-full mt-6 bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Cleaned Data Preview</h3>
          <div style={{ height: 400, width: "100%" }}>
            <DataGrid rows={cleanedData} columns={columns} pageSize={5} />
          </div>
          <br></br>
<div className="down">
          {/* Download Button */}
          <Button
            variant="contained"
            color="success"
            className="mt-4"
            onClick={handleDownload}
          >
            Download Cleaned CSV
          </Button>
          </div>
        </div>
      )}

<footer className="footer">
<hr></hr>
<h2>Contact Us</h2>
        <p>We'd love to hear from you! Get in touch for your next big project.</p>
        
        <a href="mailto:reshma@example.com" class="btn">Email Us:reshma541@gmail.com</a><br></br>
       
        <p>@2025 Reshma M S. All Rights Reserved.</p>
</footer>
    </div>
    
  );


};


export default App;
