import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Book, LogOut, Search, User, Shield } from 'lucide-react';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="glass-panel" style={{ borderRadius: 0, borderTop: 0, borderLeft: 0, borderRight: 0, position: 'sticky', top: 0, zIndex: 100, background: 'rgba(255,255,255,0.8)' }}>
            <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '80px' }}>
                <Link to="/" className="gradient-text" style={{ fontSize: '1.8rem', fontWeight: '800', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.75rem', letterSpacing: '-0.02em' }}>
                    <Book size={28} color="#db2777" />
                    MoodSync
                </Link>

                {user && (
                    <div style={{ display: 'flex', gap: '2.5rem', alignItems: 'center' }}>
                        <Link to="/" style={{ color: '#64748b', textDecoration: 'none', fontWeight: 600, fontSize: '0.95rem' }}>Dashboard</Link>
                        <Link to="/catalog" style={{ color: '#64748b', textDecoration: 'none', fontWeight: 600, fontSize: '0.95rem' }}>Catalog</Link>
                        {user.role === 'admin' && (
                            <Link to="/admin" style={{ color: '#06b6d4', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.95rem' }}>
                                <Shield size={16} /> Admin
                            </Link>
                        )}
                    </div>
                )}

                <div style={{ display: 'flex', gap: '1rem' }}>
                    {user ? (
                        <button onClick={handleLogout} className="btn btn-secondary" style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}>
                            <LogOut size={18} /> Logout
                        </button>
                    ) : (
                        <Link to="/login" className="btn btn-primary">Login</Link>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
