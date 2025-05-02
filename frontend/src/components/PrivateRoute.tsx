// src/components/PrivateRoute.tsx
//import { ReactNode } from "react";
import { Navigate,Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function PrivateRoute() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  console.log("🔒 PrivateRoute:", isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return <Outlet />;

  //return <>{children}</>;
}
