'use client';

import { useState, useEffect } from 'react';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { Loader2, ChevronLeft, ChevronRight } from 'lucide-react';

export default function ItemsPage() {
    const { isAuthenticated, isLoading: authLoading } = useAuth();
    const [items, setItems] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const pageSize = 20;

    useEffect(() => {
        if (isAuthenticated) {
            fetchItems();
        } else if (!authLoading) {
            setLoading(false);
        }
    }, [isAuthenticated, authLoading, page]);

    const fetchItems = async () => {
        setLoading(true);
        try {
            const response = await api.get('/items/get_all_items', {
                params: { page, page_size: pageSize }
            });
            if (response.data && response.data.body) {
                setItems(response.data.body);
            }
        } catch (error) {
            console.error("Failed to fetch items", error);
        } finally {
            setLoading(false);
        }
    };

    if (authLoading) {
        return <div className="flex justify-center items-center min-h-screen"><Loader2 className="animate-spin h-8 w-8 text-indigo-600" /></div>;
    }

    if (!isAuthenticated) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Access Restricted</h2>
                <p className="text-gray-600 mb-8 text-center">You need to be logged in to view the items catalog.</p>
                <Link href="/login" className="bg-indigo-600 text-white px-6 py-3 rounded-md font-medium hover:bg-indigo-700 transition-colors">
                    Sign In
                </Link>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">All Items</h1>

            {loading ? (
                <div className="flex justify-center py-12">
                    <Loader2 className="animate-spin h-8 w-8 text-indigo-600" />
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {items.map((item, index) => (
                            <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                                <div className="p-4">
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.itemName}</h3>
                                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">{item.description}</p>
                                    <div className="flex justify-between items-center">
                                        <span className="text-indigo-600 font-bold">${item.price}</span>
                                        <span className={`text-xs px-2 py-1 rounded-full ${item.quantity > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {item.quantity > 0 ? 'In Stock' : 'Out of Stock'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Pagination */}
                    <div className="mt-8 flex justify-center items-center space-x-4">
                        <button
                            onClick={() => setPage(p => Math.max(1, p - 1))}
                            disabled={page === 1}
                            className="p-2 rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <ChevronLeft className="h-5 w-5" />
                        </button>
                        <span className="text-gray-700">Page {page}</span>
                        <button
                            onClick={() => setPage(p => p + 1)}
                            disabled={items.length < pageSize}
                            className="p-2 rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <ChevronRight className="h-5 w-5" />
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
