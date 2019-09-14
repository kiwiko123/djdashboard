import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { get, isNumber, isNil } from 'lodash';
import { getFromSubmittedTiles } from "./util/gameLogic";
import { onDragStart } from './util/gameUI';
import { classes } from '../../common/js/util';
import TextCell from './TextCell';

import '../../pazaak/styles/common.css';
import '../styles/ScrabbleBoard.css';

function onDragTileOutOfBoard(event, row, column) {
    event.preventDefault();
    const payload = JSON.stringify({
        row,
        column,
    });
    onDragStart(event, payload);
}

export default class ScrabbleBoard extends Component {
    static propTypes = {
        board: PropTypes.arrayOf(
            PropTypes.arrayOf(PropTypes.string),
        ).isRequired,
        submittedTiles: PropTypes.arrayOf(PropTypes.shape({
            index: PropTypes.number.isRequired,
            row: PropTypes.number.isRequired,
            column: PropTypes.number.isRequired,
        })),
        dropTileHandler: PropTypes.func.isRequired,
        clickTileHandler: PropTypes.func,
    };

    static defaultProps = {
        board: [],
        submittedTiles: [],
        clickTileHandler: null,
    };

    constructor(props) {
        super(props);
        this._onDropTile = this._onDropTile.bind(this);
    }

    render() {
        const board = this.props.board
            .map((row, index) => this._getRow(row, index));

        return (
            <div className="ScrabbleBoard">
                {board}
            </div>
        );
    }

    _getCell(text, row, column) {
        const submittedTile = getFromSubmittedTiles(row, column, this.props.submittedTiles);
        const tileIndex = get(submittedTile, 'index');
        const isOccupied = !isNil(tileIndex);
        const key = `${row}${column}`;
        const className = classes({
            'border-white': true,
            'parent-center': true,
            'game-cell': true,
            'clickable': isOccupied,
        });

        return (
            <TextCell
                className={className}
                text={text}
                key={key}
                draggable={isOccupied}
                onDragStart={event => onDragTileOutOfBoard(event, row, column)}
                onDrop={event => this._onDropTile(event, row, column)}
                onClick={() => this.props.clickTileHandler(row, column)}
            />
        );
    }

    _getRow(row, rowIndex) {
        const key = `row-${rowIndex}`;
        const elements = row.map((text, columnIndex) => this._getCell(text, rowIndex, columnIndex));
        return (
            <div
                className="row"
                key={key}
            >
                {elements}
            </div>
        );
    }

    _onDropTile(event, droppedRow, droppedColumn) {
        event.preventDefault();
        // event.stopPropagation();

        let tileIndex = event.dataTransfer.getData('text/plain');
        if (!isNumber(tileIndex)) {
            console.error(`Invalid tile index "${tileIndex}" set on drop`);
        }

        tileIndex = Number(tileIndex);
        console.log(`tileIndex=${tileIndex}; row=${droppedRow}; column=${droppedColumn}`);
        this.props.dropTileHandler(tileIndex, droppedRow, droppedColumn);
    }
}