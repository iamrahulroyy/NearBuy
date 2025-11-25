'use client';

import { useState, useEffect } from 'react';
import { MapPin, Heart, Users, TrendingUp, ArrowRight } from 'lucide-react';

export default function AboutPage() {
    return (
        <div className="min-h-screen bg-white overflow-hidden">
            {/* Hero Section */}
            <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32">
                {/* Background Gradients */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-orange-50 via-white to-white"></div>
                    <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-[#FF6B35]/10 rounded-full blur-3xl animate-pulse-slow"></div>
                    <div className="absolute bottom-[10%] left-[-10%] w-[400px] h-[400px] bg-orange-200/20 rounded-full blur-3xl animate-pulse-slow delay-700"></div>
                </div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
                    <span className="inline-block py-1 px-3 rounded-full bg-orange-100 text-[#FF6B35] text-sm font-bold tracking-wide uppercase mb-6">
                        Our Story
                    </span>
                    <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 mb-8 tracking-tight leading-tight">
                        Connecting communities,<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#FF6B35] to-[#FF9F43]">
                            one search at a time.
                        </span>
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-500 max-w-3xl mx-auto leading-relaxed">
                        NearBuy isn't just a platform; it's a movement to bring neighborhoods closer by making local commerce accessible, transparent, and thriving.
                    </p>
                </div>
            </section>

            {/* Mission Section (Glass Card) */}
            <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20 mb-24">
                <div className="bg-white/70 backdrop-blur-xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-3xl p-8 md:p-16 text-center">
                    <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Mission</h2>
                    <p className="text-lg md:text-xl text-slate-600 leading-relaxed">
                        "NearBuy transforms underused dark stores into efficient, customer-ready local hubs. We turn hidden inventory into discoverable, fast-access retail, giving local businesses a real way to reach nearby shoppers and keeping community commerce alive."
                    </p>
                </div>
            </section>

            {/* How It Works */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">How It Works</h2>
                    <p className="text-slate-500">Simple steps to support your local economy.</p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {[
                        {
                            step: '01',
                            title: 'Search',
                            description: 'Type what you need. From "AA Batteries" to "Basmati Rice".',
                            icon: '🔍'
                        },
                        {
                            step: '02',
                            title: 'Discover',
                            description: 'Instantly see which nearby shops have it in stock.',
                            icon: '📍'
                        },
                        {
                            step: '03',
                            title: 'Visit',
                            description: 'Walk over, buy it, and say hello to your local shopkeeper.',
                            icon: '👋'
                        }
                    ].map((item, idx) => (
                        <div
                            key={idx}
                            className="group relative bg-white rounded-3xl p-8 border border-gray-100 hover:border-orange-100 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                        >
                            <div className="absolute top-6 right-6 text-6xl opacity-5 group-hover:opacity-10 transition-opacity font-black text-[#FF6B35]">
                                {item.step}
                            </div>
                            <div className="w-14 h-14 bg-orange-50 rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform duration-300">
                                {item.icon}
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-3">{item.title}</h3>
                            <p className="text-slate-500 leading-relaxed">{item.description}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Animated Stats Section */}
            <section className="py-24 bg-slate-50 relative overflow-hidden">
                {/* Growth Curve SVG Background */}
                <svg className="absolute top-0 left-0 w-full h-full pointer-events-none opacity-20" viewBox="0 0 1000 300" preserveAspectRatio="none">
                    <path d="M0,300 C300,300 500,100 1000,0 L1000,300 Z" fill="url(#growthGradient)" />
                    <defs>
                        <linearGradient id="growthGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#FF6B35" stopOpacity="0" />
                            <stop offset="100%" stopColor="#FF6B35" stopOpacity="0.5" />
                        </linearGradient>
                    </defs>
                </svg>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-12">
                        <StatCard number="19" suffix="+" label="Cities Covered" delay={0} />
                        <StatCard number="200" suffix="+" label="Partner Shops" delay={100} />
                        <StatCard number="10" suffix="k+" label="Happy Users" delay={200} />
                        <StatCard number="100" suffix="%" label="Local Growth" delay={300} />
                    </div>
                </div>
            </section>

            {/* Contact Section */}
            <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                <div className="relative rounded-[2.5rem] overflow-hidden bg-[#FF6B35] text-white p-12 md:p-20 text-center shadow-2xl shadow-orange-500/30">
                    {/* Decorative Circles */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
                    <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-10 rounded-full translate-y-1/2 -translate-x-1/2"></div>

                    <div className="relative z-10">
                        <h2 className="text-3xl md:text-5xl font-bold mb-6">Ready to join the neighborhood?</h2>
                        <p className="text-lg md:text-xl opacity-90 mb-10 max-w-2xl mx-auto">
                            Whether you're a shopper or a shop owner, we'd love to have you on board.
                        </p>
                        <button className="bg-white text-[#FF6B35] px-10 py-4 rounded-full font-bold text-lg hover:bg-orange-50 transition-colors inline-flex items-center gap-2 group">
                            Get in Touch
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
}

// Simple animated counter component
const StatCard = ({ number, suffix, label, delay }: { number: string, suffix: string, label: string, delay: number }) => {
    const [count, setCount] = useState(0);
    const target = parseInt(number);

    useEffect(() => {
        const duration = 3000;
        const steps = 60;
        const stepTime = duration / steps;
        let current = 0;

        const timer = setTimeout(() => {
            const interval = setInterval(() => {
                current += target / steps;
                if (current >= target) {
                    setCount(target);
                    clearInterval(interval);
                } else {
                    setCount(Math.ceil(current));
                }
            }, stepTime);
            return () => clearInterval(interval);
        }, delay);

        return () => clearTimeout(timer);
    }, [target, delay]);

    return (
        <div className="liquid-display bg-white p-6 flex flex-col items-center justify-center text-center h-40 hover:scale-105 transition-transform duration-300">
            <div className="text-4xl font-bold text-slate-900 mb-2 font-inter">
                {count}{suffix}
            </div>
            <div className="text-sm text-slate-500 font-medium uppercase tracking-wide">
                {label}
            </div>
        </div>
    );
};
