import React from 'react';
import b_ from 'b_';

import File from './File'

const b = b_.with('snippet-info');

async function getSnippet(snippetUid) {
    const res = await fetch(`http://0.0.0.0:5000/api/snippets/${snippetUid}`);

    return res.json();
}


class SnippetInfo extends React.Component {
    state = {
        loaded: false,
        snippet: {}
    }

    async componentDidMount() {
        const { snippet_uid } = this.props;
        const snippetJson = await getSnippet(snippet_uid);

        this.setState({
            loaded: true,
            snippet: snippetJson,
        });
    }

    render() {
        const { snippet } = this.state;
        const files = snippet.files
        console.log(files)

        if (files) {
            return (
                <>
                    <div className={b('description')}>
                        <h2>{ snippet.description }</h2><br></br>
                    </div>
                    <div className={b()}>
                    {Object.values(snippet.files)
                        .map(file => (
                            <File
                            key={file.snippet_uid}
                            content={file.content}
                            lang={file.lang}
                            />
                        ))}
                    </div>
                </>
            )
        }
        return (
            <div className={b()}>
                <h1>Not loaded yet</h1>
            </div>
        )

        
    }
}

export default SnippetInfo;