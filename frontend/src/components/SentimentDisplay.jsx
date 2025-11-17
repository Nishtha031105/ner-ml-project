function SentimentDisplay({ sentiment, entitySentiments }) {
  if (!sentiment) return null;

  // Color based on sentiment
  const getSentimentColor = (polarity) => {
    if (polarity > 0.1) return 'bg-green-100 border-green-400 text-green-800';
    if (polarity < -0.1) return 'bg-red-100 border-red-400 text-red-800';
    return 'bg-gray-100 border-gray-400 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Sentiment Analysis</h2>
      
      {/* Overall Sentiment */}
      <div className={`p-4 rounded-lg border-2 ${getSentimentColor(sentiment.polarity)} mb-4`}>
        <div className="flex items-center justify-between">
          <div>
            <span className="text-4xl mr-3">{sentiment.emoji}</span>
            <span className="text-xl font-bold">{sentiment.label}</span>
          </div>
          <div className="text-right">
            <div className="text-sm">Polarity Score</div>
            <div className="text-2xl font-bold">{sentiment.polarity}</div>
          </div>
        </div>
        <p className="mt-2 text-sm">{sentiment.description}</p>
      </div>

      {/* Sentiment Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-sm text-gray-600">Polarity</div>
          <div className="text-xl font-bold text-blue-700">
            {sentiment.polarity > 0 ? '+' : ''}{sentiment.polarity}
          </div>
          <div className="text-xs text-gray-500">(-1 = negative, +1 = positive)</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="text-sm text-gray-600">Subjectivity</div>
          <div className="text-xl font-bold text-purple-700">{sentiment.subjectivity}</div>
          <div className="text-xs text-gray-500">(0 = objective, 1 = subjective)</div>
        </div>
      </div>

      {/* Entity-Level Sentiments */}
      {entitySentiments && entitySentiments.length > 0 && (
        <div className="mt-4">
          <h3 className="font-semibold text-gray-700 mb-2">Sentiment by Entity:</h3>
          <div className="space-y-2">
            {entitySentiments.map((es, idx) => (
              <div key={idx} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                <span className="font-medium">{es.entity}</span>
                <span className={`px-3 py-1 rounded text-sm ${
                  es.sentiment > 0.1 ? 'bg-green-200 text-green-800' :
                  es.sentiment < -0.1 ? 'bg-red-200 text-red-800' :
                  'bg-gray-200 text-gray-800'
                }`}>
                  {es.sentiment_label} ({es.sentiment})
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default SentimentDisplay;