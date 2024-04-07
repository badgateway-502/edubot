"use client";

import { create_teacher } from "@/actions";
import { useFormState } from "react-dom";

const CreateTeacherForm = () => {
  const [state, formAction] = useFormState<any, FormData>(create_teacher, undefined);

  return (
    <form action={formAction}>
      <input type="text" name="name" required placeholder="Имя" />
      <input type="text" name="surname" required placeholder="Фамилия" />
      <input type="email" name="email" required placeholder="Email" />
      <input type="password" name="password" required placeholder="Пароль" />
      <button>Добавить</button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
};

export default CreateTeacherForm;
