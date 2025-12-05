'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types/auth';
import { Menu, X, ShoppingBag, User, LogOut, ChevronDown, Github } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const [isOpen, setIsOpen] = useState(false);

    const isVendorOrAdmin = user?.role === UserRole.VENDOR || user?.role === UserRole.ADMIN;

    return (
        <nav className="bg-white sticky top-0 z-50 border-b border-gray-100 pr-[6px]">
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
                        {/* GitHub Link */}
                        <a
                            href="https://github.com/iamrahulroyy/NearBuy"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-500 hover:text-gray-900 transition-colors p-2 hover:bg-gray-100 rounded-full"
                            title="View on GitHub"
                        >
                            <Github className="w-5 h-5" />
                        </a>
                        {isAuthenticated ? (
                            <div className="flex items-center gap-4">
                                {isVendorOrAdmin && (
                                    <Link href="/dashboard" className="flex items-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 text-sm font-medium px-4 py-2 rounded-full transition-all">
                                        <ShoppingBag className="w-4 h-4" />
                                        Dashboard
                                    </Link>
                                )}
                                <div className="flex items-center gap-1 text-gray-700 text-sm font-medium cursor-pointer hover:text-black transition-colors">
                                    <span>{user?.fullName}</span>
                                    <ChevronDown className="w-4 h-4" />
                                </div>
                                <button onClick={() => logout()} className="text-gray-400 hover:text-gray-600">
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </div>
                        ) : (
                            <div className="flex items-center gap-3">
                                <Link href="/login" className="flex items-center gap-2 text-gray-700 hover:text-black text-sm font-medium px-4 py-2 rounded-full hover:bg-gray-50 transition-all">
                                    <User className="w-4 h-4" />
                                    Login
                                </Link>
                                <Link href="/signup/vendor" className="flex items-center gap-2 bg-[#E8E5FF] hover:bg-[#DDD8FF] text-[#6366F1] text-sm font-medium px-5 py-2 rounded-full transition-all shadow-sm hover:shadow-md">
                                    <ShoppingBag className="w-4 h-4" />
                                    Vendor
                                </Link>
                            </div>
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
                        <Link href="/" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Explore
                        </Link>
                        <Link href="/categories" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Categories
                        </Link>
                        <Link href="/shops" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            Shops
                        </Link>
                        <Link href="/about" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                            About us
                        </Link>
                        {isAuthenticated ? (
                            <>
                                {isVendorOrAdmin && (
                                    <Link href="/dashboard" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-indigo-600 bg-indigo-50 rounded-md">
                                        Dashboard
                                    </Link>
                                )}
                                <button onClick={() => { logout(); setIsOpen(false); }} className="w-full text-left block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link href="/login" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md">
                                    Login
                                </Link>
                                <Link href="/signup/vendor" onClick={() => setIsOpen(false)} className="block px-3 py-2 text-base font-medium text-[#6366F1] bg-[#E8E5FF] hover:bg-[#DDD8FF] rounded-md transition-colors font-semibold">
                                    Vendor Signup
                                </Link>
                            </>
                        )}
                        <a
                            href="https://github.com/iamrahulroyy/NearBuy"
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={() => setIsOpen(false)}
                            className="flex items-center gap-2 px-3 py-2 text-base font-medium text-gray-700 hover:text-black hover:bg-gray-50 rounded-md"
                        >
                            <Github className="w-5 h-5" />
                            <span>Star on GitHub</span>
                        </a>
                    </div>
                </div>
            )}
            {/* Modern Glassy Liquid Line */}
            <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gray-100 overflow-visible">
                <div className="absolute -bottom-[1px] left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-[#FF6B35]/40 to-transparent blur-[1px]"></div>
                <div className="absolute -bottom-4 left-0 w-full h-8 bg-gradient-to-r from-transparent via-[#FF6B35]/5 to-transparent blur-xl opacity-0 hover:opacity-100 transition-opacity duration-700"></div>
            </div>
        </nav>
    );
};

export default Navbar;
