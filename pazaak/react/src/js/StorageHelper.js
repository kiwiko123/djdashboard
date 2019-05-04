import { STORAGE_MODE_LOCAL, STORAGE_MODE_SESSION } from '../constants/storage';

export default class StorageHelper {

    static getItem(storageMode, key) {
        const storage = StorageHelper._getStorage(storageMode);
        const item = storage.getItem(key);
        return item && JSON.parse(item);
    }

    static setItem(storageMode, key, value) {
        if (!key) {
            console.error(`Attempting to set storage invalid key '${key}'`);
            return;
        }

        const serialized = JSON.stringify(value);
        const storage = StorageHelper._getStorage(storageMode);
        storage.setItem(key, serialized);
    }

    static clear(storageMode) {
        const storage = StorageHelper._getStorage(storageMode);
        storage.clear();
    }

    static _getStorage(storageMode) {
        let result;

        switch (storageMode) {
            case STORAGE_MODE_LOCAL:
                result = localStorage;
                break;
            case STORAGE_MODE_SESSION:
                result = sessionStorage;
                break;
            default:
                result = null;
        }

        return result;
    }
}