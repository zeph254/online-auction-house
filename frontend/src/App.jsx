import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Contact from "./pages/Contact";
import NoPage from "./pages/NoPage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AboutUs from './pages/AboutUs';
import PlaceBid from './pages/PlaceBid';
import Profile from './pages/Profile';
import AddAuctionItem from './pages/AddAuctionItem';
import AdminDashboard from './pages/AdminDashboard';
import AuctionListing from './pages/AuctionListing';
import AuctionDetails from './pages/AuctionDetails';
import AuctionResults from './pages/AuctionResults';

export default function App() {
  return (
    <Routes> {/* ✅ No extra <BrowserRouter> */}
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="contact" element={<Contact />} />
        <Route path="register" element={<Register />} />
        <Route path="*" element={<NoPage />} />
        <Route path="login" element={<Login />} />
        <Route path="aboutus" element={<AboutUs />} />
        <Route path="addauctionitem" element={<AddAuctionItem />} />
        <Route path="auctionlisting/:id" element={<AuctionListing />} />
        <Route path="admindashboard" element={<AdminDashboard />} />
        <Route path="auctiondetails/:id" element={<AuctionDetails />} />
        <Route path="auctionresults" element={<AuctionResults />} />
        <Route path="placebid/:id" element={<PlaceBid />} />
        <Route path="profile" element={<Profile />} />
      </Route>
    </Routes>
  );
}
