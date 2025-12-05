'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { LogIn, ArrowLeft } from 'lucide-react';

const loginSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
    keepLogin: z.boolean().optional(),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
    const { login } = useAuth();
    const [error, setError] = useState<string | null>(null);
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormValues>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            keepLogin: true,
        },
    });

    const onSubmit = async (data: LoginFormValues) => {
        try {
            setError(null);
            await login(data);
        } catch (err: any) {
            setError(err.response?.data?.message || 'Login failed. Please check your credentials.');
        }
    };

    return (
        <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-orange-50 via-white to-orange-50 relative overflow-hidden py-8">
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
                                <LogIn className="w-8 h-8" />
                            </div>
                            <h2 className="text-3xl font-bold mb-4">Welcome Back!</h2>
                            <p className="text-orange-100 text-lg mb-8">
                                Sign in to discover local shops and find what you need nearby
                            </p>
                            <div className="space-y-4">
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Find Local Shops</h3>
                                        <p className="text-orange-100 text-sm">Discover stores in your area</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Track Availability</h3>
                                        <p className="text-orange-100 text-sm">Check product stock nearby</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <span className="text-xs">✓</span>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold">Save Time</h3>
                                        <p className="text-orange-100 text-sm">Shop smarter with NearBuy</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Side - Form */}
                    <div className="p-8 md:p-12 flex flex-col justify-center">
                        <div className="mb-8">
                            <h3 className="text-2xl font-bold text-slate-900">Sign In</h3>
                            <p className="text-sm text-slate-500 mt-1">Enter your credentials to continue</p>
                        </div>

                        <form className="space-y-5" onSubmit={handleSubmit(onSubmit)}>
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
                                    autoComplete="current-password"
                                    required
                                    className={`w-full px-3 py-2.5 text-sm border ${errors.password ? 'border-red-300' : 'border-slate-200'} rounded-xl focus:outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20 transition-all`}
                                    placeholder="••••••••"
                                    {...register('password')}
                                />
                                {errors.password && (
                                    <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>
                                )}
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <input
                                        id="keep-login"
                                        type="checkbox"
                                        className="h-4 w-4 text-[#FF6B35] focus:ring-[#FF6B35] border-slate-300 rounded cursor-pointer"
                                        {...register('keepLogin')}
                                    />
                                    <label htmlFor="keep-login" className="ml-2 block text-xs text-slate-600 cursor-pointer select-none">
                                        Remember me
                                    </label>
                                </div>

                                <div className="text-xs">
                                    <a href="#" className="font-medium text-[#FF6B35] hover:underline">
                                        Forgot password?
                                    </a>
                                </div>
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
                                {isSubmitting ? 'Signing in...' : 'Sign In'}
                            </button>

                            <div className="text-center pt-2">
                                <p className="text-xs text-slate-500">
                                    Don't have an account?{' '}
                                    <Link href="/signup/user" className="font-bold text-[#FF6B35] hover:underline">
                                        Create one now
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
