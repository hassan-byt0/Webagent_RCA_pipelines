import React, { useState, useEffect } from 'react';
import { 
  Search, 
  BookOpen, 
  User, 
  Calendar, 
  FileText, 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Activity,
  Target,
  Database,
  Globe
} from 'lucide-react';

const ArXivRootCauseAnalyzer = ({ analysisData }) => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');

  // Sample data structure - replace with actual props
  const defaultData = {
    tasks: [
      {
        id: 'arxiv_neural_networks_2023',
        framework: 'selenium',
        status: 'failed',
        rootCause: 'AGENT_REASONING_FAILURE',
        failureStep: 2,
        authorFailureType: 'wrong_author_hallucination',
        dateFailureType: null,
        confidence: 0.92,
        steps: [
          { id: 1, name: 'Navigation and Page Load Verification', status: 'success' },
          { id: 2, name: 'Author Input Field Analysis', status: 'failed' },
          { id: 3, name: 'Classification Label Processing', status: 'failed' },
          { id: 4, name: 'Date Input Validation', status: 'failed' },
          { id: 5, name: 'Search Execution and Results Verification', status: 'failed' }
        ],
        searchQuery: 'Neural Network Optimization',
        targetAuthor: 'Geoffrey Hinton',
        actualInput: 'John Smith',
        dateRange: '2023-01-01 to 2023-12-31',
        classification: 'cs.LG',
        timestamp: '2025-09-02T22:03:19Z'
      },
      {
        id: 'arxiv_quantum_computing_search',
        framework: 'playwright',
        status: 'success',
        rootCause: 'SUCCESS',
        failureStep: null,
        authorFailureType: null,
        dateFailureType: null,
        confidence: 0.98,
        steps: [
          { id: 1, name: 'Navigation and Page Load Verification', status: 'success' },
          { id: 2, name: 'Author Input Field Analysis', status: 'success' },
          { id: 3, name: 'Classification Label Processing', status: 'success' },
          { id: 4, name: 'Date Input Validation', status: 'success' },
          { id: 5, name: 'Search Execution and Results Verification', status: 'success' }
        ],
        searchQuery: 'quantum computing algorithms',
        targetAuthor: 'Peter Shor',
        actualInput: 'Peter Shor',
        dateRange: '2020-01-01 to 2025-01-01',
        classification: 'quant-ph',
        timestamp: '2025-09-02T21:45:12Z'
      },
      {
        id: 'arxiv_captcha_blocked',
        framework: 'selenium',
        status: 'failed',
        rootCause: 'WEBSITE_STATE_FAILURE',
        failureStep: 1,
        authorFailureType: null,
        dateFailureType: null,
        confidence: 0.95,
        steps: [
          { id: 1, name: 'Navigation and Page Load Verification', status: 'failed' },
          { id: 2, name: 'Author Input Field Analysis', status: 'skipped' },
          { id: 3, name: 'Classification Label Processing', status: 'skipped' },
          { id: 4, name: 'Date Input Validation', status: 'skipped' },
          { id: 5, name: 'Search Execution and Results Verification', status: 'skipped' }
        ],
        searchQuery: 'machine learning',
        targetAuthor: 'Yann LeCun',
        actualInput: null,
        dateRange: '2024-01-01 to 2024-12-31',
        classification: 'cs.AI',
        timestamp: '2025-09-02T20:30:45Z'
      }
    ],
    summary: {
      totalTasks: 3,
      successRate: 33.3,
      commonFailures: [
        { type: 'AGENT_REASONING_FAILURE', count: 1, percentage: 33.3 },
        { type: 'WEBSITE_STATE_FAILURE', count: 1, percentage: 33.3 }
      ],
      avgConfidence: 0.95
    }
  };

  const data = analysisData || defaultData;

  useEffect(() => {
    if (data.tasks.length > 0) {
      setSelectedTask(data.tasks[0]);
    }
  }, [data]);

  const getRootCauseIcon = (rootCause) => {
    const iconMap = {
      'SUCCESS': <CheckCircle className="w-5 h-5 text-green-600" />,
      'AGENT_REASONING_FAILURE': <AlertTriangle className="w-5 h-5 text-orange-600" />,
      'DOM_PARSING_FAILURE': <FileText className="w-5 h-5 text-red-600" />,
      'ELEMENT_INTERACTION_FAILURE': <Target className="w-5 h-5 text-purple-600" />,
      'DYNAMIC_CONTENT_FAILURE': <Activity className="w-5 h-5 text-blue-600" />,
      'WEBSITE_STATE_FAILURE': <Globe className="w-5 h-5 text-gray-600" />
    };
    return iconMap[rootCause] || <XCircle className="w-5 h-5 text-red-600" />;
  };

  const getRootCauseColor = (rootCause) => {
    const colorMap = {
      'SUCCESS': 'bg-green-100 text-green-800 border-green-200',
      'AGENT_REASONING_FAILURE': 'bg-orange-100 text-orange-800 border-orange-200',
      'DOM_PARSING_FAILURE': 'bg-red-100 text-red-800 border-red-200',
      'ELEMENT_INTERACTION_FAILURE': 'bg-purple-100 text-purple-800 border-purple-200',
      'DYNAMIC_CONTENT_FAILURE': 'bg-blue-100 text-blue-800 border-blue-200',
      'WEBSITE_STATE_FAILURE': 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colorMap[rootCause] || 'bg-red-100 text-red-800 border-red-200';
  };

  const getStepIcon = (stepId) => {
    const iconMap = {
      1: <Globe className="w-4 h-4" />,
      2: <User className="w-4 h-4" />,
      3: <BookOpen className="w-4 h-4" />,
      4: <Calendar className="w-4 h-4" />,
      5: <Search className="w-4 h-4" />
    };
    return iconMap[stepId] || <Activity className="w-4 h-4" />;
  };

  const getStepStatus = (status) => {
    const statusMap = {
      'success': { color: 'text-green-600', bg: 'bg-green-100', icon: <CheckCircle className="w-4 h-4" /> },
      'failed': { color: 'text-red-600', bg: 'bg-red-100', icon: <XCircle className="w-4 h-4" /> },
      'skipped': { color: 'text-gray-500', bg: 'bg-gray-100', icon: <AlertTriangle className="w-4 h-4" /> }
    };
    return statusMap[status] || statusMap['failed'];
  };

  const filteredTasks = data.tasks.filter(task => {
    if (filterStatus === 'all') return true;
    if (filterStatus === 'success') return task.status === 'success';
    if (filterStatus === 'failed') return task.status === 'failed';
    return true;
  });

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gray-50 min-h-screen">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="w-8 h-8 text-indigo-600" />
          <h1 className="text-3xl font-bold text-gray-900">ArXiv Search Root Cause Analyzer</h1>
        </div>
        
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Searches</p>
                <p className="text-2xl font-bold text-gray-900">{data.summary.totalTasks}</p>
              </div>
              <Database className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Success Rate</p>
                <p className="text-2xl font-bold text-green-600">{data.summary.successRate.toFixed(1)}%</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Confidence</p>
                <p className="text-2xl font-bold text-indigo-600">{(data.summary.avgConfidence * 100).toFixed(0)}%</p>
              </div>
              <Target className="w-8 h-8 text-indigo-600" />
            </div>
          </div>
          
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Top Failure</p>
                <p className="text-xs font-medium text-gray-700">
                  {data.summary.commonFailures[0]?.type.replace(/_/g, ' ') || 'None'}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-orange-600" />
            </div>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setFilterStatus('all')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              filterStatus === 'all' 
                ? 'bg-indigo-600 text-white' 
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            All Tasks
          </button>
          <button
            onClick={() => setFilterStatus('success')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              filterStatus === 'success' 
                ? 'bg-green-600 text-white' 
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            Successful
          </button>
          <button
            onClick={() => setFilterStatus('failed')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              filterStatus === 'failed' 
                ? 'bg-red-600 text-white' 
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            Failed
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Task List */}
        <div className="lg:col-span-1">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Results</h2>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredTasks.map((task) => (
              <div
                key={task.id}
                onClick={() => setSelectedTask(task)}
                className={`p-4 bg-white rounded-lg border cursor-pointer transition-all hover:shadow-md ${
                  selectedTask?.id === task.id ? 'ring-2 ring-indigo-500 border-indigo-300' : 'border-gray-200'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-900 truncate">{task.id}</span>
                  {getRootCauseIcon(task.rootCause)}
                </div>
                
                <div className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border ${getRootCauseColor(task.rootCause)}`}>
                  {task.rootCause.replace(/_/g, ' ')}
                </div>
                
                <div className="mt-2 text-xs text-gray-500">
                  <p>Query: {task.searchQuery}</p>
                  <p>Framework: {task.framework}</p>
                  <p>Confidence: {(task.confidence * 100).toFixed(0)}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Task Details */}
        <div className="lg:col-span-2">
          {selectedTask ? (
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">{selectedTask.id}</h2>
                  <div className={`inline-flex items-center px-3 py-1 rounded-md text-sm font-medium border ${getRootCauseColor(selectedTask.rootCause)}`}>
                    {getRootCauseIcon(selectedTask.rootCause)}
                    <span className="ml-2">{selectedTask.rootCause.replace(/_/g, ' ')}</span>
                  </div>
                </div>

                {/* Search Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Search Parameters</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <Search className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">Query:</span>
                        <span className="font-medium">{selectedTask.searchQuery}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <BookOpen className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">Classification:</span>
                        <span className="font-medium">{selectedTask.classification}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">Date Range:</span>
                        <span className="font-medium">{selectedTask.dateRange}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Author Analysis</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">Target:</span>
                        <span className="font-medium">{selectedTask.targetAuthor}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-600">Actual:</span>
                        <span className={`font-medium ${selectedTask.actualInput === selectedTask.targetAuthor ? 'text-green-600' : 'text-red-600'}`}>
                          {selectedTask.actualInput || 'Not entered'}
                        </span>
                      </div>
                      {selectedTask.authorFailureType && (
                        <div className="flex items-center gap-2">
                          <AlertTriangle className="w-4 h-4 text-orange-500" />
                          <span className="text-gray-600">Failure Type:</span>
                          <span className="font-medium text-orange-600">{selectedTask.authorFailureType.replace(/_/g, ' ')}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Step Analysis */}
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Step-by-Step Analysis</h3>
                  <div className="space-y-3">
                    {selectedTask.steps.map((step) => {
                      const stepStatus = getStepStatus(step.status);
                      return (
                        <div
                          key={step.id}
                          className={`flex items-center p-3 rounded-lg border ${
                            step.status === 'success' ? 'border-green-200 bg-green-50' :
                            step.status === 'failed' ? 'border-red-200 bg-red-50' :
                            'border-gray-200 bg-gray-50'
                          }`}
                        >
                          <div className="flex items-center mr-4">
                            <div className={`w-8 h-8 rounded-full ${stepStatus.bg} ${stepStatus.color} flex items-center justify-center mr-3`}>
                              {step.id}
                            </div>
                            {getStepIcon(step.id)}
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <span className="font-medium text-gray-900">{step.name}</span>
                              <div className={`flex items-center ${stepStatus.color}`}>
                                {stepStatus.icon}
                                <span className="ml-1 text-sm font-medium capitalize">{step.status}</span>
                              </div>
                            </div>
                            {selectedTask.failureStep === step.id && (
                              <p className="text-sm text-red-600 mt-1">
                                ⚠️ Primary failure point identified
                              </p>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Failure Details */}
                {selectedTask.status === 'failed' && (
                  <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <h3 className="text-lg font-medium text-red-900 mb-2">Failure Analysis</h3>
                    <div className="space-y-2 text-sm text-red-800">
                      <p><strong>Root Cause:</strong> {selectedTask.rootCause.replace(/_/g, ' ')}</p>
                      <p><strong>Failed at Step:</strong> {selectedTask.failureStep} - {selectedTask.steps.find(s => s.id === selectedTask.failureStep)?.name}</p>
                      {selectedTask.authorFailureType && (
                        <p><strong>Author Issue:</strong> {selectedTask.authorFailureType.replace(/_/g, ' ')}</p>
                      )}
                      {selectedTask.dateFailureType && (
                        <p><strong>Date Issue:</strong> {selectedTask.dateFailureType.replace(/_/g, ' ')}</p>
                      )}
                      <p><strong>Analysis Confidence:</strong> {(selectedTask.confidence * 100).toFixed(1)}%</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 p-6 text-center text-gray-500">
              <BookOpen className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>Select a task from the list to view detailed analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ArXivRootCauseAnalyzer;
