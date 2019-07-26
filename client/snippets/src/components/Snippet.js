import React from 'react'

function Snippet(props) {
    console.log(props)
    return (
        <div className="snippet">
            <p>created at: {props.created_at}</p>
            <p>description: {props.description}</p>
            <p>files count: {props.files_count}</p><br></br>
        </div>
    )
}


export default Snippet;