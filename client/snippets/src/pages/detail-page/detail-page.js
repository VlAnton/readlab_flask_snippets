import React from 'react';
import b_ from 'b_';

import SnippetInfo from '../../components/Snippet-info'

import './detail-page.css';

const b = b_.with('list-page');


class DetailPage extends React.Component {
    render() {
        const { match: { params: { uid } } } = this.props;

        return (
            <div className={b()}>
                <SnippetInfo snippet_uid={uid} />
            </div>
        );
    }
}

export default DetailPage;