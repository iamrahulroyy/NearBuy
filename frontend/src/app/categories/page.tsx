'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import axios from 'axios';
import { Sparkles, ArrowRight } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8050/api/v1';

interface Category {
    id: string;
    name: string;
    icon: string;
    count: number;
}

export default function CategoriesPage() {
    const [categories, setCategories] = useState<Category[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await axios.get(`${API_URL}/categories`);
            setCategories(response.data.categories || []);
        } catch (error) {
            console.error('Error fetching categories:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-white overflow-hidden">
            {/* Header Section */}
            <section className="relative pt-32 pb-20">
                {/* Background Gradients */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-orange-50 via-white to-white"></div>
                    <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-[#FF6B35]/10 rounded-full blur-3xl animate-pulse-slow"></div>
                </div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
                    <div className="flex items-center justify-center gap-2 mb-6">
                        <Sparkles className="w-5 h-5 text-[#FF6B35]" />
                        <span className="text-sm font-bold text-slate-500 uppercase tracking-wider">Explore</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 mb-6 tracking-tight">
                        Browse <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#FF6B35] to-[#FF9F43]">Categories</span>
                    </h1>
                    <p className="text-xl text-slate-500 max-w-2xl mx-auto leading-relaxed">
                        Discover local shops organized by what they offer. From daily essentials to specialty items.
                    </p>
                </div>
            </section>

            {/* Categories Grid */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-32">
                {loading ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {[...Array(8)].map((_, i) => (
                            <div key={i} className="bg-gray-50 rounded-3xl h-64 animate-pulse" />
                        ))}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {categories.map((category) => (
                            <Link
                                key={category.id}
                                href={`/shops?category=${category.id}`}
                                className="group relative bg-white border border-gray-100 rounded-3xl p-8 hover:border-orange-100 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 flex flex-col items-center text-center overflow-hidden"
                            >
                                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#FF6B35] to-[#FF9F43] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>

                                <div className="w-20 h-20 bg-orange-50 rounded-full flex items-center justify-center text-4xl mb-6 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                                    {category.icon}
                                </div>

                                <h3 className="text-2xl font-bold text-slate-900 mb-2 group-hover:text-[#FF6B35] transition-colors">
                                    {category.name}
                                </h3>

                                <p className="text-slate-400 font-medium mb-6">
                                    {category.count} {category.count === 1 ? 'shop' : 'shops'}
                                </p>

                                <div className="mt-auto opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300">
                                    <span className="inline-flex items-center text-[#FF6B35] font-bold text-sm">
                                        View Shops <ArrowRight className="w-4 h-4 ml-1" />
                                    </span>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}

                {!loading && categories.length === 0 && (
                    <div className="text-center py-24 bg-gray-50 rounded-3xl border border-gray-100">
                        <p className="text-2xl text-gray-400 font-medium">No categories available yet</p>
                    </div>
                )}
            </section>
        </div>
    );
}
