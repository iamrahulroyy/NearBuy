'use client';

import { Search, ChevronDown, SlidersHorizontal, Sparkles, MapPin } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

interface HeroProps {
    onSearch: (query: string) => void;
    radius: number;
    onRadiusChange: (radius: number) => void;
}

const Hero = ({ onSearch, radius, onRadiusChange }: HeroProps) => {
    const [query, setQuery] = useState('');
    const [isRadiusOpen, setIsRadiusOpen] = useState(false);
    const radiusRef = useRef<HTMLDivElement>(null);

    const handleSearch = (searchQuery: string = query) => {
        if (searchQuery.trim()) {
            onSearch(searchQuery);
            setQuery(searchQuery); // Ensure input reflects the search
        }
    };

    // Close radius dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (radiusRef.current && !radiusRef.current.contains(event.target as Node)) {
                setIsRadiusOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const quickChips = [
        { label: 'Batteries', icon: '🔋' },
        { label: 'Milk', icon: '🥛' },
        { label: 'Chargers', icon: '🔌' },
        { label: 'Rice', icon: '🍚' },
        { label: 'Headphones', icon: '🎧' },
        { label: 'Cooking Oil', icon: '🍳' },
        { label: 'Dumbbells', icon: '🏋️' },
        { label: 'Football', icon: '⚽' },
        { label: 'Bookshelf', icon: '📚' },
    ];

    return (
        <section className="relative w-full bg-gradient-to-br from-orange-50 via-white to-orange-50 pt-20 pb-24 overflow-hidden">
            {/* Background Decorative Blobs */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-[#FF6B35]/10 rounded-full blur-3xl animate-pulse-slow"></div>
                <div className="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-orange-200/20 rounded-full blur-3xl animate-pulse-slow delay-1000"></div>
            </div>

            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                <div className="text-center mb-10">
                    <h1 className="text-3xl md:text-5xl font-extrabold text-slate-900 mb-4 tracking-tight leading-tight">
                        Find what you need in <span className="text-[#FF6B35]">shops near you</span>.
                    </h1>
                    <p className="text-lg text-slate-500 max-w-2xl mx-auto">
                        Search for products, browse local inventories, and find the best deals in your neighborhood.
                    </p>
                </div>

                {/* Glass Card Container */}
                <div className="bg-white/70 backdrop-blur-xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-3xl p-6 md:p-10">

                    {/* Unified Search Block - Liquid Display */}
                    <div className="max-w-3xl mx-auto mb-10 relative z-20">
                        <div className="liquid-display flex items-center p-2">

                            {/* Radius Selector - Apple Liquid Glass */}
                            <div className="relative" ref={radiusRef}>
                                <button
                                    onClick={() => setIsRadiusOpen(!isRadiusOpen)}
                                    className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-slate-800 font-bold px-6 py-3 rounded-full ml-1 transition-colors"
                                >
                                    <SlidersHorizontal className="w-4 h-4 text-slate-700" />
                                    <span className="whitespace-nowrap">{radius} km</span>
                                    <ChevronDown className={`w-4 h-4 text-slate-700 transition-transform ${isRadiusOpen ? 'rotate-180' : ''}`} />
                                </button>

                                {/* Dropdown */}
                                {isRadiusOpen && (
                                    <div className="absolute top-full left-0 mt-4 w-56 liquid-display overflow-hidden py-3 animate-in fade-in zoom-in-95 duration-200 z-50">
                                        <div className="px-5 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider">Search Radius</div>
                                        {[1, 5, 10, 25, 50].map((r) => (
                                            <button
                                                key={r}
                                                onClick={() => {
                                                    onRadiusChange(r);
                                                    setIsRadiusOpen(false);
                                                }}
                                                className={`w-full text-left px-5 py-3 text-sm font-bold transition-colors flex items-center justify-between ${radius === r ? 'bg-orange-50 text-[#FF6B35]' : 'text-gray-600 hover:bg-gray-50'
                                                    }`}
                                            >
                                                <span>{r} km</span>
                                                {radius === r && <div className="w-2 h-2 rounded-full bg-[#FF6B35] shadow-[0_0_10px_#FF6B35]" />}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Search Input */}
                            <div className="flex-1 flex items-center px-4">
                                <Search className="w-6 h-6 text-gray-500 mr-3" />
                                <input
                                    type="text"
                                    placeholder="Search for items..."
                                    className="flex-1 bg-transparent border-none outline-none text-gray-900 placeholder:text-gray-500 h-12 text-lg w-full font-medium"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                                />
                            </div>

                            {/* GO Button - Apple Liquid Glass */}
                            <div className="relative group">
                                <button
                                    onClick={() => handleSearch()}
                                    className="apple-liquid-glass relative z-10 text-slate-900 rounded-full px-10 py-4 font-bold text-lg"
                                >
                                    <span className="relative z-10">GO</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Quick Search Section */}
                    <div className="text-center">
                        <div className="flex items-center justify-center gap-2 mb-6 opacity-80">
                            <Sparkles className="w-4 h-4 text-[#FF6B35]" />
                            <span className="text-sm font-bold text-slate-500 uppercase tracking-wider">Quick Search</span>
                        </div>
                        <div className="flex flex-wrap justify-center gap-3">
                            {quickChips.map((chip) => (
                                <button
                                    key={chip.label}
                                    onClick={() => handleSearch(chip.label)}
                                    className="group flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 rounded-full text-sm font-semibold text-slate-600 hover:border-[#FF6B35] hover:text-[#FF6B35] hover:bg-orange-50 transition-all duration-300 shadow-sm hover:shadow-md hover:-translate-y-0.5"
                                >
                                    <span className="text-lg group-hover:scale-110 transition-transform duration-300">{chip.icon}</span>
                                    <span>{chip.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
