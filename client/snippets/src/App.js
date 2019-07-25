import React, { Component } from 'react';
import axios from "axios";

import SnippetsList from './components/SnippetsList'


class App extends Component {
  state = {
    snippets: []
  }

  async componentDidMount() {
    axios
    .get('http://0.0.0.0:5000/api/snippets')
    .then(response => {
      const newContacts = response.data.map(snippet => {
        return {
          snippet_uid: snippet.snippet_uid,
          created_at: snippet.created_at,
          description: snippet.description
        };
      });

      const newState = Object.assign({}, this.state, { snippets: newContacts });

      this.setState(newState);
    })
    .catch(err => {
      console.log(err)
    })
  }

  render() {
    return (
      <div className="App">
        <SnippetsList snippets={this.state.snippets} />
      </div>
    );
  }
}


export default App;
