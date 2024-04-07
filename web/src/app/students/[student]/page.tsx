import { getSession } from "@/actions";
import Link from "next/link";



const StudentPage = async ( { params }: { params: { student: string } } ) => {

    let response = await fetch(`http://127.0.0.1:8000/students${params.student}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
        });

    let student = await response.json()

    let response_subjects = await fetch(`http://127.0.0.1:8000/subjects/?teacher_id=${(await getSession()).userId}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
        });

    const subjects_love: [] = await response_subjects.json()

    console.log(subjects_love)

    let subjects_list = subjects_love.map((subject) => {
        return (
        <li key={subject["id"]} style={{listStyleType: 'none'}}>
            <Link href={`students${params.student}/students-subject` + subject["id"]}>{subject["name"]}</Link>
        </li>
    )})


    return (
        <div>
            <div style={{'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}}>
                <h2>
                    {student['firstname']} {student['lastname']}
                </h2>
            </div>
            <div style={{'width': '1000px', 'marginTop': '25px'}}>
                <h3>
                    Успеваемость по Вашим предметам:
                </h3>
                <ul>
                    {subjects_list}
                </ul>
            </div>
        </div>
    )
}

export default StudentPage;