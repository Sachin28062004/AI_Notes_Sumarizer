import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import formidable from 'formidable';
import fs from 'fs';
import FormData from 'form-data';

// Disable the default body parser to handle file uploads
export const config = {
  api: {
    bodyParser: false,
  },
};

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Parse form with uploaded file
    const form = new formidable.IncomingForm();
    
    const { fields, files } = await new Promise<{ fields: any, files: any }>((resolve, reject) => {
      form.parse(req, (err, fields, files) => {
        if (err) return reject(err);
        resolve({ fields, files });
      });
    });

    // Create form data to send to backend
    const formData = new FormData();
    
    // Add file if present
    if (files.file) {
      const file = files.file;
      const fileData = fs.readFileSync(file.filepath);
      formData.append('file', new Blob([fileData]), file.originalFilename);
    }
    
    // Add other fields
    Object.entries(fields).forEach(([key, value]) => {
      formData.append(key, value);
    });

    // Send request to backend
    const response = await axios.post(
      `${BACKEND_URL}/api/summarizer/upload-document`, 
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return res.status(200).json(response.data);
  } catch (error) {
    console.error('API proxy error:', error);
    return res.status(500).json({ 
      error: 'Error processing your request',
      details: error.message 
    });
  }
}