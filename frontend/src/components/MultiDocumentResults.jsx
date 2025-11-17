function MultiDocumentResults({ results }) {
    if (!results) return null;

    const getStatusColor = (status) => {
        return status === 'success' ? 'bg-green-100 border-green-400' : 'bg-red-100 border-red-400';
    };

    const getSentimentEmoji = (sentiment) => {
        if (!sentiment) return '😐';
        if (sentiment.polarity > 0.1) return '😊';
        if (sentiment.polarity < -0.1) return '😞';
        return '😐';
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Multi-Document Analysis Results</h2>

            {/* Summary Stats */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-blue-700">{results.total_files}</div>
                    <div className="text-sm text-gray-600">Total Files</div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-green-700">{results.successful}</div>
                    <div className="text-sm text-gray-600">Successful</div>
                </div>
                <div className="bg-red-50 p-4 rounded-lg text-center">
                    <div className="text-3xl font-bold text-red-700">{results.failed}</div>
                    <div className="text-sm text-gray-600">Failed</div>
                </div>
            </div>

            {/* Individual File Results */}
            <div className="space-y-4">
                {results.results.map((result, index) => (
                    <div key={index} className={`border-2 rounded-lg p-4 ${getStatusColor(result.status)}`}>
                        {/* File Header */}
                        <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-2">
                                <span className="text-2xl">
                                    {result.filename.endsWith('.pdf') ? '📄' :
                                        result.filename.endsWith('.docx') ? '📝' : '📋'}
                                </span>
                                <span className="font-bold text-gray-800">{result.filename}</span>
                            </div>
                            <span className={`px-3 py-1 rounded text-sm font-semibold ${result.status === 'success' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                                }`}>
                                {result.status}
                            </span>
                        </div>

                        {/* Error Message */}
                        {result.status === 'error' && (
                            <div className="text-red-700 text-sm">
                                Error: {result.error}
                            </div>
                        )}

                        {/* Success Details */}
                        {result.status === 'success' && (
                            <div>
                                {/* Quick Stats */}
                                <div className="grid grid-cols-4 gap-3 mb-3">
                                    <div className="bg-white p-2 rounded text-center">
                                        <div className="text-lg font-bold text-gray-700">{result.text_length}</div>
                                        <div className="text-xs text-gray-500">Characters</div>
                                    </div>
                                    <div className="bg-white p-2 rounded text-center">
                                        <div className="text-lg font-bold text-blue-700">{result.total_entities}</div>
                                        <div className="text-xs text-gray-500">Entities</div>
                                    </div>
                                    <div className="bg-white p-2 rounded text-center">
                                        <div className="text-lg">{getSentimentEmoji(result.sentiment)}</div>
                                        <div className="text-xs text-gray-500">
                                            {result.sentiment?.label || 'N/A'}
                                        </div>
                                    </div>
                                    <div className="bg-white p-2 rounded text-center">
                                        <div className="text-sm font-bold text-purple-700">
                                            {result.category?.primary_category?.split(' ')[0] || 'N/A'}
                                        </div>
                                        <div className="text-xs text-gray-500">Category</div>
                                    </div>
                                </div>

                                {/* Text Preview */}
                                <div className="bg-white p-3 rounded mb-3">
                                    <div className="text-xs text-gray-500 mb-1">Text Preview:</div>
                                    <div className="text-sm text-gray-700 italic">
                                        {result.text_preview}
                                    </div>
                                </div>

                                {/* Entity Counts */}
                                {result.counts && Object.keys(result.counts).length > 0 && (
                                    <div className="bg-white p-3 rounded">
                                        <div className="text-xs text-gray-500 mb-2">Entity Breakdown:</div>
                                        <div className="flex flex-wrap gap-2">
                                            {Object.entries(result.counts).map(([label, count]) => (
                                                <span key={label} className="px-2 py-1 bg-gray-200 rounded text-xs font-semibold">
                                                    {label}: {count}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Top Entities */}
                                {result.entities && result.entities.length > 0 && (
                                    <div className="mt-3">
                                        <div className="text-xs text-gray-500 mb-1">Sample Entities:</div>
                                        <div className="flex flex-wrap gap-2">
                                            {result.entities.slice(0, 5).map((ent, idx) => (
                                                <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                                                    {ent.text}
                                                </span>
                                            ))}
                                            {result.entities.length > 5 && (
                                                <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                                                    +{result.entities.length - 5} more
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Export All Button */}
            <button className="w-full mt-6 bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 font-semibold">
                Export All Results as CSV
            </button>
        </div>
    );
}

export default MultiDocumentResults;