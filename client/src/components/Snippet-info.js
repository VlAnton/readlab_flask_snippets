import React from 'react';
import b_ from 'b_';

import Snippet from './Snippet'


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
        const snippetData = await getSnippet(snippet_uid);
        var snippetJson;

        if (snippetData.length > 0) {
            const [created_at, isPublic, description] = snippetData.pop();
            snippetJson = {snippet_uid, created_at, isPublic: isPublic.toString(), description};
        }

        this.setState({
            loaded: true,
            snippet: snippetJson,
        });
    }

    render() {
        const { snippet } = this.state;

        if (snippet) {
            return (
                <div className={b()}>
                    <Snippet
                        key={snippet.snippet_uid}
                        created_at={snippet.created_at}
                        description={snippet.description}
                        isPublic={snippet.isPublic}
                    />
                </div>
            )
        } else {
            return (
                <div>Wrong uid</div>
            )
        }
    }
}

export default SnippetInfo;
