/* @refresh reload */
import { render } from 'solid-js/web';
import './index.css';
import App from './App';

// Set default theme to business
document.documentElement.setAttribute('data-theme', 'business');

// Don't initialize development authentication - use real authentication flow
console.log('Authentication will be handled through login flow');

const root = document.getElementById('root');

if (!(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?'
  );
}

render(() => (
  <App />
), root!);
