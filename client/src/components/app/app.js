import React from 'react';
import b_ from 'b_';

import './app.css';

const b = b_.with('app');

class App extends React.Component {
    render() {
        const { children } = this.props;

        return (
            <div className={b()}>
                {children}
            </div>
        );
    }
}

export default App;