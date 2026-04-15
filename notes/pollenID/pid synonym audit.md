**One-line purpose:** select key_synonyms
**Short summary:** make naming uniform
**Agent:** 
**SoT:** yes
**Main Index:** [[__pollenID]]

---

```sh
python3 scripts/audit_key_synonyms.py
```

2026-04-13 to resolve

Key synonym audit (endpoint id.name)
keys_scanned=75
conflict_groups=30

 1. Geen match | variants=4 endpoints=5
    -   2x Geen match. Ga terug naar de hoofdkey. [te verifiëren]  (e.g. keys/beug/beug22-tricolporatae-ret-fumana.json step 1 choice 1)
    -   1x Geen match.  (e.g. keys/beug/beug24-stephanocolpatae.json step 11 choice 1)
    -   1x Geen match. Zie Medicago sativa-type (Blz. 207) [te verifiëren]  (e.g. keys/beug/beug23-tricolporoidatae-ret.json step 5 choice 0)
    -   1x Geen match. Zie Stephanoporatae (Blz. 441) [te verifiëren]  (e.g. keys/beug/beug24-stephanocolpatae.json step 6 choice 1)

 2. Callitriche palustris-type | variants=3 endpoints=5
    -   3x Callitriche palustris-type (Blz... 424)  (e.g. keys/beug/beug11-dicolpatae.json step 3 choice 1)
    -   1x 30.2 Callitriche palustris-type (Blz. 424)  (e.g. keys/beug/beug30-diporatae.json step 3 choice 1)
    -   1x Callitriche palustris-type (Blz. 424)  (e.g. keys/beug/beug24-stephanocolpatae.json step 4 choice 0)

 3. Rubus chamaemorus | variants=3 endpoints=4
    -   2x Rubus chamaemorus (kruipbraam)  (e.g. keys/eide/rosaceae-eide.json step 15 choice 0)
    -   1x 16.4 Rubus chamaemorus (Blz... 214)  (e.g. keys/beug/beug16-ttt-clav.json step 6 choice 1)
    -   1x Rubus chamaemorus type (Rubus chamaemorus - kruipbraam)  (e.g. keys/reitsma/rosaceae-reitsma.json step 12 choice 1)

 4. Sanguisorba officinalis | variants=3 endpoints=4
    -   2x Sanguisorba officinalis (grote pimpernel)  (e.g. keys/eide/rosaceae-eide.json step 3 choice 1)
    -   1x 25.15 Sanguisorba officinalis (Blz. 400)  (e.g. keys/beug/beug25-stephanocolporatae.json step 15 choice 0)
    -   1x Sanguisorba officinalis subtype (Sanguisorba officinalis - grote pimpernel)  (e.g. keys/reitsma/rosaceae-reitsma.json step 26 choice 1)

 5. Centaurea jacea-type | variants=3 endpoints=3
    -   1x 16.8 Centaurea jacea-type (Blz... 216)  (e.g. keys/beug/beug17-ttt-ech.json step 1 choice 1)
    -   1x 17.1.10 Centaurea jacea-type (Blz... 230)  (e.g. keys/beug/beug17-ttt-ech-asteraceae.json step 10 choice 0)
    -   1x Centaurea jacea-type (S. 230)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 22 choice 0)

 6. Sanguisorba minor-type | variants=2 endpoints=4
    -   3x Sanguisorba minor-type (S. 130)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 17 choice 0)
    -   1x 13.7 Sanguisorba minor-type (Blz... 130)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 10 choice 0)

 7. Comarum palustre | variants=2 endpoints=3
    -   2x Comarum palustre (wateraardbei)  (e.g. keys/eide/rosaceae-eide.json step 7 choice 0)
    -   1x Comarum palustre subtype (Comarum palustre - wateraardbei)  (e.g. keys/reitsma/rosaceae-reitsma.json step 17 choice 0)

 8. Fragaria vesca | variants=2 endpoints=3
    -   2x Fragaria vesca (bosaardbei)  (e.g. keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json step 7 choice 0)
    -   1x Fragaria vesca synoniem Potentilla palustris (bosaardbei)  (e.g. keys/eide/rosaceae-eide.json step 8 choice 0)

 9. Rosa canina | variants=2 endpoints=3
    -   2x Rosa canina (hondsroos)  (e.g. keys/eide/rosaceae-eide.json step 12 choice 2)
    -   1x Rosa canina type (Rosa canina - hondsroos)  (e.g. keys/reitsma/rosaceae-reitsma.json step 9 choice 0)

