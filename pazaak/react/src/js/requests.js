import { endsWith, startsWith } from 'lodash';


class RequestService {

	constructor(base_url, persistentPayload) {
		this._base_url = base_url
		this._persistentPayload = persistentPayload;
	}

	setPersistentPayload(payload) {
		this._persistentPayload = payload;
	}

	async get(url) {
		url = this._normalize_url(url);
		const response = await fetch(url);
	  	return response.json();
	}

	async post(url, payload) {
		url = this._normalize_url(url);
		payload = this._get_persistent_payload(payload);
		const params = {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
			},
			body: JSON.stringify(payload),
		};

		const response = await fetch(url, params);
		return response.json();
	}

	_normalize_url(url) {
		if (!startsWith(url, '/')) {
			url = `/${url}`;
		}
		if (!endsWith(url, '/')) {
			url = `${url}/`;
		}

		return `${this._base_url}${url}`;
	}

	_get_persistent_payload(payload) {
		payload = payload || {};
		return {
			...this._persistentPayload,
			...payload,
		};
	}
}

export default RequestService;