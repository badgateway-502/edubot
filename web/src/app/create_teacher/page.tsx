import { getSession } from "@/actions";
import Link from "next/link";
import { redirect } from "next/navigation";
import CreateTeacherForm from "@/components/CreateTeacherForm";

const PremiumPage = async () => {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect("/login");
  }

  return (
    <div className="create_teacher">
      <h1>Создайте аккаунт для преподавателя</h1>
      <CreateTeacherForm/>
    </div>
  );
};

export default PremiumPage;
