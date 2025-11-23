'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '@/services/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { UserRole } from '@/types/auth';

const signupSchema = z.object({
    fullName: z.string().min(2, 'Full name is required'),
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type SignupFormValues = z.infer<typeof signupSchema>;

export default function UserSignupPage() {
    const router = useRouter();
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
            router.push('/login');
        } catch (err: any) {
            setError(err.response?.data?.message || 'Signup failed. Please try again.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 relative overflow-hidden">
            {/* Decorative Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-orange-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob"></div>
                <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-yellow-100 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
            </div>

            <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl shadow-2xl relative z-10 border border-slate-100">
                <div className="text-center">
                    <div className="flex justify-center mb-6">
                        <div className="w-16 h-16 bg-orange-50 rounded-full flex items-center justify-center">
                            <span className="text-3xl">👋</span>
                        </div>
                    </div>
                    <h2 className="text-3xl font-bold text-slate-900 tracking-tight">
                        Create Account
                    </h2>
                    <p className="mt-2 text-sm text-slate-500">
                        Join NearBuy to find shops near you
                    </p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
                    <div className="space-y-5">
                        <div>
                            <label htmlFor="fullName" className="block text-sm font-medium text-slate-700 mb-1">
                                Full Name
                            </label>
                            <input
                                id="fullName"
                                type="text"
                                required
                                className={`appearance-none block w-full px-4 py-3 border ${errors.fullName ? 'border-red-300 focus:ring-red-200' : 'border-slate-200 focus:ring-orange-100'} rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#FF6B35] focus:ring-4 transition-all duration-200`}
                                placeholder="John Doe"
                                {...register('fullName')}
                            />
                            {errors.fullName && (
                                <p className="mt-1 text-sm text-red-500 font-medium">{errors.fullName.message}</p>
                            )}
                        </div>
                        <div>
                            <label htmlFor="email-address" className="block text-sm font-medium text-slate-700 mb-1">
                                Email address
                            </label>
                            <input
                                id="email-address"
                                type="email"
                                autoComplete="email"
                                required
                                className={`appearance-none block w-full px-4 py-3 border ${errors.email ? 'border-red-300 focus:ring-red-200' : 'border-slate-200 focus:ring-orange-100'} rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#FF6B35] focus:ring-4 transition-all duration-200`}
                                placeholder="you@example.com"
                                {...register('email')}
                            />
                            {errors.email && (
                                <p className="mt-1 text-sm text-red-500 font-medium">{errors.email.message}</p>
                            )}
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">
                                Password
                            </label>
                            <input
                                id="password"
                                type="password"
                                autoComplete="new-password"
                                required
                                className={`appearance-none block w-full px-4 py-3 border ${errors.password ? 'border-red-300 focus:ring-red-200' : 'border-slate-200 focus:ring-orange-100'} rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#FF6B35] focus:ring-4 transition-all duration-200`}
                                placeholder="••••••••"
                                {...register('password')}
                            />
                            {errors.password && (
                                <p className="mt-1 text-sm text-red-500 font-medium">{errors.password.message}</p>
                            )}
                        </div>
                    </div>

                    {error && (
                        <div className="rounded-xl bg-red-50 p-4 border border-red-100 animate-shake">
                            <div className="flex">
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">{error}</h3>
                                </div>
                            </div>
                        </div>
                    )}

                    <div>
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="group relative w-full flex justify-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-[#FF6B35] hover:bg-[#e55a2b] focus:outline-none focus:ring-4 focus:ring-orange-500/30 disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-orange-500/30 hover:shadow-orange-500/40 hover:-translate-y-0.5 active:translate-y-0"
                        >
                            {isSubmitting ? (
                                <span className="flex items-center gap-2">
                                    <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Creating account...
                                </span>
                            ) : 'Sign Up'}
                        </button>
                    </div>

                    <div className="mt-6 text-center space-y-4">
                        <p className="text-sm text-slate-500">
                            Already have an account?{' '}
                            <Link href="/login" className="font-bold text-slate-900 hover:text-[#FF6B35] transition-colors">
                                Sign in
                            </Link>
                        </p>
                        <div className="border-t border-slate-100 pt-4">
                            <Link href="/signup/vendor" className="text-xs font-medium text-slate-400 hover:text-primary transition-colors">
                                Want to sell on NearBuy? Sign up as a Vendor
                            </Link>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
