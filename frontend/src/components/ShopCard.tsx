'use client';

import { Star, MapPin } from 'lucide-react';
import { Shop } from '@/types';

interface ShopCardProps {
    data: Shop;
}

export default function ShopCard({ data }: ShopCardProps) {
    return (
        <div className="group bg-white rounded-2xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-xl transition-all duration-300 cursor-pointer hover:-translate-y-1">
            {/* Image Section - Placeholder for now as backend might not have images yet */}
            <div className="relative h-48 w-full overflow-hidden bg-slate-100 flex items-center justify-center">
                <span className="text-4xl">🏪</span>
                {/* <img 
                    src={data.image} 
                    alt={data.shopName} 
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                /> */}
                <div className={`absolute top-3 right-3 px-2 py-1 rounded-lg text-xs font-bold shadow-sm ${data.is_open ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {data.is_open ? 'Open' : 'Closed'}
                </div>
            </div>

            {/* Content Section */}
            <div className="p-5">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-bold text-slate-900 line-clamp-1">{data.shopName}</h3>
                    <div className="flex items-center gap-1 bg-slate-50 px-2 py-0.5 rounded-md">
                        <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />
                        <span className="text-xs font-bold text-slate-700">New</span>
                    </div>
                </div>

                <p className="text-sm text-slate-500 mb-4 line-clamp-2">{data.fullName}</p>

                <div className="flex items-center justify-between pt-4 border-t border-slate-50">
                    <div className="flex items-center gap-1 text-slate-400 text-xs">
                        <MapPin className="w-3 h-3" />
                        <span>{data.distance || 'Nearby'}</span>
                    </div>
                    <div className="text-xs font-medium text-slate-500">
                        {data.address}
                    </div>
                </div>
            </div>
        </div>
    );
}
