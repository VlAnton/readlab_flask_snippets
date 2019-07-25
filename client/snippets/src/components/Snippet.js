import React from 'react';


function Snippet(props) {
    return (
        <div className="snippet">
            <p>created at: {props.created_at}</p><br></br>
            <p>description: {props.description}</p>
        </div>
    )
}


export default Snippet;