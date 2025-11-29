'use client';

import { useState, useEffect, useRef } from 'react';
import { MapPin, Heart, Users, TrendingUp, ArrowRight, Search, Store, ShoppingBag } from 'lucide-react';
import { motion, useScroll, useTransform, useInView } from 'framer-motion';

export default function AboutPage() {
    return (
        <div data-cursor-section="content" className="min-h-screen bg-white overflow-hidden cursor-none">
            {/* Hero Section */}
            <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32">
                {/* Background Gradients */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-orange-50 via-white to-white"></div>
                    <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-[#FF6B35]/10 rounded-full blur-3xl animate-pulse-slow"></div>
                    <div className="absolute bottom-[10%] left-[-10%] w-[400px] h-[400px] bg-orange-200/20 rounded-full blur-3xl animate-pulse-slow delay-700"></div>
                </div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
                    <motion.span
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="inline-block py-1 px-3 rounded-full bg-orange-100 text-[#FF6B35] text-sm font-bold tracking-wide uppercase mb-6"
                    >
                        Our Story
                    </motion.span>
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-5xl md:text-7xl font-extrabold text-slate-900 mb-8 tracking-tight leading-tight"
                    >
                        Connecting communities,<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#FF6B35] to-[#FF9F43]">
                            one search at a time.
                        </span>
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="text-xl md:text-2xl text-slate-500 max-w-3xl mx-auto leading-relaxed"
                    >
                        NearBuy isn't just a platform; it's a movement to bring neighborhoods closer by making local commerce accessible, transparent, and thriving.
                    </motion.p>
                </div>
            </section>

            {/* Mission Section (Glass Card) */}
            <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 relative z-20 mb-24">
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.7 }}
                    className="bg-white/70 backdrop-blur-xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-3xl p-8 md:p-16 text-center"
                >
                    <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Mission</h2>
                    <p className="text-lg md:text-xl text-slate-600 leading-relaxed">
                        "NearBuy transforms underused dark stores into efficient, customer-ready local hubs. We turn hidden inventory into discoverable, fast-access retail, giving local businesses a real way to reach nearby shoppers and keeping community commerce alive."
                    </p>
                </motion.div>
            </section>

            {/* How It Works - Redesigned */}
            <HowItWorksSection />

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
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5 }}
                    className="relative rounded-[2.5rem] overflow-hidden bg-[#FF6B35] text-white p-12 md:p-20 text-center shadow-2xl shadow-orange-500/30"
                >
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
                </motion.div>
            </section>
        </div>
    );
}

function HowItWorksSection() {
    const steps = [
        {
            id: 1,
            title: 'Search',
            description: 'Type what you need. From "AA Batteries" to "Basmati Rice".',
            icon: Search,
            color: 'bg-blue-50 text-blue-600',
            borderColor: 'group-hover:border-blue-200'
        },
        {
            id: 2,
            title: 'Discover',
            description: 'Instantly see which nearby shops have it in stock.',
            icon: Store,
            color: 'bg-orange-50 text-orange-600',
            borderColor: 'group-hover:border-orange-200'
        },
        {
            id: 3,
            title: 'Visit',
            description: 'Walk over, buy it, and say hello to your local shopkeeper.',
            icon: ShoppingBag,
            color: 'bg-green-50 text-green-600',
            borderColor: 'group-hover:border-green-200'
        }
    ];

    return (
        <section className="py-24 bg-white relative overflow-hidden">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
                <div className="text-center mb-20">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-3xl md:text-5xl font-bold text-slate-900 mb-6"
                    >
                        How It Works
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="text-lg text-slate-500 max-w-2xl mx-auto"
                    >
                        Experience the convenience of local shopping with modern technology.
                    </motion.p>
                </div>

                <div className="relative grid md:grid-cols-3 gap-12">
                    {/* Connecting Line (Desktop) */}
                    <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-slate-100 -translate-y-1/2 z-0">
                        <motion.div
                            initial={{ scaleX: 0, originX: 0 }}
                            whileInView={{ scaleX: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 1.5, ease: "easeInOut" }}
                            className="h-full bg-gradient-to-r from-blue-200 via-orange-200 to-green-200"
                        />
                    </div>

                    {steps.map((step, idx) => (
                        <motion.div
                            key={step.id}
                            initial={{ opacity: 0, y: 40 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: idx * 0.2, duration: 0.5 }}
                            className="relative z-10 group"
                        >
                            <div className={`bg-white rounded-[2rem] p-8 border-2 border-slate-50 shadow-sm hover:shadow-xl transition-all duration-500 hover:-translate-y-2 ${step.borderColor}`}>
                                <div className={`w-20 h-20 mx-auto ${step.color} rounded-2xl flex items-center justify-center mb-8 transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-500 shadow-sm`}>
                                    <step.icon className="w-10 h-10" />
                                </div>
                                <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-white px-4 py-1 rounded-full border border-slate-100 text-sm font-bold text-slate-400 shadow-sm">
                                    Step 0{step.id}
                                </div>
                                <h3 className="text-2xl font-bold text-slate-900 mb-4 text-center">{step.title}</h3>
                                <p className="text-slate-500 text-center leading-relaxed">
                                    {step.description}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}

// Simple animated counter component
const StatCard = ({ number, suffix, label, delay }: { number: string, suffix: string, label: string, delay: number }) => {
    const [count, setCount] = useState(0);
    const target = parseInt(number);
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, margin: "-50px" });

    useEffect(() => {
        if (!isInView) return;

        const duration = 2000;
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
    }, [target, delay, isInView]);

    return (
        <motion.div
            ref={ref}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={isInView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.5, delay: delay / 1000 }}
            className="liquid-display bg-white p-6 flex flex-col items-center justify-center text-center h-40 hover:scale-105 transition-transform duration-300 rounded-2xl shadow-sm border border-slate-100"
        >
            <div className="text-4xl font-bold text-slate-900 mb-2 font-inter">
                {count}{suffix}
            </div>
            <div className="text-sm text-slate-500 font-medium uppercase tracking-wide">
                {label}
            </div>
        </motion.div>
    );
};
