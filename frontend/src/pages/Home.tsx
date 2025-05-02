// frontend/src/pages/Home.tsx
//import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"

//console.log("hello0")

export default function Home() {
  //console.log("hello1")
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  console.log(user)

  return (
    <div style={{ padding: 20 }}>
      <header style={{ marginBottom: 20 }}>
      <span>こんにちは、{user ?? "ゲスト"} さん</span>
        <button
          onClick={() => {
            logout()
            navigate("/login", { replace: true })
          }}
          style={{ marginLeft: 12 }}
        >
          ログアウト
        </button>
      </header>
      <h1>基本情報演習</h1>
      <button
        onClick={() => navigate("/quiz")}
        style={{ marginTop: 20 }}
      >
        演習を始める
      </button>
    </div>
  )
}
