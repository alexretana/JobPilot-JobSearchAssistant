export interface AIActivity {
  id: string;
  type: 'search' | 'browse' | 'analyze' | 'generate';
  description: string;
  timestamp: Date;
  details?: string;
}

// Sample AI activities data
export const sampleAIActivities: AIActivity[] = [
  {
    id: '1',
    type: 'search',
    description: 'Searching for software engineering jobs in San Francisco',
    timestamp: new Date(Date.now() - 300000),
    details: 'Query: "software engineer san francisco", Sites: LinkedIn, Indeed, Glassdoor'
  },
  {
    id: '2',
    type: 'browse',
    description: 'Visiting job posting on LinkedIn',
    timestamp: new Date(Date.now() - 240000),
    details: 'URL: https://linkedin.com/jobs/view/12345'
  },
  {
    id: '3',
    type: 'analyze',
    description: 'Analyzing job requirements',
    timestamp: new Date(Date.now() - 180000),
    details: 'Extracting key skills: JavaScript, React, Node.js, AWS'
  },
  {
    id: '4',
    type: 'browse',
    description: 'Visiting company website',
    timestamp: new Date(Date.now() - 120000),
    details: 'URL: https://google.com/careers'
  },
  {
    id: '5',
    type: 'generate',
    description: 'Generating job match summary',
    timestamp: new Date(Date.now() - 60000),
    details: 'Created summary for 5 matching positions'
  }
];

// Function to get activity icon based on type
export const getActivityIcon = (type: AIActivity['type']) => {
  switch (type) {
    case 'search':
      return '🔍';
    case 'browse':
      return '🌐';
    case 'analyze':
      return '📊';
    case 'generate':
      return '📝';
    default:
      return '⚡';
  }
};

// Function to get activity color based on type
export const getActivityColor = (type: AIActivity['type']) => {
  switch (type) {
    case 'search':
      return 'bg-blue-500';
    case 'browse':
      return 'bg-green-500';
    case 'analyze':
      return 'bg-purple-500';
    case 'generate':
      return 'bg-yellow-500';
    default:
      return 'bg-gray-500';
  }
};