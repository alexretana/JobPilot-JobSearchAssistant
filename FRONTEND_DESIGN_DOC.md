# JobPilot Frontend Design Document

## Overview
JobPilot is a career assistance platform with a clean, modern interface designed to help users with job searching, resume building, and AI-powered career guidance. The application features a responsive layout that works well on both desktop and mobile devices, with a focus on transparency in AI operations.

## Layout & Structure

### Main Layout
The application follows a three-section vertical layout:
1. **Header Navigation**: A fixed top bar with branding, main navigation tabs, and theme selector
2. **Main Content Area**: The primary workspace that changes based on the selected tab
3. **System Status Panel**: A slide-out panel accessible from the header for quick actions and system status

### Header
- Left side: JobPilot logo and brand name
- Center: Three main navigation tabs (AI Chat, Job Search, Resume Builder)
- Right side: Theme selector dropdown with multiple color scheme options (Light, Dark, Retro, Cyberpunk, Valentine, Aqua)

## Color Scheme & Design System
The application uses DaisyUI with TailwindCSS, providing a clean and accessible design system with multiple theme options. The default theme features:
- Clean, professional color palette
- Card-based design with subtle shadows for depth
- Rounded corners on most UI elements
- Consistent spacing and typography
- Visual feedback on interactive elements (hover states, active states)

## Navigation & Tabs

### AI Chat Tab (Default)
The primary interface consists of two main panels:
1. **Chat Interface** (Left Panel):
   - Chat message display area with scrolling history
   - Message input area with multi-line text support
   - Send button with processing state indicator
   - Connection status badge showing WebSocket connectivity
   - Progress indicator for AI operations

2. **Browser Viewport** (Right Panel):
   - Real-time display of websites the AI is visiting
   - URL display
   - Content preview of visited pages

### Job Search Tab
A dedicated job search interface with three sub-tabs:
1. **Jobs Tab**: 
   - Job listing cards in a responsive grid
   - Each card displays job title, company, location, salary, and required skills
   - Save/unsave functionality for each job
   - Visit link to original job posting
   - Detailed view option for each job

2. **Applications Tab**: 
   - Tracking of job applications
   - Status indicators for each application

3. **Leads Tab**: 
   - Potential job opportunities
   - Lead management features

### Resume Builder Tab
A comprehensive resume building workspace with three views:
1. **Resume List View**: 
   - Grid of existing resumes
   - Create new resume button
   - Edit/Delete options for existing resumes

2. **Resume Builder View**: 
   - Form-based resume editor
   - Sections for personal information, work experience, education, skills
   - Real-time preview capability

3. **Resume Preview View**: 
   - Print-ready resume preview
   - Edit option to return to builder

## Key UI Components

### Chat Interface
- Message bubbles with distinct styling for user vs AI messages
- Markdown-like formatting support
- Special formatting for job listings with dedicated styling
- Auto-scrolling to latest messages
- Connection status indicator
- Progress bar for long-running AI operations

### Job Cards
- Clean card design with hover effects
- Prominent job title display
- Company and location information
- Job type and remote work indicators
- Salary information when available
- Skills tags with truncation for long lists
- Description preview
- Action buttons (Save, Visit, View Details)

### Modals & Drawers
- Job Details Modal: Full job information display
- Timeline Modal: Chronological activity log
- Status Panel Drawer: Slide-out panel for quick actions and system status

### Responsive Design
- Adapts layout for different screen sizes
- On mobile: Stacked vertical layout instead of side-by-side panels
- Touch-friendly button sizes
- Appropriate spacing for mobile interaction

## Behavior & Interactions

### AI Transparency Features
- Real-time browser viewport showing websites the AI visits
- Timeline modal showing all AI activities and tool usage
- Progress indicators during AI processing
- Clear labeling of AI actions vs user actions

### User Interactions
- Tab-based navigation between main sections
- Clickable job cards for detailed views
- Save/unsave functionality for job listings
- Theme switching with immediate visual feedback
- Form validation in resume builder
- Real-time preview of resume changes

### System Status Indicators
- Connection status badges
- Processing/loading states with spinners
- Progress bars for multi-step operations
- Success/error feedback for user actions

## Accessibility Features
- Semantic HTML structure
- Proper contrast ratios in all themes
- Focus states for keyboard navigation
- Screen reader-friendly labeling
- Sufficient touch target sizes

## Visual Design Elements
- Consistent icon usage throughout the interface
- Gradient accents for primary actions and branding
- Subtle animations and transitions for state changes
- Card-based design with appropriate shadows for depth
- Clear visual hierarchy with typography
- Consistent spacing using a defined scale

This design document provides a comprehensive overview of the JobPilot frontend without referencing any specific packages or implementation details, making it suitable for recreation with any modern frontend framework.