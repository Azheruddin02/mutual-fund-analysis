import requests, pandas as pd, os
os.makedirs('data/raw', exist_ok=True)
print('Fetching NAV from mfapi.in...\n')
for code, name in [(125497,'HDFC Top 100 Direct'),(119551,'SBI Bluechip'),(120503,'ICICI Bluechip'),(118632,'Nippon Large Cap'),(119092,'Axis Bluechip'),(120841,'Kotak Bluechip')]:
    try:
        r = requests.get(f'https://api.mfapi.in/mf/{code}')
        data = r.json()
        if data.get('status') == 'SUCCESS':
            df = pd.DataFrame(data['data'])
            df['scheme_code'] = code
            df['scheme_name'] = name
            df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df = df.sort_values('date', ascending=False).reset_index(drop=True)
            df.to_csv(f'data/raw/nav_{code}_{name.replace(" ","_")}.csv', index=False)
            print(f'✅ {name} | Latest NAV: ₹{df["nav"].iloc[0]}')
    except:
        print(f'Failed {name}')
print('\nLive NAV fetch completed!')
