import React from 'react';
import { Link } from 'react-router-dom';
import { Star } from 'lucide-react';

const ItemCard = ({ item }) => {
    return (
        <Link to={`/items/${item.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="glass-panel card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <div style={{ height: '280px', background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#cbd5e1', overflow: 'hidden' }}>
                    {item.cover_image_url ? (
                        <img
                            src={item.cover_image_url}
                            alt={item.title}
                            style={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.5s' }}
                            className="card-img"
                            onError={(e) => {
                                e.target.onerror = null;
                                // Fallback to a unique random aesthetic image based on ID
                                e.target.src = `https://picsum.photos/seed/${item.id}/300/450`;
                            }}
                        />
                    ) : (
                        <span style={{ fontSize: '3rem', fontWeight: 'bold', opacity: 0.5 }}>{item.title[0]}</span>
                    )}
                </div>
                <div style={{ padding: '1.25rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                        <h3 style={{ margin: 0, fontSize: '1.15rem', fontWeight: 600, color: '#334155' }}>{item.title}</h3>
                    </div>
                    <div style={{ marginBottom: '0.75rem' }}>
                        <span className={`badge ${item.type === 'book' ? 'badge-blue' : 'badge-purple'}`}>
                            {item.type}
                        </span>
                    </div>
                    <p style={{ margin: 0, color: '#64748b', fontSize: '0.9rem', marginBottom: '1rem' }}>{item.author_or_director}</p>
                    <div style={{ marginTop: 'auto', display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                        {item.genres.split(',').slice(0, 2).map(g => (
                            <span key={g} style={{ fontSize: '0.75rem', color: '#64748b', background: '#f1f5f9', padding: '4px 8px', borderRadius: '6px' }}>
                                {g.trim()}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </Link>
    );
};

export default ItemCard;
