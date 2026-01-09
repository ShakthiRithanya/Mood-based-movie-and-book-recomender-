import React, { useEffect, useState } from 'react';
import api from '../api';
import ItemCard from '../components/ItemCard';
import MoodSelector from '../components/MoodSelector';

const Dashboard = () => {
    const [recs, setRecs] = useState([]);
    const [moodRecs, setMoodRecs] = useState([]);
    const [selectedMood, setSelectedMood] = useState('Happy'); // Default
    const [popular, setPopular] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const recRes = await api.get('/recommendations/user');
                setRecs(recRes.data);

                const allRes = await api.get('/items?limit=10');
                setPopular(allRes.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchMood = async () => {
            if (!selectedMood) return;
            try {
                const res = await api.get(`/recommendations/mood?mood=${selectedMood}`);
                setMoodRecs(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchMood();
    }, [selectedMood]);

    // Dynamic background images based on mood
    const moodBackgrounds = {
        'Happy': 'url("https://images.unsplash.com/photo-1493246507139-91e8fad9978e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")', // Sunny landscape/flowers
        'Sad': 'url("https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")',   // Rain details
        'Excited': 'url("https://images.unsplash.com/photo-1504609773096-104ff2c73ba4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")', // Sparks/Fireworks
        'Chill': 'url("https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")',   // Calm nature
        'Scared': 'url("https://images.unsplash.com/photo-1509248961158-e54f6934749c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")',  // Foggy dark forest
        'Inspired': 'url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")',// Space/Galaxy
    };

    const currentBg = selectedMood ? moodBackgrounds[selectedMood] : 'none';

    return (
        <div style={{
            minHeight: '100vh',
            backgroundImage: currentBg,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundAttachment: 'fixed',
            transition: 'background-image 0.5s ease-in-out',
            paddingBottom: '4rem',
            position: 'relative'
        }}>
            {/* Overlay for readability */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: selectedMood === 'Scared' || selectedMood === 'Inspired' ? 'rgba(15, 23, 42, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                zIndex: 0,
                pointerEvents: 'none'
            }}></div>

            <div className="container" style={{ position: 'relative', zIndex: 1 }}>
                <header style={{ padding: '6rem 0 4rem 0', textAlign: 'center' }}>
                    <h1 className="gradient-text" style={{ fontSize: '3.5rem', margin: 0, fontWeight: 800, letterSpacing: '-0.03em' }}>
                        How are you feeling?
                    </h1>
                    <p style={{ color: '#64748b', fontSize: '1.25rem', marginTop: '1rem', maxWidth: '600px', margin: '1rem auto' }}>
                        Select your current mood and we'll find the perfect story for you.
                    </p>

                    <MoodSelector onSelect={setSelectedMood} selectedMood={selectedMood} />
                </header>

                {selectedMood && (
                    <section style={{ marginBottom: '5rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                            <h2 style={{ fontSize: '2rem', margin: 0, color: '#334155' }}>Top picks for "{selectedMood}"</h2>
                            <div style={{ flex: 1, height: '1px', background: 'linear-gradient(90deg, #e2e8f0, transparent)' }}></div>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '2rem' }}>
                            {moodRecs.length > 0 ? (
                                moodRecs.map(item => <ItemCard key={item.id} item={item} />)
                            ) : (
                                <p style={{ color: 'var(--text-secondary)' }}>No specific items found for this mood.</p>
                            )}
                        </div>
                    </section>
                )}

                {recs.length > 0 && (
                    <section style={{ marginBottom: '5rem' }}>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', color: '#64748b', fontWeight: 600 }}>Because you rated highly</h2>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '2rem' }}>
                            {recs.map(item => <ItemCard key={item.id} item={item} />)}
                        </div>
                    </section>
                )}

                <section>
                    <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', color: '#64748b', fontWeight: 600 }}>Discover Library</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '2rem' }}>
                        {popular.map(item => <ItemCard key={item.id} item={item} />)}
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Dashboard;
