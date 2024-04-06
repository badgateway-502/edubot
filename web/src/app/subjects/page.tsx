import { getSession } from "@/actions";
import { redirect } from "next/navigation";
import Link from "next/link";

const ProfilePage = async () => {
  const session = await getSession();

  if(!session.isLoggedIn){
    redirect("/login")
  }

  const subjects = [
    [0, 'Математика'],
    [1, 'Философия'],
    [2, 'Ядерная Физика'],
    [3, 'Линейная алгкбра'],
  ]

  const subjects_list = subjects.map((subject) => {
    return (
      <li key={subject[0]} style={{listStyleType: 'none'}}>
          <Link href={'subjects/' + subject[0]}>{subject[1]}</Link>
      </li>
  )
  })

  return (
    <div className="table_of">
      <ul>
        {subjects_list}
      </ul>
    </div>
  );
};

export default ProfilePage;
