import React from 'react'

function Snippet(props) {
    return (
        <div className="snippet">
            <p>created at: {props.created_at}</p>
            <p>description: {props.description}</p><br></br>
        </div>
    )
}


export default Snippet;