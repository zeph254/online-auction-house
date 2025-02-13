import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Profile = () => {
    const { user, logout } = useUser();
    const [editMode, setEditMode] = useState(false);
    const [name, setName] = useState(user.name);
    const [email, setEmail] = useState(user.email);
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    // Handle account deletion
    const handleDeleteAccount = async () => {
        if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            try {
                await axios.delete(`http://localhost:5000/api/user/delete/${user.user_id}`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
                });
                logout();
                navigate('/login');
            } catch (err) {
                setError('Failed to delete account. Please try again.');
            }
        }
    };

    // Handle profile update
    const handleUpdateProfile = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.patch(`http://localhost:5000/api/user/update/${user.user_id}`, {
                name,
                email,
                password,
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
            });
            if (response.data.message) {
                setSuccess('Profile updated successfully!');
                setError('');
                setEditMode(false);
            }
        } catch (err) {
            setError('Failed to update profile. Please try again.');
        }
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Your Profile</h1>
            <div className="card p-4">
                {error && <div className="alert alert-danger">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}

                {editMode ? (
                    <form onSubmit={handleUpdateProfile}>
                        <div className="mb-3">
                            <label htmlFor="name" className="form-label">Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Email</label>
                            <input
                                type="email"
                                className="form-control"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="password" className="form-label">New Password (leave blank to keep current)</label>
                            <input
                                type="password"
                                className="form-control"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <button type="submit" className="btn btn-primary me-2">Save Changes</button>
                        <button type="button" className="btn btn-secondary" onClick={() => setEditMode(false)}>Cancel</button>
                    </form>
                ) : (
                    <>
                        <p><strong>Name:</strong> {user.name}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>Role:</strong> {user.role}</p>
                        <button className="btn btn-primary me-2" onClick={() => setEditMode(true)}>Edit Profile</button>
                        <button className="btn btn-danger" onClick={handleDeleteAccount}>Delete Account</button>
                    </>
                )}
            </div>
        </div>
    );
};

export default Profile;