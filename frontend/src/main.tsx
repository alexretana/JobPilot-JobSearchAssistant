/* @refresh reload */
import { render } from 'solid-js/web';
import './index.css';
import App from './App';

// Initialize theme from localStorage
try {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }
} catch (e) {
  console.warn('Failed to initialize theme from localStorage', e);
}

const root = document.getElementById('root');

if (!(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?'
  );
}

render(() => (
  <App />
), root!);
