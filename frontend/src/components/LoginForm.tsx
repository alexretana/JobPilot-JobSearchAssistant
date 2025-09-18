import type { Component } from 'solid-js';
import { createSignal } from 'solid-js';
import { AuthService, LoginCredentials } from '../services/AuthService';

interface LoginFormProps {
  onLoginSuccess: () => void;
  onSwitchToRegister: () => void;
}

const LoginForm: Component<LoginFormProps> = (props) => {
  const [email, setEmail] = createSignal('');
  const [password, setPassword] = createSignal('');
  const [error, setError] = createSignal('');
  const [loading, setLoading] = createSignal(false);

  const authService = new AuthService();

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const credentials: LoginCredentials = {
        email: email(),
        password: password()
      };

      const response = await authService.login(credentials);
      console.log('Login successful:', response);
      props.onLoginSuccess();
    } catch (err) {
      console.error('Login failed:', err);
      setError('Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="flex items-center justify-center min-h-screen bg-base-200">
      <div class="card w-full max-w-md shadow-2xl bg-base-100">
        <div class="card-body">
          <h2 class="card-title text-center">Login to JobPilot</h2>
          <form onSubmit={handleSubmit}>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Email</span>
              </label>
              <input
                type="email"
                placeholder="email@example.com"
                class="input input-bordered"
                value={email()}
                onInput={(e) => setEmail(e.currentTarget.value)}
                required
              />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Password</span>
              </label>
              <input
                type="password"
                placeholder="password"
                class="input input-bordered"
                value={password()}
                onInput={(e) => setPassword(e.currentTarget.value)}
                required
              />
            </div>
            {error() && (
              <div class="alert alert-error mt-4">
                <span>{error()}</span>
              </div>
            )}
            <div class="form-control mt-6">
              <button 
                type="submit" 
                class={`btn btn-primary ${loading() ? 'loading' : ''}`}
                disabled={loading()}
              >
                {loading() ? 'Logging in...' : 'Login'}
              </button>
            </div>
          </form>
          <div class="divider">OR</div>
          <p class="text-center">
            Don't have an account?{' '}
            <button onClick={props.onSwitchToRegister} class="link link-primary">
              Register here
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;