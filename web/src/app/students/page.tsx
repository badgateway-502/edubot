import { getSession } from "@/actions";
import Link from "next/link";
import { redirect } from "next/navigation";

const StudentsPage = async () => {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect("/login");
  }

  const students = [
    [0, 'Миша Стркнников'],
    [1, 'Павел Стркнников'],
    [2, 'Дмитрий Скрынник'],
    [3, 'Владимир Сыктывкар'],
  ]

  const student_list = students.map((student) => {
    return (
      <li key={student[0]} style={{listStyleType: 'none'}}>
          <Link href={'students/' + student[0]}>{student[1]}</Link>
      </li>
  )
  })

  return (
    <div className="table_of">
      <ul>
        {student_list}
      </ul>
    </div>
  );
};

export default StudentsPage;
