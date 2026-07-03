# CloakBrowser Integration

## Install
```bash
uv pip install cloakbrowser --python /home/chillalot/.hermes/hermes-agent/venv/bin/python3
```

## Usage
```python
from cloakbrowser import launch
browser = launch(humanize=True)
page = browser.new_page()
page.goto("https://target.com/")
browser.close()
```

## When to use
- Site blocked by Cloudflare / NinjaFirewall
- browser_navigate fails with 403
- Need JavaScript-rendered content

## Status
- Installed: cloakbrowser==0.4.7
- playwright==1.61.0 installed as dependency
