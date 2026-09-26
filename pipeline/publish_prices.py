"""Validate reviewed market observations and publish a region-specific game feed."""
import argparse
import json
import math
from collections import defaultdict
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from statistics import median
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VN = timezone(timedelta(hours=7))


def build(payload, today=None):
    today = today or datetime.now(VN).date()
    groups, rejected = defaultdict(list), []
    for i, row in enumerate(payload.get('observations', [])):
        try:
            if row.get('approved') is not True:
                raise ValueError('Chưa duyệt đối chiếu nguồn và quy cách game')
            if row.get('source_type') not in ('market_retail_press_report', 'market_retail'):
                raise ValueError('Không phải giá bán lẻ tại chợ')
            if row.get('region') not in ('Hà Nội', 'TP.HCM'):
                raise ValueError('Ngoài hai khu vực')
            for key in ('market', 'ingredient', 'variant', 'source_url', 'reviewed_by'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    raise ValueError('Thiếu ' + key)
            if urlsplit(row['source_url']).scheme != 'https':
                raise ValueError('Thiếu nguồn HTTPS')
            observed = date.fromisoformat(row.get('surveyed_on') or '')
            if not 0 <= (today - observed).days <= 2:
                raise ValueError('Ngày khảo sát quá cũ hoặc ở tương lai')
            if row.get('unit') not in ('kg', 'litre', 'piece'):
                raise ValueError('Chưa chuẩn hóa đơn vị')
            low, high = row['price_min_vnd'], row['price_max_vnd']
            if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (low, high)) or not 100 <= low <= high <= 10000000:
                raise ValueError('Khoảng giá không hợp lệ')
            if high > low * 2:
                raise ValueError('Khoảng giá quá rộng')
            groups[(row['region'], row['ingredient'], row['unit'], row['variant'])].append(row)
        except (ValueError, TypeError, KeyError) as error:
            rejected.append({'index': i, 'reason': str(error)})
    regions = {region: {} for region in ('Hà Nội', 'TP.HCM')}
    conflicts = set()
    for (region, item, unit, variant), rows in groups.items():
        # One value per market: duplicate articles cannot create independent evidence.
        markets = defaultdict(list)
        for row in rows:
            markets[row['market'].strip().casefold()].append(row)
        if len(markets) < 2:
            rejected.append({'ingredient': item, 'region': region, 'reason': 'Cần ít nhất hai chợ độc lập cùng quy cách'})
            continue
        values, dates = [], []
        for observations in markets.values():
            newest = max(r['surveyed_on'] for r in observations)
            fresh = [r for r in observations if r['surveyed_on'] == newest]
            values.append(median(set((r['price_min_vnd'] + r['price_max_vnd']) / 2 for r in fresh)))
            dates.append(newest)
        if max(values) > min(values) * 2:
            rejected.append({'ingredient': item, 'reason': 'Chênh lệch giữa chợ quá lớn'})
            continue
        if item in regions[region] or (region, item) in conflicts:
            regions[region].pop(item, None)
            conflicts.add((region, item))
            rejected.append({'ingredient': item, 'reason': 'Nhiều quy cách cùng tên game; cần chọn một quy cách'})
            continue
        valid_until = (date.fromisoformat(min(dates)) + timedelta(days=2)).isoformat()
        regions[region][item] = dict(price_vnd=round(median(values)), unit=unit, variant=variant,
            surveyed_on=min(dates), valid_until=valid_until, markets=sorted(markets),
            sources=sorted(set(r['source_url'] for r in rows)))
    return {'schema_version': 1, 'generated_on': today.isoformat(), 'regions': regions}, rejected


def publish(source, output):
    feed, rejected = build(json.loads(Path(source).read_text(encoding='utf-8')))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name, data in [('latest.json', feed), ('quality-report.json', {'rejected': rejected})]:
        target = output / name
        tmp = target.with_suffix('.tmp')
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(target)
    history = output / 'history'
    history.mkdir(exist_ok=True)
    (history / (feed['generated_on'] + '.json')).write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Published:', sum(len(v) for v in feed['regions'].values()), 'Rejected:', len(rejected))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'data/market-prices/latest.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'public/prices')
    args = parser.parse_args()
    publish(args.input, args.output)
