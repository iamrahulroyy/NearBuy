'use client';

import { Sliders } from 'lucide-react';

interface DistanceFilterProps {
    selectedDistance: number;
    onDistanceChange: (distance: number) => void;
}

const DISTANCE_OPTIONS = [
    { value: 1, label: '1 km' },
    { value: 5, label: '5 km' },
    { value: 10, label: '10 km' },
    { value: 25, label: '25 km' },
    { value: 50, label: '50 km' },
];

export default function DistanceFilter({ selectedDistance, onDistanceChange }: DistanceFilterProps) {
    return (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
            <div className="flex items-center gap-2 mb-4">
                <Sliders className="w-5 h-5 text-slate-700" />
                <h3 className="text-lg font-semibold text-slate-900">Search Radius</h3>
            </div>

            <div className="flex flex-wrap gap-2">
                {DISTANCE_OPTIONS.map((option) => (
                    <button
                        key={option.value}
                        onClick={() => onDistanceChange(option.value)}
                        className={`px-4 py-2 rounded-full font-medium transition-all ${selectedDistance === option.value
                            ? 'bg-[#E50914] text-white shadow-md'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }`}
                    >
                        {option.label}
                    </button>
                ))}
            </div>

            <p className="text-sm text-slate-500 mt-3">
                Showing shops within <span className="font-semibold text-slate-700">{selectedDistance} km</span> of your location
            </p>
        </div>
    );
}
