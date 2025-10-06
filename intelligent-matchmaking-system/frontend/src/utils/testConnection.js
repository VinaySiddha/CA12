import axios from 'axios';

// Test function to verify API connectivity
export const testBackendConnection = async () => {
  try {
    console.log('Testing backend connection...');
    
    // Test basic health endpoint through proxy
    const response = await axios.get('/api/v1/health', {
      timeout: 5000
    });
    
    console.log('✅ Backend connection successful!');
    console.log('Status:', response.status);
    console.log('Data:', response.data);
    return true;
    
  } catch (error) {
    console.error('❌ Backend connection failed:');
    console.error('Error:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      console.error('Backend server is not running on port 8000');
      console.error('Please start the backend server: cd backend && python -m uvicorn app.main:app --reload');
    }
    
    return false;
  }
};

// Test auth endpoint
export const testAuthEndpoint = async () => {
  try {
    console.log('Testing auth endpoint...');
    
    const response = await axios.get('/api/v1/auth/me', {
      timeout: 5000
    });
    
    console.log('Auth endpoint response:', response.status);
    return true;
    
  } catch (error) {
    if (error.response?.status === 401) {
      console.log('✅ Auth endpoint working (401 expected without token)');
      return true;
    }
    
    console.error('❌ Auth endpoint failed:', error.message);
    return false;
  }
};

// Run tests
export const runConnectivityTests = async () => {
  console.log('🚀 Running connectivity tests...');
  
  const healthTest = await testBackendConnection();
  const authTest = await testAuthEndpoint();
  
  if (healthTest && authTest) {
    console.log('🎉 All connectivity tests passed!');
    console.log('Frontend can successfully communicate with backend');
  } else {
    console.log('⚠️ Some connectivity tests failed');
    console.log('Check if backend server is running on port 8000');
  }
  
  return healthTest && authTest;
};

export default { testBackendConnection, testAuthEndpoint, runConnectivityTests };