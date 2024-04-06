const SubjectPage = async ( { params }: { params: { subject: string } } ) => {

    return <p>Post: {params.subject}</p>

}

export default SubjectPage;