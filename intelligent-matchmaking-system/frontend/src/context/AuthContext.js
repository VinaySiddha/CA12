import React, { createContext, useContext, useReducer, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

// Configure axios defaults
axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
axios.defaults.headers.common['Content-Type'] = 'application/json';

const AuthContext = createContext();

// Initial state
const initialState = {
  isAuthenticated: false,
  user: null,
  token: localStorage.getItem('token'),
  loading: true,
  error: null,
};

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, loading: true, error: null };
    
    case 'AUTH_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        loading: false,
        error: null,
      };
    
    case 'AUTH_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        loading: false,
        error: action.payload,
      };
    
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        loading: false,
        error: null,
      };
    
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload },
      };
    
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    
    default:
      return state;
  }
};

// Axios interceptor setup
const setupAxiosInterceptors = (token, dispatch) => {
  // Request interceptor
  axios.interceptors.request.use(
    (config) => {
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        dispatch({ type: 'LOGOUT' });
        localStorage.removeItem('token');
        toast.error('Session expired. Please login again.');
      }
      return Promise.reject(error);
    }
  );
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Set up axios interceptors when token changes
  useEffect(() => {
    if (state.token) {
      setupAxiosInterceptors(state.token, dispatch);
      
      // Set up token auto-refresh
      const expiresAt = localStorage.getItem('expiresAt');
      if (expiresAt) {
        const expiryTime = parseInt(expiresAt, 10);
        const timeUntilRefresh = Math.max(expiryTime - new Date().getTime() - (5 * 60 * 1000), 0); // Refresh 5 minutes before expiry
        
        const refreshTimer = setTimeout(() => {
          refreshToken();
        }, timeUntilRefresh);
        
        return () => clearTimeout(refreshTimer);
      }
    }
  }, [state.token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('t oken');
      
      if (!token) {
        dispatch({ type: 'AUTH_FAILURE', payload: 'No token found' });
        return;
      }

      try {
        dispatch({ type: 'AUTH_START' });
        
        const response = await axios.get('/users/profile', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        dispatch({
          type: 'AUTH_SUCCESS',
          payload: {
            user: response.data,
            token: token,
          },
        });
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        dispatch({ type: 'AUTH_FAILURE', payload: 'Token validation failed' });
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (email, password) => {
    try {
      dispatch({ type: 'AUTH_START' });
      
      // Create form data for OAuth2PasswordRequestForm
      const formData = new FormData();
      formData.append('username', email); // Backend uses 'username' field for email
      formData.append('password', password);
      
      const response = await axios.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      const { access_token, token_type, user, expires_in } = response.data;
      console.log(response.data);
      
      // Store token first
      localStorage.setItem('token', access_token);
      
      // Store expiration time if provided
      if (expires_in) {
        const expiresAt = new Date().getTime() + expires_in * 1000;
        localStorage.setItem('expiresAt', expiresAt);
      }
      
      // Set axios default authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // If user data is included in response, use it directly
      let userData = user;
      
      // Otherwise fetch user data using the token
      if (!userData) {
        const userResponse = await axios.get('/auth/me');
        userData = userResponse.data;
      }
      
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: userData,
          token: access_token,
        },
      });
      
      // Personalized welcome message based on role
      const welcomeMessages = {
        student: `Welcome back, ${userData.full_name || userData.email}! Ready to continue learning?`,
        teacher: `Welcome back, Professor ${userData.full_name || userData.email}!`,
        admin: `Welcome back, Admin ${userData.full_name || userData.email}!`,
        mentor: `Welcome back, Mentor ${userData.full_name || userData.email}!`
      };
      
      toast.success(welcomeMessages[userData.role] || `Welcome back, ${userData.full_name || userData.email}!`);
      return { success: true };
      
    } catch (error) {
      console.error('Login error:', error);
      let message = 'Login failed';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle FastAPI validation errors
        if (Array.isArray(errorData.detail)) {
          message = errorData.detail.map(err => err.msg).join(', ');
        } else if (typeof errorData.detail === 'string') {
          message = errorData.detail;
        } else if (errorData.message) {
          message = errorData.message;
        }
      } else if (error.message) {
        message = error.message;
      }
      
      console.error('Login failed:', message);
      dispatch({ type: 'AUTH_FAILURE', payload: message });
      toast.error(message);
      return { success: false, error: message };
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      dispatch({ type: 'AUTH_START' });
      
      // Transform frontend data to match backend schema
      const registerData = {
        email: userData.email,
        username: userData.username || userData.email.split('@')[0], // Use email prefix as username if not provided
        full_name: userData.full_name,
        password: userData.password,
        confirm_password: userData.confirmPassword || userData.password, // Convert camelCase to snake_case
        role: userData.role || 'student',
        teaching_subjects: userData.teaching_subjects,
        years_experience: userData.years_experience ? parseInt(userData.years_experience) : null,
      };
      
      // Register the user
      const registerResponse = await axios.post('/auth/register', registerData);
      
      // Backend returns {message, user_id} but no token
      // So we need to log the user in after successful registration
      if (registerResponse.data.message) {
        // Auto-login after successful registration
        const loginResult = await login(userData.email, userData.password);
        
        if (loginResult.success) {
          toast.success(`Welcome to the platform, ${userData.full_name || userData.email}!`);
          return { success: true };
        } else {
          // Registration succeeded but auto-login failed
          toast.success('Registration successful! Please log in.');
          dispatch({ type: 'AUTH_FAILURE', payload: null });
          return { success: true, requiresLogin: true };
        }
      }
      
      throw new Error('Registration failed - no response from server');
      
    } catch (error) {
      console.error('Registration error:', error);
      let message = 'Registration failed';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle FastAPI validation errors
        if (Array.isArray(errorData.detail)) {
          message = errorData.detail.map(err => `${err.loc ? err.loc.join('.') + ': ' : ''}${err.msg}`).join(', ');
        } else if (typeof errorData.detail === 'string') {
          message = errorData.detail;
        } else if (errorData.message) {
          message = errorData.message;
        }
      } else if (error.message) {
        message = error.message;
      }
      
      dispatch({ type: 'AUTH_FAILURE', payload: message });
      toast.error(message);
      return { success: false, error: message };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // Optional: Call logout endpoint
      if (state.token) {
        await axios.post('/auth/logout');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      dispatch({ type: 'LOGOUT' });
      toast.success('Logged out successfully');
    }
  };

  // Update user profile
  const updateUser = async (updates) => {
    try {
      const response = await axios.put('/users/profile', updates);
      
      dispatch({ type: 'UPDATE_USER', payload: response.data });
      toast.success('Profile updated successfully');
      return { success: true, data: response.data };
      
    } catch (error) {
      console.error('Update user error:', error);
      let message = 'Update failed';
      
      if (error.response?.data) {
        const errorData = error.response.data;
        
        // Handle FastAPI validation errors
        if (Array.isArray(errorData.detail)) {
          message = errorData.detail.map(err => err.msg).join(', ');
        } else if (typeof errorData.detail === 'string') {
          message = errorData.detail;
        } else if (errorData.message) {
          message = errorData.message;
        }
      } else if (error.message) {
        message = error.message;
      }
      
      toast.error(message);
      return { success: false, error: message };
    }
  };

  // Refresh token
  const refreshToken = async () => {
    try {
      const response = await axios.post('/token/refresh');
      const { access_token, expires_in, user } = response.data;
      
      localStorage.setItem('token', access_token);
      
      // Update expiration time if provided
      if (expires_in) {
        const expiresAt = new Date().getTime() + expires_in * 1000;
        localStorage.setItem('expiresAt', expiresAt);
      }
      
      // Update user data if provided
      const userData = user || state.user;
      
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: userData,
          token: access_token,
        },
      });
      
      return { success: true };
      
    } catch (error) {
      console.error('Token refresh failed:', error);
      // Only logout if the error is unauthorized
      if (error.response?.status === 401) {
        dispatch({ type: 'LOGOUT' });
        localStorage.removeItem('token');
        localStorage.removeItem('expiresAt');
        toast.error('Your session has expired. Please login again.');
      }
      return { success: false };
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    refreshToken,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};