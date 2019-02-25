import React from 'react';
import ReactDOM from 'react-dom';
import PazaakGame from '../components/PazaakGame'

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<PazaakGame />, div);
  ReactDOM.unmountComponentAtNode(div);
});
