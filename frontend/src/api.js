import axios from "axios";
const API_BASE_URL = "http://localhost:8000";

export const analyzeText = async (text) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
      text: text
    });
    return response.data;
  } catch (error) {
    console.error("Error analyzing text:", error);
    throw error;
  }
};

// analyze single file
export const analyzeFile = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/analyze-file`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing file:', error);
    throw error;
  }
};

//analyse multiple files
export const analyzeMultipleFiles = async (files) => {
  try {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await axios.post(`${API_BASE_URL}/analyze-multiple-files`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing multiple files:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error("Backend not responding", error);
    return null;
  }
};
