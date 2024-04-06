import { getSession } from "@/actions"
import LoginForm from "@/components/loginForm"
import { redirect } from "next/navigation"

const LoginPage = async () => {  
  const session = await getSession()

  if(session.isLoggedIn){
    redirect("/")
  }
  return (
    <div className="login">
      <h1>Чтобы получить права преподавателя, войдите</h1>
      <LoginForm/>
    </div>
  )
}

export default LoginPage