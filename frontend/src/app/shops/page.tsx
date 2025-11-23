'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
import { MapPin, Phone, Clock, Navigation, Filter, Store } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8050/api/v1';

interface Shop {
    shop_id: string;
    shopName: string;
    fullName: string;
    address: string;
    contact?: string;
    description?: string;
    is_open: boolean;
    latitude?: number;
    longitude?: number;
    category: string;
    city: string;
}

// Comprehensive list of Indian cities for filter
const INDIAN_CITIES = [
    "Agartala", "Ahmedabad", "Aizawl", "Amritsar", "Bangalore", "Bhopal", "Bhubaneswar",
    "Chandigarh", "Chennai", "Coimbatore", "Daman", "Dehradun", "Faridabad", "Gangtok",
    "Gurugram", "Guwahati", "Hyderabad", "Imphal", "Indore", "Itanagar", "Jaipur",
    "Kavaratti", "Kochi", "Kohima", "Kolkata", "Leh", "Lucknow", "Ludhiana", "Mumbai",
    "Mysore", "Nagpur", "New Delhi", "Noida", "Panaji", "Patna", "Port Blair", "Puducherry",
    "Pune", "Raipur", "Ranchi", "Shillong", "Shimla", "Srinagar", "Surat",
    "Thiruvananthapuram", "Udaipur", "Varanasi", "Vijayawada", "Visakhapatnam"
].sort();

export default function ShopsPage() {
    const searchParams = useSearchParams();
    const categoryParam = searchParams.get('category');

    const [shops, setShops] = useState<Shop[]>([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        category: categoryParam || '',
        city: '',
        isOpen: '' as '' | 'true' | 'false'
    });

    useEffect(() => {
        fetchShops();
    }, [filters]);

    const fetchShops = async () => {
        setLoading(true);
        try {
            const params: any = {};
            if (filters.category) params.category = filters.category;
            if (filters.city) params.city = filters.city;
            if (filters.isOpen) params.is_open = filters.isOpen === 'true';

            const response = await axios.get(`${API_URL}/public/shops`, { params });
            setShops(response.data.shops || []);
        } catch (error) {
            console.error('Error fetching shops:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-white overflow-hidden">
            {/* Header */}
            <section className="relative pt-32 pb-16">
                {/* Background Gradients */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-orange-50 via-white to-white"></div>
                    <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-[#FF6B35]/10 rounded-full blur-3xl animate-pulse-slow"></div>
                </div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
                    <div className="flex items-center justify-center gap-2 mb-6">
                        <Store className="w-5 h-5 text-[#FF6B35]" />
                        <span className="text-sm font-bold text-slate-500 uppercase tracking-wider">Marketplace</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 mb-6 tracking-tight">
                        Discover <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#FF6B35] to-[#FF9F43]">Local Shops</span>
                    </h1>
                    <p className="text-xl text-slate-500 max-w-2xl mx-auto">
                        Browse {shops.length} shops in your area and find exactly what you need.
                    </p>
                </div>
            </section>

            {/* Filters */}
            <section className="sticky top-20 z-30 bg-white/80 backdrop-blur-md border-y border-gray-100 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex flex-wrap items-center justify-center gap-4">
                        <div className="flex items-center gap-2 text-slate-400 mr-2">
                            <Filter className="w-4 h-4" />
                            <span className="text-sm font-bold uppercase tracking-wide">Filter By:</span>
                        </div>

                        <select
                            value={filters.isOpen}
                            onChange={(e) => setFilters({ ...filters, isOpen: e.target.value as any })}
                            className="px-6 py-2.5 rounded-full border border-gray-200 bg-white text-slate-700 font-medium focus:border-[#FF6B35] focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all hover:border-gray-300 cursor-pointer"
                        >
                            <option value="">All Status</option>
                            <option value="true">Open Now</option>
                            <option value="false">Closed</option>
                        </select>

                        <select
                            value={filters.city}
                            onChange={(e) => setFilters({ ...filters, city: e.target.value })}
                            className="px-6 py-2.5 rounded-full border border-gray-200 bg-white text-slate-700 font-medium focus:border-[#FF6B35] focus:ring-2 focus:ring-orange-100 focus:outline-none transition-all hover:border-gray-300 cursor-pointer"
                        >
                            <option value="">All Cities</option>
                            {INDIAN_CITIES.map(city => (
                                <option key={city} value={city}>{city}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </section>

            {/* Shops Grid */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 pb-32">
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {[...Array(6)].map((_, i) => (
                            <div key={i} className="bg-gray-50 rounded-3xl h-80 animate-pulse" />
                        ))}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {shops.map((shop) => (
                            <div
                                key={shop.shop_id}
                                className="group bg-white border border-gray-100 rounded-3xl p-8 hover:border-orange-100 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 flex flex-col"
                            >
                                <div className="flex items-start justify-between mb-6">
                                    <div>
                                        <span className="inline-block px-3 py-1 rounded-full bg-orange-50 text-[#FF6B35] text-xs font-bold uppercase tracking-wide mb-3">
                                            {shop.category}
                                        </span>
                                        <h3 className="text-2xl font-bold text-slate-900 leading-tight">
                                            {shop.shopName}
                                        </h3>
                                    </div>
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${shop.is_open
                                        ? 'bg-green-50 text-green-600'
                                        : 'bg-red-50 text-red-600'
                                        }`}>
                                        <span className={`w-2 h-2 rounded-full ${shop.is_open ? 'bg-green-500' : 'bg-red-500'}`}></span>
                                        {shop.is_open ? 'Open' : 'Closed'}
                                    </span>
                                </div>

                                {shop.description && (
                                    <p className="text-slate-500 text-sm mb-6 line-clamp-2 leading-relaxed">
                                        {shop.description}
                                    </p>
                                )}

                                <div className="mt-auto space-y-3">
                                    <div className="flex items-start gap-3 text-slate-600 text-sm">
                                        <MapPin className="w-5 h-5 text-gray-400 shrink-0 mt-0.5" />
                                        <span className="line-clamp-2">{shop.address}</span>
                                    </div>
                                    {shop.contact && (
                                        <div className="flex items-center gap-3 text-slate-600 text-sm">
                                            <Phone className="w-5 h-5 text-gray-400 shrink-0" />
                                            <span>{shop.contact}</span>
                                        </div>
                                    )}
                                </div>

                                <button className="w-full mt-8 bg-slate-900 hover:bg-[#FF6B35] text-white font-bold py-4 rounded-2xl transition-all duration-300 shadow-lg shadow-slate-200 hover:shadow-orange-200 hover:-translate-y-1">
                                    View Details
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {!loading && shops.length === 0 && (
                    <div className="text-center py-24 bg-gray-50 rounded-3xl border border-gray-100">
                        <Store className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <p className="text-2xl text-gray-400 font-medium">No shops found matching your criteria</p>
                        <button
                            onClick={() => setFilters({ category: '', city: '', isOpen: '' })}
                            className="mt-6 text-[#FF6B35] font-bold hover:underline"
                        >
                            Clear all filters
                        </button>
                    </div>
                )}
            </section>
        </div>
    );
}
