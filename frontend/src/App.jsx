import { useState } from 'react';
import Editor from './components/Editor';
import HighlightedText from './components/HighlightedText';
import EntryList from './components/EntryList';
import SentimentDisplay from './components/SentimentDisplay';
import CategoryDisplay from './components/CategoryDisplay';
import FileUpload from './components/FileUpload';
import MultiDocumentResults from './components/MultiDocumentResults';
import { analyzeText, analyzeFile, analyzeMultipleFiles } from './api';

function App() {
  // Existing state
  const [analyzedText, setAnalyzedText] = useState('');
  const [entities, setEntities] = useState([]);
  const [counts, setCounts] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [error, setError] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [entitySentiments, setEntitySentiments] = useState([]);
  const [category, setCategory] = useState(null);

  // NEW: Multi-document state
  const [multiDocResults, setMultiDocResults] = useState(null);
  const [activeTab, setActiveTab] = useState('text'); // 'text' or 'files'

  // Existing text analyze function
  const handleAnalyze = async (text) => {
    setIsLoading(true);
    setError(null);
    setMultiDocResults(null); // Clear multi-doc results

    try {
      const result = await analyzeText(text);

      setAnalyzedText(text);
      setEntities(result.entities);
      setCounts(result.counts);
      setSentiment(result.sentiment);
      setEntitySentiments(result.entity_sentiments);
      setCategory(result.category);
      setSelectedEntity(null);

    } catch (err) {
      setError('Failed to analyze text. Make sure backend is running on port 8000.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: Single file analyze
  const handleFileAnalyze = async (file) => {
    setIsLoading(true);
    setError(null);
    setMultiDocResults(null);

    try {
      const result = await analyzeFile(file);

      if (result.error) {
        setError(result.error);
        return;
      }

      setAnalyzedText(result.text);
      setEntities(result.entities);
      setCounts(result.counts);
      setSentiment(result.sentiment);
      setEntitySentiments(result.entity_sentiments);
      setCategory(result.category);
      setSelectedEntity(null);

    } catch (err) {
      setError('Failed to analyze file: ' + err.message);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: Multiple files analyze
  const handleMultipleFilesAnalyze = async (files) => {
    setIsLoading(true);
    setError(null);

    // Clear single document results
    setAnalyzedText('');
    setEntities([]);
    setCounts({});
    setSentiment(null);
    setEntitySentiments([]);
    setCategory(null);

    try {
      const result = await analyzeMultipleFiles(files);
      setMultiDocResults(result);

    } catch (err) {
      setError('Failed to analyze files: ' + err.message);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEntityClick = (entityText) => {
    setSelectedEntity(selectedEntity === entityText ? null : entityText);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-800 mb-2">
            📝 Named Entity Recognition Tool
          </h1>
          <p className="text-gray-600 text-lg">
            Extract names, places, organizations, and more with AI-powered analysis
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-6">
          <div className="bg-white rounded-lg shadow-md p-1 inline-flex">
            <button
              onClick={() => setActiveTab('text')}
              className={`px-6 py-2 rounded-md font-semibold transition ${activeTab === 'text'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
                }`}
            >
              Text Input
            </button>
            <button
              onClick={() => setActiveTab('files')}
              className={`px-6 py-2 rounded-md font-semibold transition ${activeTab === 'files'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
                }`}
            >
              File Upload
            </button>
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="bg-red-100 border-2 border-red-400 text-red-800 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {/* Text Input Tab */}
        {activeTab === 'text' && (
          <>
            <div className="mb-6">
              <Editor onAnalyze={handleAnalyze} isLoading={isLoading} />
            </div>

            {/* Sentiment Display */}
            {sentiment && (
              <div className="mb-6">
                <SentimentDisplay
                  sentiment={sentiment}
                  entitySentiments={entitySentiments}
                />
              </div>
            )}

            {/* Category Display */}
            {category && (
              <div className="mb-6">
                <CategoryDisplay category={category} />
              </div>
            )}

            {/* Results */}
            {entities.length > 0 && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <HighlightedText
                    text={analyzedText}
                    entities={entities}
                    selectedEntity={selectedEntity}
                  />
                </div>
                <div className="lg:col-span-1">
                  <EntryList
                    entities={entities}
                    counts={counts}
                    onEntityClick={handleEntityClick}
                    selectedEntity={selectedEntity}
                  />
                </div>
              </div>
            )}

            {/* Empty state */}
            {entities.length === 0 && !isLoading && (
              <div className="text-center py-12 bg-white rounded-lg shadow-md">
                <p className="text-gray-500 text-lg">
                  👆 Paste some text above and click "Analyze Text" to get started!
                </p>
              </div>
            )}
          </>
        )}

        {/* File Upload Tab */}
        {activeTab === 'files' && (
          <>
            <div className="mb-6">
              <FileUpload
                onFileAnalyze={handleFileAnalyze}
                onMultipleFilesAnalyze={handleMultipleFilesAnalyze}
                isLoading={isLoading}
              />
            </div>

            {/* Multi-Document Results */}
            {multiDocResults && (
              <div className="mb-6">
                <MultiDocumentResults results={multiDocResults} />
              </div>
            )}

            {/* Single File Results */}
            {!multiDocResults && entities.length > 0 && (
              <>
                {sentiment && (
                  <div className="mb-6">
                    <SentimentDisplay
                      sentiment={sentiment}
                      entitySentiments={entitySentiments}
                    />
                  </div>
                )}

                {category && (
                  <div className="mb-6">
                    <CategoryDisplay category={category} />
                  </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <HighlightedText
                      text={analyzedText}
                      entities={entities}
                      selectedEntity={selectedEntity}
                    />
                  </div>
                  <div className="lg:col-span-1">
                    <EntryList
                      entities={entities}
                      counts={counts}
                      onEntityClick={handleEntityClick}
                      selectedEntity={selectedEntity}
                    />
                  </div>
                </div>
              </>
            )}

            {/* Empty state */}
            {!multiDocResults && entities.length === 0 && !isLoading && (
              <div className="text-center py-12 bg-white rounded-lg shadow-md">
                <p className="text-gray-500 text-lg">
                  📁 Upload files to analyze multiple documents at once!
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;