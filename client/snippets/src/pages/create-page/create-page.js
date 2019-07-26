import React from 'react';
import b_ from 'b_';


import './create-page.css';

const b = b_.with('create-page');


class CreatePage extends React.Component {
    render() {
        return (
            <div className={b()}>
                {/* <BackButton /> */}
            </div>
        );
    }
}

export default CreatePage;