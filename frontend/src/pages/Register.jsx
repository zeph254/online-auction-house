import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Register() {
    const navigate = useNavigate();

    return (
        <div className="card">
            <div className="card-info">
                <form>
                    <h2 className="title">Sign Up</h2>
                    <div className="mb-3">
                        <label htmlFor="name" className="form-label">Name</label>
                        <input type="name" className="form-control" id="name" required />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">Email Address</label>
                        <input type="email" className="form-control" id="email" required />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input type="password" className="form-control" id="password" required />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                        <input type="password" className="form-control" id="confirmPassword" required />
                    </div>
                    <button type="submit" className="btn btn-primary">Sign Up</button>
                    <p className="toggle-text" onClick={() => navigate('/login')}>
                        Already have an account? Login
                    </p>
                </form>
            </div>
        </div>
    );
}
