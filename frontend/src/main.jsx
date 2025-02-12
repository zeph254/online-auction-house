import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';  // ✅ Import BrowserRouter
import "bootstrap/dist/css/bootstrap.min.css";
import './index.css';
import App from './App.jsx';
import { UserProvider } from './context/UserContext.jsx';
import { ItemProvider } from './context/ItemContext.jsx'; // ✅ Import ItemProvider
import { BidProvider } from './context/BidContext.jsx'; // ✅ Import BidProvider

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter> {/* ✅ Wrap everything inside BrowserRouter */}
      <UserProvider>
        <ItemProvider>
          <BidProvider>
            <App />
          </BidProvider>
        </ItemProvider>
      </UserProvider>
    </BrowserRouter>
  </StrictMode>,
);
