export default function Footer() {
    return (
        <footer className="auction-footer">
    <div className="footer-container">
        <div className="footer-left">
            <h2>Online Auction House</h2>
            <p>Bringing transparency, efficiency, and security to online auctions.</p>
        </div>
        <div className="footer-center">
            <h3>Quick Links</h3>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">Auctions</a></li>
                <li><a href="#">About Us</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>
        <div className="footer-right">
            <h3>Follow Us</h3>
            <div className="social-icons">
                <a href="#"><i className="fab fa-facebook"></i></a>
                <a href="#"><i className="fab fa-twitter"></i></a>
                <a href="#"><i className="fab fa-instagram"></i></a>
                <a href="#"><i className="fab fa-linkedin"></i></a>
            </div>
        </div>
    </div>
    <div className="footer-bottom">
        <p>&copy; 2025 Online Auction House. All rights reserved.</p>
    </div>
</footer>

    );
}