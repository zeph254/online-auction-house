import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext"; // Import useUser hook

export default function Navbar() {
    const { user, isAuthenticated, logout } = useUser(); // Get user and logout function

    return (
        <nav className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
               <img className = "auction-logo"src="data:image/jpeg;base64,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" alt="" />   
          <a className="navbar-brand" href="#">AUCTIGON</a>
                <Link to="/" className="navbar-brand">AUCTIGON</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <Link to="/" className="nav-link active" aria-current="page">Home</Link>
                        </li>
                        {isAuthenticated && (
                            <li className="nav-item">
                                <Link to="/dashboard" className="nav-link">Dashboard</Link>
                            </li>
                        )}
                        {!isAuthenticated && (
                            <>
                                <li className="nav-item">
                                    <Link to="/login" className="nav-link">Login</Link>
                                </li>
                                <li className="nav-item">
                                    <Link to="/register" className="nav-link">Register</Link>
                                </li>
                            </>
                        )}
                        {isAuthenticated && (
                            <>
                                <li className="nav-item">
                                    <Link to="/profile" className="nav-link">Profile</Link>
                                </li>
                                <li className="nav-item">
    <button 
        className="btn btn-danger btn-sm ms-3" 
        onClick={async () => {
            const success = await logout();
            if (success) {
                navigate('/login'); // Ensure navigation happens after logout
            }
        }}
    >
        Logout
    </button>
</li>


                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
}