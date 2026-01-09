import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const Admin = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        type: 'book',
        author_or_director: '',
        genres: '',
        year: new Date().getFullYear(),
        language: 'English',
        description: '',
        availability_status: 'Available'
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/items', formData);
            alert('Item added successfully!');
            navigate('/catalog');
        } catch (err) {
            alert('Failed to add item');
        }
    };

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            <div className="glass-panel" style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem' }}>
                <h1 style={{ marginBottom: '2rem' }}>Add New Item</h1>
                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem' }}>
                    <input name="title" placeholder="Title" className="input" onChange={handleChange} required />
                    <select name="type" className="input" onChange={handleChange}>
                        <option value="book">Book</option>
                        <option value="movie">Movie</option>
                    </select>
                    <input name="author_or_director" placeholder="Author/Director" className="input" onChange={handleChange} required />
                    <input name="genres" placeholder="Genres (comma separated)" className="input" onChange={handleChange} required />
                    <input name="year" type="number" placeholder="Year" className="input" onChange={handleChange} required />
                    <input name="language" placeholder="Language" className="input" onChange={handleChange} required />
                    <textarea name="description" placeholder="Description" className="input" rows={4} onChange={handleChange} required />
                    <select name="availability_status" className="input" onChange={handleChange}>
                        <option value="Available">Available</option>
                        <option value="Issued">Issued</option>
                        <option value="Reference">Reference</option>
                    </select>
                    <button type="submit" className="btn btn-primary">Add Item</button>
                </form>
            </div>
        </div>
    );
};

export default Admin;
