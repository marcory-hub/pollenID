# Willekeurig

Zelfde kenmerken-stappen als op [Pollenkenmerken](../herkennen/pollenkenmerken/_index.md): vorm, apertuur, sculptuur, grootteband (alle opties), daarna naam (4 opties). Of lookalike: één beeld, twee namen.

<div data-palynoquest class="md-typeset">
  <p style="margin: 0 0 12px 0; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
    <label for="pq-level">Niveau</label>
    <select data-pq-level id="pq-level" style="width: min(420px, 100%);">
      <option value="kenmerken">Kenmerken: vaak in NL-honing</option>
      <option value="kenmerken-2">Kenmerken: overige pollen</option>
      <option value="kenmerken-3">Kenmerken: minder frequent</option>
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
      </p>
      <div data-pq-info hidden style="margin-top: 12px;"></div>
    </div>

    <div style="min-width: min(320px, 100%);">
      <p data-pq-status style="margin: 0 0 12px 0;"></p>

      <div data-pq-kenmerken-panel hidden>
        <h3 style="margin-top: 0;">Kenmerken</h3>
        <p data-pq-feature-prompt style="margin: 0 0 8px 0;">Welk kenmerk zie je?</p>
      </div>

      <div data-pq-lookalike-panel hidden>
        <h3 style="margin-top: 0;">Lookalike</h3>
        <p data-pq-lookalike-prompt style="margin: 0 0 8px 0;">Welke naam hoort bij dit beeld?</p>
      </div>

      <p data-pq-mcqstatus style="margin: 0 0 8px 0;"></p>
      <div data-pq-mcq hidden style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
    </div>
  </div>
</div>
