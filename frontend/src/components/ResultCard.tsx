import { MapPin, AlertTriangle, CheckCircle } from 'lucide-react';

interface SearchResult {
    id: string;
    shopName: string;
    itemName: string;
    price: number;
    stockStatus: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK';
    distance?: string;
}

interface ResultCardProps {
    result: SearchResult;
    onHover?: (id: string) => void;
    onClick?: (id: string) => void;
}

export default function ResultCard({ result, onHover, onClick }: ResultCardProps) {
    const isLowStock = result.stockStatus === 'LOW_STOCK';
    const isOutOfStock = result.stockStatus === 'OUT_OF_STOCK';

    return (
        <div
            className="group relative flex flex-col gap-3 rounded-xl border border-slate-800 bg-slate-800/50 p-4 transition-all hover:bg-slate-800 hover:shadow-lg hover:shadow-indigo-500/10 cursor-pointer"
            onMouseEnter={() => onHover?.(result.id)}
            onClick={() => onClick?.(result.id)}
        >
            <div className="flex justify-between items-start">
                <div>
                    <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors">
                        {result.shopName}
                    </h3>
                    <p className="text-sm text-slate-400 flex items-center gap-1 mt-1">
                        <MapPin className="w-3 h-3" />
                        {result.distance || '0.5km'} away
                    </p>
                </div>
                <div className="flex flex-col items-end gap-1">
                    <span className="text-xl font-bold text-white">${result.price.toFixed(2)}</span>
                </div>
            </div>

            <div className="flex justify-between items-center mt-2">
                <p className="text-slate-300 font-medium">{result.itemName}</p>

                <div className={`
          px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5
          ${isLowStock ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' : ''}
          ${isOutOfStock ? 'bg-red-500/20 text-red-400 border border-red-500/30' : ''}
          ${!isLowStock && !isOutOfStock ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : ''}
        `}>
                    {isLowStock && <AlertTriangle className="w-3 h-3" />}
                    {!isLowStock && !isOutOfStock && <CheckCircle className="w-3 h-3" />}
                    {result.stockStatus.replace('_', ' ')}
                </div>
            </div>
        </div>
    );
}
