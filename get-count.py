import argparse
from os import path
from auditorium import config
from auditorium.visitorcounter import VisitorCounter

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="Source image path")
    ap.add_argument("--blob-nearby-point-area", help="Blob detection nearby points search radius value.",
                    default=config.BLOB_NEARBY_POINT_AREA)
    ap.add_argument("--blob-filter-min-area", help="Blob detection min area filter value.",
                    default=config.BLOB_MIN_AREA_DEFAULT_VALUE)
    ap.add_argument("--threshold-value", help="Binary inverted threshold value.",
                    default=config.THRESHOLD_DEFAULT_VALUE)
    args = vars(ap.parse_args())

    if args.get("source", None) is None:
        raise Exception("Source argument should be specified")

    source = args.get("source")

    if not path.isdir(source):
        raise Exception("Invalid source path")

    blob_nearby_point_area_percents = int(args.get("blob_nearby_point_area"))

    if not 0 <= blob_nearby_point_area_percents <= 100:
        raise Exception("Invalid blob_nearby_point_area_percents value.")

    vc = VisitorCounter(
        source,
        blob_nearby_point_area_percents=blob_nearby_point_area_percents,
        blob_filter_min_area=float(args.get("blob_filter_min_area")),
        threshold_value=int(args.get("threshold_value"))
    )
    count = vc.count()

    print("Total: %d" % count[0])

    for frame, value in count[1].items():
        print(frame, "Visitors: %d" % value)
