import Link from "next/link";

const SubjectPage = async ( { params }: { params: { subject_id: string } } ) => {

    let response = await fetch(`http://127.0.0.1:8000/subjects/${params.subject_id}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    });


    let subjects: [] = (await response.json())['lectures']

    const lectures_list = subjects.map((subject) => {
        if (params.subject_id){
            return (
                <li key={subject['id']} style={{listStyleType: 'none'}}>
                    <Link href={`${params.subject_id}/` + subject['id']}>{subject['title']}</Link>
                </li>
            )
        }
    else{
        return []
    }})
        
    

    return <div>
        <div>
                    <h2 style={{'marginBottom': '30px'}}>Список лекций данного предмета</h2>

        </div>
        <ul>
              {lectures_list}
        </ul>
    </div>

}

export default SubjectPage;