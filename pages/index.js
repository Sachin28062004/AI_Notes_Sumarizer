import { useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { jsPDF } from 'jspdf';
import {
  Clipboard,
  Download,
  Upload,
  FileText,
  Loader2,
  CheckCircle,
  AlertCircle,
  Moon,
  Sun,
} from 'lucide-react';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000';

export default function Home() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [summary, setSummary] = useState('');
  const [originalText, setOriginalText] = useState('');
  const [length, setLength] = useState('medium');
  const [format, setFormat] = useState('paragraph');
  const [error, setError] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.classList.toggle('bg-dark', darkMode);
    document.body.classList.toggle('text-light', darkMode);
  }, [darkMode]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        setText('');
      }
    },
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'audio/mpeg': ['.mp3'],
      'audio/wav': ['.wav'],
    },
    maxFiles: 1,
  });

  const downloadPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(12);
    doc.text(summary, 10, 10, { maxWidth: 180 });
    doc.save('summary.pdf');
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      alert('Copied to clipboard!');
    } catch {
      alert('Failed to copy.');
    }
  };

  const handleTextChange = (e) => {
    setText(e.target.value);
    setFile(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsProcessing(true);
    setSummary('');
    setOriginalText('');

    try {
      let response;
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('length', length);
        formData.append('format', format);
        response = await axios.post(`${BACKEND_URL}/api/summarizer/upload-document`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setOriginalText(response.data.original_text);
      } else if (text.trim()) {
        response = await axios.post(`${BACKEND_URL}/api/summarizer/summarize-text`, {
          text,
          length,
          format,
        });
        setOriginalText(text);
      } else {
        throw new Error('Please provide text or upload a file');
      }
      setSummary(response.data.summary);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'An error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container py-5">
      <header className="bg-primary text-white p-4 d-flex justify-content-between align-items-center rounded">
        <div>
          <h1 className="h3 mb-1">AI Notes Summarizer</h1>
          <small className="text-light">Summarize text, PDFs, handwritten images, and audio files easily.</small>
        </div>
      </header>

      <main className="mt-4">
        <form onSubmit={handleSubmit} className="bg-light p-4 rounded shadow">
          <div className="mb-3">
            <label className="form-label">Enter Text</label>
            <textarea
              className="form-control"
              placeholder="Type or paste your notes here..."
              value={text}
              onChange={handleTextChange}
              disabled={isProcessing}
              rows={5}
            />
            <small className="text-muted float-end">{text.length} characters</small>
          </div>

          <div className="mb-3">
            <label className="form-label">Or Upload a File</label>
            <div
              {...getRootProps()}
              className={`border border-secondary border-dashed rounded p-4 text-center ${isDragActive ? 'bg-info bg-opacity-10' : ''}`}
              style={{ cursor: 'pointer' }}
            >
              <input {...getInputProps()} disabled={isProcessing} />
              <Upload className="mb-2" />
              {file ? (
                <p className="text-success"><FileText className="me-2" />{file.name}</p>
              ) : (
                <>
                  <p className="fw-semibold">Drag and drop, or click to upload</p>
                  <small className="text-muted">Supports: .txt, .pdf, .png, .jpg, .mp3, .wav</small>
                </>
              )}
            </div>
          </div>

          <div className="row g-3 mb-3">
            <div className="col-md">
              <label className="form-label">Summary Length</label>
              <select className="form-select" value={length} onChange={(e) => setLength(e.target.value)} disabled={isProcessing}>
                <option value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>
            <div className="col-md">
              <label className="form-label">Output Format</label>
              <select className="form-select" value={format} onChange={(e) => setFormat(e.target.value)} disabled={isProcessing}>
                <option value="paragraph">Paragraph</option>
                <option value="bullets">Bullet Points</option>
                <option value="mindmap">Mind Map</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className={`btn btn-primary w-100 d-flex justify-content-center align-items-center ${isProcessing ? 'disabled' : ''}`}
            disabled={isProcessing || (!text && !file)}
          >
            {isProcessing ? <><Loader2 className="me-2 spinner-border spinner-border-sm" /> Processing...</> : 'Generate Summary'}
          </button>

          {error && (
            <div className="alert alert-danger mt-3 d-flex align-items-center">
              <AlertCircle className="me-2" /> {error}
            </div>
          )}
        </form>

        {summary && (
          <div className="bg-light p-4 rounded shadow mt-4">
            <h2 className="h5 mb-3">Summary Result</h2>
            <div className="mb-3">
              <h3 className="h6 mb-2">
                {format === 'mindmap' ? 'Mind Map' : `${length.charAt(0).toUpperCase() + length.slice(1)} Summary`}
              </h3>
              <div className="border p-3 bg-white">
                {format === 'bullets' ? (
                  <ul className="ps-3">
                    {summary.split('\n').map((line, i) => (
                      <li key={i}>{line.replace('• ', '')}</li>
                    ))}
                  </ul>
                ) : format === 'mindmap' ? (
                  <pre className="small">{summary}</pre>
                ) : (
                  <p>{summary}</p>
                )}
              </div>
            </div>

            <div className="mt-3 d-flex gap-2">
              <button onClick={copyToClipboard} className="btn btn-outline-primary">
                <Clipboard size={18} className="me-1" /> Copy
              </button>
              <button onClick={downloadPDF} className="btn btn-outline-success">
                <Download size={18} className="me-1" /> Download PDF
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}