10. Rosa rubiginosa | variants=2 endpoints=3
    -   2x Rosa rubiginosa (egelantier)  (e.g. keys/eide/rosaceae-eide.json step 12 choice 0)
    -   1x Rosa rubiginosa subtype (Rosa rubiginosa - egelantier)  (e.g. keys/reitsma/rosaceae-reitsma.json step 21 choice 0)

11. Sanguisorba dodecandra | variants=2 endpoints=3
    -   2x Sanguisorba dodecandra (S. 130)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 17 choice 1)
    -   1x 13.8 Sanguisorba dodecandra (Blz... 130)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 10 choice 1)

12. Sanguisorba minor | variants=2 endpoints=3
    -   2x Sanguisorba minor (kleine pimpernel)  (e.g. keys/eide/rosaceae-eide.json step 3 choice 0)
    -   1x Sanguisorba minor subtype (Sanguisorba minor - kleine pimpernel)  (e.g. keys/reitsma/rosaceae-reitsma.json step 26 choice 0)

13. Bistorta officinalis | variants=2 endpoints=2
    -   1x 14.9 (Bistorta officinalis-) Polygonum bistorta-type (S. 163)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 11 choice 0)
    -   1x 14.9.1 Bistorta officinalis Bistorta officinalis (L.) Delabre (2) 45,5-63  (e.g. keys/beug/beug14-tricolpatae-ps-bistorta.json step 1 choice 0)

14. Centaurea cyanus | variants=2 endpoints=2
    -   1x 14.14 Centaurea cyanus (S. 190)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 21 choice 0)
    -   1x [Asteraceae](https://pollen.tstebler.ch/MediaWiki/index.php?title=Kategorie:Asteraceae) (composieten) - Centaurea - Centaurea cyanus  (e.g. keys/vanderham/vanderham-pollentabel.json step 40 choice 0)

15. Chelidonium majus | variants=2 endpoints=2
    -   1x 21.14 Chelidonium majus (Blz... 298)  (e.g. keys/beug/beug21-tricolpatae-ret.json step 16 choice 0)
    -   1x Papaveraceae (Chelidonium majus)  (e.g. keys/vanderham/vanderham-pollentabel.json step 27 choice 2)

16. Comandra elegans | variants=2 endpoints=2
    -   1x 13.6 Comandra elegans (Blz... 129)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 8 choice 0)
    -   1x Comandra elegans (Blz... 130)  (e.g. keys/beug/beug21-tricolpatae-ret.json step 2 choice 0)

17. Cornus sanguinea | variants=2 endpoints=2
    -   1x 15.1.1 Cornus sanguinea  (e.g. keys/beug/beug15-tricolporoidatae-ps-cornus.json step 1 choice 0)
    -   1x Cornus sanguinea (S. 203)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 49 choice 0)

18. Geum rivale | variants=2 endpoints=2
    -   1x Geum rivale (knikkend nagelkruid)  (e.g. keys/reitsma/rosaceae-reitsma.json step 24 choice 1)
    -   1x Geum rivale (knikkend nagelkruid) 27 (23.2-30.6)  (e.g. keys/eide/rosaceae-eide.json step 21 choice 0)

19. Ginkgo biloba | variants=2 endpoints=2
    -   1x 9.37 Ginkgo biloba (Blz... 110)  (e.g. keys/beug/beug09-monocolpatae.json step 37 choice 0)
    -   1x Ginkgo biloba (Blz... 110)  (e.g. keys/beug/beug08-monoporatae.json step 4 choice 0)

