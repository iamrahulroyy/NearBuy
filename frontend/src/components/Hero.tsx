'use client';

import { Search } from 'lucide-react';
import { useState } from 'react';

interface HeroProps {
    onSearch: (query: string) => void;
}

const Hero = ({ onSearch }: HeroProps) => {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <section className="relative bg-slate-50 pt-12 pb-20 md:pt-20 md:pb-32 overflow-hidden min-h-[600px] flex items-center">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
                <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-20">

                    {/* Left Content */}
                    <div className="w-full lg:w-1/2 text-center lg:text-left">
                        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-slate-900 leading-tight mb-8">
                            Find what you need<br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#E50914] to-orange-500">
                                in shops near you.
                            </span>
                        </h1>

                        <div className="relative max-w-xl mx-auto lg:mx-0">
                            <div className="bg-white p-2 rounded-full shadow-2xl flex items-center border border-slate-100 transform transition-transform hover:scale-[1.02]">
                                <div className="pl-6 pr-4 text-slate-400">
                                    <Search className="w-6 h-6" />
                                </div>
                                <input
                                    type="text"
                                    placeholder="Search for items (e.g. batteries, milk)..."
                                    className="flex-1 bg-transparent border-none outline-none text-slate-700 placeholder:text-slate-400 h-12 text-lg w-full"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                                />
                                <button
                                    onClick={handleSearch}
                                    className="bg-[#E50914] hover:bg-red-700 text-white rounded-full px-6 sm:px-10 py-3 sm:py-4 font-bold transition-all shadow-lg shadow-red-500/30 hover:shadow-red-500/50 active:scale-95"
                                >
                                    GO
                                </button>
                            </div>
                            <p className="mt-4 text-slate-500 text-sm font-medium">
                                Popular: <span className="text-slate-700 cursor-pointer hover:text-[#E50914]">Batteries</span>, <span className="text-slate-700 cursor-pointer hover:text-[#E50914]">Milk</span>, <span className="text-slate-700 cursor-pointer hover:text-[#E50914]">Chargers</span>
                            </p>
                        </div>
                    </div>

                    {/* Right Image - Circular Animation */}
                    <div className="w-full lg:w-1/2 relative mt-10 lg:mt-0">
                        <div className="relative w-full max-w-[500px] lg:max-w-[600px] aspect-square mx-auto">
                            {/* Decorative Blobs */}
                            <div className="absolute top-0 right-0 w-64 h-64 bg-red-100 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
                            <div className="absolute bottom-0 left-0 w-64 h-64 bg-orange-100 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
                            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-white/50 rounded-full blur-3xl -z-10"></div>

                            {/* Main Central Image */}
                            <div className="absolute inset-0 flex items-center justify-center z-10">
                                <div className="relative w-64 h-64 sm:w-80 sm:h-80 bg-white rounded-full shadow-2xl flex items-center justify-center animate-float border-8 border-white">
                                    <span className="text-[8rem] sm:text-[10rem] drop-shadow-lg transform hover:scale-110 transition-transform duration-300 cursor-default">🛍️</span>
                                </div>
                            </div>

                            {/* Orbiting Items */}
                            {/* Item 1: Top Left */}
                            <div className="absolute top-[10%] left-[15%] bg-white p-3 sm:p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-pop-in animation-delay-0 hover:scale-110 transition-transform cursor-pointer z-20">
                                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-50 rounded-full flex items-center justify-center text-2xl">🔋</div>
                                <div className="hidden sm:block">
                                    <p className="text-xs text-slate-500 font-bold uppercase">Electronics</p>
                                    <p className="text-sm font-bold text-slate-900">Batteries</p>
                                </div>
                            </div>

                            {/* Item 2: Top Right */}
                            <div className="absolute top-[15%] right-[10%] bg-white p-3 sm:p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-pop-in animation-delay-1000 hover:scale-110 transition-transform cursor-pointer z-20">
                                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-orange-50 rounded-full flex items-center justify-center text-2xl">🥛</div>
                                <div className="hidden sm:block">
                                    <p className="text-xs text-slate-500 font-bold uppercase">Dairy</p>
                                    <p className="text-sm font-bold text-slate-900">Fresh Milk</p>
                                </div>
                            </div>

                            {/* Item 3: Bottom Right */}
                            <div className="absolute bottom-[20%] right-[5%] bg-white p-3 sm:p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-pop-in animation-delay-2000 hover:scale-110 transition-transform cursor-pointer z-20">
                                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-green-50 rounded-full flex items-center justify-center text-2xl">🥦</div>
                                <div className="hidden sm:block">
                                    <p className="text-xs text-slate-500 font-bold uppercase">Fresh</p>
                                    <p className="text-sm font-bold text-slate-900">Vegetables</p>
                                </div>
                            </div>

                            {/* Item 4: Bottom Left */}
                            <div className="absolute bottom-[10%] left-[5%] bg-white p-3 sm:p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-pop-in animation-delay-3000 hover:scale-110 transition-transform cursor-pointer z-20">
                                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-purple-50 rounded-full flex items-center justify-center text-2xl">🧴</div>
                                <div className="hidden sm:block">
                                    <p className="text-xs text-slate-500 font-bold uppercase">Essentials</p>
                                    <p className="text-sm font-bold text-slate-900">Shampoo</p>
                                </div>
                            </div>

                            {/* Item 5: Top Center (Mobile only mostly) */}
                            <div className="absolute -top-[5%] left-1/2 transform -translate-x-1/2 bg-white p-3 sm:p-4 rounded-2xl shadow-xl flex items-center gap-3 animate-pop-in animation-delay-1500 hover:scale-110 transition-transform cursor-pointer z-20">
                                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-yellow-50 rounded-full flex items-center justify-center text-2xl">🍞</div>
                                <div className="hidden sm:block">
                                    <p className="text-xs text-slate-500 font-bold uppercase">Bakery</p>
                                    <p className="text-sm font-bold text-slate-900">Bread</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
