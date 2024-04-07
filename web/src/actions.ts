"use server";

import { sessionOptions, SessionData, defaultSession } from "@/lib";
import { getIronSession } from "iron-session";
import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

let isBlocked = true;

export const getSession = async () => {
  const session = await getIronSession<SessionData>(cookies(), sessionOptions);

  if (!session.isLoggedIn) {
    session.isLoggedIn = defaultSession.isLoggedIn;
  }
  session.isBlocked = isBlocked;

  return session;
};

export const login = async (
  prevState: { error: undefined | string },
  formData: FormData
) => {
  const session = await getSession();

  const formEmail = formData.get("email") as string;
  const formPassword = formData.get("password") as string;

  let response = await fetch('http://127.0.0.1:8000/teachers/login/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `username=${formEmail}&password=${formPassword}`
  });

  let response_json = await response.json()

  if (response.status == 422){
    return { error: "Неверный формат почты" };
  }
  else if (response.status != 200) {
    return { error: "Неверные данные" };
  }

  let response_me = await fetch('http://127.0.0.1:8000/teachers/me', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `${response_json['token_type']} ${response_json['access_token']}`
    },
  });

  session.bearer = response_json['token_type']
  session.token = response_json['access_token']

  response_json = await response_me.json()

  session.userId = response_json['id'];
  session.username = formEmail;
  session.isLoggedIn = true;

  await session.save();
  redirect("/");
};

export const logout = async () => {
  const session = await getSession();
  session.destroy();
  redirect("/");
};

export const create_teacher = async (
  prevState: { error: undefined | string },
  formData: FormData
) => {

  const formEmail = formData.get("email") as string;
  const formPassword = formData.get("password") as string;
  const formFirstName = formData.get("name") as string;
  const formLastname = formData.get("surname") as string;

  let user = {
    'email': formEmail,
    'firstname': formFirstName,
    'lastname': formLastname,
    'password': formPassword,
  };

  let response = await fetch('http://127.0.0.1:8000/teachers/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify(user)
  });

  if (response.status == 422){
    return { error: "Неверная почта" };
  }
  else if (response.status != 200) {
    return { error: "Преподаватель с таким email существует" };
  }

  redirect("/");
};

export const edit_lecture = async(  
  prevState: { error: undefined | string },
  formData: FormData
  ) => {
  const formName = formData.get("name") as string;
  const formText = formData.get("text") as string;
  const formVideo = formData.get("video");
  const formPdf = formData.get("pdf");

  let user = {
    'title': formName,
    'text_description': formText,
  };

  let response = await fetch(`http://127.0.0.1:8000/subjects/2/lectures/2`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify(user)
  });

}
export const delete_lecture = async(id:number, subject_id:number) => {
  let session = await getSession()
  let a = await fetch(`http://127.0.0.1:8000/subjects/${subject_id}/lectures/${id}`, {
    method: 'DELETE',
    headers: {
      'accept': 'application/json',
      'Authorization': `${session.bearer} ${session.token}`
    },
  });
  console.log(a)
}
