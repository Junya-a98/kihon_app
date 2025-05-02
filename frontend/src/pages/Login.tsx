// frontend/src/pages/Login.tsx
import { useState, } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { useAuth } from "../contexts/AuthContext"


export default function Login() {
 
  const { login } = useAuth()
  const nav = useNavigate()

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    console.log("▶️ handleSubmit start", { username, password });
    try {
      const res = await axios.post("/api/token/", { username, password })
      console.log("✅ token response", res.data);
      await login(res.data.access, res.data.refresh)
      console.log("▶️ after login(), user should be set");
      //console.log(nav)
      nav("/", { replace: true });  // ホームへリダイレクト

    } catch (err) {
      console.error("❌ login failed", err);
      alert("ログインに失敗しました")
      console.error(err)
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>ログイン</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            ユーザー名:
            <input
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
          </label>
        </div>
        <div style={{ marginTop: 8 }}>
          <label>
            パスワード:
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit" style={{ marginTop: 12 }}>
          ログイン
        </button>
      </form>
    </div>
  )
}
