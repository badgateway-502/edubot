import { getSession } from "@/actions";
import { redirect } from "next/navigation";
import Link from "next/link";

const ProfilePage = async () => {
  const session = await getSession();

  if(!session.isLoggedIn){
    redirect("/login")
  }

  let response = await fetch(`http://127.0.0.1:8000/subjects/?teacher_id=${session.userId}`, {
    method: 'GET',
    headers: {
        'Accept': 'application/json',
    },
    });

  console.log(response)
  const subjects: [] = await response.json()

  const subjects_list = subjects.map((subject) => {
    return (
      <li key={subject['id']} style={{listStyleType: 'none'}}>
          <Link href={'subjects/' + subject['id']}>{subject['name']}</Link>
      </li>
  )
  })

  return (
    <div className="table_of">
      <h2 style={{'marginBottom':'25px'}}>Список предметов</h2>
      <ul>
        {subjects_list}
      </ul>
    </div>
  );
};

export default ProfilePage;
