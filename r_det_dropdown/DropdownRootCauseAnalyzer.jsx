import React, { useState, useEffect } from 'react';
import { ChevronRight, AlertTriangle, CheckCircle, XCircle, RefreshCw, Clock } from 'lucide-react';

const DropdownRootCauseAnalyzer = () => {
  const [framework, setFramework] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState({});
  const [rootCause, setRootCause] = useState(null);
  const [analysisComplete, setAnalysisComplete] = useState(false);

  const frameworks = ['React', 'Vue', 'Angular', 'jQuery', 'Bootstrap', 'Tailwind', 'Vanilla'];

  const steps = [
    {
      id: 'dropdown_detection',
      title: 'Step 1: Initial Element Detection',
      questions: [
        {
          id: 'dropdown_detected',
          text: 'Can the webagent detect dropdown elements in the DOM?',
          type: 'boolean'
        },
        {
          id: 'dropdown_interaction_success',
          text: 'Did the webagent successfully interact with the dropdown?',
          type: 'conditional',
          condition: (responses) => responses.dropdown_detected === true,
          subtype: 'boolean'
        }
      ]
    },
    {
      id: 'category_navigation',
      title: 'Step 2: Primary Category Navigation',
      questions: [
        {
          id: 'men_option_clicked',
          text: 'Did the webagent successfully click the "Men" option?',
          type: 'boolean'
        },
        {
          id: 'action_timing',
          text: 'What was the timing of the Men option click?',
          type: 'conditional',
          condition: (responses) => responses.men_option_clicked === true,
          subtype: 'select',
          options: ['< 500ms (too fast)', '500ms - 2s (normal)', '> 2s (slow)']
        },
        {
          id: 'agent_searched_instead',
          text: 'Did the agent search instead of clicking?',
          type: 'conditional',
          condition: (responses) => responses.men_option_clicked === false,
          subtype: 'boolean'
        }
      ]
    },
    {
      id: 'subcategory_selection',
      title: 'Step 3: Subcategory Selection Validation',
      questions: [
        {
          id: 'subcategory_options_loaded',
          text: 'Are subcategory options (Shoes, Clothing) visible in the DOM?',
          type: 'boolean'
        },
        {
          id: 'correct_subcategory_selected',
          text: 'Did the webagent select the correct subcategory (Shoes instead of Clothing)?',
          type: 'conditional',
          condition: (responses) => responses.subcategory_options_loaded === true,
          subtype: 'boolean'
        }
      ]
    },
    {
      id: 'filter_application',
      title: 'Step 4: Filter Application Verification',
      questions: [
        {
          id: 'nike_filter_applied',
          text: 'Did the webagent apply the Nike brand filter?',
          type: 'boolean'
        },
        {
          id: 'product_grid_updated',
          text: 'Did the product grid update after applying the filter?',
          type: 'conditional',
          condition: (responses) => responses.nike_filter_applied === true,
          subtype: 'boolean'
        },
        {
          id: 'server_response_error',
          text: 'Was there a server response error during filter application?',
          type: 'conditional',
          condition: (responses) => responses.nike_filter_applied === true && responses.product_grid_updated === false,
          subtype: 'boolean'
        }
      ]
    },
    {
      id: 'product_analysis',
      title: 'Step 5: Product Analysis and Selection',
      questions: [
        {
          id: 'price_elements_detected',
          text: 'Can the webagent detect price elements in the DOM?',
          type: 'boolean'
        },
        {
          id: 'price_parsing_success',
          text: 'Did the webagent successfully parse price values?',
          type: 'conditional',
          condition: (responses) => responses.price_elements_detected === true,
          subtype: 'boolean'
        },
        {
          id: 'correct_cheapest_identified',
          text: 'Did the webagent correctly identify the cheapest product?',
          type: 'conditional',
          condition: (responses) => responses.price_parsing_success === true,
          subtype: 'boolean'
        }
      ]
    },
    {
      id: 'transaction_completion',
      title: 'Step 6: Transaction Completion',
      questions: [
        {
          id: 'correct_item_added',
          text: 'Was the correct item added to cart?',
          type: 'boolean'
        },
        {
          id: 'checkout_elements_detected',
          text: 'Can the webagent detect checkout elements?',
          type: 'conditional',
          condition: (responses) => responses.correct_item_added === true,
          subtype: 'boolean'
        },
        {
          id: 'checkout_interaction_success',
          text: 'Did the webagent successfully interact with checkout elements?',
          type: 'conditional',
          condition: (responses) => responses.checkout_elements_detected === true,
          subtype: 'boolean'
        }
      ]
    }
  ];

  const analyzeRootCause = (responses, framework) => {
    // Step 1: Initial Element Detection
    if (responses.dropdown_detected === false) {
      return {
        category: 'DOM Parsing Failure',
        subcategory: 'Dropdown Element Not Detected',
        recommendation: 'Update dropdown element selectors or wait strategies',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dom_parsing')
      };
    }

    if (responses.dropdown_detected === true && responses.dropdown_interaction_success === false) {
      return {
        category: 'Element Interaction Failure',
        subcategory: 'Dropdown Interaction Failed',
        recommendation: 'Fix dropdown interaction mechanism',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'interaction')
      };
    }

    // Step 2: Primary Category Navigation
    if (responses.men_option_clicked === false) {
      if (responses.agent_searched_instead === true) {
        return {
          category: 'Dynamic Content Failure',
          subcategory: 'Agent Searched Instead of Clicked',
          recommendation: 'Improve click detection and interaction patterns',
          frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dynamic_rendering')
        };
      }
    }

    if (responses.men_option_clicked === true && responses.action_timing === '< 500ms (too fast)') {
      return {
        category: 'Dynamic Content Failure',
        subcategory: 'Action Timing Too Fast',
        recommendation: 'Implement proper wait strategies for dynamic content loading',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dynamic_rendering')
      };
    }

    // Step 3: Subcategory Selection Validation
    if (responses.correct_subcategory_selected === false) {
      return {
        category: 'Agent Reasoning Failure',
        subcategory: 'Wrong Subcategory Selected',
        recommendation: 'Improve subcategory selection logic and reasoning',
        frameworkSpecific: null
      };
    }

    if (responses.subcategory_options_loaded === false) {
      return {
        category: 'Dynamic Content Failure',
        subcategory: 'Subcategory Options Not Loaded',
        recommendation: 'Implement better wait strategies for dynamic subcategory loading',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dynamic_rendering')
      };
    }

    // Step 4: Filter Application
    if (responses.nike_filter_applied === true && responses.product_grid_updated === false) {
      if (responses.server_response_error === true) {
        return {
          category: 'Website State Failure',
          subcategory: 'Server Response Error',
          recommendation: 'Handle server errors gracefully and implement retry logic',
          frameworkSpecific: null
        };
      } else {
        return {
          category: 'Dynamic Content Failure',
          subcategory: 'Product Grid Not Updated',
          recommendation: 'Improve detection of dynamic product grid updates',
          frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dynamic_rendering')
        };
      }
    }

    // Step 5: Product Analysis
    if (responses.price_elements_detected === true && responses.price_parsing_success === false) {
      return {
        category: 'DOM Parsing Failure',
        subcategory: 'Price Element Parsing Failed',
        recommendation: 'Update price parsing selectors and logic',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dom_parsing')
      };
    }

    if (responses.price_elements_detected === false) {
      return {
        category: 'DOM Parsing Failure',
        subcategory: 'Price Elements Not Found',
        recommendation: 'Update price element selectors',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dom_parsing')
      };
    }

    if (responses.correct_cheapest_identified === false) {
      return {
        category: 'Agent Reasoning Failure',
        subcategory: 'Wrong Product Identified as Cheapest',
        recommendation: 'Improve price comparison and product selection logic',
        frameworkSpecific: null
      };
    }

    // Step 6: Transaction Completion
    if (responses.correct_item_added === false) {
      return {
        category: 'Agent Reasoning Failure',
        subcategory: 'Wrong Item Added to Cart',
        recommendation: 'Improve item selection and cart addition logic',
        frameworkSpecific: null
      };
    }

    if (responses.checkout_elements_detected === false) {
      return {
        category: 'DOM Parsing Failure',
        subcategory: 'Checkout Elements Not Found',
        recommendation: 'Update checkout element selectors',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'dom_parsing')
      };
    }

    if (responses.checkout_elements_detected === true && responses.checkout_interaction_success === false) {
      return {
        category: 'Element Interaction Failure',
        subcategory: 'Checkout Interaction Failed',
        recommendation: 'Fix checkout interaction mechanism',
        frameworkSpecific: getFrameworkSpecificAdvice(framework, 'interaction')
      };
    }

    // Success case
    return {
      category: 'Success',
      subcategory: 'All Steps Completed Successfully',
      recommendation: 'No action needed',
      frameworkSpecific: null
    };
  };

  const getFrameworkSpecificAdvice = (framework, errorType) => {
    const advice = {
      'React': {
        'dom_parsing': 'Use React Testing Library queries or React-specific selectors',
        'dynamic_rendering': 'Use useEffect hooks and state updates to handle async content',
        'interaction': 'Use React event handlers and synthetic events for reliable interactions'
      },
      'Vue': {
        'dom_parsing': 'Use Vue Test Utils or Vue-specific component queries',
        'dynamic_rendering': 'Use Vue reactivity system and $nextTick for DOM updates',
        'interaction': 'Use Vue event handlers and custom directives'
      },
      'Angular': {
        'dom_parsing': 'Use Angular Testing utilities and component queries',
        'dynamic_rendering': 'Use Angular change detection and async/await patterns',
        'interaction': 'Use Angular event binding and component methods'
      },
      'jQuery': {
        'dom_parsing': 'Use jQuery selectors with proper specificity',
        'dynamic_rendering': 'Use jQuery promises and .ready() for dynamic content',
        'interaction': 'Use jQuery event delegation for dynamic elements'
      },
      'Bootstrap': {
        'dom_parsing': 'Use Bootstrap utility classes and data attributes',
        'dynamic_rendering': 'Account for Bootstrap component initialization timing',
        'interaction': 'Use Bootstrap event callbacks and component APIs'
      },
      'Tailwind': {
        'dom_parsing': 'Use semantic attributes instead of utility classes for selection',
        'dynamic_rendering': 'Tailwind is CSS-only, focus on underlying JavaScript framework',
        'interaction': 'Use JavaScript framework event handling, not Tailwind-specific'
      },
      'Vanilla': {
        'dom_parsing': 'Use robust native selectors (querySelector, getElementById)',
        'dynamic_rendering': 'Use MutationObserver or polling for dynamic content detection',
        'interaction': 'Use native event listeners with proper event delegation'
      }
    };

    return advice[framework]?.[errorType] || null;
  };

  // Check for immediate failure after each response
  useEffect(() => {
    const analysis = analyzeRootCause(responses, framework);
    if (analysis && analysis.category !== 'Success' && Object.keys(responses).length > 0) {
      setRootCause(analysis);
      setAnalysisComplete(true);
    }
  }, [responses, framework]);

  const handleResponse = (questionId, value) => {
    const newResponses = { ...responses, [questionId]: value };
    setResponses(newResponses);
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      const analysis = analyzeRootCause(responses, framework);
      setRootCause(analysis);
      setAnalysisComplete(true);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const restart = () => {
    setFramework('');
    setCurrentStep(0);
    setResponses({});
    setRootCause(null);
    setAnalysisComplete(false);
  };

  const shouldShowQuestion = (question) => {
    if (question.type !== 'conditional') return true;
    return question.condition(responses);
  };

  const isStepComplete = () => {
    const currentStepQuestions = steps[currentStep].questions.filter(shouldShowQuestion);
    return currentStepQuestions.every(q => responses[q.id] !== undefined);
  };

  if (!framework) {
    return (
      <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-6 text-blue-900">
          Dropdown WebAgent Root Cause Analyzer
        </h1>
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Select Framework Used:</h2>
          <div className="grid grid-cols-2 gap-3">
            {frameworks.map((fw) => (
              <button
                key={fw}
                onClick={() => setFramework(fw)}
                className="p-3 border-2 border-blue-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors text-center font-medium"
              >
                {fw}
              </button>
            ))}
          </div>
        </div>
        <div className="text-sm text-gray-600 bg-gray-50 p-4 rounded-lg">
          <p className="font-medium mb-2">About this tool:</p>
          <p>This analyzer implements the deterministic cascade dropdown algorithm to identify root causes of webagent failures in e-commerce dropdown workflows. Analysis shows immediately when a failure is detected.</p>
        </div>
      </div>
    );
  }

  if (analysisComplete) {
    return (
      <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-blue-900 mb-2">Root Cause Analysis</h1>
          <p className="text-gray-600">Framework: <span className="font-semibold">{framework}</span></p>
        </div>
        
        <div className="bg-gray-50 p-6 rounded-lg mb-6">
          <div className="flex items-center mb-4">
            {rootCause.category === 'Success' ? (
              <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
            ) : (
              <AlertTriangle className="h-8 w-8 text-red-500 mr-3" />
            )}
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{rootCause.category}</h2>
              <p className="text-lg text-gray-700">{rootCause.subcategory}</p>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Recommendation:</h3>
              <p className="text-gray-700 bg-white p-3 rounded border-l-4 border-blue-500">
                {rootCause.recommendation}
              </p>
            </div>
            
            {rootCause.frameworkSpecific && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">{framework}-Specific Advice:</h3>
                <p className="text-gray-700 bg-white p-3 rounded border-l-4 border-orange-500">
                  {rootCause.frameworkSpecific}
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-center">
          <button
            onClick={restart}
            className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <RefreshCw className="h-5 w-5 mr-2" />
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  const currentStepData = steps[currentStep];
  const visibleQuestions = currentStepData.questions.filter(shouldShowQuestion);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold text-blue-900 mb-2">Dropdown Root Cause Analysis</h1>
        <p className="text-gray-600">Framework: <span className="font-semibold">{framework}</span></p>
      </div>

      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600">Progress</span>
          <span className="text-sm text-gray-600">{currentStep + 1} of {steps.length}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">{currentStepData.title}</h2>
        
        <div className="space-y-6">
          {visibleQuestions.map((question) => (
            <div key={question.id} className="bg-gray-50 p-4 rounded-lg">
              <label className="block text-lg font-medium text-gray-900 mb-3">
                {question.text}
              </label>
              
              {question.type === 'boolean' || question.subtype === 'boolean' ? (
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleResponse(question.id, true)}
                    className={`px-4 py-2 rounded-lg border-2 transition-colors ${
                      responses[question.id] === true
                        ? 'border-green-500 bg-green-50 text-green-700'
                        : 'border-gray-300 hover:border-green-300'
                    }`}
                  >
                    Yes
                  </button>
                  <button
                    onClick={() => handleResponse(question.id, false)}
                    className={`px-4 py-2 rounded-lg border-2 transition-colors ${
                      responses[question.id] === false
                        ? 'border-red-500 bg-red-50 text-red-700'
                        : 'border-gray-300 hover:border-red-300'
                    }`}
                  >
                    No
                  </button>
                </div>
              ) : question.subtype === 'select' && question.options ? (
                <select
                  value={responses[question.id] || ''}
                  onChange={(e) => handleResponse(question.id, e.target.value)}
                  className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                >
                  <option value="">Select an option...</option>
                  {question.options.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              ) : null}
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-between">
        <button
          onClick={prevStep}
          disabled={currentStep === 0}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Previous Step
        </button>
        
        <button
          onClick={nextStep}
          disabled={!isStepComplete()}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {currentStep === steps.length - 1 ? 'Complete Analysis' : 'Next Step'}
          <ChevronRight className="h-4 w-4 ml-2" />
        </button>
      </div>
    </div>
  );
};

export default DropdownRootCauseAnalyzer;
