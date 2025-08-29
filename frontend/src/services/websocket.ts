// Simple WebSocket service mock
export const webSocketService = {
  connect: () => {
    console.log('WebSocket connected');
  },
  disconnect: () => {
    console.log('WebSocket disconnected');
  },
  sendMessage: (message: any) => {
    console.log('WebSocket message sent:', message);
  },
  onMessage: (callback: (message: any) => void) => {
    console.log('WebSocket message handler registered');
  }
};