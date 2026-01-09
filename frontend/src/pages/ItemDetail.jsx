import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import ItemCard from '../components/ItemCard';
import { Star } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const ItemDetail = () => {
    const { id } = useParams();
    const [item, setItem] = useState(null);
    const [similar, setSimilar] = useState([]);
    const [userRating, setUserRating] = useState(0);
    const { user } = useAuth();

    useEffect(() => {
        fetchData();
    }, [id]);

    const fetchData = async () => {
        try {
            const itemRes = await api.get(`/items/${id}`);
            setItem(itemRes.data);

            const simRes = await api.get(`/recommendations/item/${id}`);
            setSimilar(simRes.data);

            setUserRating(0);
        } catch (err) {
            console.error(err);
        }
    };

    const handleRate = async (rating) => {
        setUserRating(rating);
        try {
            await api.post('/ratings', { item_id: item.id, rating });
        } catch (err) {
            console.error("Failed to rate");
        }
    };

    if (!item) return <div className="container" style={{ padding: '4rem' }}>Loading...</div>;

    return (
        <div className="container" style={{ padding: '3rem 1rem' }}>
            <div className="glass-panel" style={{ padding: '2.5rem', display: 'flex', gap: '3rem', flexWrap: 'wrap', alignItems: 'start' }}>
                <div style={{ width: '100%', maxWidth: '300px', borderRadius: '16px', overflow: 'hidden', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)', flexShrink: 0 }}>
                    {item.cover_image_url ? (
                        <img
                            src={item.cover_image_url}
                            alt={item.title}
                            style={{ width: '100%', height: 'auto', display: 'block' }}
                            onError={(e) => {
                                e.target.onerror = null;
                                e.target.src = `https://picsum.photos/seed/${item.id}/300/450`;
                            }}
                        />
                    ) : (
                        <div style={{ width: '100%', height: '400px', background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '4rem', opacity: 0.5 }}>{item.title[0]}</div>
                    )}
                </div>

                <div style={{ flex: 1, minWidth: '300px' }}>
                    <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '1.5rem' }}>
                        <span className={`badge ${item.type === 'book' ? 'badge-blue' : 'badge-purple'}`}>{item.type}</span>
                        <span className="badge badge-green">{item.availability_status}</span>
                    </div>

                    <h1 style={{ fontSize: '3rem', margin: '0 0 0.5rem 0', fontWeight: 800, color: '#334155' }}>{item.title}</h1>
                    <h3 style={{ fontSize: '1.25rem', color: '#64748b', fontWeight: 500, margin: '0 0 2rem 0' }}>
                        by {item.author_or_director} <span style={{ opacity: 0.5 }}>•</span> {item.year}
                    </h3>

                    <p style={{ lineHeight: 1.8, color: '#475569', marginBottom: '2.5rem', fontSize: '1.1rem' }}>{item.description}</p>

                    <div style={{ marginBottom: '2.5rem' }}>
                        <h4 style={{ marginBottom: '1rem', color: '#334155' }}>Genres</h4>
                        <div style={{ display: 'flex', gap: '0.75rem' }}>
                            {item.genres.split(',').map(g => (
                                <span key={g} style={{ background: 'white', border: '1px solid #e2e8f0', color: '#64748b', padding: '6px 14px', borderRadius: '99px', fontSize: '0.9rem', fontWeight: 500 }}>{g.trim()}</span>
                            ))}
                        </div>
                    </div>

                    {user && (
                        <div style={{ padding: '2rem', background: 'rgba(255,255,255,0.6)', borderRadius: '20px', border: '1px solid rgba(255,255,255,0.8)' }}>
                            <p style={{ margin: '0 0 1rem 0', fontWeight: 700, color: '#334155' }}>Rated by you:</p>
                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        onClick={() => handleRate(star)}
                                        style={{ background: 'none', border: 'none', cursor: 'pointer', transition: 'transform 0.1s' }}
                                        onMouseEnter={(e) => e.target.style.transform = 'scale(1.2)'}
                                        onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                                    >
                                        <Star fill={star <= userRating ? '#fbbf24' : '#e2e8f0'} color={star <= userRating ? '#fbbf24' : '#cbd5e1'} size={36} />
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <div style={{ marginTop: '5rem' }}>
                <h2 style={{ fontSize: '2rem', marginBottom: '2rem', color: '#334155', fontWeight: 700 }}>You Might Also Like</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '2rem' }}>
                    {similar.map(sim => <ItemCard key={sim.id} item={sim} />)}
                </div>
            </div>
        </div>
    );
};

export default ItemDetail;
