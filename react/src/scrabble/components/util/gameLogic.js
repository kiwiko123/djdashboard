import { find } from 'lodash';


export function getAvailableTiles(allTiles, submittedTiles) {
    if (!allTiles) {
        return [];
    }
    if (!submittedTiles) {
        return allTiles;
    }

    const submittedTileIndices = new Set(submittedTiles.map(tile => tile.index));
    return allTiles.filter(tile => !submittedTileIndices.has(tile.index));
}

export function createTileInfo(tiles) {
    const result = tiles || [];
    return result.map((tile, index) => ({
        index,
        value: tile,
    }));
}

export function getFromSubmittedTiles(row, column, submittedTiles) {
    return find(submittedTiles, tile => tile.row === row && tile.column === column);
}