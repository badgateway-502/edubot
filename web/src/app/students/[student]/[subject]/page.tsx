import { getSession } from "@/actions";
import Link from "next/link";


const StudentPage = async ( { params }: { params: { student: string, subject: string } } ) => {

    let response = await fetch(`http://127.0.0.1:8000/students${params.subject}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
        });

    let student = await response.json()


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
            </div>
        </div>
    )
}

export default StudentPage;