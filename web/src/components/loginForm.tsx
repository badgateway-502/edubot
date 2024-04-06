"use client";

import { login } from "@/actions";
import { useFormState } from "react-dom";

const LoginForm = () => {
  const [state, formAction] = useFormState<any, FormData>(login, undefined);

  return (
    <form action={formAction}>
      <input type="email" name="email" required placeholder="Email" />
      <input type="password" name="password" required placeholder="Пароль" />
      <button>Войти</button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
};

export default LoginForm;
