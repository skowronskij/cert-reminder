# Cert reminder

Simple tool for checking SSL/TLS certificate expiry date with builtin alert sending mechanism.

## Getting Started

### Dependencies

If running without docker:

- python3
- packages listed in `requirements.txt`
- cron (if you want to use builit cronjob)

#### Parameters

| Script arg       | Settings key  | Description                                                                 | Required |
| ---------------- | ------------- | --------------------------------------------------------------------------- | -------- |
| --urls           | URLS          | List of domains to check.                                                   | True     |
| --days_buffer    | DAYS_BUFFER   | Number of days left defining "about to expire"                              | True     |
| --webhook_urls   | WEBHOOK_URLS  | List of webhook urls                                                        | False    |
| --message        | MESSAGE       | Preformated webhook message. Use {days_left} and {url} to fill information. | False    |
| --settings       | -             | Settings json path. If settings file is defined - ignore other args         | False    |
| --no-init-messag | -             | Don't send initial webhook message                                          | False    |
| --cronjob        | -             | Add cronjob to crontab                                                      | False    |
|                  | CRON_SCHEDULE | Cron schedule strin. Default _"0 0 \* \* \*"_                               | False    |
|                  | PYTHON_PATH   | Python path. Default _"python3"_                                            | False    |

### Run examples without docker

If you want to just check domains certs without recurring reminders run

```
python3 main.py --urls google.com github.com --days_buffer 10
```

with settings file:

```
pytohn3 main.py --settings settings.json
```

Create cronjob with script (**at this time, settings file required**)

```
python3 main.py --settings settings.json --cronjob
```

### Running with docker (recurring reminder)

1. Create `settings.json` (see [template_settings.json](https://github.com/skowronskij/cert-reminder/blob/main/template_settings.json))
2. Build image:

```
docker build -t cert-reminder .
```

3. Run container:

```
docker run -d --rm cert-reminder
```
