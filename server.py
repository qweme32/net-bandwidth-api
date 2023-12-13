from subprocess import check_output
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response, jsonify
from typing import Dict

scheduler = BackgroundScheduler()
app = Flask(__name__)
cache: Dict[str, str] = {
    "send": "unknown",
    "receive": "unknown"
}

def __bandwidth_task():
    cmd = check_output(["iftop", "-t", "-s", "1"]).decode("utf-8")

    lines = cmd.split("\n")
    lines.reverse()
    
    for line in lines:
        if "Total send rate:" in line:
            line = line.replace("Total send rate:", "").split(" ")
            cache["send"] = line[-1]

        elif "Total receive rate:" in line:
            line = line.replace("Total receive rate:", "").split(" ")
            cache["receive"] = line[-1]

@app.get("/bandwidth")
def __api() -> Response:
    return jsonify(cache)


if __name__ == "__main__":
    __bandwidth_task()
    scheduler.add_job(__bandwidth_task, 'interval', seconds=10)
    scheduler.start()
    app.run("0.0.0.0", 16789)

