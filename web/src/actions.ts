"use server";

import { sessionOptions, SessionData, defaultSession } from "@/lib";
import { getIronSession } from "iron-session";
import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

let email = "john@com";
let password = "1";
let isPro = true;
let isBlocked = true;

export const getSession = async () => {
  const session = await getIronSession<SessionData>(cookies(), sessionOptions);

  if (!session.isLoggedIn) {
    session.isLoggedIn = defaultSession.isLoggedIn;
  }

  // CHECK THE USER IN THE DB
  session.isBlocked = isBlocked;
  session.isPro = isPro;

  return session;
};

export const login = async (
  prevState: { error: undefined | string },
  formData: FormData
) => {
  const session = await getSession();

  const formEmail = formData.get("email") as string;
  const formPassword = formData.get("password") as string;

  // CHECK USER IN THE DB
  // const user = await db.getUser({email,password})

  if (formEmail !== email || formPassword !== password) {
    return { error: "Неверные данные" };
  }

  session.userId = "1";
  session.username = formEmail;
  session.isPro = isPro;
  session.isLoggedIn = true;

  await session.save();
  redirect("/");
};

export const logout = async () => {
  const session = await getSession();
  session.destroy();
  redirect("/");
};

// export const changePremium = async () => {
//   const session = await getSession();

//   isPro = !session.isPro;
//   session.isPro = isPro;
//   await session.save();
//   revalidatePath("/profile");
// };

// export const changeUsername = async (formData: FormData) => {
//   const session = await getSession();

//   const newUsername = formData.get("username") as string;

//   email = newUsername;

//   session.username = email;
//   await session.save();
//   revalidatePath("/profile");
// };


export const create_teacher = async (
  prevState: { error: undefined | string },
  formData: FormData
) => {

  const formEmail = formData.get("email") as string;
  const formPassword = formData.get("password") as string;

  // CHECK USER IN THE DB
  // const user = await db.getTeacher({email})
  const emails = ['john@com', 'polko@mail', 'vsesneshka@kool']

  if (emails.includes(formEmail)) {
    return { error: "Преподаватель с таким email существует" };
  }

  // POST to db
  // db.create(teacher())
  redirect("/");
};