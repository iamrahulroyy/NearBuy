'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '@/services/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { UserRole } from '@/types/auth';
import { UserPlus, ArrowLeft } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

const signupSchema = z.object({
    fullName: z.string().min(2, 'Full name is required'),
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type SignupFormValues = z.infer<typeof signupSchema>;

export default function UserSignupPage() {
    const router = useRouter();
    const { checkAuth } = useAuth();
    const [error, setError] = useState<string | null>(null);
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<SignupFormValues>({
        resolver: zodResolver(signupSchema),
    });

    const onSubmit = async (data: SignupFormValues) => {
        try {
            setError(null);
            await api.post('/users/signup/user', {
                ...data,
                role: UserRole.USER,
            });
            // After successful signup, check auth to update context
            await checkAuth();
            // Redirect to home for regular users
            router.push('/');
        } catch (err: any) {
            setError(err.response?.data?.message || 'Signup failed. Please try again.');
        }
    };

    return (
        <div className="h-screen flex items-center justify-center bg-gradient-to-br from-orange-50 via-white to-orange-50 relative overflow-hidden">
            {/* Decorative Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute -top-[20%] -right-[10%] w-[500px] h-[500px] bg-orange-200/30 rounded-full blur-3xl"></div>
                <div className="absolute -bottom-[20%] -left-[10%] w-[500px] h-[500px] bg-orange-100/40 rounded-full blur-3xl"></div>
            </div>

            {/* Back Button */}
            <Link href="/" className="absolute top-6 left-6 flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors z-20">
                <ArrowLeft className="w-5 h-5" />
                <span className="font-medium">Back</span>
            </Link>

            <div className="max-w-5xl w-full mx-4 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl relative z-10 border border-white/50 overflow-hidden">
                <div className="grid md:grid-cols-2 gap-0">
                    {/* Left Side - Branding */}
                    <div className="hidden md:flex flex-col justify-center p-12 bg-gradient-to-br from-[#FF6B35] to-[#FF8A65] text-white relative overflow-hidden">
                        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
                        <div className="relative z-10">
                            <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mb-6">
                                <UserPlus className="w-8 h-8" />
                            </div>
                            <h2 className="text-3xl font-bold mb-4">Join NearBuy</h2>
                            <p className="text-orange-100 text-lg mb-8">
                                Create your account and discover shops in your neighborhood
                            </p>
                            <div className="space-y-4">
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Quick & Easy</h3>
                                        <p className="text-orange-100 text-sm">Sign up in seconds</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Find Nearby</h3>
                                        <p className="text-orange-100 text-sm">Search local inventories</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Save Time</h3>
                                        <p className="text-orange-100 text-sm">Shop smarter locally</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Side - Form */}
                    <div className="p-8 md:p-12 flex flex-col justify-center">
                        <div className="mb-8">
                            <h3 className="text-2xl font-bold text-slate-900">Create Account</h3>
                            <p className="text-sm text-slate-500 mt-1">Fill in your details to get started</p>
                        </div>

                        <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
                            <div>
                                <label htmlFor="fullName" className="block text-xs font-semibold text-slate-700 mb-1">
                                    Full Name
                                </label>
                                <input
                                    id="fullName"
                                    type="text"
                                    required
                                    className={`w-full px-3 py-2.5 text-sm border ${errors.fullName ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20 transition-all`}
                                    placeholder="John Doe"
                                    {...register('fullName')}
                                />
                                {errors.fullName && (
                                    <p className="mt-1 text-xs text-red-500">{errors.fullName.message}</p>
                                )}
                            </div>
                            <div>
                                <label htmlFor="email-address" className="block text-xs font-semibold text-slate-700 mb-1">
                                    Email address
                                </label>
                                <input
                                    id="email-address"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    className={`w-full px-3 py-2.5 text-sm border ${errors.email ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20 transition-all`}
                                    placeholder="you@example.com"
                                    {...register('email')}
                                />
                                {errors.email && (
                                    <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>
                                )}
                            </div>
                            <div>
                                <label htmlFor="password" className="block text-xs font-semibold text-slate-700 mb-1">
                                    Password
                                </label>
                                <input
                                    id="password"
                                    type="password"
                                    autoComplete="new-password"
                                    required
                                    className={`w-full px-3 py-2.5 text-sm border ${errors.password ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20 transition-all`}
                                    placeholder="••••••••"
                                    {...register('password')}
                                />
                                {errors.password && (
                                    <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>
                                )}
                            </div>

                            {error && (
                                <div className="rounded-xl bg-red-50 p-3 border border-red-100">
                                    <p className="text-xs text-red-800 font-medium">{error}</p>
                                </div>
                            )}

                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full py-3 px-4 bg-[#FF6B35] hover:bg-[#e55a2b] text-white text-sm font-bold rounded-xl transition-all disabled:opacity-70 shadow-sm hover:shadow-md"
                            >
                                {isSubmitting ? 'Creating account...' : 'Sign Up'}
                            </button>

                            <div className="text-center pt-2">
                                <p className="text-xs text-slate-500">
                                    Already have an account?{' '}
                                    <Link href="/login" className="font-bold text-[#FF6B35] hover:underline">
                                        Sign in
                                    </Link>
                                </p>
                                <p className="text-xs text-slate-400 mt-2">
                                    Want to sell?{' '}
                                    <Link href="/signup/vendor" className="font-medium text-slate-500 hover:text-[#FF6B35]">
                                        Vendor Signup
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