20. Gratiola officinalis | variants=2 endpoints=2
    -   1x 15.3 Gratiola officinalis (S. 204)  (e.g. keys/beug/beug15-tricolporoidatae-ps.json step 11 choice 0)
    -   1x Gratiola officinalis (Blz... 204)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 23 choice 0)

21. Hottonia palustris | variants=2 endpoints=2
    -   1x 21.24 Hottonia palustris (Blz... 304)  (e.g. keys/beug/beug21-tricolpatae-ret.json step 31 choice 0)
    -   1x Hottonia palustris (Blz. 304)  (e.g. keys/beug/beug23-tricolporoidatae-ret.json step 22 choice 0)

22. Mespilus germanica | variants=2 endpoints=2
    -   1x Mespilus germanica (mispel)  (e.g. keys/feagri-iversen/rosaceae-feagri-iversen-273-288.json step 11 choice 0)
    -   1x Mespilus germanica (wilde mispel)  (e.g. keys/eide/rosaceae-eide.json step 17 choice 0)

23. Myriophyllum alterniflorum | variants=2 endpoints=2
    -   1x 32.8 Myriophyllum alterniflorum (Blz. 448)  (e.g. keys/beug/beug32-stephanoporatae.json step 10 choice 1)
    -   1x Myriophyllum alterniflorum (Blz. 448)  (e.g. keys/beug/beug30-diporatae.json step 5 choice 0)

24. Phacelia tanacetifolia | variants=2 endpoints=2
    -   1x 24.3 Phacelia tanacetifolia (Blz. 382)  (e.g. keys/beug/beug24-stephanocolpatae.json step 3 choice 0)
    -   1x Hydrophyllaceae (Phacelia tanacetifolia)  (e.g. keys/vanderham/vanderham-pollentabel.json step 15 choice 1)

25. Potentilla anserina | variants=2 endpoints=2
    -   1x Potentilla anserina 25 (23.2-27.7) μm (zilverschoon  (e.g. keys/eide/rosaceae-eide.json step 8 choice 1)
    -   1x Potentilla anserina subtype (Potentilla anserina - zilverschoon)  (e.g. keys/reitsma/rosaceae-reitsma.json step 17 choice 1)

26. Rosa pimpinellifolia | variants=2 endpoints=2 | HAS_SYN
    -   1x [syn] Rosa pimpinellifolia (duinroos) syn Rosa spinosissima  (e.g. keys/eide/rosaceae-eide.json step 27 choice 1)
    -   1x Rosa pimpinellifolia (duinroos)  (e.g. keys/eide/rosaceae-eide.json step 12 choice 1)

27. Sambucus nigra | variants=2 endpoints=2
    -   1x Caprifoliaceae (Sambucus nigra)  (e.g. keys/vanderham/vanderham-pollentabel.json step 25 choice 0)
    -   1x [Caprifoliaceae](https://pollen.tstebler.ch/MediaWiki/index.php?title=Kategorie:Caprifoliaceae) (kamperfoeliefamilie) - (Sambucus nigra)  (e.g. keys/vanderham/vanderham-pollentabel.json step 71 choice 1)

28. Sciadopitys verticillata | variants=2 endpoints=2
    -   1x 9.3 Sciadopitys verticillata (Blz... 99)  (e.g. keys/beug/beug09-monocolpatae.json step 4 choice 0)
    -   1x Sciadopitys verticillata (Blz... 99)  (e.g. keys/beug/beug08-monoporatae.json step 2 choice 0)

29. Verbena officinalis | variants=2 endpoints=2
    -   1x 14.4 Verbena officinalis (S. 162)  (e.g. keys/beug/beug14-tricolporatae-ps.json step 6 choice 0)
    -   1x Verbena officinalis (Blz. 163)  (e.g. keys/beug/beug28-heterocolpatae.json step 5 choice 1)

30. Viola odorata-type | variants=2 endpoints=2
    -   1x 13.18 Viola odorata-type (Blz... 138)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 21 choice 0)
    -   1x 13.18 Viola odorata-type (Blz... 140)  (e.g. keys/beug/beug13-tricolpatae-ps.json step 23 choice 1)