import json
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
import data_filter

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def filter_data(json_data, frame_range, selected_names):
    filtered_data = []

    i = 0
    for frame in json_data["frames"][frame_range[0] : frame_range[1]]:
        sequence_id = frame["sequence_id"]
        frame_id = frame["frame_id"]

        if "annos" not in frame:
            continue

        names = frame["annos"]["names"]
        boxes_3d = frame["annos"]["boxes_3d"]

        for name, box in zip(names, boxes_3d):
            if name in selected_names:
                entry = {
                    "index": i,
                    "sequence_id": sequence_id,
                    "frame_id": frame_id,
                    "name": name,
                    "cx": round(box[0], 2),
                    "cy": round(box[1], 2),
                    "cz": round(box[2], 2),
                    "l": round(box[3], 2),
                    "w": round(box[4], 2),
                    "h": round(box[5], 2),
                    "θ": round(box[6], 2),
                }
                filtered_data.append(entry)
                i += 1

    return filtered_data


def save_csv(data, filename):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = [
            "index",
            "sequence_id",
            "frame_id",
            "name",
            "cx",
            "cy",
            "cz",
            "l",
            "w",
            "h",
            "θ",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Load your JSON data
with open("data.json") as f:
    json_data = json.load(f)

    # Set the frame range and names you want to filter
    @app.route("/filter", methods=["POST"])
    def filter_endpoint():
        frame_range = request.json["frame_range"]
        selected_names = request.json["selected_names"]

        filtered_data = filter_data(json_data, frame_range, selected_names)

        # Instead of saving to a file, return the data as a JSON response
        save_csv(filtered_data, "filtered_data.csv")
        data_head = filtered_data[0:10]
        data_filter.gen_doc()
        return jsonify({"response": "OK!", "preview": data_head})

    if __name__ == "__main__":
        app.run(debug=True)
