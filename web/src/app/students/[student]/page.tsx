const StudentPage = async ( { params }: { params: { student: string } } ) => {

    return <p>Post: {params.student}</p>
    
}

export default StudentPage;