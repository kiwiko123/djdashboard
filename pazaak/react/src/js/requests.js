

class RequestService {

	constructor(base_url) {
		this._base_url = base_url
	}

	async get(url) {
		url = `${this._base_url}${url}/`;
		const response = await fetch(url);
	  	return response.json();
	}

	async post(url, payload) {
		url = `${this._base_url}${url}/`;
		const params = {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
        		'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		};

		const response = await fetch(url, params);
		return response.json();
	}
}

export default RequestService;