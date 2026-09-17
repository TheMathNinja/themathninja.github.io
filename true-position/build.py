"""Build the cheatsheet from preserved Google Sheets and MFL snapshots."""
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://docs.google.com/spreadsheets/d/1lg_5ccUx7e1fKwKJLCN54tbRmnjLz9eG1LkZtxvHujI'
history = json.loads((ROOT / 'data/history.json').read_text(encoding='utf8'))
current = json.loads((ROOT / 'data/2026.json').read_text(encoding='utf8'))
years = [current, *history]
esc = html.escape
tabs, panels = [], []
for index, year in enumerate(years):
    y = year['year']
    active = index == 0
    tabs.append(f'<button role="tab" id="tab-{y}" aria-controls="panel-{y}" aria-selected="{str(active).lower()}" tabindex="{0 if active else -1}" data-year="{y}">{y}</button>')
    rows = []
    for record in year['rows']:
        league = ' + '.join(record.get('leagues', []))
        rows.append(f'<tr data-custom="{esc(record["custom"])}" data-leagues="{esc(league)}"><td>{esc(record["player"])}</td><td><span class="position">{esc(record["custom"])}</span></td><td>{esc(record["default"])}</td>' + (f'<td>{esc(league)}</td>' if y == '2026' else '') + '</tr>')
    if y == '2026':
        description = f'<p class="notes">{esc(year["notes"])}</p><p class="snapshot">Snapshot: {esc(year["asOf"])} · ADL: {year["counts"]["ADL"]} changes · FAFL: {year["counts"]["FAFL"]} changes</p>'
        sources = ' · '.join(f'<a href="{esc(url, quote=True)}">{esc(label)}</a>' for label, url in year['sources'].items())
        description += f'<details class="source-notes"><summary>Source data</summary><p>{sources}</p><p>Players are matched by MFL player ID. Only positions that differ from MFL’s current default are listed. These overrides include offensive and defensive players.</p></details>'
    else:
        description = '<details class="source-notes"><summary>Original sheet notes</summary><p class="original-notes">' + esc(year['notes']) + '</p></details>'
    colspan = 4 if y == '2026' else 3
    panels.append(f'<section role="tabpanel" id="panel-{y}" aria-labelledby="tab-{y}" tabindex="0" {"" if active else "hidden"}><div class="panel-heading"><h2>{y} position changes</h2><a class="download" href="data/{y}.csv" download>Download CSV</a></div>{description}<p class="row-count" aria-live="polite">{len(rows)} changes</p><div class="table-wrap"><table><caption class="sr-only">{y} True Position Cheatsheet</caption><thead><tr><th scope="col">Player</th><th scope="col">Custom position</th><th scope="col">Default MFL position</th>{"<th scope=col>League</th>" if y == "2026" else ""}</tr></thead><tbody>{"".join(rows)}</tbody></table></div><p class="empty" hidden>No players match these filters.</p></section>')
    with (ROOT / f'data/{y}.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['PLAYER', 'CUSTOM POSITION', 'DEFAULT MFL POSITION'] + (['LEAGUE', 'MFL ID'] if y == '2026' else []))
        for record in year['rows']:
            writer.writerow([record['player'], record['custom'], record['default']] + ([' + '.join(record['leagues']), record['id']] if y == '2026' else []))

page = (ROOT / 'template.html').read_text(encoding='utf8')
page = page.replace('__TABS__', ''.join(tabs)).replace('__PANELS__', ''.join(panels)).replace('__SOURCE__', SOURCE)
(ROOT / 'index.html').write_text(page, encoding='utf8')
print(f'Built {len(years)} tabs with {sum(len(y["rows"]) for y in years)} rows.')
