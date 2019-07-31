import React from 'react'


function Line(props) {
    return (
        <div className="line">
            <pre>{props.line === "" ? '\n' : props.line}</pre>
        </div>
    )
}

function File(props) {
    const text = props.content.split('\n')

    return (
        <div className="snippet">
            <p>lang: {props.lang}</p>
            <p>content:</p>
            {text
            .map((line, index) => (
                <Line
                key={index}
                line={line}
                />
            ))}<br></br>
        </div>
    )
}


export default File;