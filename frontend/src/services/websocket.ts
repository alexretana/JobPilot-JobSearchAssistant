// Simple WebSocket service mock with SolidJS reactivity
import { createSignal } from 'solid-js';

export const webSocketService = (() => {
  const [isConnected, setIsConnected] = createSignal(false);
  let messageHandlers: Array<(message: any) => void> = [];
  
  return {
    connect: () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    },
    disconnect: () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    },
    sendMessage: (message: any) => {
      console.log('WebSocket message sent:', message);
    },
    onMessage: (callback: (message: any) => void) => {
      console.log('WebSocket message handler registered');
    },
    getIsConnected: () => {
      return isConnected;
    },
    addMessageHandler: (handler: (message: any) => void) => {
      messageHandlers.push(handler);
      console.log('Message handler added');
      
      // Return a function to remove the handler
      return () => {
        const index = messageHandlers.indexOf(handler);
        if (index > -1) {
          messageHandlers.splice(index, 1);
          console.log('Message handler removed');
        }
      };
    }
  };
})();