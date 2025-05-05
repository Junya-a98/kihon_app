// frontend/src/pages/Register.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import styles from "./css/Register.module.css";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post("/api/register/", { username, password, email });
      alert("登録が完了しました。ログインページへ移動します。");
      navigate("/login", { replace: true });
    } catch (err:any) {
        console.error("registration failed", err.response?.data);
        alert("登録に失敗しました：" + JSON.stringify(err.response?.data));
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>
        基本情報技術者試験対策アプリ
        <br />
        新規登録
      </h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <label className={styles.label}>
          ユーザー名
          <input
            className={styles.input}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label className={styles.label}>
          メールアドレス
          <input
            type="email"
            className={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label className={styles.label}>
          パスワード
          <input
            type="password"
            className={styles.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit" className={styles.button}>
          登録
        </button>
      </form>
    </div>
);
}
