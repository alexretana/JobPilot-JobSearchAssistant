// Utility function to format messages with markdown-like syntax
export const formatMessage = (text: string): string => {
  // Convert markdown-like bold syntax (**text**) to HTML
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // Convert markdown-like italic syntax (*text*) to HTML
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // Convert markdown-like code syntax (`code`) to HTML
  text = text.replace(/`(.*?)`/g, '<code class="bg-base-200 px-1 rounded">$1</code>');
  
  // Convert markdown-like headers (# Header) to HTML
  text = text.replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-2 mb-1">$1</h1>');
  text = text.replace(/^## (.*$)/gm, '<h2 class="text-xl font-bold mt-2 mb-1">$1</h2>');
  text = text.replace(/^### (.*$)/gm, '<h3 class="text-lg font-bold mt-2 mb-1">$1</h3>');
  
  // Convert markdown-like bullet points (* item) to HTML
  text = text.replace(/^\* (.*$)/gm, '<li class="ml-4">$1</li>');
  text = text.replace(/(<li.*<\/li>\n?)+/gs, '<ul class="list-disc my-2">$&</ul>');
  
  // Handle job listings with special formatting
  // Format: [JOB]Job Title|Company|Location|Salary|Description[JOB]
  text = text.replace(
    /\[JOB\](.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\[JOB\]/g,
    (_, title, company, location, salary, description) => `
      <div class="card bg-base-100 shadow-lg my-2">
        <div class="card-body p-4">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-bold text-lg">${title}</h4>
              <div class="text-sm opacity-70">${company} • ${location}</div>
            </div>
            <div class="badge badge-primary">${salary}</div>
          </div>
          <p class="my-2 text-sm">${description}</p>
          <div class="card-actions justify-end">
            <button class="btn btn-xs btn-outline">Save</button>
            <button class="btn btn-xs btn-primary">Apply</button>
          </div>
        </div>
      </div>
    `
  );
  
  // Convert line breaks to <br> tags
  text = text.replace(/\n/g, '<br>');
  
  return text;
};