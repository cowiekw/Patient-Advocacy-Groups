# Patient-Advocacy-Groups

Identifying US-based patient advocacy and disease organizations and their lobbying practices

### Data Sources

- Nonprofit Data: https://projects.propublica.org/nonprofits/api
- NTEEs Codes: https://urbaninstitute.github.io/nccs-legacy/ntee/ntee-history.html#overview
- Lobbying data: LDA.SENATE.GOV.

Senate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.SENATE.GOV.

## Methods

- Scrape NTEE codes into a csv
- Annotate the CSV to identify codes that may correspong to Patient Advocacy Groups (PAGs)
- Search the Propubilc nonprofit api for nonprofits under the selected NTEE classifications

### NTEE Major Groups

I. Arts, Culture, and Humanities - A
II. Education - B
III. Environment and Animals - C, D
IV. Health - E, F, G, H
V. Human Services - I, J, K, L, M, N, O, P
VI. International, Foreign Affairs - Q
VII. Public, Societal Benefit - R, S, T, U, V, W
VIII. Religion Related - X
IX. Mutual/Membership Benefit - Y
X. Unknown, Unclassified - Z
