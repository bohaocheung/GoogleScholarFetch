# Task Description
- Find a shcolar's all published papers in Google Scholar
- Find papers citing the designed paper
# Start
- pip install -r requirements.txt
- With VPN, Chrome in private browsing, search the title and click the `Cited by`
<img width="1280" height="559" alt="image" src="https://github.com/user-attachments/assets/de2e468f-0b88-410b-bcd4-af35f3c96665" />
- make sure you have access to the cited page and language is English
<img width="1280" height="559" alt="image" src="https://github.com/user-attachments/assets/183929c5-dcad-4a4e-af78-e042ad45a3c6" />
<img width="1280" height="1023" alt="image" src="https://github.com/user-attachments/assets/eafbd70b-72cb-46c0-bcfd-ccd3c74e482c" />
<img width="1280" height="680" alt="image" src="https://github.com/user-attachments/assets/b5510462-8941-46e4-afc7-4a9b0268085f" />
- Acquire Cookie: click right mouse button and click `check`. Then click `Network`, `Headers`, and find `Cookie`
<img width="1280" height="568" alt="image" src="https://github.com/user-attachments/assets/7a5a1368-68f0-46e4-a4ae-f41fb1aa565e" />
<img width="1280" height="680" alt="image" src="https://github.com/user-attachments/assets/501b30e0-6745-4dfc-9a4e-f7ff62e308a2" />
- In the `config.yaml`
  - paste the acquired cookie to `cookie` variable
  - set `title` to your purpose papaer
  - `start_item ` should be `0` when first search this paper
  - `cites`should be equal with `Cited by`, meaning total cites
# Problem
- Meeting `Forbidden for url` or `Too Many Requests`, meaning that your VPN is forbideen by Google Scholar, it's time to 1. clean the cookie cache in Chrome, 2. choose another VPN, another country better, 3. repeat steps in `Start` until acquiring the cookie (maybe need to pass the `reCAPTCHA`)
