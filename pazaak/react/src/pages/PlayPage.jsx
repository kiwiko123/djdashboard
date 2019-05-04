import React, { PureComponent } from 'react';
import PazaakGame from '../components/PazaakGame';
import AccountHeaderControls from '../components/AccountHeaderControls';

import '../styles/colors.css';
import '../styles/common.css';


export default class PlayPage extends PureComponent {

    render() {
        return (
            <div className="Play Page">
                <AccountHeaderControls
                    history={this.props.history}
                />
                <PazaakGame />
            </div>
        );
    }

}
