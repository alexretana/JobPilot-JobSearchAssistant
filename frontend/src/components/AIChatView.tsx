import type { Component } from 'solid-js';

const AIChatView: Component = () => {
  return (
    <div class="container mx-auto px-4 py-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Chat Interface */}
        <div class="flex flex-col h-[calc(100vh-180px)]">
          <div class="bg-base-200 rounded-lg p-4 flex-grow mb-4 overflow-y-auto">
            <div class="text-center py-10">
              <h2 class="text-2xl font-bold mb-2">AI Career Assistant</h2>
              <p class="text-base-content/70">Ask me anything about your job search, resume, or career advice</p>
            </div>
            
            {/* Sample chat messages */}
            <div class="space-y-4">
              <div class="chat chat-start">
                <div class="chat-bubble">Hi there! I'm your AI career assistant. How can I help you today?</div>
              </div>
              <div class="chat chat-end">
                <div class="chat-bubble">Can you help me find software engineering jobs in San Francisco?</div>
              </div>
              <div class="chat chat-start">
                <div class="chat-bubble">Of course! I can search for software engineering positions in San Francisco. Would you like me to include remote opportunities as well?</div>
              </div>
            </div>
          </div>
          
          {/* Message Input Area */}
          <div class="bg-base-200 rounded-lg p-4">
            <div class="flex items-end space-x-2">
              <textarea 
                class="textarea textarea-bordered flex-grow" 
                placeholder="Type your message here..."
                rows={2}
              ></textarea>
              <button class="btn btn-primary">
                Send
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
              <div class="badge badge-neutral">Idle</div>
            </div>
            
            <div class="bg-white rounded-lg border border-base-300 h-full flex items-center justify-center">
              <div class="text-center p-8">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-base-content/30 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <p class="text-base-content/50">AI browsing activity will appear here</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChatView;