import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function runTestsWithTimeout() {
  try {
    // Run tests with a 5-minute timeout (300000 milliseconds)
    const { stdout, stderr } = await execAsync('npx playwright test', { 
      timeout: 300000,
      cwd: process.cwd()
    });
    
    console.log('Test output:', stdout);
    if (stderr) {
      console.error('Test errors:', stderr);
    }
  } catch (error) {
    if (error.killed) {
      console.error('Test execution was killed due to timeout');
    } else if (error.code === 1) {
      console.error('Tests failed');
    } else {
      console.error('Error running tests:', error.message);
    }
    process.exit(1);
  }
}

// Run the tests
runTestsWithTimeout();