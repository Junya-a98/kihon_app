// src/contexts/AuthContext.tsx
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
 } from "react";
 
 
 import {jwtDecode} from "jwt-decode";
 
 
 interface JwtPayload { username: string; exp?: number }
 interface AuthContextType {
  user: string | null;
  isAuthenticated: boolean;
  login: (access: string, refresh: string) => void;
  logout: () => void;
 }
 
 
 const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
 });
 
 
 export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
 
 
  const login = (access: string, refresh: string) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    try {
      const { username } = jwtDecode<JwtPayload>(access);
      setUser(username);
      setIsAuthenticated(true);
      console.log("✅ Authenticated as", username);
    } catch {
      setUser(null);
      setIsAuthenticated(false);
    }
  };
 
 
  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
    setIsAuthenticated(false);
  };
 
 
  // マウント時にトークンチェック
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      try {
        const { username } = jwtDecode<JwtPayload>(token);
        setUser(username);
        setIsAuthenticated(true);
      } catch {
        logout();
      }
    }
  }, []);
 
 
  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
 }
 
 
 export const useAuth = () => useContext(AuthContext);
 
 
 
 