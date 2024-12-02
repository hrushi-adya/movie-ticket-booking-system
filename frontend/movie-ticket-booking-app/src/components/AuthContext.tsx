import React, { createContext, useContext, useState } from 'react';

interface AuthContextType {
    isLoggedIn: boolean;
    username?: string;
    userType?: string;
    login: (username: string, userType: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState<string | undefined>(undefined);
    const [userType, setUserType] = useState<string | undefined>(undefined);

    const login = (username: string, userType: string) => {
        setIsLoggedIn(true);
        setUsername(username);
        setUserType(userType);
    };

    const logout = () => {
        setIsLoggedIn(false);
        setUsername(undefined);
        setUserType(undefined);
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, username, userType, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
