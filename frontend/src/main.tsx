import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import './app.css';
import Home from './pages/Home';
import Browse from './pages/Browse';
import ProductPage from './pages/ProductPage';

function Layout() {
    return (
        <div className="max-w-6xl mx-auto p-4">
            <header className="flex items-center justify-between mb-6">
                <Link to="/" className="text-xl font-semibold">
                    GNN Reco
                </Link>
                <nav className="flex gap-4 text-sm">
                    <Link to="/">Home</Link>
                    <Link to="/browse">Browse</Link>
                </nav>
            </header>

            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/browse" element={<Browse />} />
                <Route path="/product/:id" element={<ProductPage />} />
            </Routes>
        </div>
    );
}

createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <Layout />
        </BrowserRouter>
    </React.StrictMode>
);
