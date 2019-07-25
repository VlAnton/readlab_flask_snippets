import React from 'react';
import b_ from 'b_';
import { func } from 'prop-types';

import Snippet from './Snippet'
// import IssueCard from '../issue-card';


// const b = b_.with('issues');

// class SnippetsList extends React.Component {
//   state = {
//     snippets: []
//   }

//   async componentDidMount() {
//     const res = await fetch('http://0.0.0.0:5000/api/snippets')
//   }
// }

function SnippetsList(props) {
    return (
    <div>
      {props.snippets.map(c => <Snippet
          key={c.snippet_uid}
          created_at={c.created_at}
          description={c.description}
        />)}
     </div> 
  );
}



export default SnippetsList;