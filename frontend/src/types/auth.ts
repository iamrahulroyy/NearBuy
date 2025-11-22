export enum UserRole {
    USER = 'USER',
    VENDOR = 'VENDOR',
    ADMIN = 'ADMIN',
    STATE_CONTRIBUTER = 'STATE_CONTRIBUTER',
}

export interface User {
    id: string;
    email: string;
    fullName: string;
    role: UserRole;
    shop_id?: string; // For vendors
}

export interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
}
