'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '@/services/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { UserRole } from '@/types/auth';
import { Store, ArrowLeft } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

const vendorSignupSchema = z.object({
    fullName: z.string().min(2, 'Full name is required'),
    shopName: z.string().min(2, 'Shop name is required'),
    address: z.string().min(5, 'Address is required'),
    contact: z.string().optional(),
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type VendorSignupFormValues = z.infer<typeof vendorSignupSchema>;

export default function VendorSignupPage() {
    const router = useRouter();
    const { checkAuth } = useAuth();
    const [error, setError] = useState<string | null>(null);
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<VendorSignupFormValues>({
        resolver: zodResolver(vendorSignupSchema),
    });

    const onSubmit = async (data: VendorSignupFormValues) => {
        try {
            setError(null);
            await api.post('/users/signup/vendor', {
                ...data,
                role: UserRole.VENDOR,
            });
            // After successful signup, check auth to update context
            await checkAuth();
            // Redirect to dashboard for vendors
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.message || 'Signup failed. Please try again.');
        }
    };

    return (
        <div className="h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-white to-blue-50 relative overflow-hidden">
            {/* Decorative Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute -top-[20%] -right-[10%] w-[500px] h-[500px] bg-purple-200/30 rounded-full blur-3xl"></div>
                <div className="absolute -bottom-[20%] -left-[10%] w-[500px] h-[500px] bg-blue-200/30 rounded-full blur-3xl"></div>
            </div>

            {/* Back Button */}
            <Link href="/" className="absolute top-6 left-6 flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors z-20">
                <ArrowLeft className="w-5 h-5" />
                <span className="font-medium">Back</span>
            </Link>

            <div className="max-w-5xl w-full mx-4 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl relative z-10 border border-white/50 overflow-hidden">
                <div className="grid md:grid-cols-2 gap-0">
                    {/* Left Side - Branding */}
                    <div className="hidden md:flex flex-col justify-center p-12 bg-gradient-to-br from-[#6366F1] to-[#8B5CF6] text-white relative overflow-hidden">
                        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
                        <div className="relative z-10">
                            <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mb-6">
                                <Store className="w-8 h-8" />
                            </div>
                            <h2 className="text-3xl font-bold mb-4">Become a Vendor</h2>
                            <p className="text-purple-100 text-lg mb-8">
                                Join NearBuy and reach thousands of customers in your area
                            </p>
                            <div className="space-y-4">
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Easy Setup</h3>
                                        <p className="text-purple-100 text-sm">Get started in minutes</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Local Customers</h3>
                                        <p className="text-purple-100 text-sm">Reach nearby shoppers</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Grow Your Business</h3>
                                        <p className="text-purple-100 text-sm">Increase your visibility</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Side - Form */}
                    <div className="p-8 md:p-10 flex flex-col justify-center">
                        <div className="mb-6">
                            <h3 className="text-2xl font-bold text-slate-900">Create Account</h3>
                            <p className="text-sm text-slate-500 mt-1">Fill in your details to get started</p>
                        </div>

                        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label htmlFor="fullName" className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                                    <input
                                        id="fullName"
                                        type="text"
                                        required
                                        className={`w-full px-3 py-2 text-sm border ${errors.fullName ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all`}
                                        placeholder="John Doe"
                                        {...register('fullName')}
                                    />
                                    {errors.fullName && <p className="mt-1 text-xs text-red-500">{errors.fullName.message}</p>}
                                </div>
                                <div>
                                    <label htmlFor="shopName" className="block text-xs font-semibold text-slate-700 mb-1">Shop Name</label>
                                    <input
                                        id="shopName"
                                        type="text"
                                        required
                                        className={`w-full px-3 py-2 text-sm border ${errors.shopName ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all`}
                                        placeholder="My Shop"
                                        {...register('shopName')}
                                    />
                                    {errors.shopName && <p className="mt-1 text-xs text-red-500">{errors.shopName.message}</p>}
                                </div>
                            </div>

                            <div>
                                <label htmlFor="address" className="block text-xs font-semibold text-slate-700 mb-1">Shop Address</label>
                                <input
                                    id="address"
                                    type="text"
                                    required
                                    className={`w-full px-3 py-2 text-sm border ${errors.address ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all`}
                                    placeholder="123 Main St, City"
                                    {...register('address')}
                                />
                                {errors.address && <p className="mt-1 text-xs text-red-500">{errors.address.message}</p>}
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label htmlFor="contact" className="block text-xs font-semibold text-slate-700 mb-1">Contact (Optional)</label>
                                    <input
                                        id="contact"
                                        type="text"
                                        className="w-full px-3 py-2 text-sm border border-slate-200 rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all"
                                        placeholder="+1 234 567 890"
                                        {...register('contact')}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="email-address" className="block text-xs font-semibold text-slate-700 mb-1">Email</label>
                                    <input
                                        id="email-address"
                                        type="email"
                                        required
                                        className={`w-full px-3 py-2 text-sm border ${errors.email ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all`}
                                        placeholder="you@example.com"
                                        {...register('email')}
                                    />
                                    {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
                                </div>
                            </div>

                            <div>
                                <label htmlFor="password" className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                                <input
                                    id="password"
                                    type="password"
                                    required
                                    className={`w-full px-3 py-2 text-sm border ${errors.password ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#6366F1] focus:ring-2 focus:ring-[#6366F1]/20 transition-all`}
                                    placeholder="••••••••"
                                    {...register('password')}
                                />
                                {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
                            </div>

                            {error && (
                                <div className="rounded-xl bg-red-50 p-3 border border-red-100">
                                    <p className="text-xs text-red-800 font-medium">{error}</p>
                                </div>
                            )}

                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full py-3 px-4 bg-[#E8E5FF] hover:bg-[#DDD8FF] text-[#6366F1] text-sm font-bold rounded-xl transition-all disabled:opacity-70 shadow-sm hover:shadow-md"
                            >
                                {isSubmitting ? 'Creating account...' : 'Sign Up as Vendor'}
                            </button>

                            <div className="text-center pt-2">
                                <p className="text-xs text-slate-500">
                                    Already have an account?{' '}
                                    <Link href="/login" className="font-bold text-[#6366F1] hover:underline">
                                        Sign in
                                    </Link>
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}
