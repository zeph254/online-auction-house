import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Create UserContext
export const UserContext = createContext();

// Custom hook to use UserContext
export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error("useUser must be used within a UserProvider");
    }
    return context;
};

// Detect if localStorage is allowed
const isStorageAvailable = (() => {
    try {
        localStorage.setItem('__test__', 'test');
        localStorage.removeItem('__test__');
        return true;
    } catch (e) {
        return false;
    }
})();

const storage = isStorageAvailable ? localStorage : sessionStorage; // Use sessionStorage as a fallback

// UserProvider component
export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    // Check storage for user data on component mount
    useEffect(() => {
        const storedUser = storage.getItem('user');
        const token = storage.getItem('token');

        if (storedUser && token) {
            try {
                const parsedUser = JSON.parse(storedUser);
                if (parsedUser?.user_id) {
                    setUser(parsedUser);
                    setIsAuthenticated(true);
                } else {
                    throw new Error("Invalid user data");
                }
            } catch (error) {
                console.error("Error parsing user data:", error);
                storage.removeItem('user');
                storage.removeItem('token');
            }
        }
    }, []);

    // Clear user data from state and storage
    const clearUserData = () => {
        setUser(null);
        setIsAuthenticated(false);
        storage.removeItem('user');
        storage.removeItem('token');
    };

    // Login function
    const login = async (email, password) => {
        try {
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
    
            const textResponse = await response.text(); // Read raw response
            console.log("Raw Server Response:", textResponse);
    
            const data = JSON.parse(textResponse); // Try parsing JSON
    
            if (!data.access_token) {
                throw new Error('Invalid response from server');
            }
    
            // Fetch user data using the access token
            const userResponse = await fetch('http://localhost:5000/api/auth/current_user', {
                method: 'GET',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${data.access_token}`
                }
            });
    
            const userData = await userResponse.json();
    
            if (!userData.user_id) {
                throw new Error('Invalid user data');
            }
    
            storage.setItem('user', JSON.stringify(userData));
            storage.setItem('token', data.access_token);
    
            setUser(userData);
            setIsAuthenticated(true);
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            alert(error.message || 'Login failed. Please check your credentials.');
            return false;
        }
    };

    // Logout function
    const logout = async () => {
        try {
            const token = storage.getItem('token');
            if (!token) {
                clearUserData();
                navigate('/login');
                return;
            }

            const response = await fetch('http://localhost:5000/api/auth/logout', {
                method: 'DELETE',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Logout failed');
            }

            clearUserData();
            navigate('/login');
            return true;
        } catch (error) {
            console.error('Logout failed:', error);
            alert('Logout failed. Please try again.');
            return false;
        }
    };

    return (
        <UserContext.Provider value={{ user, isAuthenticated, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};
