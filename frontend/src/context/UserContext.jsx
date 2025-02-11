import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Create the UserContext
const UserContext = createContext();

// Create a custom hook to use the UserContext
export const useUser = () => useContext(UserContext);

// Create the UserProvider component
export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null); // Store user details
    const [isAuthenticated, setIsAuthenticated] = useState(false); // Track authentication status
    const navigate = useNavigate();

    // Check if the user is already logged in (e.g., from localStorage or session)
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
            setIsAuthenticated(true);
        }
    }, []);

    // Login function
    const login = async (email, password) => {
        try {
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                throw new Error('Invalid email or password');
            }

            const data = await response.json();
            setUser(data.user);
            setIsAuthenticated(true);
            localStorage.setItem('user', JSON.stringify(data.user)); // Store user in localStorage
            navigate('/'); // Redirect to home page after login
        } catch (error) {
            console.error('Login failed:', error);
            alert('Login failed. Please check your credentials.');
        }
    };

    // Logout function
    const logout = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/auth/logout', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Logout failed');
            }

            setUser(null);
            setIsAuthenticated(false);
            localStorage.removeItem('user'); // Remove user from localStorage
            navigate('/login'); // Redirect to login page after logout
        } catch (error) {
            console.error('Logout failed:', error);
            alert('Logout failed. Please try again.');
        }
    };

    // Register function
    const register = async (name, email, password) => {
        try {
            const response = await fetch('http://localhost:5000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',  // ✅ Ensure cookies & authentication tokens are sent
                body: JSON.stringify({ name, email, password }),
            });
    
            if (!response.ok) {
                throw new Error('Registration failed');
            }
    
            const data = await response.json();
            setUser(data.user);
            setIsAuthenticated(true);
            localStorage.setItem('user', JSON.stringify(data.user));
            navigate('/');
        } catch (error) {
            console.error('Registration failed:', error);
            alert('Registration failed. Please try again.');
        }
    };
    
    

    // Provide the context value
    const value = {
        user,
        isAuthenticated,
        login,
        logout,
        register,
    };

    return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};