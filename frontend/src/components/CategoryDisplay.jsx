function CategoryDisplay({ category }) {
  if (!category) return null;

  // Icons for categories
  const categoryIcons = {
    "Business & Finance": "💼",
    "Technology & Science": "🔬",
    "Politics & Government": "🏛️",
    "Sports & Entertainment": "⚽",
    "Health & Medicine": "🏥",
    "Education & Research": "📚",
    "Travel & Tourism": "✈️",
    "Legal & Law": "⚖️",
    "Environment & Nature": "🌿",
    "General News": "📰"
  };

  const getConfidenceColor = (conf) => {
    if (conf > 0.7) return 'text-green-600';
    if (conf > 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Content Category</h2>

      {/* Primary Category */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border-2 border-blue-200 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-4xl mr-3">
              {categoryIcons[category.primary_category] || "📄"}
            </span>
            <div>
              <div className="text-xl font-bold text-gray-800">
                {category.primary_category}
              </div>
              <div className="text-sm text-gray-600">Primary Category</div>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-3xl font-bold ${getConfidenceColor(category.confidence)}`}>
              {Math.round(category.confidence * 100)}%
            </div>
            <div className="text-xs text-gray-500">Confidence</div>
          </div>
        </div>
      </div>

      {/* Top Categories */}
      {category.top_categories && category.top_categories.length > 1 && (
        <div>
          <h3 className="font-semibold text-gray-700 mb-2">Other Possible Categories:</h3>
          <div className="space-y-2">
            {category.top_categories.slice(1).map((cat, idx) => (
              <div key={idx} className="flex items-center justify-between bg-gray-50 p-3 rounded">
                <div className="flex items-center">
                  <span className="text-2xl mr-2">{categoryIcons[cat.category] || "📄"}</span>
                  <span className="font-medium">{cat.category}</span>
                </div>
                <span className="text-gray-600 font-semibold">
                  {Math.round(cat.confidence * 100)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Entity Hints */}
      {category.entity_hints && category.entity_hints.length > 0 && (
        <div className="mt-4 p-3 bg-yellow-50 rounded border border-yellow-200">
          <div className="text-sm font-semibold text-yellow-800 mb-1">
            Classification Hints:
          </div>
          <ul className="text-sm text-yellow-700 list-disc list-inside">
            {category.entity_hints.map((hint, idx) => (
              <li key={idx}>{hint}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default CategoryDisplay;