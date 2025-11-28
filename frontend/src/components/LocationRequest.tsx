'use client';

import { MapPin } from 'lucide-react';
import dynamic from 'next/dynamic';

// Dynamically import Map to avoid SSR issues with Leaflet
const Map = dynamic(() => import('./Map'), { ssr: false });

interface LocationRequestProps {
    onAllow: () => void;
    onDeny: () => void;
}

const LocationRequest = ({ onAllow, onDeny }: LocationRequestProps) => {
    return (
        <div className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 pb-6 sm:pb-0">
            {/* Backdrop */}
            <div className="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity" />

            {/* Card */}
            <div className="relative w-full max-w-md bg-white p-8 rounded-3xl shadow-2xl animate-in slide-in-from-bottom-10 fade-in duration-500">
                <div className="flex flex-col items-center text-center">
                    <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-6">
                        <MapPin className="w-8 h-8 text-red-500 fill-red-500" />
                    </div>

                    <h2 className="text-2xl font-bold text-slate-900 mb-3">
                        Allow Location Access
                    </h2>

                    <p className="text-slate-500 mb-8 leading-relaxed">
                        We need access to your location to provide accurate and tailored results for your area. You can manage this in your settings anytime.
                    </p>

                    <div className="w-full space-y-3">
                        <button
                            onClick={onAllow}
                            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3.5 rounded-xl transition-colors shadow-lg shadow-blue-500/30"
                        >
                            Allow Access
                        </button>

                        <button
                            onClick={onDeny}
                            className="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-3.5 rounded-xl transition-colors"
                        >
                            Deny Access
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LocationRequest;
