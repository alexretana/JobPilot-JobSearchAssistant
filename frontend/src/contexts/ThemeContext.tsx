import { createContext, createSignal, onMount, useContext, JSX } from 'solid-js';

interface Theme {
  name: string;
  label: string;
}

interface ThemeContextType {
  currentTheme: () => string;
  changeTheme: (theme: string) => void;
  themes: Theme[];
}

const themes: Theme[] = [
  { name: 'business', label: 'Business' },
  { name: 'dark', label: 'Dark' },
  { name: 'dim', label: 'Dim' },
  { name: 'emerald', label: 'Emerald' },
  { name: 'lemonade', label: 'Lemonade' },
  { name: 'nord', label: 'Nord' },
];

const ThemeContext = createContext<ThemeContextType>();

export const ThemeProvider = (props: { children: JSX.Element }) => {
  const [currentTheme, setCurrentTheme] = createSignal('business');

  const changeTheme = (theme: string) => {
    // Validate theme is in available themes
    const isValidTheme = themes.some(t => t.name === theme);
    if (isValidTheme) {
      setCurrentTheme(theme);
      // Save to localStorage
      localStorage.setItem('jobpilot-theme', theme);
      // Update the DOM directly
      document.documentElement.setAttribute('data-theme', theme);
    }
  };

  // Load saved theme on mount
  onMount(() => {
    const savedTheme = localStorage.getItem('jobpilot-theme') || 'business';
    // Validate theme is in available themes
    const isValidTheme = themes.some(t => t.name === savedTheme);
    if (isValidTheme) {
      setCurrentTheme(savedTheme);
      // Make sure the DOM is updated with the saved theme
      document.documentElement.setAttribute('data-theme', savedTheme);
    }
  });

  return (
    <ThemeContext.Provider value={{ currentTheme, changeTheme, themes }}>
      {props.children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};