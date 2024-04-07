import { getSession } from "@/actions";
import Link from "next/link";
import { redirect } from "next/navigation";

const StudentsPage = async () => {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect("/login");
  }

  let response = await fetch('http://127.0.0.1:8000/students/', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  let students: [] = await response.json()

  const student_list = students.map((student) => {
    return (
      <li key={student["id"]} style={{listStyleType: 'none'}}>
          <Link href={'students/' + student["id"]}>{student["firstname"]} {student["lastname"]}</Link>
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
