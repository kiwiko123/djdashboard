import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Cell from './Cell';

import '../../pazaak/styles/common.css';
import '../styles/ScrabbleBoard.css';


export default class ScrabbleBoard extends Component {

    static propTypes = {
        board: PropTypes.arrayOf(
            PropTypes.arrayOf(PropTypes.string),
        ).isRequired,
        dropTileHandler: PropTypes.func.isRequired,
    };

    static defaultProps = {
        board: [],
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
        const key = `${row}${column}`;
        return (
            <Cell
                className="border-white parent-center"
                text={text}
                key={key}
                onDrop={event => this._onDropTile(event, row, column)}
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
        const tileIndex = event.dataTransfer.getData('text/plain');
        console.log(`tileIndex=${tileIndex}; row=${droppedRow}; column=${droppedColumn}`);
        this.props.dropTileHandler(tileIndex, droppedRow, droppedColumn);
    }
}