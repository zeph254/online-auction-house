import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const navigate = useNavigate();

    return (
        <div className="card">
            <div className="card-info">
                <form>
                    <h2 className="title">Login</h2>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email Address</label>
                        <input type="email" className="form-control" id="email" required />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input type="password" className="form-control" id="password" required />
                    </div>
                    <button type="submit" className="btn btn-primary">Login</button>
                    <p className="toggle-text" onClick={() => navigate('/register')}>
                        Don't have an account? Sign Up
                    </p>
                </form>
            </div>
        </div>
    );
}
