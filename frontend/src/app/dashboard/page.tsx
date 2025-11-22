'use client';

import { Package, DollarSign, AlertTriangle, TrendingUp } from 'lucide-react';
import KPICard from '@/components/dashboard/KPICard';
import InventoryTable from '@/components/dashboard/InventoryTable';

interface InventoryItem {
    id: string;
    name: string;
    quantity: number;
    price: number;
    lastRestocked: string;
    status: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK';
}

const MOCK_INVENTORY: InventoryItem[] = [
    { id: '1', name: 'Organic Apples', quantity: 150, price: 4.99, lastRestocked: '2 days ago', status: 'IN_STOCK' },
    { id: '2', name: 'USB-C Cable', quantity: 20, price: 12.50, lastRestocked: '1 week ago', status: 'LOW_STOCK' },
    { id: '3', name: 'Sourdough Bread', quantity: 0, price: 3.50, lastRestocked: 'Yesterday', status: 'OUT_OF_STOCK' },
    { id: '4', name: 'Avocados', quantity: 45, price: 2.00, lastRestocked: '3 days ago', status: 'IN_STOCK' },
    { id: '5', name: 'Vitamins', quantity: 12, price: 15.00, lastRestocked: '2 weeks ago', status: 'LOW_STOCK' },
];

export default function DashboardPage() {
    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
                    <p className="text-slate-500 mt-1">Welcome back, here's what's happening with your store today.</p>
                </div>
                <div className="flex gap-3">
                    <button className="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50">
                        Export Report
                    </button>
                    <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 shadow-sm shadow-indigo-200">
                        + Add Product
                    </button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <KPICard
                    title="Total Products"
                    value="1,245"
                    trend={{ value: 12, isPositive: true }}
                    icon={Package}
                    color="indigo"
                />
                <KPICard
                    title="Total Stock Value"
                    value="$45,231.89"
                    trend={{ value: 8, isPositive: true }}
                    icon={DollarSign}
                    color="emerald"
                />
                <KPICard
                    title="Critical Low Stock"
                    value="15"
                    trend={{ value: 2, isPositive: false }}
                    icon={AlertTriangle}
                    color="rose"
                />
            </div>

            {/* Inventory Table */}
            <InventoryTable items={MOCK_INVENTORY} />
        </div>
    );
}
