'use client';

import { useEffect, useState } from 'react';
import { Sparkles } from 'lucide-react';
import { getSuggestions } from '@/services/api';

interface SearchSuggestionsProps {
    lat: number;
    lon: number;
    onSuggestionClick: (suggestion: string) => void;
}

export default function SearchSuggestions({ lat, lon, onSuggestionClick }: SearchSuggestionsProps) {
    const [suggestions, setSuggestions] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSuggestions = async () => {
            setLoading(true);
            try {
                const results = await getSuggestions(lat, lon, 10);
                // Show only first 8 suggestions for UI cleanliness
                setSuggestions(results.slice(0, 8));
            } catch (error) {
                console.error('Error fetching suggestions:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSuggestions();
    }, [lat, lon]);

    if (loading) {
        return (
            <div className="flex gap-2 flex-wrap">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                    <div key={i} className="h-8 w-24 bg-slate-200 rounded-full animate-pulse"></div>
                ))}
            </div>
        );
    }

    if (suggestions.length === 0) {
        return null;
    }

    return (
        <div className="mt-6">
            <div className="flex items-center gap-2 mb-3">
                <Sparkles className="w-4 h-4 text-[#E50914]" />
                <p className="text-sm font-medium text-slate-700">Available in your area:</p>
            </div>
            <div className="flex flex-wrap gap-2">
                {suggestions.map((suggestion) => (
                    <button
                        key={suggestion}
                        onClick={() => onSuggestionClick(suggestion)}
                        className="px-4 py-2 bg-slate-50 hover:bg-[#E50914] hover:text-white text-slate-700 rounded-full text-sm font-medium transition-all border border-slate-200 hover:border-[#E50914]"
                    >
                        {suggestion}
                    </button>
                ))}
            </div>
        </div>
    );
}
