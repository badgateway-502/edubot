import { logout } from "@/actions"

const LogoutForm = () => {
  return (
    <form action={logout}>
      <button>Выйти</button>
    </form>
  )
}

export default LogoutForm