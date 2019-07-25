import React from 'react';
import ReactDOM from 'react-dom';

import AppRouter from './router';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<AppRouter />, document.getElementById('root'));

serviceWorker.unregister();
