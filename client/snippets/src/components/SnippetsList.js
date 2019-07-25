import React from 'react';
import b_ from 'b_';

import Snippet from './Snippet'

const b = b_.with('issues');

class SnippetsList extends React.Component {
  state = {
    loaded: false,
    snippets: []
  }

  async componentDidMount() {
    const res = await fetch('http://0.0.0.0:5000/api/snippets');
    const json = await res.json();

    this.setState({
      loaded: true,
      snippets: json
    });
  }

  render() {
    const { snippets } = this.state

    return (
      <div className={b()}>
          {snippets
          .map(snippet => (
            <Snippet
              key={snippet.snippet_uid}
              created_at={snippet.created_at}
              description={snippet.description}
              />
          ))}
      </div>
    );
  }
}


export default SnippetsList;