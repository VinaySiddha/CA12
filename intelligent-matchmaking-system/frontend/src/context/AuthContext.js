import React, { createContext, useContext, useReducer, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

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
    }
  }, [state.token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
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
      
      const { access_token, token_type } = response.data;
      
      // Store token first
      localStorage.setItem('token', access_token);
      
      // Set axios default authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Fetch user data using the token
      const userResponse = await axios.get('/auth/me');
      const user = userResponse.data;
      
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user,
          token: access_token,
        },
      });
      
      toast.success(`Welcome back, ${user.full_name || user.email}!`);
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
      
      dispatch({ type: 'AUTH_FAILURE', payload: message });
      toast.error(message);
      return { success: false, error: message };
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      dispatch({ type: 'AUTH_START' });
      
      const response = await axios.post('/auth/register', userData);
      
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user,
          token: access_token,
        },
      });
      
      toast.success(`Welcome to the platform, ${user.profile?.full_name || user.email}!`);
      return { success: true };
      
    } catch (error) {
      console.error('Registration error:', error);
      let message = 'Registration failed';
      
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
      const response = await axios.post('/auth/refresh');
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user: state.user,
          token: access_token,
        },
      });
      
      return { success: true };
      
    } catch (error) {
      dispatch({ type: 'LOGOUT' });
      localStorage.removeItem('token');
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