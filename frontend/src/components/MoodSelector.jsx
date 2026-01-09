import React from 'react';
import { Sun, CloudRain, Zap, Coffee, Ghost, Lightbulb } from 'lucide-react';

const MoodSelector = ({ onSelect, selectedMood }) => {
    const moods = [
        { label: 'Happy', Icon: Sun, color: '#fbcfe8' },
        { label: 'Sad', Icon: CloudRain, color: '#c7d2fe' },
        { label: 'Excited', Icon: Zap, color: '#fef08a' },
        { label: 'Chill', Icon: Coffee, color: '#bbf7d0' },
        { label: 'Scared', Icon: Ghost, color: '#e9d5ff' },
        { label: 'Inspired', Icon: Lightbulb, color: '#fed7aa' },
    ];

    return (
        <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', justifyContent: 'center', margin: '3rem 0' }}>
            {moods.map((m) => {
                const Icon = m.Icon;
                return (
                    <button
                        key={m.label}
                        onClick={() => onSelect(m.label)}
                        style={{
                            background: selectedMood === m.label ? m.color : 'rgba(255,255,255,0.7)',
                            border: selectedMood === m.label ? `3px solid ${m.color}` : '1px solid rgba(255,255,255,0.5)',
                            borderRadius: '24px',
                            padding: '1.5rem 3rem',
                            fontSize: '1.5rem',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            transition: 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '1rem',
                            color: '#1e293b',
                            transform: selectedMood === m.label ? 'scale(1.1)' : 'scale(1)',
                            boxShadow: selectedMood === m.label ? '0 20px 25px -5px rgba(0,0,0,0.2)' : '0 4px 6px -1px rgba(0,0,0,0.1)'
                        }}
                    >
                        <Icon size={32} strokeWidth={2} />
                        <span>{m.label}</span>
                    </button>
                )
            })}
        </div>
    );
};

export default MoodSelector;
