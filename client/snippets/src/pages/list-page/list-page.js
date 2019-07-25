import React from 'react';
import b_ from 'b_';

import SnippetsList from '../../components/SnippetsList'

import './list-page.css';

const b = b_.with('list-page');


class ListPage extends React.Component {
    render() {
        return (
            <div className={b()}>
                <SnippetsList />
            </div>
        );
    }
}

export default ListPage;