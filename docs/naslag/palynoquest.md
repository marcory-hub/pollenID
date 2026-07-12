# PalynoQuest

<div data-palynoquest class="md-typeset">
  <div style="display: grid; grid-template-columns: minmax(260px, 420px) minmax(320px, 1fr); gap: 12px 16px; align-items: start;">
    <div style="max-width: 420px;">
      <img data-pq-image style="display: block; height: auto;" />
      <div data-pq-gallery hidden style="margin-top: 8px;"></div>
      <div data-pq-wrongpreview hidden style="margin-top: 8px;"></div>
      <p style="margin: 12px 0 0 0;">
        <button data-pq-next type="button" class="md-button">Volgende (random)</button>
      </p>
      <div data-pq-info hidden style="margin-top: 12px;"></div>
    </div>

    <div style="min-width: min(320px, 100%);">
      <h3 style="margin-top: 0;">Open vraag</h3>
      <p style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 8px 0;">
        <input data-pq-input type="text" placeholder="Naam (bijv. taxon, type of familie)..." style="flex: 1 1 240px; min-width: min(240px, 100%);" />
        <button data-pq-submit type="button" class="md-button md-button--primary">Controleer</button>
      </p>
      <p data-pq-status style="margin: 0 0 12px 0;"></p>

      <h3>Meerkeuze</h3>
      <p style="margin: 0 0 8px 0;">
        <button data-pq-showmcq type="button" class="md-button">Toon meerkeuze</button>
      </p>
      <p data-pq-mcqstatus style="margin: 0 0 8px 0;"></p>
      <div data-pq-mcq hidden style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
    </div>
  </div>

  <h3>Sleutel</h3>
  <p style="margin: 0 0 8px 0;">
    <select data-pq-keyselect style="width: min(560px, 100%);"></select>
  </p>
  <p style="margin: 0 0 8px 0; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
    <button data-pq-loadkey type="button" class="md-button">Laad sleutel</button>
    <button data-pq-jump type="button" class="md-button" hidden>Spring naar verwacht pad</button>
  </p>
  <div data-pq-keywrap></div>
  <div data-pq-path hidden style="margin-top: 12px;"></div>
</div>
