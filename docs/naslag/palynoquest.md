# PalynoQuest

<div data-palynoquest class="md-typeset">
  <p style="margin: 0 0 12px 0; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
    <label for="pq-level">Niveau</label>
    <select data-pq-level id="pq-level" style="width: min(420px, 100%);">
      <option value="kenmerken">Kenmerken: Niveau 1</option>
      <option value="1">1: Vaak in NL-honing</option>
      <option value="2">2: + Alle prioriteit</option>
      <option value="3">3: Alles</option>
      <option value="lookalike">Lookalike: Alle</option>
      <option value="lookalike-easy">Lookalike: Makkelijk</option>
      <option value="lookalike-moderate">Lookalike: Matig</option>
      <option value="lookalike-difficult">Lookalike: Moeilijk</option>
    </select>
  </p>
  <p data-pq-progress style="margin: 0 0 12px 0;"></p>
  <div style="display: grid; grid-template-columns: minmax(260px, 420px) minmax(320px, 1fr); gap: 12px 16px; align-items: start;">
    <div style="max-width: 420px;">
      <img data-pq-image style="display: block; height: auto;" />
      <div data-pq-gallery hidden style="margin-top: 8px;"></div>
      <div data-pq-wrongpreview hidden style="margin-top: 8px;"></div>
      <p style="margin: 12px 0 0 0; display: flex; flex-wrap: wrap; gap: 8px;">
        <button data-pq-next type="button" class="md-button">Volgende (random)</button>
        <button data-pq-export-confusions type="button" class="md-button" title="Kopieer lokale verwarringen als JSON">Exporteer verwarringen</button>
      </p>
      <div data-pq-info hidden style="margin-top: 12px;"></div>
    </div>

    <div style="min-width: min(320px, 100%);">
      <p data-pq-status style="margin: 0 0 12px 0;"></p>

      <div data-pq-kenmerken-panel hidden>
        <h3 style="margin-top: 0;">Kenmerken</h3>
        <p data-pq-feature-prompt style="margin: 0 0 8px 0;">Welk kenmerk zie je?</p>
      </div>

      <div data-pq-normal-panel>
        <h3 style="margin-top: 0;">Open vraag</h3>
        <p style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 8px 0;">
          <input data-pq-input type="text" placeholder="Naam (bijv. taxon, type of familie)..." style="flex: 1 1 240px; min-width: min(240px, 100%);" />
          <button data-pq-submit type="button" class="md-button md-button--primary">Controleer</button>
        </p>

        <h3>Meerkeuze</h3>
        <p style="margin: 0 0 8px 0;">
          <button data-pq-showmcq type="button" class="md-button">Toon meerkeuze</button>
        </p>
      </div>

      <div data-pq-lookalike-panel hidden>
        <h3 style="margin-top: 0;">Lookalike</h3>
        <p data-pq-lookalike-prompt style="margin: 0 0 8px 0;">Welke naam hoort bij dit beeld?</p>
      </div>

      <p data-pq-mcqstatus style="margin: 0 0 8px 0;"></p>
      <div data-pq-mcq hidden style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
    </div>
  </div>

  <div data-pq-normal-panel>
    <h3>Sleutel</h3>
    <p style="margin: 0 0 8px 0;">
      <select data-pq-keyselect style="width: min(560px, 100%);"></select>
    </p>
    <p style="margin: 0 0 8px 0; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
      <button data-pq-loadkey type="button" class="md-button">Laad sleutel</button>
      <button data-pq-backtrack type="button" class="md-button" hidden>Eén stap terug</button>
      <button data-pq-jump type="button" class="md-button" hidden>Spring naar verwacht pad</button>
    </p>
    <div data-pq-keywrap></div>
    <div data-pq-path hidden style="margin-top: 12px;"></div>
  </div>
</div>
