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
        <nav className="bg-white sticky top-0 z-50 border-b border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Left Side: Logo + Browse */}
                    <div className="flex items-center gap-8">
                        {/* Logo */}
                        <div className="flex-shrink-0 flex items-center">
                            <Link href="/" className="flex items-center">
                                <span className="text-2xl font-bold text-black tracking-tight">NearBuy.</span>
                            </Link>
                        </div>

                        {/* Desktop Navigation */}
                        <div className="hidden md:flex items-center space-x-8">
                            <Link href="/" className="text-gray-500 hover:text-black text-sm font-medium transition-colors">
                                Explore
                            </Link>
                            <Link href="/categories" className="text-gray-500 hover:text-black text-sm font-medium transition-colors">
                                Categories
                            </Link>
                            <Link href="/shops" className="text-gray-500 hover:text-black text-sm font-medium transition-colors">
                                Shops
                            </Link>
                            <Link href="/about" className="text-gray-500 hover:text-black text-sm font-medium transition-colors">
                                About us
                            </Link>
                        </div>
                    </div>

                    {/* Right Side Actions */}
                    <div className="hidden md:flex items-center space-x-4">
                        {isAuthenticated ? (
                            <div className="flex items-center gap-4">
                                <div className="flex items-center gap-1 text-gray-700 text-sm font-medium cursor-pointer hover:text-black transition-colors">
                                    <span>{user?.fullName}</span>
                                    <ChevronDown className="w-4 h-4" />
                                </div>
                                <button onClick={() => logout()} className="text-gray-400 hover:text-gray-600">
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </div>
                        ) : (
                            <Link href="/login" className="flex items-center gap-2 bg-white border border-gray-200 hover:bg-gray-50 text-black text-sm font-medium px-5 py-2 rounded-full transition-all">
                                <User className="w-4 h-4" />
                                Account
                            </Link>
                        )}
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-black focus:outline-none"
                        >
                            {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden bg-white border-t border-gray-100 absolute w-full shadow-xl">
                    <div className="px-4 pt-2 pb-4 space-y-1">
                        <Link href="/" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Explore
                        </Link>
                        <Link href="/categories" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Categories
                        </Link>
                        <Link href="/shops" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Shops
                        </Link>
                        <Link href="/about" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            About us
                        </Link>
                        {isAuthenticated ? (
                            <button onClick={() => logout()} className="w-full text-left block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                                Logout
                            </button>
                        ) : (
                            <Link href="/login" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
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
