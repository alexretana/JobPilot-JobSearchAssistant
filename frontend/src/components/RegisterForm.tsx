import type { Component } from 'solid-js';
import { createSignal } from 'solid-js';
import { AuthService, RegisterData } from '../services/AuthService';

interface RegisterFormProps {
  onRegisterSuccess: () => void;
  onSwitchToLogin: () => void;
}

const RegisterForm: Component<RegisterFormProps> = (props) => {
  const [email, setEmail] = createSignal('');
  const [password, setPassword] = createSignal('');
  const [firstName, setFirstName] = createSignal('');
  const [lastName, setLastName] = createSignal('');
  const [error, setError] = createSignal('');
  const [loading, setLoading] = createSignal(false);

  const authService = new AuthService();

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const userData: RegisterData = {
        email: email(),
        password: password(),
        first_name: firstName(),
        last_name: lastName()
      };

      const response = await authService.register(userData);
      console.log('Registration successful:', response);
      props.onRegisterSuccess();
    } catch (err) {
      console.error('Registration failed:', err);
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="flex items-center justify-center min-h-screen bg-base-200">
      <div class="card w-full max-w-md shadow-2xl bg-base-100">
        <div class="card-body">
          <h2 class="card-title text-center">Register for JobPilot</h2>
          <form onSubmit={handleSubmit}>
            <div class="form-control">
              <label class="label">
                <span class="label-text">First Name</span>
              </label>
              <input
                type="text"
                placeholder="First Name"
                class="input input-bordered"
                value={firstName()}
                onInput={(e) => setFirstName(e.currentTarget.value)}
                required
              />
            </div>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Last Name</span>
              </label>
              <input
                type="text"
                placeholder="Last Name"
                class="input input-bordered"
                value={lastName()}
                onInput={(e) => setLastName(e.currentTarget.value)}
                required
              />
            </div>
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
                {loading() ? 'Registering...' : 'Register'}
              </button>
            </div>
          </form>
          <div class="divider">OR</div>
          <p class="text-center">
            Already have an account?{' '}
            <button onClick={props.onSwitchToLogin} class="link link-primary">
              Login here
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;