import { useState } from 'react';

function FileUpload({ onFileAnalyze, onMultipleFilesAnalyze, isLoading }) {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [dragActive, setDragActive] = useState(false);

    const handleFileSelect = (event) => {
        const files = Array.from(event.target.files);
        setSelectedFiles(files);
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const files = Array.from(e.dataTransfer.files);
            setSelectedFiles(files);
        }
    };

    const handleAnalyze = () => {
        if (selectedFiles.length === 0) return;

        if (selectedFiles.length === 1) {
            onFileAnalyze(selectedFiles[0]);
        } else {
            onMultipleFilesAnalyze(selectedFiles);
        }
    };

    const removeFile = (index) => {
        setSelectedFiles(files => files.filter((_, i) => i !== index));
    };

    const clearFiles = () => {
        setSelectedFiles([]);
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Upload Documents</h2>

            {/* Drag and Drop Area */}
            <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'
                    }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <div className="mb-4">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                </div>

                <p className="text-lg mb-2 text-gray-700">
                    Drag and drop files here, or click to select
                </p>
                <p className="text-sm text-gray-500 mb-4">
                    Supports: .txt, .pdf, .docx (Max 10 files)
                </p>

                <input
                    type="file"
                    id="file-upload"
                    multiple
                    accept=".txt,.pdf,.docx,.doc"
                    onChange={handleFileSelect}
                    className="hidden"
                />
                <label
                    htmlFor="file-upload"
                    className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 cursor-pointer font-semibold"
                >
                    Choose Files
                </label>
            </div>

            {/* Selected Files List */}
            {selectedFiles.length > 0 && (
                <div className="mt-4">
                    <div className="flex justify-between items-center mb-2">
                        <h3 className="font-semibold text-gray-700">
                            Selected Files ({selectedFiles.length})
                        </h3>
                        <button
                            onClick={clearFiles}
                            className="text-sm text-red-600 hover:text-red-800"
                        >
                            Clear All
                        </button>
                    </div>

                    <div className="space-y-2 max-h-60 overflow-y-auto">
                        {selectedFiles.map((file, index) => (
                            <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded">
                                <div className="flex items-center space-x-3">
                                    <div className="text-2xl">
                                        {file.name.endsWith('.pdf') ? '📄' :
                                            file.name.endsWith('.docx') || file.name.endsWith('.doc') ? '📝' :
                                                '📋'}
                                    </div>
                                    <div>
                                        <div className="font-medium text-gray-800">{file.name}</div>
                                        <div className="text-sm text-gray-500">
                                            {(file.size / 1024).toFixed(2)} KB
                                        </div>
                                    </div>
                                </div>
                                <button
                                    onClick={() => removeFile(index)}
                                    className="text-red-500 hover:text-red-700"
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>

                    {/* Analyze Button */}
                    <button
                        onClick={handleAnalyze}
                        disabled={isLoading || selectedFiles.length === 0}
                        className="w-full mt-4 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
                    >
                        {isLoading ? 'Analyzing...' : `Analyze ${selectedFiles.length} File${selectedFiles.length > 1 ? 's' : ''}`}
                    </button>
                </div>
            )}
        </div>
    );
}

export default FileUpload;