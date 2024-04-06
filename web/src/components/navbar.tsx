import Link from "next/link"
import LogoutForm from "./logoutForm"
import { getSession } from "@/actions"

const Navbar = async () => {
  const session = await getSession()

  return (
    <nav>
      <Link href="/">Главная</Link>
      <Link href="/students">Ученики</Link>
      <Link href="/subjects">Предметы</Link>
      <Link href="/create_teacher">Добавить преподавателя</Link>
      {!session.isLoggedIn && <Link href="/login">Войти</Link>}
      {session.isLoggedIn && <LogoutForm/>}
    </nav>
  )
}

export default Navbar