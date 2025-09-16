export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  type: string;
  remote: boolean;
  hybrid: boolean;
  description: string;
  skills: string[];
  isSaved: boolean;
  url: string;
}

export const sampleJobs: Job[] = [
  {
    id: '1',
    title: 'Senior Software Engineer',
    company: 'Google',
    location: 'San Francisco, CA',
    salary: '$120k - $150k',
    type: 'Full-time',
    remote: true,
    hybrid: false,
    description: "We're looking for an experienced software engineer to join our team...",
    skills: ['JavaScript', 'React', 'Node.js', 'Python'],
    isSaved: false,
    url: 'https://google.com/jobs/1'
  },
  {
    id: '2',
    title: 'Product Manager',
    company: 'Microsoft',
    location: 'Seattle, WA',
    salary: '$130k - $160k',
    type: 'Full-time',
    remote: false,
    hybrid: false,
    description: 'Join our product team to help shape the future of our cloud platform...',
    skills: ['Product Strategy', 'Agile', 'Analytics', 'Roadmapping'],
    isSaved: false,
    url: 'https://microsoft.com/jobs/2'
  },
  {
    id: '3',
    title: 'UX Designer',
    company: 'Apple',
    location: 'Cupertino, CA',
    salary: '$110k - $140k',
    type: 'Full-time',
    remote: false,
    hybrid: true,
    description: 'Create beautiful and intuitive user experiences for our next generation products...',
    skills: ['Figma', 'Prototyping', 'User Research', 'Interaction Design'],
    isSaved: true,
    url: 'https://apple.com/jobs/3'
  },
  {
    id: '4',
    title: 'Data Scientist',
    company: 'Amazon',
    location: 'Remote',
    salary: '$140k - $170k',
    type: 'Full-time',
    remote: true,
    hybrid: false,
    description: 'Join our data science team to build machine learning models...',
    skills: ['Python', 'Machine Learning', 'SQL', 'Statistics'],
    isSaved: false,
    url: 'https://amazon.com/jobs/4'
  },
  {
    id: '5',
    title: 'Frontend Developer',
    company: 'Netflix',
    location: 'Los Angeles, CA',
    salary: '$115k - $145k',
    type: 'Full-time',
    remote: true,
    hybrid: true,
    description: 'Build amazing user interfaces for our streaming platform...',
    skills: ['JavaScript', 'React', 'CSS', 'HTML'],
    isSaved: false,
    url: 'https://netflix.com/jobs/5'
  },
  {
    id: '6',
    title: 'DevOps Engineer',
    company: 'Spotify',
    location: 'Stockholm, Sweden',
    salary: '$90k - $120k',
    type: 'Full-time',
    remote: true,
    hybrid: false,
    description: 'Help us scale our infrastructure and deployment processes...',
    skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
    isSaved: true,
    url: 'https://spotify.com/jobs/6'
  }
];