'use client';

import { useState } from 'react';
import { MoreHorizontal, ArrowUpDown, Edit2 } from 'lucide-react';

interface InventoryItem {
    id: string;
    name: string;
    quantity: number;
    price: number;
    lastRestocked: string;
    status: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK';
}

interface InventoryTableProps {
    items: InventoryItem[];
}

export default function InventoryTable({ items }: InventoryTableProps) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
                <h3 className="text-lg font-bold text-slate-900">Inventory Items</h3>
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Search items..."
                        className="px-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors">
                        Add Item
                    </button>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-slate-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">Item Name</th>
                            <th className="px-6 py-4">
                                <div className="flex items-center gap-1 cursor-pointer hover:text-slate-700">
                                    Quantity <ArrowUpDown className="w-3 h-3" />
                                </div>
                            </th>
                            <th className="px-6 py-4">Price</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Last Restocked</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {items.map((item) => (
                            <tr key={item.id} className="hover:bg-slate-50/50 transition-colors group">
                                <td className="px-6 py-4 font-medium text-slate-900">{item.name}</td>
                                <td className="px-6 py-4 text-slate-600">{item.quantity}</td>
                                <td className="px-6 py-4 text-slate-600">${item.price.toFixed(2)}</td>
                                <td className="px-6 py-4">
                                    <span className={`
                    inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                    ${item.status === 'IN_STOCK' ? 'bg-emerald-100 text-emerald-800' : ''}
                    ${item.status === 'LOW_STOCK' ? 'bg-amber-100 text-amber-800' : ''}
                    ${item.status === 'OUT_OF_STOCK' ? 'bg-rose-100 text-rose-800' : ''}
                  `}>
                                        {item.status.replace('_', ' ')}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-slate-500">{item.lastRestocked}</td>
                                <td className="px-6 py-4 text-right">
                                    <button className="p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100">
                                        <Edit2 className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-between items-center text-xs text-slate-500">
                <span>Showing {items.length} items</span>
                <div className="flex gap-2">
                    <button className="px-3 py-1 border border-slate-200 rounded bg-white hover:bg-slate-50 disabled:opacity-50">Previous</button>
                    <button className="px-3 py-1 border border-slate-200 rounded bg-white hover:bg-slate-50">Next</button>
                </div>
            </div>
        </div>
    );
}
