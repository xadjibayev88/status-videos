# Fact-check: queue-2026-11-13

Method note: WebFetch could not reach en.wikipedia.org or journals.plos.org (network not allowed in this session), and the memory MCP (Company / Brand rules) was not available. Every verdict below rests on WebSearch result summaries that quote Wikipedia, PLOS ONE, National Geographic, Dallas Morning News, NPR, Britannica-type sources. Primary pages were not opened. JSON files were not edited. All facts are pre-2024 (only Quick et al. 2020 is mentioned, as context, and is not used in any script).

Sources used (links)
- Gillette: https://en.wikipedia.org/wiki/Gillette , https://en.wikipedia.org/wiki/King_C._Gillette
- Pet Rock: https://www.npr.org/2015/04/01/396726696/gary-dahl-creator-of-the-pet-rock-dies-at-78 , https://dallasnews.com/business/2015/04/01/pet-project-made-gary-ross-dahl-a-1970s-pop-culture-rock-star-and-a-bunch-of-money , https://encyclopedia.com/history/culture-magazines/pet-rocks , https://www.pbs.org/newshour/arts/pet-rock-tribute
- Pepsi: https://en.wikipedia.org/wiki/Pepsi , https://en.wikipedia.org/wiki/Charles_Guth , https://www.historyoasis.com/post/sugar-pepsi-bankrupt
- LEGO: https://en.wikipedia.org/wiki/Ole_Kirk_Christiansen , https://en.wikipedia.org/wiki/History_of_Lego , https://lemelson.mit.edu/resources/ole-christiansen
- Whale: https://pmc.ncbi.nlm.nih.gov/articles/PMC3966784 (Schorr et al. 2014, PLOS ONE 9(3):e92633) , https://www.nationalgeographic.com/animals/article/140326-cuvier-beaked-whale-record-dive-depth-ocean-animal-science

---
## apex_1 (Gillette) - PASS WITH FIXES (minor)

| # | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| 1 | 1903: 51 razors sold | TRUE | Wikipedia Gillette; several business-history sites agree (51/168 is the consistent version; one forum says 52, one site swaps units, both outliers) | none |
| 2 | 1903: 168 blades also sold | TRUE | same | none |
| 3 | 1904: 90,884 razors and 123,648 blades ("90 mingdan ortiq", "123 mingdan ortiq") | TRUE | Wikipedia Gillette. Note: invent.org says "two million blades" for 1904; that disagrees with the rest and is not used | none |
| 4 | Idea: blade you throw away when dull | TRUE | Britannica / Wikipedia King C. Gillette | none |
| 5 | "yangi bir kompaniya ... Bu King Jillett kompaniyasi edi" in 1903 | MISLEADING | Company was founded 1901 as American Safety Razor Co. and renamed Gillette Safety Razor Co. in 1904 (Wikipedia). 1903 was the first sales year, not the founding year | see fixes |
| 6 | "Birinchi yili" (hook) | TRUE | 1903 was the first sales year | none |
| 7 | "Sekin boshlanish hali mag'lubiyat emas" | opinion, not checkable | | none |

Fixes
- Scene 1: "1903 yilda yangi bir kompaniya atigi 51 ta ustara sotdi." -> "1903 yilda yangi mahsulot atigi 51 ta ustara sotdi." (or keep, low risk)
- Scene 3: "Bu King Jillett kompaniyasi edi." -> "Bu King Jillett asos solgan kompaniya edi."
- Description: "King Jillett kompaniyasi 1903 yilda" -> "King Jillett asos solgan kompaniya 1903 yilda"

---
## apex_2 (Pet Rock) - PASS WITH FIXES

| # | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| 1 | Gary Dahl sold 1.5 million rocks | MISLEADING | 1.5 million is Dahl's own estimate (Dallas Morning News, PBS); Encyclopedia.com says "over one million by Christmas"; his daughter said 4 million. Not a hard audited number | add "taxminan" |
| 2 | "1975 yilda" sold 1.5 million | MISLEADING | Craze ran Aug/late 1975 to about Feb 1976 (about six months). Not all sold in 1975 | say "1975 yildan boshlab" / "bir necha oyda" |
| 3 | Sold as a pet, name "Pet Rock" | TRUE | NPR, PBS | none |
| 4 | Box with air holes + care manual | TRUE | box with holes for the "pet" to breathe; 32-page "Care and Training of Your Pet Rock" (search summaries of Wikipedia-type sources) | none |
| 5 | Price $3.95 | TRUE (weak confirmation) | Widely cited as $3.95; searches also showed "$3.99" and "about $4" in single outlets. Wikipedia page could not be opened, so re-check once if possible | none, or "taxminan 4 dollar" for safety |
| 6 | Became a millionaire in a few months | TRUE | "overnight millionaire", fad lasted about 6 months (NPR/PBS) | none |
| 7 | "Odamlar hazil va hikoyani sotib oldi" | opinion | | none |

Fixes (old -> new)
- Title: "Geri Dal 1975 yilda 1,5 million dona oddiy tosh sotgan" -> "Geri Dal bir necha oyda taxminan 1,5 million oddiy tosh sotgan"
- Hook: "1,5 million dona oddiy tosh sotilgan." -> "Taxminan 1,5 million dona oddiy tosh sotilgan."
- Scene 1: "1975 yilda Geri Dal 1,5 million dona oddiy tosh sotdi." -> "1975 yildan boshlab Geri Dal taxminan 1,5 million oddiy tosh sotdi."
- Description: "Geri Dal 1975 yilda Pet Rock nomli oddiy toshni qutiga solib, 3,95 dollardan sotgan. Bir necha oyda 1,5 million dona sotilib, u millioner bo'lgan." -> "Geri Dal 1975 yildan boshlab Pet Rock nomli oddiy toshni qutiga solib, 3,95 dollardan sotgan. Bir necha oyda taxminan 1,5 million dona sotilib, u millioner bo'lgan."
- thumbnail "3,95 DOLLARLIK TOSH" stays.

---
## apex_3 (Pepsi) - PASS (one optional precision)

| # | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| 1 | 1923: Pepsi-Cola company went bankrupt | TRUE | Wikipedia Pepsi; historyoasis; sources agree on 1923 | none |
| 2 | Cause: sugar price swings after WWI, big losses | TRUE | WWI sugar shortage then price collapse; "speculation on volatile sugar prices" (Wikipedia Pepsi) | none |
| 3 | Bankrupt again 1931 | TRUE | 8 June 1931, Megargel's National Pepsi-Cola Co. after 3 years of losses; assets then taken by Guth/Loft (Wikipedia Charles Guth) | none |
| 4 | Later sold a 12 oz bottle for 5 cents | TRUE | Wikipedia Pepsi (12 oz bottle dated 1934 under Guth / Loft) | optional: add the year |
| 5 | "Deyarli ikki baravar katta" than competitor | TRUE | Coke bottle was 6.5 oz for the same nickel; 12/6.5 = 1.85 | none |
| 6 | "Ikki marta yiqilgan brend ... qaytdi" | TRUE (interpretation) | | none |

Note: conflicting sources claim Guth bought Pepsi in 1923 after Coca-Cola refused him a discount. The script correctly omits that.
Optional fix: Scene 4 "Keyin Pepsi 12 unsiyalik shishani 5 sentga sotdi." -> "1934 yilda Pepsi 12 unsiyalik shishani 5 sentga sotdi." (same length; the year is dated by Wikipedia only, so use it only if you want the precision).

---
## apex_4 (LEGO) - PASS WITH FIXES (minor)

| # | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| 1 | 1932: Danish carpenter Ole Kirk Christiansen began making wooden toys | TRUE | Wikipedia; started 10 Aug 1932 (piggy banks, pull toys, vehicles) | none |
| 2 | In Billund | TRUE | Wikipedia | none |
| 3 | During the Great Depression | TRUE | Wikipedia / Lemelson | none |
| 4 | 1934: named company Lego from "leg godt" (play well) | MISLEADING | Name and its meaning are TRUE. 1934 is the standard date (staff naming contest), but the LEGO Group's own 2026 history page says the name first appeared in company documents in early 1936 and became the company name that January. The company before that was "Billund Maskinsnedkeri" | say he "came up with the name", not "named the company" |
| 5 | 1949: plastic bricks | TRUE | "Automatic Binding Bricks", 1949 (Wikipedia). Based on Kiddicraft bricks seen ~1947; not claimed in script | none |
| 6 | 1958: today's brick shape patented | TRUE | Patent applied 28 Jan 1958 (Denmark) by Godtfred; Ole died March 1958. Script does not name who applied, so fine | none |
| 7 | "Eng mashhur brendlardan biri" | TRUE (hedged) | | none |

Fixes (old -> new)
- Scene 3: "1934 yilda u kompaniyaga nom berdi: daniyacha leg godt, ya'ni yaxshi o'yna. Qisqasi, Lego." -> "1934 yilda u nom o'ylab topdi: daniyacha leg godt, ya'ni yaxshi o'yna. Qisqasi, Lego."
- Description: "1934 yilda kompaniyani Lego deb atagan" -> "1934 yilda Lego nomini o'ylab topgan"
- Scene 4 and description: "1958 yilda bugungi g'ishtcha patentlandi" -> "1958 yilda bugungi g'ishtcha patentga topshirildi" (the 28 Jan 1958 date is the application; grant date not confirmed).

---
## facts_1 (Cuvier's beaked whale) - PASS WITH FIXES

| # | Claim | Verdict | Source | Fix |
|---|---|---|---|---|
| 1 | Dive to 2,992 m | TRUE | Schorr et al. 2014: "dives to 2992 m depth and lasting 137.5 min, both new mammalian dive records" (PMC3966784); NatGeo 9,816 ft / 2,992 m | none |
| 2 | Longest dive 137.5 min ("137 daqiqadan oshgan") | TRUE | same paper | none |
| 3 | Deepest and longest were the same whale ("bu kitning bitta sho'ng'ishi") | MISLEADING | Per NatGeo, one whale made the 2,992 m dive and a second whale stayed down 138 min. Eight whales were tagged. Scene 4 reads as if the same animal | see fix |
| 4 | Published in 2014 | TRUE | PLOS ONE 9(3) e92633, March 2014 | none |
| 5 | No sunlight, very cold, very high pressure at that depth | TRUE | NOAA: no light below ~1,000 m | none |
| 6 | Breathes air, so dive made on one breath | TRUE | breath-hold record (phys.org / Britannica) | none |
| 7 | Description: "eng uzun sho'ng'ish 137,5 daqiqa" | MISLEADING (scope) | Longest in that study. A later paper (Quick et al. 2020) reported 222 min, so do not call it the species record | keep wording "xuddi shu tadqiqotda" |

Fixes (old -> new)
- Scene 4: "O'sha tadqiqotda bu kitning bitta sho'ng'ishi 137 daqiqadan oshgan." -> "O'sha tadqiqotda eng uzun sho'ng'ish 137 daqiqadan oshgan."
- Description is already scoped ("Xuddi shu tadqiqotda eng uzun sho'ng'ish 137,5 daqiqa davom etgan") and needs no change.

---
## Verdict summary

| Story | Verdict | TRUE | MISLEADING | FALSE | UNVERIFIED |
|---|---|---|---|---|---|
| apex_1 Gillette | PASS WITH FIXES | 5 | 1 | 0 | 0 |
| apex_2 Pet Rock | PASS WITH FIXES | 4 | 2 | 0 | 0 |
| apex_3 Pepsi | PASS | 5 | 0 | 0 | 0 |
| apex_4 LEGO | PASS WITH FIXES | 6 | 1 | 0 | 0 |
| facts_1 Whale | PASS WITH FIXES | 5 | 2 | 0 | 0 |

Overall: FIX (apply the listed replacements, then queue). No story is rejected. Re-check the Pet Rock $3.95 price against the Wikipedia/NYT page when the network allows.
