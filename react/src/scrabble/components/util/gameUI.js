import React from 'react';
import Cell from '../Cell';
import { classes } from '../../../common/js/util';


function renderPlayerTiles(characters, disabled) {
    const elements = characters.map((character, index) => _renderTile(character, index, disabled));
    return (
        <div className="row">
            {elements}
        </div>
    )
}

function _onDragStart(event, characterIndex) {
    event.dataTransfer.setData('text/plain', characterIndex);
    event.dataTransfer.dropEffect = 'move';
}

function _renderTile(character, index, disabled) {
    const key = `player-character-${index}`;
    const classNames = classes({
        'border-white': true,
        'parent-center': true,
        'clickable': !disabled,
    });

    return (
        <Cell
            className={classNames}
            text={character}
            key={key}
            draggable={true}
            onDragStart={event => _onDragStart(event, index)}
        />
    );
}

export { renderPlayerTiles };