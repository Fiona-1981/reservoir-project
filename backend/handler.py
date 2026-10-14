import os
import boto3
from models import ReservoirLevels
from scrape_uu import fetch_page, parse_table

HISTORY_KEY = "history.json"

# Created once per Lambda container, so warm invocations reuse it
s3 = boto3.client("s3")


def merge_week(history, week):
    # Returns a new history; replaces any existing week with the same date
    weeks = [w for w in history.weeks if w.date != week.date] + [week]
    weeks.sort(key=lambda w: w.date)
    return history.model_copy(update={"weeks": weeks})


def read_history(bucket):
    try:
        response = s3.get_object(Bucket=bucket, Key=HISTORY_KEY)
    except s3.exceptions.NoSuchKey:
        return ReservoirLevels(water_company="United Utilities", weeks=[])
    return ReservoirLevels.model_validate_json(response["Body"].read())


def write_json(bucket, key, model):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=model.model_dump_json(indent=2),
        ContentType="application/json",
    )


def lambda_handler(event, context):
    bucket = os.environ["BUCKET_NAME"]

    week = parse_table(fetch_page())
    write_json(bucket, f"snapshots/{week.date.isoformat()}.json", week)

    history = merge_week(read_history(bucket), week)
    write_json(bucket, HISTORY_KEY, history)

    return {"date": week.date.isoformat(), "weeks": len(history.weeks)}
