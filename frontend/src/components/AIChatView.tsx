import type { Component } from 'solid-js';
import { createSignal, For, onMount, createEffect } from 'solid-js';
import { formatMessage } from '../utils/messageFormatter';
import TimelineModal from './TimelineModal';
import { sampleAIActivities } from '../utils/aiActivities';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface BrowserActivity {
  id: string;
  url: string;
  title: string;
  timestamp: Date;
}

const AIChatView: Component = () => {
  let messagesContainerRef: HTMLDivElement | undefined;
  const [messages, setMessages] = createSignal<Message[]>([
    { id: '1', text: 'Hi there! I\'m your **AI career assistant**. How can I help you today?', sender: 'ai', timestamp: new Date() },
    { id: '2', text: 'Can you help me find software engineering jobs in San Francisco?', sender: 'user', timestamp: new Date() },
    { id: '3', text: 'Of course! I can search for software engineering positions in San Francisco. Would you like me to show you the **top 5 matches**?\n\n[JOB]Senior Software Engineer|Google|San Francisco, CA|$120k - $150k|We\'re looking for an experienced software engineer to join our team[JOB]\n\n[JOB]Frontend Developer|Facebook|Menlo Park, CA|$110k - $140k|Join our frontend team to build amazing user experiences[JOB]', sender: 'ai', timestamp: new Date() }
  ]);
  
  const [inputText, setInputText] = createSignal('');
  const [isAiProcessing, setIsAiProcessing] = createSignal(false);
  const [browserActivity, setBrowserActivity] = createSignal<BrowserActivity[]>([]);
  const [isTimelineOpen, setIsTimelineOpen] = createSignal(false);

  // Auto-scroll to bottom when messages change
  const scrollToBottom = () => {
    if (messagesContainerRef) {
      messagesContainerRef.scrollTop = messagesContainerRef.scrollHeight;
    }
  };

  // Scroll to bottom on initial mount and when messages change
  onMount(() => {
    scrollToBottom();
  });

  // Create an effect that runs when messages change
  createEffect(() => {
    // This will run whenever messages() changes
    messages();
    // Use setTimeout to ensure DOM is updated before scrolling
    setTimeout(scrollToBottom, 0);
  });

  const handleSendMessage = () => {
    if (inputText().trim() === '') return;
    
    // Add user message
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: inputText(),
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages([...messages(), newUserMessage]);
    setInputText('');
    
    // Set AI processing state
    setIsAiProcessing(true);
    
    // Simulate browser activity
    setBrowserActivity([
      { id: '1', url: 'https://linkedin.com/jobs', title: 'LinkedIn Jobs', timestamp: new Date() },
      { id: '2', url: 'https://indeed.com/software-engineer', title: 'Indeed - Software Engineer Jobs', timestamp: new Date() }
    ]);
    
    // Simulate AI response after a delay
    setTimeout(() => {
      const newAiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'I found several software engineering positions in San Francisco. Would you like me to show you the **top 5 matches**?\n\n[JOB]Senior Software Engineer|Microsoft|Seattle, WA|$130k - $160k|Join our cloud team to build scalable distributed systems[JOB]\n\n[JOB]Full Stack Developer|Apple|Cupertino, CA|$125k - $155k|Work on our next generation products[JOB]',
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newAiMessage]);
      setIsAiProcessing(false);
      
      // Add more browser activity
      setBrowserActivity(prev => [
        ...prev,
        { id: '3', url: 'https://glassdoor.com/salaries', title: 'Glassdoor - Salary Comparison', timestamp: new Date() }
      ]);
    }, 3000);
  };

  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div class="container mx-auto px-4 py-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Chat Interface */}
        <div class="flex flex-col h-[calc(100vh-180px)]">
          <div 
            ref={messagesContainerRef}
            class="bg-base-200 rounded-lg p-4 flex-grow mb-4 overflow-y-auto"
            id="chat-messages-container"
          >
            {/* Welcome message when no messages */}
            {messages().length === 0 && (
              <div class="text-center py-10">
                <h2 class="text-2xl font-bold mb-2">AI Career Assistant</h2>
                <p class="text-base-content/70">Ask me anything about your job search, resume, or career advice</p>
              </div>
            )}
            
            {/* Chat messages */}
            <div class="space-y-4">
              <For each={messages()}>
                {(message) => (
                  <div class={`chat ${message.sender === 'user' ? 'chat-end' : 'chat-start'}`}>
                    {message.sender === 'ai' && (
                      <div class="chat-header text-xs opacity-50 mb-1">
                        <span class="font-bold">AI Assistant</span>
                        <span class="ml-2">{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                    )}
                    <div class={`chat-bubble ${message.sender === 'user' ? 'chat-bubble-primary' : ''}`}>
                      <div innerHTML={formatMessage(message.text)} />
                    </div>
                    {message.sender === 'user' && (
                      <div class="chat-header text-xs opacity-50 mt-1">
                        <span class="font-bold">You</span>
                        <span class="ml-2">{message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                    )}
                  </div>
                )}
              </For>
            </div>
            
            {/* Progress indicator when AI is processing */}
            {isAiProcessing() && (
              <div class="chat chat-start">
                <div class="chat-bubble">
                  <div class="flex items-center">
                    <span class="mr-2">Thinking</span>
                    <div class="flex space-x-1">
                      <div class="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                      <div class="w-2 h-2 bg-current rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Message Input Area */}
          <div class="bg-base-200 rounded-lg p-4">
            <div class="flex items-end space-x-2">
              <textarea 
                class="textarea textarea-bordered flex-grow" 
                placeholder="Type your message here..."
                rows={2}
                value={inputText()}
                onInput={(e) => setInputText(e.currentTarget.value)}
                onKeyDown={handleKeyPress}
              ></textarea>
              <button 
                class="btn btn-primary"
                onClick={handleSendMessage}
                disabled={isAiProcessing()}
              >
                {isAiProcessing() ? (
                  <>
                    <span class="loading loading-spinner loading-sm mr-1"></span>
                    Sending...
                  </>
                ) : (
                  'Send'
                )}
              </button>
            </div>
            <div class="flex items-center justify-between mt-2">
              <div class="flex items-center">
                <div class="badge badge-success gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                  </svg>
                  Connected
                </div>
                {/* Timeline button */}
                <button 
                  class="btn btn-ghost btn-xs ml-2"
                  onClick={() => setIsTimelineOpen(true)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Timeline
                </button>
              </div>
              <div class="text-sm text-base-content/50">
                AI Assistant v1.0
              </div>
            </div>
          </div>
        </div>
        
        {/* Right Panel - Browser Viewport */}
        <div class="flex flex-col h-[calc(100vh-180px)]">
          <div class="bg-base-200 rounded-lg p-4 flex-grow">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold">Browser Viewport</h3>
              <div class={`badge ${isAiProcessing() ? 'badge-warning' : 'badge-neutral'}`}>
                {isAiProcessing() ? 'Processing' : 'Idle'}
              </div>
            </div>
            
            <div class="bg-white rounded-lg border border-base-300 h-full overflow-y-auto">
              {browserActivity().length > 0 ? (
                <div class="p-4">
                  <div class="space-y-4">
                    <For each={browserActivity()}>
                      {(activity) => (
                        <div class="card bg-base-100 shadow-md">
                          <div class="card-body p-4">
                            <div class="flex items-start">
                              <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mr-3" />
                              <div class="flex-grow">
                                <h4 class="font-bold text-sm truncate">{activity.title}</h4>
                                <p class="text-xs text-base-content/70 truncate">{activity.url}</p>
                                <p class="text-xs text-base-content/50 mt-1">
                                  {activity.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </For>
                  </div>
                </div>
              ) : (
                <div class="flex items-center justify-center h-full">
                  <div class="text-center p-8">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-base-content/30 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9 3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                    <p class="text-base-content/50">AI browsing activity will appear here</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* Timeline Modal */}
      <TimelineModal 
        activities={sampleAIActivities}
        isOpen={isTimelineOpen()}
        onClose={() => setIsTimelineOpen(false)}
      />
    </div>
  );
};

export default AIChatView;