'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { Loader2, Plus, Edit, Trash } from 'lucide-react';

// Schemas
const addItemSchema = z.object({
    itemName: z.string().min(2, 'Item name is required'),
    price: z.number().min(0.01, 'Price must be greater than 0'),
    description: z.string().optional(),
    note: z.string().optional(),
});

const updateInventorySchema = z.object({
    quantity: z.number().min(0),
    min_quantity: z.number().optional(),
    max_quantity: z.number().optional(),
    status: z.enum(['IN_STOCK', 'OUT_OF_STOCK', 'LOW_STOCK']).optional(),
});

type AddItemFormValues = z.infer<typeof addItemSchema>;
type UpdateInventoryFormValues = z.infer<typeof updateInventorySchema>;

export default function ItemsInventoryPage() {
    const { user } = useAuth();
    const [shop, setShop] = useState<any>(null);
    const [inventory, setInventory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'items' | 'inventory'>('inventory');
    const [showAddModal, setShowAddModal] = useState(false);
    const [editingInventory, setEditingInventory] = useState<any>(null);

    // Forms
    const addItemForm = useForm<AddItemFormValues>({
        resolver: zodResolver(addItemSchema),
    });

    const updateInventoryForm = useForm<UpdateInventoryFormValues>({
        resolver: zodResolver(updateInventorySchema),
    });

    useEffect(() => {
        if (user?.id) {
            fetchShopAndInventory();
        }
    }, [user]);

    const fetchShopAndInventory = async () => {
        try {
            // 1. Get Shop
            const shopRes = await api.get(`/shops/view_shop?owner_id=${user?.id}`);
            if (shopRes.data && shopRes.data.body) {
                const shopData = shopRes.data.body;
                setShop(shopData);

                // 2. Get Inventory
                if (shopData.shop_id) {
                    const invRes = await api.get(`/inventory/shop/${shopData.shop_id}`);
                    if (invRes.data && invRes.data.body) {
                        setInventory(invRes.data.body);
                    }
                }
            }
        } catch (error) {
            console.error("Failed to fetch data", error);
        } finally {
            setLoading(false);
        }
    };

    const onAddItem = async (data: AddItemFormValues) => {
        try {
            const response = await api.post('/items/add_item', {
                ...data,
                shop_id: shop.shop_id
            });

            const newItem = response.data.body;

            if (newItem && newItem.id) {
                if (confirm("Item added! Do you want to add stock for this item now?")) {
                    // Open inventory modal for this new item
                    // We need to adapt the editingInventory state or create a new state for "adding inventory to item"
                    // Since our current modal is "Update Inventory" which assumes an existing inventory record (with inventory_id),
                    // we need to handle "Create Inventory" flow.
                    // The backend has POST /inventory/add

                    // Let's reuse the editing state but mark it as 'new'
                    setEditingInventory({
                        item_id: newItem.id,
                        shop_id: shop.shop_id,
                        quantity: 0,
                        isNew: true // Flag to distinguish
                    });
                    updateInventoryForm.reset({
                        quantity: 0,
                        min_quantity: 5,
                        max_quantity: 100,
                        status: 'IN_STOCK'
                    });
                }
            } else {
                alert("Item added, but ID was missing. Please refresh.");
            }

            setShowAddModal(false);
            addItemForm.reset();
        } catch (error: any) {
            alert(error.response?.data?.message || "Failed to add item");
        }
    };

    const onUpdateInventory = async (data: UpdateInventoryFormValues) => {
        if (!editingInventory) return;
        try {
            if (editingInventory.isNew) {
                // Create new inventory
                await api.post('/inventory/add', {
                    shop_id: editingInventory.shop_id,
                    item_id: editingInventory.item_id,
                    ...data
                });
            } else {
                // Update existing
                await api.patch('/inventory/update', {
                    inventory_id: editingInventory.inventory_id,
                    ...data
                });
            }
            setEditingInventory(null);
            fetchShopAndInventory();
        } catch (error: any) {
            alert(error.response?.data?.message || "Failed to update inventory");
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!shop) return <div>Please create a shop first.</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">Items & Inventory</h1>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                    <Plus className="h-4 w-4 mr-2" />
                    Add New Item
                </button>
            </div>

            {/* Inventory List */}
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                    {inventory.map((inv) => (
                        <li key={inv.inventory_id} className="px-4 py-4 sm:px-6">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-indigo-600 truncate">
                                        Item ID: {inv.item_id}
                                    </p>
                                    <p className="text-sm text-gray-500">
                                        Quantity: {inv.quantity} | Status: {inv.status}
                                    </p>
                                </div>
                                <div className="flex space-x-2">
                                    <button
                                        onClick={() => {
                                            setEditingInventory(inv);
                                            updateInventoryForm.reset({
                                                quantity: inv.quantity,
                                                min_quantity: inv.min_quantity,
                                                max_quantity: inv.max_quantity,
                                                status: inv.status
                                            });
                                        }}
                                        className="p-2 text-gray-400 hover:text-gray-500"
                                    >
                                        <Edit className="h-5 w-5" />
                                    </button>
                                </div>
                            </div>
                        </li>
                    ))}
                    {inventory.length === 0 && (
                        <li className="px-4 py-4 text-center text-gray-500">
                            No inventory found. Add items to see them here (requires backend fix).
                        </li>
                    )}
                </ul>
            </div>

            {/* Add Item Modal */}
            {showAddModal && (
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg max-w-md w-full p-6">
                        <h3 className="text-lg font-medium mb-4">Add New Item</h3>
                        <form onSubmit={addItemForm.handleSubmit(onAddItem)} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Item Name</label>
                                <input type="text" {...addItemForm.register('itemName')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                                {addItemForm.formState.errors.itemName && <p className="text-red-600 text-sm">{addItemForm.formState.errors.itemName.message}</p>}
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Price</label>
                                <input type="number" step="0.01" {...addItemForm.register('price', { valueAsNumber: true })} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                                {addItemForm.formState.errors.price && <p className="text-red-600 text-sm">{addItemForm.formState.errors.price.message}</p>}
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Description</label>
                                <textarea {...addItemForm.register('description')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                            </div>
                            <div className="flex justify-end space-x-3 mt-6">
                                <button type="button" onClick={() => setShowAddModal(false)} className="px-4 py-2 text-gray-700 hover:text-gray-900">Cancel</button>
                                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">Add Item</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Edit Inventory Modal */}
            {editingInventory && (
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg max-w-md w-full p-6">
                        <h3 className="text-lg font-medium mb-4">Update Inventory</h3>
                        <form onSubmit={updateInventoryForm.handleSubmit(onUpdateInventory)} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Quantity</label>
                                <input type="number" {...updateInventoryForm.register('quantity', { valueAsNumber: true })} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Min Qty</label>
                                    <input type="number" {...updateInventoryForm.register('min_quantity', { valueAsNumber: true })} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Max Qty</label>
                                    <input type="number" {...updateInventoryForm.register('max_quantity', { valueAsNumber: true })} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                                </div>
                            </div>
                            <div className="flex justify-end space-x-3 mt-6">
                                <button type="button" onClick={() => setEditingInventory(null)} className="px-4 py-2 text-gray-700 hover:text-gray-900">Cancel</button>
                                <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">Update</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
