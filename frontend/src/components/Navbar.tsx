'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types/auth';
import { Menu, X, ShoppingBag, User, LogOut, ChevronDown } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const [isOpen, setIsOpen] = useState(false);

    const isVendorOrAdmin = user?.role === UserRole.VENDOR || user?.role === UserRole.ADMIN;

    return (
        <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    {/* Logo */}
                    <div className="flex-shrink-0 flex items-center gap-1">
                        <div className="flex flex-col justify-center h-full">
                            <div className="space-y-1.5 cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
                                <div className="w-6 h-0.5 bg-slate-800"></div>
                                <div className="w-4 h-0.5 bg-slate-800"></div>
                                <div className="w-6 h-0.5 bg-slate-800"></div>
                            </div>
                        </div>
                        <Link href="/" className="ml-4 flex items-center">
                            <span className="text-2xl font-bold text-slate-900 tracking-tight">NearBuy</span>
                            <span className="text-3xl text-primary leading-none">.</span>
                        </Link>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        <Link href="/" className="text-slate-600 hover:text-primary text-sm font-medium transition-colors relative group">
                            Explore
                            <span className="absolute -bottom-1 left-1/2 w-0 h-0.5 bg-primary transition-all group-hover:w-full group-hover:left-0"></span>
                        </Link>
                        <Link href="/categories" className="text-slate-600 hover:text-primary text-sm font-medium transition-colors">
                            Categories
                        </Link>
                        <Link href="/shops" className="text-slate-600 hover:text-primary text-sm font-medium transition-colors">
                            Shops
                        </Link>
                        <Link href="/about" className="text-slate-600 hover:text-primary text-sm font-medium transition-colors">
                            About us
                        </Link>
                    </div>

                    {/* Right Side Actions */}
                    <div className="hidden md:flex items-center space-x-6">
                        {isAuthenticated ? (
                            <div className="flex items-center gap-4">
                                <div className="flex items-center gap-1 text-slate-700 text-sm font-medium cursor-pointer hover:text-[#E50914] transition-colors">
                                    <span>{user?.fullName}</span>
                                    <ChevronDown className="w-4 h-4" />
                                </div>
                                <button onClick={() => logout()} className="text-slate-400 hover:text-slate-600">
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </div>
                        ) : (
                            <Link href="/login" className="flex items-center gap-2 bg-[#E50914] hover:bg-red-700 text-white text-sm font-bold px-6 py-2.5 rounded-full shadow-lg shadow-red-500/20 transition-all hover:scale-105 active:scale-95">
                                <User className="w-4 h-4" />
                                Account
                            </Link>
                        )}

                        <div className="relative cursor-pointer">
                            <ShoppingBag className="w-6 h-6 text-slate-700" />
                            <span className="absolute -top-1 -right-1 bg-primary text-white text-[10px] font-bold w-4 h-4 flex items-center justify-center rounded-full border-2 border-white">
                                1
                            </span>
                        </div>

                        <button className="bg-[#E50914] hover:bg-red-700 text-white text-sm font-bold px-6 py-2.5 rounded-full shadow-lg shadow-red-500/20 transition-all hover:scale-105 active:scale-95">
                            Confirm order
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="inline-flex items-center justify-center p-2 rounded-md text-slate-700 hover:text-primary focus:outline-none"
                        >
                            {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden bg-white border-t border-slate-100 absolute w-full shadow-xl">
                    <div className="px-4 pt-2 pb-4 space-y-1">
                        <Link href="/" className="block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md">
                            Explore
                        </Link>
                        <Link href="/categories" className="block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md">
                            Categories
                        </Link>
                        <Link href="/shops" className="block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md">
                            Shops
                        </Link>
                        {isAuthenticated ? (
                            <button onClick={() => logout()} className="w-full text-left block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md">
                                Logout
                            </button>
                        ) : (
                            <Link href="/login" className="block px-3 py-2 text-base font-medium text-slate-700 hover:text-primary hover:bg-slate-50 rounded-md">
                                Login
                            </Link>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
