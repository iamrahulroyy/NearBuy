'use client';

import { useState, useRef, useEffect } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';

interface BottomSheetProps {
    children: React.ReactNode;
    isOpen?: boolean;
}

export default function BottomSheet({ children }: BottomSheetProps) {
    const [isExpanded, setIsExpanded] = useState(false);
    const sheetRef = useRef<HTMLDivElement>(null);

    const toggleSheet = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div
            ref={sheetRef}
            className={`
        fixed bottom-0 left-0 right-0 z-20 
        bg-slate-900 border-t border-slate-800 
        rounded-t-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.5)]
        transition-all duration-500 ease-in-out
        ${isExpanded ? 'h-[80vh]' : 'h-[25vh]'}
      `}
        >
            {/* Handle for dragging/tapping */}
            <div
                className="w-full h-8 flex items-center justify-center cursor-pointer"
                onClick={toggleSheet}
            >
                <div className="w-12 h-1.5 bg-slate-700 rounded-full mb-1" />
            </div>

            {/* Content Area */}
            <div className="h-full overflow-y-auto px-4 pb-20">
                <div className="flex justify-between items-center mb-4 px-2">
                    <h2 className="text-white font-bold text-lg">Nearby Results</h2>
                    <button
                        onClick={toggleSheet}
                        className="text-slate-400 hover:text-white"
                    >
                        {isExpanded ? <ChevronDown /> : <ChevronUp />}
                    </button>
                </div>
                {children}
            </div>
        </div>
    );
}
