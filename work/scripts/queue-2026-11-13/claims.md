# Claims for fact-checker: queue-2026-11-13

Writer notes:
- No shell was available in this session, so `git fetch` / `ls-tree origin/main` and `python3 -m json.tool` were NOT run. The schema was taken from local `shorts-agent/queue_apex/rejected/20_krok.json` and `agent/story.py` (`validate`, `_fact_check`). Duplicate checks used local `shorts-agent/data/history.json`, `data/history_apex.json` (to 2026-11-11), `work/analytics/experiment-2026-11-09-log.csv` and both trend files. Before queueing, re-check origin/main for anything added after 2026-11-11 and run json.tool.
- `names` uses the shape `_fact_check` reads: Uzbek spelling -> original spelling. The brief asked for original -> Uzbek. Flip it if the existing queue files use that order.
- The existing files have a single `source` string, not `sources`, so the URLs are listed here only.
- Arms (experiment 2026-11-09): apex_1 B, apex_2 A, apex_3 B, apex_4 B, facts_1 B.
- Word counts (regex `\w[\w']*`): apex_1 53, apex_2 51, apex_3 51, apex_4 53, facts_1 54 (55 if the pipeline adds the "Bilarmidingiz" opener).
- Topics skipped as repeats: topics.md apex #1, 2, 4, 5, 6, 7 (already drafted 45-54 in the experiment log); #3 Starbucks/Schultz (his Milan trip was published 2026-11-03); #9 McDonald brothers (the Kroc story was published 2026-11-05 and 20_krok covers the 1961 sale). Facts #1, 2, 6, 8 already drafted.
- apex_2 (Pet Rock) is unused #7 from trends-2026-11-08. apex_4 (LEGO) is not in either trends file: only 4 apex topics in topics.md were left, and 2 of them would repeat a published story.

## apex_1: Gillette (topics.md apex #8), title "Birinchi yili atigi 51 ta sotilgan ustara..."
1. In 1903 the company sold only 51 razors. Sources: https://en.wikipedia.org/wiki/Gillette_(brand) , https://www.britannica.com/biography/King-C-Gillette
2. In 1903 it also sold 168 blades. Source: https://en.wikipedia.org/wiki/Gillette_(brand)
3. It was King C. Gillette's company, and the idea was a disposable blade you throw away when it goes dull instead of sharpening it. Source: https://www.britannica.com/biography/King-C-Gillette
4. In 1904 it sold more than 90,000 razors (90,884) and more than 123,000 blades (123,648). The exact figures are in the description. Source: https://en.wikipedia.org/wiki/Gillette_(brand)
Risk: the 1903/1904 counts are widely cited. Confirm they are on the Wikipedia page or its cited source. If not, soften to "50 dan sal ko'p" / "90 mingdan ortiq".

## apex_2: Pet Rock (trends-2026-11-08 apex #7), title "Geri Dal 1975 yilda 1,5 million dona oddiy tosh sotgan"
1. In 1975 Gary Dahl sold about 1.5 million ordinary stones as "Pet Rock". Sources: https://en.wikipedia.org/wiki/Pet_Rock , https://www.nytimes.com/2015/04/01/business/gary-dahl-creator-of-the-pet-rock-dies-at-78.html
2. He sold the stone as a pet, under the name Pet Rock. Source: https://en.wikipedia.org/wiki/Pet_Rock
3. Each stone came in a box with air holes, with a care/training manual. Source: https://en.wikipedia.org/wiki/Pet_Rock
4. The price was $3.95. Source: https://en.wikipedia.org/wiki/Pet_Rock
5. Within a few months Dahl became a millionaire. Source: NYT obituary above (verify the wording)
Risk: some sources say "over 1 million" or "1.5 million". If the checker finds only "over 1 million", change to "1 million dan ortiq".

## apex_3: Pepsi (topics.md apex #10, without the Coca-Cola refusal claim), title "Ikki marta bankrot bo'lgan ichimlik keyin nima qildi?"
1. In 1923 the Pepsi-Cola company went bankrupt. Sources: https://en.wikipedia.org/wiki/Pepsi , https://www.britannica.com/topic/PepsiCo-Inc
2. The cause was losses from sugar price swings after World War I. Source: https://en.wikipedia.org/wiki/Pepsi
3. It went bankrupt again in 1931. Source: https://en.wikipedia.org/wiki/Pepsi
4. Later Pepsi sold a 12-ounce bottle for 5 cents. Source: https://en.wikipedia.org/wiki/Pepsi
5. That was almost twice the competitor's bottle (Coca-Cola's 6.5 oz for the same price; "twice as much for a nickel"). Source: https://en.wikipedia.org/wiki/Pepsi
Dropped: "Coca-Cola declined to buy Pepsi" (no solid source, as topics.md warned).

## apex_4: LEGO (new topic, not in the trend files), title "Duradgorning yog'och o'yinchoqlari nimaga aylandi?"
1. In 1932 the Danish carpenter Ole Kirk Christiansen began making wooden toys (in Billund, per the description). Sources: https://en.wikipedia.org/wiki/The_Lego_Group , https://en.wikipedia.org/wiki/Ole_Kirk_Christiansen
2. That was during the Great Depression. Sources: https://en.wikipedia.org/wiki/Ole_Kirk_Christiansen , https://www.britannica.com/topic/LEGO
3. In 1934 he named the company LEGO, from the Danish "leg godt" ("play well"). Source: https://en.wikipedia.org/wiki/The_Lego_Group
4. In 1949 Lego began making plastic bricks (Automatic Binding Bricks). Source: https://en.wikipedia.org/wiki/The_Lego_Group
5. The modern brick design was patented in 1958 (28 January 1958). Source: https://en.wikipedia.org/wiki/Lego
6. Lego became one of the world's best-known toy brands. This is a hedged superlative ("eng mashhurlaridan biri"). Source: https://www.britannica.com/topic/LEGO

## facts_1: Cuvier's beaked whale (topics.md facts #10), title "2992 metr chuqurlikka tushgan sut emizuvchi qaysi?"
1. A Cuvier's beaked whale dove to 2,992 m. Sources: Schorr et al. 2014, PLOS ONE 9(3): e92633, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0092633 , https://www.britannica.com/animal/beaked-whale
2. At that depth there is no sunlight, the water is very cold and the pressure is very high. Source: https://oceanservice.noaa.gov/facts/light_travel.html (no light below about 1,000 m)
3. The record was reported in a study published in 2014. Source: Schorr et al. 2014 (above)
4. In the same study one dive lasted more than 137 minutes (137.5 min). Source: Schorr et al. 2014 (above)
5. The whale breathes air, so it made the dive on one breath. Source: https://www.britannica.com/animal/beaked-whale
Note: the 3 h 42 min (222 min) dive comes from a different paper (Quick et al. 2020, J. Exp. Biol.) and was left out on purpose to avoid mixing the two studies.
