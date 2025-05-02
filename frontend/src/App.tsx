// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import PrivateRoute from "./components/PrivateRoute";

import Home   from "./pages/Home";
import Quiz   from "./pages/Quiz";
import Result from "./pages/Result";
import Login  from "./pages/Login";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* 1. こちらは常に開放 */}
          <Route path="/login" element={<Login />} />

          {/* 2. ここから下は認証必須 */}
          <Route element={<PrivateRoute/>}>
            <Route index element={<Home />} />        {/* path="/" */}
            <Route path="quiz" element={<Quiz />} />  {/* path="/quiz" */}
            <Route path="result" element={<Result />} />{/* path="/result" */}
          </Route>

          {/* 3. 上記以外は / へ */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
