import L from 'leaflet';

export class ZoomWithHome extends L.Control.Zoom {
	public onAdd(map: L.Map): HTMLElement {
		const container = super.onAdd(map);
		this._createButton('&#9679;', 'Home', 'leaflet-control-zoom-home', container, () => {
			if (!this._disabled) {
				this._map.locate({ setView: true, maxZoom: 16 });
			}
		});
		this._createButton('&spades;', 'Reset view', 'leaflet-control-zoom-reset', container, () => {
			if (!this._disabled) {
				this._map.resetView();
			}
		});
		return container;
	}
}
export class TimelineControl extends L.Control {
	readonly #content;
	constructor(content: HTMLElement) {
		super({ position: 'bottomleft' });
		this.#content = content;
	}
	public onAdd(_map: L.Map) {
		const container = L.DomUtil.create('div', 'timeline leaflet-bar');
		if (this.#content) {
			container.appendChild(this.#content);
		}
		return container;
	}
}

export class Connections extends L.Control {
	readonly #content;
	constructor(content: HTMLElement) {
		super({ position: 'topright' });
		this.#content = content;
	}
	public onAdd(map: L.Map): HTMLElement {
		const container = L.DomUtil.create('div', 'connections leaflet-bar');
		if (this.#content) {
			container.appendChild(this.#content);
		}
		return container;
	}
}
