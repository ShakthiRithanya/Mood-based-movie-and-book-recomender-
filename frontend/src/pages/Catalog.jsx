import React, { useEffect, useState } from 'react';
import api from '../api';
import ItemCard from '../components/ItemCard';
import { Search, Filter } from 'lucide-react';

const Catalog = () => {
    const [items, setItems] = useState([]);
    const [search, setSearch] = useState('');
    const [type, setType] = useState('');

    useEffect(() => {
        fetchItems();
    }, [type]); // Re-fetch on filter change

    const fetchItems = async () => {
        try {
            let url = '/items?limit=100';
            if (search) url += `&search=${search}`;
            if (type) url += `&type=${type}`;

            const res = await api.get(url);
            setItems(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        fetchItems();
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
                <form onSubmit={handleSearch} style={{ flex: 1, display: 'flex', gap: '0.5rem' }}>
                    <div style={{ position: 'relative', flex: 1 }}>
                        <Search size={20} style={{ position: 'absolute', left: '12px', top: '12px', color: '#94a3b8' }} />
                        <input
                            type="text"
                            className="input"
                            style={{ paddingLeft: '2.5rem' }}
                            placeholder="Search by title, author, director..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">Search</button>
                </form>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Filter size={20} color="#94a3b8" />
                    <select className="input" style={{ width: 'auto' }} value={type} onChange={(e) => setType(e.target.value)}>
                        <option value="">All Types</option>
                        <option value="book">Books</option>
                        <option value="movie">Movies</option>
                    </select>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '2rem' }}>
                {items.map(item => <ItemCard key={item.id} item={item} />)}
                {items.length === 0 && <p style={{ color: 'var(--text-secondary)', colSpan: 'all' }}>No items found.</p>}
            </div>
        </div>
    );
};

export default Catalog;
