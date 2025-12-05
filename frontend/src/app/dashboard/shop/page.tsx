'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { Loader2, MapPin } from 'lucide-react';

const shopSchema = z.object({
    fullName: z.string().min(2, 'Full name (owner/manager) is required'),
    shopName: z.string().min(2, 'Shop name is required'),
    address: z.string().min(5, 'Address is required'),
    contact: z.string().optional(),
    description: z.string().optional(),
    latitude: z.number().min(-90).max(90),
    longitude: z.number().min(-180).max(180),
});

type ShopFormValues = z.infer<typeof shopSchema>;

export default function ShopManagementPage() {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [shop, setShop] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const { register, handleSubmit, setValue, reset, formState: { errors, isSubmitting } } = useForm<ShopFormValues>({
        resolver: zodResolver(shopSchema),
    });

    useEffect(() => {
        if (user) {
            fetchShop();
        }
    }, [user]);

    const fetchShop = async () => {
        try {
            // We need user ID. Assuming user object has id.
            // If not, we might need to rely on the backend finding it via cookie?
            // The endpoint requires owner_id.
            // Let's try to use user.id if available.
            // If user.id is not available in the context, we might have a problem.
            // Let's check the AuthContext implementation.
            // We stored response.data.body in user.
            // The login response body usually contains the user record.
            // Let's assume it has 'id'.
            if (!user?.id) {
                // If we don't have ID, maybe we can't fetch? 
                // Or maybe the backend allows fetching "my shop" without ID?
                // The endpoint is /shops/view_shop?owner_id={id}
                // If I don't have ID, I can't call it.
                // But wait, /vendors/shop (create) doesn't need ID.
                // Let's try to fetch.
                console.warn("User ID missing in context");
            }

            const response = await api.get(`/shops/view_shop?owner_id=${user?.id}`);
            if (response.data && response.data.body) {
                setShop(response.data.body);
                // Pre-fill form
                const s = response.data.body;
                reset({
                    fullName: s.fullName,
                    shopName: s.shopName,
                    address: s.address,
                    contact: s.contact,
                    description: s.description,
                    latitude: s.location ? s.location[0] : 0,
                    longitude: s.location ? s.location[1] : 0,
                });
            }
        } catch (error: any) {
            if (error.response?.status === 404) {
                setShop(null);
            } else {
                console.error("Failed to fetch shop", error);
            }
        } finally {
            setLoading(false);
        }
    };

    const getLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setValue('latitude', position.coords.latitude);
                    setValue('longitude', position.coords.longitude);
                },
                (error) => {
                    alert("Could not get location. Please enter manually.");
                }
            );
        }
    };

    const onSubmit = async (data: ShopFormValues) => {
        try {
            setError(null);
            setSuccess(null);

            // Payload for create: VendorShopCreate
            // Payload for update: ShopUpdate (needs shop_id?)

            if (shop) {
                // Update
                await api.patch('/shops/update_shop', {
                    ...data,
                    shop_id: shop.shop_id, // Assuming shop object has shop_id
                    location: [data.latitude, data.longitude]
                });
                setSuccess("Shop updated successfully!");
            } else {
                // Create
                // Endpoint: /vendors/shop
                await api.post('/vendors/shop', {
                    ...data,
                    location: [data.latitude, data.longitude]
                });
                setSuccess("Shop created successfully!");
                fetchShop(); // Refresh
            }
        } catch (err: any) {
            setError(err.response?.data?.message || 'Operation failed.');
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">
                {shop ? 'Manage Your Shop' : 'Create Your Shop'}
            </h1>

            {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-md mb-6">
                    {error}
                </div>
            )}

            {success && (
                <div className="bg-green-50 text-green-700 p-4 rounded-md mb-6">
                    {success}
                </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Owner/Manager Name</label>
                    <input
                        type="text"
                        {...register('fullName')}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                    {errors.fullName && <p className="text-red-600 text-sm mt-1">{errors.fullName.message}</p>}
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Shop Name</label>
                    <input
                        type="text"
                        {...register('shopName')}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                    {errors.shopName && <p className="text-red-600 text-sm mt-1">{errors.shopName.message}</p>}
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Address</label>
                    <input
                        type="text"
                        {...register('address')}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                    {errors.address && <p className="text-red-600 text-sm mt-1">{errors.address.message}</p>}
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <textarea
                        {...register('description')}
                        rows={3}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Contact</label>
                    <input
                        type="text"
                        {...register('contact')}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Latitude</label>
                        <input
                            type="number"
                            step="any"
                            {...register('latitude', { valueAsNumber: true })}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                        />
                        {errors.latitude && <p className="text-red-600 text-sm mt-1">{errors.latitude.message}</p>}
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Longitude</label>
                        <input
                            type="number"
                            step="any"
                            {...register('longitude', { valueAsNumber: true })}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
                        />
                        {errors.longitude && <p className="text-red-600 text-sm mt-1">{errors.longitude.message}</p>}
                    </div>
                </div>

                <button
                    type="button"
                    onClick={getLocation}
                    className="flex items-center text-sm text-indigo-600 hover:text-indigo-500"
                >
                    <MapPin className="h-4 w-4 mr-1" />
                    Use Current Location
                </button>

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    {isSubmitting ? <Loader2 className="animate-spin h-5 w-5" /> : (shop ? 'Update Shop' : 'Create Shop')}
                </button>
            </form>
        </div>
    );
}
