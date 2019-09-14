import React from 'react';
import TextCell from '../TextCell';
import { classes } from '../../../common/js/util';


export function renderPlayerTiles(tiles, disabled) {
    const elements = tiles.map(tile => _renderTile(tile, disabled));
    return (
        <div className="row">
            {elements}
        </div>
    )
}

export function onDragStart(event, text, dropEffect = 'move') {
    event.dataTransfer.setData('text/plain', text);
    event.dataTransfer.dropEffect = dropEffect;
}

function _renderTile(tile, disabled) {
    const character = tile.value;
    const index = tile.index;
    const key = `player-character-${index}`;
    const classNames = classes({
        'border-white': true,
        'parent-center': true,
        'game-cell': true,
        'clickable': !disabled,
    });

    return (
        <TextCell
            className={classNames}
            text={character}
            key={key}
            draggable={true}
            onDragStart={event => onDragStart(event, index)}
        />
    );
}
