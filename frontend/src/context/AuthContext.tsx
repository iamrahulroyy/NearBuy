'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '@/services/api';
import { AuthState, User, UserRole } from '@/types/auth';
import { useRouter, usePathname } from 'next/navigation';

interface AuthContextType extends AuthState {
    login: (data: any) => Promise<void>;
    logout: () => Promise<void>;
    checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [state, setState] = useState<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: true,
    });
    const router = useRouter();
    const pathname = usePathname();

    const checkAuth = async () => {
        try {
            const response = await api.get('/users/auth');
            if (response.data && response.data.body) {
                setState({
                    user: response.data.body,
                    isAuthenticated: true,
                    isLoading: false,
                });
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            setState({
                user: null,
                isAuthenticated: false,
                isLoading: false,
            });
        }
    };

    const login = async (data: any) => {
        try {
            await api.post('/users/login', data);
            await checkAuth();
            router.push('/');
        } catch (error) {
            console.error('Login failed', error);
            throw error;
        }
    };

    const logout = async () => {
        try {
            await api.post('/users/logout');
            setState({
                user: null,
                isAuthenticated: false,
                isLoading: false,
            });
            router.push('/login');
        } catch (error) {
            console.error('Logout failed', error);
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <AuthContext.Provider value={{ ...state, login, logout, checkAuth }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
