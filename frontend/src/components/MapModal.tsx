'use client';

import { X } from 'lucide-react';
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import Map component to avoid SSR issues
const SearchMap = dynamic(() => import('@/components/SearchMap'), {
    ssr: false,
    loading: () => <div className="h-full w-full bg-slate-100 animate-pulse flex items-center justify-center text-slate-400">Loading Map...</div>
});

import { Shop } from '@/types';

interface MapModalProps {
    isOpen: boolean;
    onClose: () => void;
    shops: Shop[];
    center?: [number, number];
    onMapClick?: (lat: number, lng: number) => void;
}

export default function MapModal({ isOpen, onClose, shops, center, onMapClick }: MapModalProps) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return null;

    return (
        <div className={`fixed inset-0 z-[100] transition-opacity duration-300 ${isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>
            {/* Backdrop */}
            <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose}></div>

            {/* Modal Content */}
            <div className={`absolute inset-4 md:inset-10 bg-white rounded-3xl overflow-hidden shadow-2xl transform transition-transform duration-300 ${isOpen ? 'scale-100' : 'scale-95'}`}>
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 z-[1000] bg-white p-2 rounded-full shadow-lg hover:bg-slate-100 transition-colors"
                >
                    <X className="w-6 h-6 text-slate-900" />
                </button>

                <div className="w-full h-full">
                    <SearchMap
                        shops={shops}
                        center={center || [28.6139, 77.2090]}
                        zoom={13}
                        onMarkerClick={() => { }}
                        onMapClick={onMapClick}
                    />
                </div>
            </div>
        </div>
    );
}
