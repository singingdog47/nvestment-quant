# Source Matrix v1.6

| Layer | Data | Primary/Secondary | Used for trade facts? | Failure behavior |
|---|---|---|---|---|
| v1.3 | screening_latest / full / quality / daily_report | internal | Candidate ranking only | preserve v1.3 quality gate |
| Market v1.5 | FRED HY/IG OAS, NFCI, DFF | primary/public | market context | missing + confidence down |
| Market v1.5 | JPX investor type / short selling / margin | primary | context; raw unless normalized | missing, never guessed |
| Market v1.5 | CFTC COT | primary | positioning only when normalized | missing, never neutral by availability alone |
| Market v1.5 | yfinance indices/assets | secondary | trend/volatility proxy | missing + confidence down |
| Company v1.6 | TDnet | primary | yes | missing blocks unsupported event claim |
| Company v1.6 | EDINET | primary | yes | missing if API key absent |
| Company v1.6 | SEC EDGAR | primary | yes | missing if User-Agent absent |
| Company v1.6 | Company IR | primary | yes when configured | best effort |
| Company v1.6 | Google News RSS | secondary | detection only | never sufficient for buy/sell |
| Company v1.6 | yfinance snapshot | secondary | fallback reference only | never overrides primary |
