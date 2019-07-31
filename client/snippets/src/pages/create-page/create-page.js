import React from 'react';
import b_ from 'b_';

import './create-page.css';

import CreateForm from '../../components/create-form/create'

const b = b_.with('create-page');


class CreatePage extends React.Component {
    render() {
        return (
            <div className={b()}>
                <CreateForm />
            </div>
        );
    }
}

export default CreatePage;