import React from 'react'

function File(props) {
    return (
        <div className="snippet">
            <p>lang: {props.lang}</p>
            <p>content: {props.content}</p><br></br>
        </div>
    )
}


export default File;